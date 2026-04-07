#!/bin/bash
# 设置 SSH 免密登录到服务器
# 运行一次即可

SERVER="root@123.60.90.100"

# 生成 SSH Key（如果没有）
if [ ! -f ~/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -b 4096 -N "" -f ~/.ssh/id_rsa
    echo "SSH key generated"
fi

# 复制公钥到服务器
echo "Copying SSH key to server..."
echo "Please enter server password when prompted:"
ssh-copy-id -o StrictHostKeyChecking=no "$SERVER"

echo ""
echo "Testing connection..."
ssh "$SERVER" "echo 'SSH key auth works!'"
