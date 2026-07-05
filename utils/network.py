import requests
from datetime import datetime

class NetworkManager:
    def __init__(self):
        # APIهای سبک فقط برای گرفتن IP (برای چک هر ثانیه)
        self.quick_providers = [
            "https://api.ipify.org?format=json",
            "https://api.ip.sb/jsonip",
            "https://api64.ipify.org?format=json"
        ]
        
        # APIهای سنگین برای گرفتن اطلاعات کامل (کشور، شهر، ISP)
        self.detail_providers = [
            "https://ipwho.is/",
            "https://ipapi.co/json/"
        ]

    def get_current_ip(self):
        """گرفتن سریع آی‌پی فعلی (سبک برای چک هر ثانیه)"""
        for provider in self.quick_providers:
            try:
                response = requests.get(provider, timeout=3)
                data = response.json()
                # استخراج آی‌پی از فرمت‌های مختلف
                return data.get("ip") or data.get("query")
            except:
                continue
        return None

    def get_network_info(self):
        """گرفتن اطلاعات کامل شبکه (فقط موقع نیاز یا تغییر IP)"""
        
        # اول آی‌پی رو پیدا کن
        ip = self.get_current_ip()
        
        # حالا اطلاعات کامل رو با APIهای سنگین بگیر
        for provider in self.detail_providers:
            try:
                response = requests.get(provider, timeout=5)
                data = response.json()
                
                # فرمت‌بندی مخصوص هر سایت
                if "ipwho.is" in provider:
                    return {
                        "status": "online",
                        "ip": data.get("ip", ip),
                        "country": data.get("country", "Unknown"),
                        "city": data.get("city", "Unknown"),
                        "isp": data.get("connection", {}).get("isp", "Unknown"),
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                elif "ipapi.co" in provider:
                    return {
                        "status": "online",
                        "ip": data.get("ip", ip),
                        "country": data.get("country_name", "Unknown"),
                        "city": data.get("city", "Unknown"),
                        "isp": data.get("org", "Unknown"),
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
            except:
                continue
                
        # اگه APIهای سنگین جواب ندادن، حداقل آی‌پی رو برگردون
        if ip:
            return {
                "status": "online",
                "ip": ip,
                "country": "Unknown",
                "city": "Unknown",
                "isp": "Unknown",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
        return {"status": "offline"}