"""
Ads 广告创建功能测试脚本

使用方式：
1. 配置测试参数（見下面的 TEST_CONFIG）
2. 运行：python test_ads_creation.py
3. 检查输出和日志
"""
import asyncio
import httpx
import json
from typing import Dict, Any, Optional

# ============ 配置 ============
TEST_CONFIG = {
    "BASE_URL": "http://localhost:8000",
    "ADVERTISER_ID": "YOUR_ADVERTISER_ID_HERE",  # 改为实际的账户ID
    "CAMPAIGN_NAME": f"TestCampaign_{__import__('time').strftime('%Y%m%d_%H%M%S')}",
    "DAILY_BUDGET": 50.0,  # $50/day
    "VIDEO_FILE": None,  # 如果要测试上传，设置为视频路径
}

# ============ 测试用例 ============

async def test_create_campaign(client: httpx.AsyncClient, config: Dict[str, Any]) -> Optional[Dict]:
    """测试：创建推广计划"""
    print("\n" + "=" * 60)
    print("测试1：创建推广计划 (CONVERSION)")
    print("=" * 60)
    
    payload = {
        "advertiser_id": config["ADVERTISER_ID"],
        "campaign_name": config["CAMPAIGN_NAME"],
        "daily_budget": config["DAILY_BUDGET"]
    }
    
    print(f"📤 发送请求：POST /ads/campaign/create")
    print(f"📋 参数：{json.dumps(payload, indent=2)}")
    
    try:
        response = await client.post(
            f"{config['BASE_URL']}/ads/campaign/create",
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功！")
            print(f"📊 响应：{json.dumps(result, indent=2, ensure_ascii=False)}")
            return result.get("data")
        else:
            print(f"❌ 失败！状态码：{response.status_code}")
            print(f"📊 响应：{response.text}")
            return None
    
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


async def test_create_full_campaign(
    client: httpx.AsyncClient,
    config: Dict[str, Any],
    video_id: Optional[str] = None
) -> Optional[Dict]:
    """测试：一键创建完整广告"""
    print("\n" + "=" * 60)
    print("测试2：一键创建完整Ads广告")
    print("=" * 60)
    
    if not video_id:
        print("⚠️  跳过此测试（需要先上传视频获取 video_id）")
        return None
    
    payload = {
        "advertiser_id": config["ADVERTISER_ID"],
        "campaign_name": f"{config['CAMPAIGN_NAME']}_Full",
        "daily_budget": config["DAILY_BUDGET"],
        "video_id": video_id,
        "landing_page_url": "https://example.com/product",
        "ad_text": "Test ad - Limited time offer!",
        "targeting": {
            "age": ["21", "35"],
            "gender": ["FEMALE"],
            "location": ["US", "CA"],
            "interest": ["shopping", "fashion"],
            "placements": ["TIKTOK"],
            "languages": ["en"]
        }
    }
    
    print(f"📤 发送请求：POST /ads/campaign/create-full")
    print(f"📋 参数：{json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        response = await client.post(
            f"{config['BASE_URL']}/ads/campaign/create-full",
            json=payload,
            timeout=30.0
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功！")
            print(f"📊 响应：{json.dumps(result, indent=2, ensure_ascii=False)}")
            return result.get("data")
        else:
            print(f"❌ 失败！状态码：{response.status_code}")
            print(f"📊 响应：{response.text}")
            return None
    
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


async def test_upload_video(
    client: httpx.AsyncClient,
    config: Dict[str, Any],
    video_file: str
) -> Optional[str]:
    """测试：上传视频"""
    print("\n" + "=" * 60)
    print("测试3：上传视频创意")
    print("=" * 60)
    
    import os
    
    if not os.path.exists(video_file):
        print(f"❌ 文件不存在：{video_file}")
        return None
    
    file_size = os.path.getsize(video_file) / (1024 * 1024)  # MB
    print(f"📤 上传文件：{video_file} ({file_size:.2f}MB)")
    
    try:
        with open(video_file, 'rb') as f:
            files = {
                'file': (os.path.basename(video_file), f, 'video/mp4')
            }
            response = await client.post(
                f"{config['BASE_URL']}/ads/video/upload",
                params={
                    "advertiser_id": config["ADVERTISER_ID"],
                    "video_name": f"TestVideo_{__import__('time').strftime('%Y%m%d_%H%M%S')}"
                },
                files=files,
                timeout=300.0  # 长时间超时，大文件需要时间
            )
        
        if response.status_code == 200:
            result = response.json()
            video_id = result.get("data", {}).get("video_id")
            print(f"✅ 上传成功！")
            print(f"📊 Video ID：{video_id}")
            print(f"📊 完整响应：{json.dumps(result, indent=2, ensure_ascii=False)}")
            return video_id
        else:
            print(f"❌ 上传失败！状态码：{response.status_code}")
            print(f"📊 响应：{response.text}")
            return None
    
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


async def test_health_check(client: httpx.AsyncClient, config: Dict[str, Any]) -> bool:
    """测试：健康检查"""
    print("\n" + "=" * 60)
    print("测试0：健康检查")
    print("=" * 60)
    
    try:
        response = await client.get(
            f"{config['BASE_URL']}/health",
            timeout=5.0
        )
        
        if response.status_code == 200:
            print(f"✅ 服务正常！")
            print(f"📊 响应：{json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"❌ 服务异常！状态码：{response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ 无法连接到服务：{e}")
        print(f"💡 提示：确保后端服务已启动（uvicorn app.main:app --reload）")
        return False


async def main():
    """主测试流程"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " TikTok Ads 创建功能测试套件".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    
    # 打印配置
    print("\n📋 测试配置：")
    print(f"  - 服务地址：{TEST_CONFIG['BASE_URL']}")
    print(f"  - 账户ID：{TEST_CONFIG['ADVERTISER_ID']}")
    print(f"  - 计划名称：{TEST_CONFIG['CAMPAIGN_NAME']}")
    print(f"  - 日预算：${TEST_CONFIG['DAILY_BUDGET']}")
    
    async with httpx.AsyncClient() as client:
        # 测试0：健康检查
        if not await test_health_check(client, TEST_CONFIG):
            print("\n❌ 后端服务未运行，无法继续测试")
            return
        
        # 测试1：创建推广计划
        campaign = await test_create_campaign(client, TEST_CONFIG)
        if not campaign:
            print("\n⚠️  无法创建推广计划，停止测试")
            return
        
        campaign_id = campaign.get("campaign_id")
        
        # 测试2：上传视频（可选）
        video_id = None
        if TEST_CONFIG.get("VIDEO_FILE"):
            video_id = await test_upload_video(client, TEST_CONFIG, TEST_CONFIG["VIDEO_FILE"])
        
        # 测试3：一键创建广告（需要video_id）
        if video_id:
            full_campaign = await test_create_full_campaign(client, TEST_CONFIG, video_id)
        
        # 总结
        print("\n" + "=" * 60)
        print("📊 测试总结")
        print("=" * 60)
        print(f"✅ 推广计划创建成功：campaign_id = {campaign_id}")
        if video_id:
            print(f"✅ 视频上传成功：video_id = {video_id}")
        print(f"\n💡 下一步：")
        print(f"   1. 登录TikTok后台查看创建的推广计划")
        print(f"   2. 验证广告组和广告的配置")
        print(f"   3. 开始投放测试")
    
    print("\n✨ 测试完成！\n")


if __name__ == "__main__":
    # 参数检查
    if TEST_CONFIG["ADVERTISER_ID"] == "YOUR_ADVERTISER_ID_HERE":
        print("⚠️  错误：请先修改 TEST_CONFIG 中的 ADVERTISER_ID")
        print("   打开 test_ads_creation.py，找到 ADVERTISER_ID = '...'")
        print("   替换为你的实际账户ID")
        exit(1)
    
    # 运行测试
    asyncio.run(main())
