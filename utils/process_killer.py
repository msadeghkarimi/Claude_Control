import psutil
import subprocess
import os

class ProcessKiller:
    """کلاس برای بستن اجباری پروسس‌ها"""
    
    def get_running_apps(self):
        """گرفتن لیست برنامه‌های کاربر (نه سیستم)"""
        apps = {}
        current_pid = os.getpid()
        
        # لیست پروسس‌های سیستمی که نباید نشون داده بشن
        system_processes = {
            'system', 'registry', 'smss.exe', 'csrss.exe', 'wininit.exe',
            'services.exe', 'lsass.exe', 'svchost.exe', 'dwm.exe', 'winlogon.exe',
            'explorer.exe', 'taskhostw.exe', 'sihost.exe', 'ctfmon.exe',
            'runtimebroker.exe', 'searchindexer.exe', 'searchhost.exe',
            'startmenuexperiencehost.exe', 'shellexperiencehost.exe',
            'textinputhost.exe', 'lockapp.exe', 'widgetservice.exe',
            'securityhealthservice.exe', 'mpsigstub.exe', 'msmpeng.exe',
            'nissrv.exe', 'system idle process', 'fontdrvhost.exe',
            'wudfhost.exe', 'conhost.exe', 'dllhost.exe', 'dashost.exe'
        }
        
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'create_time']):
            try:
                proc_name = proc.info['name']
                proc_pid = proc.info['pid']
                
                # رد کردن برنامه خودمون
                if proc_pid == current_pid:
                    continue
                
                # رد کردن پروسس‌های سیستمی
                if proc_name.lower() in system_processes:
                    continue
                
                # رد کردن پروسس‌های بدون نام یا خالی
                if not proc_name or proc_name.strip() == '':
                    continue
                
                # اگه این برنامه قبلاً اضافه نشده
                if proc_name not in apps:
                    apps[proc_name] = {
                        'name': proc_name,
                        'count': 1,
                        'pids': [proc_pid]
                    }
                else:
                    apps[proc_name]['count'] += 1
                    apps[proc_name]['pids'].append(proc_pid)
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
            except Exception:
                pass
        
        # تبدیل به لیست و مرتب‌سازی
        app_list = sorted(apps.values(), key=lambda x: x['name'].lower())
        
        return app_list
    
    def kill_selected_apps(self, selected_apps):
        """بستن برنامه‌های انتخاب شده"""
        killed = []
        failed = []
        
        print("\n" + "="*50)
        print("🔴 KILL SWITCH ACTIVATED")
        print("="*50)
        
        for app_name in selected_apps:
            try:
                print(f"\n📍 Killing: {app_name}")
                
                # پیدا کردن همه پروسس‌های این برنامه
                killed_count = 0
                for proc in psutil.process_iter(['name']):
                    try:
                        if proc.info['name'] == app_name:
                            proc.kill()
                            killed_count += 1
                    except:
                        pass
                
                # با taskkill هم امتحان کن
                result = subprocess.run(
                    ['taskkill', '/F', '/IM', app_name, '/T'],
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                if killed_count > 0 or "SUCCESS" in result.stdout:
                    killed.append(app_name)
                    print(f"  ✅ Killed: {app_name} ({killed_count} instances)")
                else:
                    failed.append(app_name)
                    print(f"  ❌ Failed: {app_name}")
                    
            except Exception as e:
                failed.append(app_name)
                print(f"  ❌ Error with {app_name}: {e}")
        
        print("\n" + "="*50)
        print(f"✅ Killed: {len(killed)} apps")
        print(f"❌ Failed: {len(failed)} apps")
        print("="*50 + "\n")
        
        return killed, failed
    
    def kill_protected_apps(self, app_list):
        """بستن برنامه‌های از پیش تعریف شده"""
        return self.kill_selected_apps(app_list)[0]