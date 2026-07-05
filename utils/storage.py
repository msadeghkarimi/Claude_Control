import json
import os

class Storage:
    def __init__(self):
        self.history_file = "config/history.json"
        self.settings_file = "config/settings.json"
        self.apps_file = "config/protected_apps.json"
        self._ensure_files()
        
    def _ensure_files(self):
        os.makedirs("config", exist_ok=True)
        
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
                
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "theme": "dark",
                    "developer": "@msadeghkarimi",
                    "safe_ip": None
                }, f, ensure_ascii=False)
                
        if not os.path.exists(self.apps_file):
            with open(self.apps_file, 'w', encoding='utf-8') as f:
                json.dump([
                    "chrome.exe",
                    "firefox.exe",
                    "msedge.exe",
                    "brave.exe",
                    "opera.exe",
                    "Code.exe",
                    "telegram.exe",
                    "discord.exe",
                    "notepad.exe"
                ], f, ensure_ascii=False)
                
    def load_history(self):
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
            
    def add_history(self, data):
        history = self.load_history()
        
        record = {
            "date": data["date"],
            "ip": data["ip"],
            "country": data["country"],
            "city": data["city"],
            "isp": data["isp"],
            "status": data.get("status", "normal")
        }
        
        history.append(record)
        
        # فقط 1000 رکورد آخر رو نگه دار
        if len(history) > 1000:
            history = history[-1000:]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
            
    def clear_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump([], f)
            
    def save_safe_ip(self, ip):
        settings = self.load_settings()
        settings["safe_ip"] = ip
        
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
            
    def load_settings(self):
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def get_safe_ip(self):
        """گرفتن IP امن ذخیره شده"""
        settings = self.load_settings()
        return settings.get("safe_ip")
            
    def get_protected_apps(self):
        try:
            with open(self.apps_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
            
    def add_protected_app(self, app):
        apps = self.get_protected_apps()
        if app not in apps:
            apps.append(app)
            with open(self.apps_file, 'w', encoding='utf-8') as f:
                json.dump(apps, f, indent=2, ensure_ascii=False)
                
    def remove_protected_app(self, app):
        apps = self.get_protected_apps()
        if app in apps:
            apps.remove(app)
            with open(self.apps_file, 'w', encoding='utf-8') as f:
                json.dump(apps, f, indent=2, ensure_ascii=False)