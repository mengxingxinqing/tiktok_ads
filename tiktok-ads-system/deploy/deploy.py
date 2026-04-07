#!/usr/bin/env python3
"""
TikTok Ads System - 宝塔部署脚本

用法:
  python deploy.py init      # 首次初始化（创建目录/数据库/Nginx/.env + 部署全量）
  python deploy.py            # 全量更新（后端+前端）
  python deploy.py backend    # 仅后端
  python deploy.py frontend   # 仅前端
  python deploy.py restart    # 重启服务
  python deploy.py logs       # 查看日志
  python deploy.py status     # 检查状态
  python deploy.py nginx      # 更新 Nginx 配置

前提:
  在宝塔面板中完成:
  1. Python项目管理器 → 安装 Python 3.11
  2. 用 Python项目管理器创建项目（或脚本自动用 supervisor 管理）
  3. SSL 证书申请
"""
import os
import sys
import time
import subprocess
import paramiko
from pathlib import Path

# ========== 加载部署配置 ==========
def _load_deploy_env():
    """从 .env.deploy 读取部署配置"""
    env_file = Path(__file__).parent / ".env.deploy"
    if not env_file.exists():
        print(f"\033[31m[ERROR]\033[0m 未找到 {env_file}")
        print(f"  请复制 .env.deploy.example 为 .env.deploy 并填入真实值")
        sys.exit(1)
    cfg = {}
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, val = line.partition("=")
        cfg[key.strip()] = val.strip()
    return cfg

_cfg = _load_deploy_env()

SERVER_HOST = _cfg["SERVER_HOST"]
SERVER_USER = _cfg.get("SERVER_USER", "root")
SERVER_PASS = _cfg["SERVER_PASS"]
REMOTE_DIR = "/www/wwwroot/tiktok-ads"
DOMAIN = "ads.tongtools.com"
BACKEND_PORT = 8890

LOCAL_BACKEND = Path(__file__).resolve().parent.parent  # tiktok-ads-system/
LOCAL_FRONTEND = LOCAL_BACKEND.parent / "tiktok-ads-frontend"
FRONTEND_DIST = LOCAL_BACKEND.parent / "tiktok-ads-frontend-dist"

# 后端上传排除
BACKEND_EXCLUDES = {
    'venv', '__pycache__', '.env', 'logs', '.git', 'scripts',
    'docs', 'deploy', '.pytest_cache', '.mypy_cache', 'node_modules',
}

# 宝塔 Python 项目管理器安装的 Python 路径
BT_PYTHON_DIR = "/www/server/panel/pyenv"


def log(msg):
    print(f"\033[36m[{time.strftime('%H:%M:%S')}]\033[0m {msg}")


def err(msg):
    print(f"\033[31m[ERROR]\033[0m {msg}")
    sys.exit(1)


class Deployer:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sftp = None

    def connect(self):
        log(f"Connecting to {SERVER_HOST}...")
        self.ssh.connect(SERVER_HOST, username=SERVER_USER, password=SERVER_PASS, timeout=10)
        self.sftp = self.ssh.open_sftp()
        log("Connected!")

    def run(self, cmd, check=True, timeout=300):
        """执行远程命令"""
        stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='replace')
        error = stderr.read().decode('utf-8', errors='replace')
        code = stdout.channel.recv_exit_status()
        if check and code != 0:
            print(f"  stdout: {out}")
            print(f"  stderr: {error}")
            err(f"Command failed (exit {code}): {cmd[:100]}...")
        return out, error, code

    def upload_dir(self, local_path, remote_path, excludes=None):
        """递归上传目录"""
        excludes = excludes or set()
        local_path = Path(local_path)
        file_count = 0
        self._mkdir_p(remote_path)

        for item in local_path.rglob('*'):
            rel = item.relative_to(local_path)
            if any(p in excludes for p in rel.parts):
                continue
            if item.name.endswith('.pyc'):
                continue
            remote_file = f"{remote_path}/{rel.as_posix()}"
            if item.is_dir():
                self._mkdir_p(remote_file)
            elif item.is_file():
                try:
                    self.sftp.put(str(item), remote_file)
                    file_count += 1
                    if file_count % 50 == 0:
                        print(f"  Uploaded {file_count} files...", flush=True)
                except Exception as e:
                    print(f"  Warning: Failed to upload {rel}: {e}")
        return file_count

    def _mkdir_p(self, remote_path):
        dirs = remote_path.split('/')
        current = ''
        for d in dirs:
            if not d:
                current = '/'
                continue
            current = f"{current}/{d}" if current != '/' else f"/{d}"
            try:
                self.sftp.stat(current)
            except FileNotFoundError:
                self.sftp.mkdir(current)

    def close(self):
        if self.sftp:
            self.sftp.close()
        self.ssh.close()


# ========== 查找可用的 Python 3.9+ ==========

def find_python(d: Deployer) -> str:
    """在服务器上查找 Python 3.9+，优先宝塔安装的版本"""
    out, _, _ = d.run(r"""
# 1. 宝塔 Python 项目管理器安装的版本
for p in /www/server/panel/pyenv/versions/*/bin/python3; do
    if [ -x "$p" ]; then
        VER=$($p -c 'import sys; print(sys.version_info.minor)' 2>/dev/null || echo 0)
        if [ "$VER" -ge 9 ]; then echo "$p"; exit 0; fi
    fi
done

# 2. 宝塔 supervisor 插件自带的
for p in /www/server/panel/plugin/supervisor/pyenv/bin/python3*; do
    if [ -x "$p" ]; then
        VER=$($p -c 'import sys; print(sys.version_info.minor)' 2>/dev/null || echo 0)
        if [ "$VER" -ge 9 ]; then echo "$p"; exit 0; fi
    fi
done

# 3. 系统路径
for p in python3.12 python3.11 python3.10 python3.9 python3; do
    REAL=$(command -v $p 2>/dev/null)
    if [ -n "$REAL" ]; then
        VER=$($REAL -c 'import sys; print(sys.version_info.minor)' 2>/dev/null || echo 0)
        if [ "$VER" -ge 9 ]; then echo "$REAL"; exit 0; fi
    fi
done

# 4. anaconda
for p in /root/anaconda3/bin/python3 /opt/anaconda3/bin/python3; do
    if [ -x "$p" ]; then
        VER=$($p -c 'import sys; print(sys.version_info.minor)' 2>/dev/null || echo 0)
        if [ "$VER" -ge 9 ]; then echo "$p"; exit 0; fi
    fi
done

echo "NONE"
""", check=False)
    return out.strip()


# ========== 初始化 ==========

def init_server(d: Deployer):
    """首次初始化服务器"""
    log("=" * 50)
    log("  Step 1/6: 创建目录")
    log("=" * 50)
    d.run(f"mkdir -p {REMOTE_DIR}/{{backend,frontend,logs}}")

    # ---------- 检测 Python ----------
    log("=" * 50)
    log("  Step 2/6: 检测 Python 环境")
    log("=" * 50)
    out, _, _ = d.run("python3 --version", check=False)
    log(f"  系统 Python: {out.strip()}")

    python_bin = find_python(d)
    if python_bin == "NONE":
        log("")
        log("  ⚠ 未找到 Python 3.9+")
        log("")
        log("  请在宝塔面板中操作:")
        log("  1. 软件商店 → 搜索 'Python项目管理器' → 安装")
        log("  2. Python项目管理器 → 版本管理 → 安装 Python 3.11")
        log("  3. 安装完成后重新运行: python deploy.py init")
        log("")
        log("  或者用 conda 快速安装（当前服务器已有 anaconda3）:")
        log("  ssh root@123.60.90.100")
        log("  conda create -n py311 python=3.11 -y")
        log("")

        # 尝试用已有的 anaconda 自动安装
        log("  正在尝试用 anaconda3 自动安装 Python 3.11...")
        d.run("""
if [ -f /root/anaconda3/bin/conda ]; then
    /root/anaconda3/bin/conda create -n py311 python=3.11 -y 2>&1 | tail -5
    echo "CONDA_INSTALL_DONE"
fi
""", check=False, timeout=600)

        # 重新查找
        python_bin = find_python(d)
        if python_bin == "NONE":
            # 再找 conda 环境
            out2, _, _ = d.run("ls /root/anaconda3/envs/py311/bin/python3* 2>/dev/null | head -1", check=False)
            if out2.strip():
                python_bin = out2.strip()

    if python_bin == "NONE":
        err("仍未找到 Python 3.9+，请手动安装后重试")

    out, _, _ = d.run(f"{python_bin} --version", check=False)
    log(f"  使用 Python: {python_bin} ({out.strip()})")

    # ---------- 创建 venv ----------
    log("=" * 50)
    log("  Step 3/6: 创建虚拟环境")
    log("=" * 50)
    d.run(f"""
cd {REMOTE_DIR}/backend
if [ ! -d "venv" ]; then
    {python_bin} -m venv venv
    echo "venv created"
else
    echo "venv already exists"
fi
{REMOTE_DIR}/backend/venv/bin/python --version
""")

    # ---------- 数据库 ----------
    log("=" * 50)
    log("  Step 4/6: 创建数据库")
    log("=" * 50)
    db_user = _cfg.get("DB_USER", "tk_ads")
    db_pass = _cfg["DB_PASS"]
    db_name = _cfg.get("DB_NAME", "tk_ads")
    d.run(f"""
mysql -u root -e "CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null || echo "跳过（可能需要密码，请在宝塔面板手动创建数据库 {db_name}）"
mysql -u root -e "GRANT ALL ON {db_name}.* TO '{db_user}'@'localhost' IDENTIFIED BY '{db_pass}';" 2>/dev/null || true
mysql -u root -e "FLUSH PRIVILEGES;" 2>/dev/null || true
echo "数据库配置完成"
""", check=False)

    # ---------- Supervisor 进程管理 ----------
    log("=" * 50)
    log("  Step 5/6: 配置进程管理（supervisor）")
    log("=" * 50)

    # 宝塔的 supervisor 插件配置
    supervisor_conf = f"""[program:tiktok-ads]
command={REMOTE_DIR}/backend/venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port {BACKEND_PORT} --workers 2 --log-level info
directory={REMOTE_DIR}/backend
autostart=true
autorestart=true
startsecs=5
startretries=3
user=root
redirect_stderr=true
stdout_logfile={REMOTE_DIR}/logs/backend.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=5
environment=PATH="{REMOTE_DIR}/backend/venv/bin:/usr/local/bin:/usr/bin"
"""
    # 写入 supervisor 配置
    sup_dir = "/www/server/panel/plugin/supervisor/config"
    d.run(f"mkdir -p {sup_dir}", check=False)
    with d.sftp.open(f"{sup_dir}/tiktok-ads.conf", 'w') as f:
        f.write(supervisor_conf)

    # 同时创建 systemd 备用
    systemd_service = f"""[Unit]
Description=TikTok Ads Backend
After=network.target mysql.service redis.service

[Service]
Type=simple
User=root
WorkingDirectory={REMOTE_DIR}/backend
Environment=PATH={REMOTE_DIR}/backend/venv/bin:/usr/local/bin:/usr/bin
ExecStart={REMOTE_DIR}/backend/venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port {BACKEND_PORT} --workers 2 --log-level info
Restart=always
RestartSec=5
StandardOutput=append:{REMOTE_DIR}/logs/backend.log
StandardError=append:{REMOTE_DIR}/logs/backend.log

[Install]
WantedBy=multi-user.target
"""
    with d.sftp.open("/etc/systemd/system/tiktok-ads.service", 'w') as f:
        f.write(systemd_service)
    d.run("systemctl daemon-reload && systemctl enable tiktok-ads", check=False)

    # 刷新 supervisor
    d.run("""
if command -v supervisorctl &>/dev/null; then
    supervisorctl reread 2>/dev/null
    supervisorctl update 2>/dev/null
    echo "supervisor 已更新"
else
    echo "supervisor 未安装，将使用 systemd 管理"
fi
""", check=False)

    # ---------- Nginx ----------
    log("=" * 50)
    log("  Step 6/6: 配置 Nginx")
    log("=" * 50)
    setup_nginx(d)

    log("")
    log("=" * 50)
    log("  初始化完成！")
    log("=" * 50)


def setup_env(d: Deployer):
    """设置生产环境 .env"""
    log("Setting up .env...")

    db_user = _cfg.get("DB_USER", "tk_ads")
    db_pass = _cfg["DB_PASS"]
    db_name = _cfg.get("DB_NAME", "tk_ads")
    env_content = f"""# TikTok API
TIKTOK_APP_ID={_cfg['TIKTOK_APP_ID']}
TIKTOK_APP_SECRET={_cfg['TIKTOK_APP_SECRET']}
TIKTOK_REDIRECT_URI=https://{DOMAIN}/auth/callback

# LLM
LLM_API_BASE={_cfg.get('LLM_API_BASE', 'https://api.tongtools.com')}
LLM_API_KEY={_cfg['LLM_API_KEY']}
LLM_MODEL={_cfg.get('LLM_MODEL', 'gpt-5')}

# Database
DATABASE_URL=mysql+aiomysql://{db_user}:{db_pass}@localhost:3306/{db_name}?charset=utf8mb4

# Redis
REDIS_URL={_cfg.get('REDIS_URL', 'redis://localhost:6379/0')}

# Security
SECRET_KEY={_cfg['SECRET_KEY']}
DEBUG=false
LOG_LEVEL=INFO
SYNC_INTERVAL_MINUTES=30
"""
    with d.sftp.open(f"{REMOTE_DIR}/backend/.env", 'w') as f:
        f.write(env_content)
    log(".env created!")


def setup_nginx(d: Deployer):
    """配置 Nginx（先创建 HTTP 版本，SSL 在宝塔面板申请后生效）"""
    log("Setting up Nginx...")

    # 先检查 SSL 证书是否存在
    out, _, _ = d.run(f"ls /www/server/panel/vhost/cert/{DOMAIN}/fullchain.pem 2>/dev/null && echo HAS_SSL || echo NO_SSL", check=False)
    has_ssl = "HAS_SSL" in out

    if has_ssl:
        nginx_conf = f"""server {{
    listen 80;
    server_name {DOMAIN};
    return 301 https://$host$request_uri;
}}

server {{
    listen 443 ssl http2;
    server_name {DOMAIN};

    ssl_certificate /www/server/panel/vhost/cert/{DOMAIN}/fullchain.pem;
    ssl_certificate_key /www/server/panel/vhost/cert/{DOMAIN}/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    root {REMOTE_DIR}/frontend;
    index index.html;

    location ~ ^/(auth|dashboard|campaigns|creatives|products|orders|ads|shop-summary|gmvmax|health|alerts|decisions|settings|rules|boost|analytics|shops|creative-groups|creative-dashboard|comments|channel) {{
        proxy_pass http://127.0.0.1:{BACKEND_PORT};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
        client_max_body_size 500M;
    }}

    location / {{
        try_files $uri $uri/ /index.html;
    }}

    location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {{
        expires 30d;
        add_header Cache-Control "public, immutable";
    }}

    access_log /www/wwwlogs/{DOMAIN}.log;
    error_log /www/wwwlogs/{DOMAIN}.error.log;
}}
"""
    else:
        log("  SSL 证书未找到，先配置 HTTP 版本")
        log("  部署完成后请在宝塔面板申请 SSL 证书，再运行: python deploy.py nginx")
        nginx_conf = f"""server {{
    listen 80;
    server_name {DOMAIN};

    root {REMOTE_DIR}/frontend;
    index index.html;

    location ~ ^/(auth|dashboard|campaigns|creatives|products|orders|ads|shop-summary|gmvmax|health|alerts|decisions|settings|rules|boost|analytics|shops|creative-groups|creative-dashboard|comments|channel) {{
        proxy_pass http://127.0.0.1:{BACKEND_PORT};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
        client_max_body_size 500M;
    }}

    location / {{
        try_files $uri $uri/ /index.html;
    }}

    location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {{
        expires 30d;
        add_header Cache-Control "public, immutable";
    }}

    access_log /www/wwwlogs/{DOMAIN}.log;
    error_log /www/wwwlogs/{DOMAIN}.error.log;
}}
"""

    conf_path = f"/www/server/panel/vhost/nginx/{DOMAIN}.conf"
    with d.sftp.open(conf_path, 'w') as f:
        f.write(nginx_conf)

    out, error, code = d.run("nginx -t", check=False)
    if code == 0:
        d.run("nginx -s reload")
        log(f"  Nginx OK! {'(HTTPS)' if has_ssl else '(HTTP only)'}")
    else:
        log(f"  ⚠ Nginx test failed: {error.strip()}")


def deploy_backend(d: Deployer):
    """部署后端代码"""
    log("Deploying backend...")

    count = d.upload_dir(LOCAL_BACKEND, f"{REMOTE_DIR}/backend", excludes=BACKEND_EXCLUDES)
    log(f"  Uploaded {count} files")

    log("Installing dependencies...")
    out, err_out, code = d.run(f"""
cd {REMOTE_DIR}/backend
source venv/bin/activate
pip install -r requirements.txt -q 2>&1 | tail -5
echo "OK"
""", check=False, timeout=300)
    print(f"  {out.strip()}")
    if code != 0:
        print(f"  stderr: {err_out}")

    log("Restarting backend...")
    # 尝试 supervisor，fallback 到 systemd
    d.run(f"""
if command -v supervisorctl &>/dev/null; then
    supervisorctl restart tiktok-ads 2>/dev/null && echo "supervisor restarted" || true
fi
systemctl restart tiktok-ads 2>/dev/null || true
""", check=False)
    time.sleep(3)

    # 验证
    out, _, _ = d.run(f"curl -s http://127.0.0.1:{BACKEND_PORT}/health", check=False)
    if 'healthy' in out:
        log(f"  Backend healthy! ✓")
    else:
        log(f"  ⚠ Health check: {out.strip()}")
        out2, _, _ = d.run(f"tail -20 {REMOTE_DIR}/logs/backend.log", check=False)
        print(f"  Last logs:\n{out2}")


def build_frontend():
    """本地构建前端"""
    log("Building frontend...")
    result = subprocess.run(
        "npm run build",
        shell=True, cwd=str(LOCAL_FRONTEND),
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(result.stderr)
        err("Frontend build failed")

    if FRONTEND_DIST.exists():
        size = sum(f.stat().st_size for f in FRONTEND_DIST.rglob('*') if f.is_file())
        log(f"  Built: {size / 1024 / 1024:.1f} MB")
    else:
        err(f"Build output not found: {FRONTEND_DIST}")


def deploy_frontend(d: Deployer):
    """构建并部署前端"""
    build_frontend()

    log("Uploading frontend...")
    # 先清空旧文件
    d.run(f"rm -rf {REMOTE_DIR}/frontend/*", check=False)
    count = d.upload_dir(FRONTEND_DIST, f"{REMOTE_DIR}/frontend")
    log(f"  Uploaded {count} files ✓")


def restart(d: Deployer):
    log("Restarting...")
    d.run(f"""
supervisorctl restart tiktok-ads 2>/dev/null || true
systemctl restart tiktok-ads 2>/dev/null || true
nginx -s reload 2>/dev/null || true
""", check=False)
    time.sleep(2)
    out, _, _ = d.run(f"curl -s http://127.0.0.1:{BACKEND_PORT}/health", check=False)
    log(f"Health: {out.strip()}")


def show_logs(d: Deployer):
    out, _, _ = d.run(f"tail -100 {REMOTE_DIR}/logs/backend.log", check=False)
    print(out)


def show_status(d: Deployer):
    out, _, _ = d.run(f"""
echo "=== Process ==="
ps aux | grep uvicorn | grep -v grep
echo ""
echo "=== Port ==="
ss -tlnp | grep {BACKEND_PORT}
echo ""
echo "=== Health ==="
curl -s http://127.0.0.1:{BACKEND_PORT}/health
echo ""
echo ""
echo "=== Disk ==="
du -sh {REMOTE_DIR}/*
echo ""
echo "=== Supervisor ==="
supervisorctl status tiktok-ads 2>/dev/null || echo "not managed by supervisor"
echo ""
echo "=== Systemd ==="
systemctl is-active tiktok-ads 2>/dev/null || echo "not managed by systemd"
""", check=False)
    print(out)


# ========== 主入口 ==========
def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "deploy"

    d = Deployer()
    try:
        d.connect()

        if action == "init":
            init_server(d)
            setup_env(d)
            deploy_backend(d)
            deploy_frontend(d)
            log(f"\n{'='*50}")
            log(f"  首次部署完成!")
            log(f"  访问: https://{DOMAIN}")
            log(f"")
            log(f"  后续步骤:")
            log(f"  1. 宝塔面板 → 网站 → {DOMAIN} → SSL → 申请证书")
            log(f"  2. 申请成功后运行: python deploy.py nginx")
            log(f"{'='*50}")
        elif action == "backend":
            deploy_backend(d)
        elif action == "frontend":
            deploy_frontend(d)
        elif action == "deploy":
            deploy_backend(d)
            deploy_frontend(d)
            log(f"\n✓ 部署完成! https://{DOMAIN}")
        elif action == "restart":
            restart(d)
        elif action == "logs":
            show_logs(d)
        elif action == "status":
            show_status(d)
        elif action == "nginx":
            setup_nginx(d)
        elif action == "env":
            setup_env(d)
        else:
            print(__doc__)
    finally:
        d.close()


if __name__ == "__main__":
    main()
