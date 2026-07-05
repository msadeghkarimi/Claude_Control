from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                               QFrame, QMessageBox, QFileDialog, QListWidget, 
                               QDialog, QLineEdit)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from utils.network import NetworkManager
from utils.storage import Storage
from utils.process_killer import ProcessKiller
import csv

class IPConfirmDialog(QDialog):
    """دیالوگ تایید IP اولیه فقط یکبار"""
    def __init__(self, current_ip, country):
        super().__init__()
        self.setWindowTitle("🔒 Set Your Safe IP")
        self.setModal(True)
        self.resize(450, 220)
        
        layout = QVBoxLayout(self)
        
        warning = QLabel("🔒 Set Your SAFE VPN IP")
        warning.setFont(QFont("Segoe UI", 14, QFont.Bold))
        warning.setAlignment(Qt.AlignCenter)
        layout.addWidget(warning)
        
        info = QLabel(f"Current IP: <b>{current_ip}</b><br>Country: <b>{country}</b>")
        info.setFont(QFont("Segoe UI", 12))
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        warning2 = QLabel("⚠️ If IP changes, all apps will close!")
        warning2.setStyleSheet("color: #f44336;")
        warning2.setFont(QFont("Segoe UI", 10, QFont.Bold))
        warning2.setAlignment(Qt.AlignCenter)
        layout.addWidget(warning2)
        
        btn_layout = QHBoxLayout()
        
        yes_btn = QPushButton("✅ Confirm & Start Protection")
        yes_btn.setObjectName("primaryButton")
        yes_btn.clicked.connect(self.accept)
        
        no_btn = QPushButton("❌ Cancel")
        no_btn.setObjectName("secondaryButton")
        no_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(yes_btn)
        btn_layout.addWidget(no_btn)
        layout.addLayout(btn_layout)


class ProcessManagerDialog(QDialog):
    """دیالوگ مدیریت برنامه‌های قابل بستن"""
    def __init__(self, storage, process_killer):
        super().__init__()
        self.storage = storage
        self.killer = process_killer
        self.setWindowTitle("⚙️ Manage Protected Apps")
        self.resize(700, 600)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("📋 Apps to Close on IP Change")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Info
        info = QLabel("⚠️ These apps will be force closed if IP changes")
        info.setStyleSheet("color: #f44336;")
        layout.addWidget(info)
        
        # Tab-like sections با دکمه‌ها
        tab_layout = QHBoxLayout()
        
        self.saved_btn = QPushButton("💾 Saved Apps")
        self.saved_btn.setObjectName("tabButton")
        self.saved_btn.setCheckable(True)
        self.saved_btn.setChecked(True)
        self.saved_btn.clicked.connect(lambda: self.switch_tab("saved"))
        
        self.running_btn = QPushButton("▶️ Running Apps")
        self.running_btn.setObjectName("tabButton")
        self.running_btn.setCheckable(True)
        self.running_btn.clicked.connect(lambda: self.switch_tab("running"))
        
        tab_layout.addWidget(self.saved_btn)
        tab_layout.addWidget(self.running_btn)
        tab_layout.addStretch()
        layout.addLayout(tab_layout)
        
        # =============== SAVED APPS SECTION ===============
        self.saved_widget = QWidget()
        saved_layout = QVBoxLayout(self.saved_widget)
        
        # List of saved apps
        self.list_widget = QListWidget()
        self.list_widget.setObjectName("appList")
        saved_layout.addWidget(self.list_widget)
        
        # Add manual section
        add_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter app name manually (e.g., chrome.exe)")
        
        add_btn = QPushButton("➕ Add")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.add_app_manual)
        
        add_layout.addWidget(self.input)
        add_layout.addWidget(add_btn)
        saved_layout.addLayout(add_layout)
        
        # Remove button
        remove_btn = QPushButton("🗑️ Remove Selected")
        remove_btn.setObjectName("secondaryButton")
        remove_btn.clicked.connect(self.remove_saved_app)
        saved_layout.addWidget(remove_btn)
        
        layout.addWidget(self.saved_widget)
        
        # =============== RUNNING APPS SECTION ===============
        self.running_widget = QWidget()
        running_layout = QVBoxLayout(self.running_widget)
        
        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter running apps...")
        self.search_input.textChanged.connect(self.filter_running_apps)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        running_layout.addLayout(search_layout)
        
        # Scroll area for checkboxes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("appScrollArea")
        
        scroll_widget = QWidget()
        self.running_layout = QVBoxLayout(scroll_widget)
        self.running_layout.setSpacing(5)
        
        scroll.setWidget(scroll_widget)
        running_layout.addWidget(scroll)
        
        # Buttons for running apps
        running_btn_layout = QHBoxLayout()
        
        select_all_btn = QPushButton("✅ Select All")
        select_all_btn.setObjectName("secondaryButton")
        select_all_btn.clicked.connect(self.select_all_running)
        
        deselect_all_btn = QPushButton("❌ Deselect All")
        deselect_all_btn.setObjectName("secondaryButton")
        deselect_all_btn.clicked.connect(self.deselect_all_running)
        
        add_selected_btn = QPushButton("➕ Add Selected to Saved")
        add_selected_btn.setObjectName("primaryButton")
        add_selected_btn.clicked.connect(self.add_selected_to_saved)
        
        running_btn_layout.addWidget(select_all_btn)
        running_btn_layout.addWidget(deselect_all_btn)
        running_btn_layout.addWidget(add_selected_btn)
        running_layout.addLayout(running_btn_layout)
        
        self.running_widget.setVisible(False)
        layout.addWidget(self.running_widget)
        
        # Close button
        close_btn = QPushButton("✅ Done")
        close_btn.setObjectName("primaryButton")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        # Load initial data
        self.load_saved_apps()
        self.checkboxes = []
        
    def switch_tab(self, tab_name):
        """تعویض بین تب‌ها"""
        if tab_name == "saved":
            self.saved_btn.setChecked(True)
            self.running_btn.setChecked(False)
            self.saved_widget.setVisible(True)
            self.running_widget.setVisible(False)
            self.load_saved_apps()
            
        elif tab_name == "running":
            self.saved_btn.setChecked(False)
            self.running_btn.setChecked(True)
            self.saved_widget.setVisible(False)
            self.running_widget.setVisible(True)
            self.load_running_apps()
    
    def load_saved_apps(self):
        """بارگذاری برنامه‌های ذخیره شده"""
        self.list_widget.clear()
        apps = self.storage.get_protected_apps()
        for app in apps:
            self.list_widget.addItem(app)
    
    def load_running_apps(self):
        """بارگذاری برنامه‌های در حال اجرا"""
        # پاک کردن لیست قبلی
        while self.running_layout.count():
            child = self.running_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.checkboxes = []
        
        # گرفتن لیست برنامه‌ها
        apps = self.killer.get_running_apps()
        
        if not apps:
            label = QLabel("No user apps running")
            label.setStyleSheet("color: #888; padding: 20px;")
            label.setAlignment(Qt.AlignCenter)
            self.running_layout.addWidget(label)
            return
        
        # ساخت چک‌باکس برای هر برنامه
        saved_apps = self.storage.get_protected_apps()
        
        for app in apps:
            checkbox = QCheckBox(f"{app['name']} ({app['count']} instance{'s' if app['count'] > 1 else ''})")
            checkbox.setObjectName("appCheckbox")
            checkbox.setFont(QFont("Segoe UI", 10))
            checkbox.app_name = app['name']
            
            # اگه قبلاً ذخیره شده، تیک بزن و Disable کن
            if app['name'] in saved_apps:
                checkbox.setChecked(True)
                checkbox.setEnabled(False)
                checkbox.setText(checkbox.text() + " ✅ Already saved")
                checkbox.setStyleSheet("color: #4CAF50;")
            
            self.checkboxes.append(checkbox)
            self.running_layout.addWidget(checkbox)
        
        self.running_layout.addStretch()
    
    def filter_running_apps(self, text):
        """فیلتر کردن برنامه‌های در حال اجرا"""
        text = text.lower()
        for checkbox in self.checkboxes:
            if text in checkbox.text().lower():
                checkbox.setVisible(True)
            else:
                checkbox.setVisible(False)
    
    def select_all_running(self):
        """انتخاب همه برنامه‌های در حال اجرا"""
        for checkbox in self.checkboxes:
            if checkbox.isVisible() and checkbox.isEnabled():
                checkbox.setChecked(True)
    
    def deselect_all_running(self):
        """لغو انتخاب همه"""
        for checkbox in self.checkboxes:
            if checkbox.isEnabled():
                checkbox.setChecked(False)
    
    def add_selected_to_saved(self):
        """اضافه کردن برنامه‌های انتخاب شده به لیست ذخیره"""
        added = []
        
        for checkbox in self.checkboxes:
            if checkbox.isChecked() and checkbox.isEnabled():
                app_name = checkbox.app_name
                self.storage.add_protected_app(app_name)
                added.append(app_name)
                
                # غیرفعال کردن چک‌باکس
                checkbox.setEnabled(False)
                checkbox.setText(checkbox.text().replace(f"({checkbox.app_name})", "") + " ✅ Added!")
                checkbox.setStyleSheet("color: #4CAF50;")
        
        if added:
            QMessageBox.information(self, "Success", 
                f"Added {len(added)} app(s) to protected list:\n" + "\n".join(added))
            self.load_saved_apps()
        else:
            QMessageBox.warning(self, "Warning", "Please select at least one app!")
    
    def add_app_manual(self):
        """اضافه کردن دستی برنامه"""
        app = self.input.text().strip()
        if app:
            # اگه .exe نداره، اضافه کن
            if not app.lower().endswith('.exe'):
                app += '.exe'
            
            self.storage.add_protected_app(app)
            self.load_saved_apps()
            self.input.clear()
            QMessageBox.information(self, "Success", f"Added: {app}")
    
    def remove_saved_app(self):
        """حذف برنامه از لیست ذخیره شده"""
        current = self.list_widget.currentItem()
        if current:
            app_name = current.text()
            reply = QMessageBox.question(self, "Confirm", 
                f"Remove {app_name} from protected list?",
                QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.storage.remove_protected_app(app_name)
                self.load_saved_apps()
                QMessageBox.information(self, "Success", f"Removed: {app_name}")

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                               QFrame, QMessageBox, QFileDialog, QListWidget, 
                               QDialog, QLineEdit, QCheckBox, QScrollArea,
                               QListWidgetItem)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from utils.network import NetworkManager
from utils.storage import Storage
from utils.process_killer import ProcessKiller
import csv


class AppSelectionDialog(QDialog):
    """دیالوگ انتخاب برنامه‌های در حال اجرا برای بستن"""
    def __init__(self, process_killer):
        super().__init__()
        self.killer = process_killer
        self.selected_apps = []
        
        self.setWindowTitle("⚙️ Select Apps to Close")
        self.setModal(True)
        self.resize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("📋 Select Apps to Close on IP Change")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Warning
        warning = QLabel("⚠️ Selected apps will be force closed when IP changes")
        warning.setStyleSheet("color: #f44336; padding: 10px; background: #2d2d30; border-radius: 5px;")
        warning.setFont(QFont("Segoe UI", 10))
        layout.addWidget(warning)
        
        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to filter apps...")
        self.search_input.textChanged.connect(self.filter_apps)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Scroll area for checkboxes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("appScrollArea")
        
        scroll_widget = QWidget()
        self.apps_layout = QVBoxLayout(scroll_widget)
        self.apps_layout.setSpacing(5)
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Select/Deselect All
        btn_layout = QHBoxLayout()
        
        select_all_btn = QPushButton("✅ Select All")
        select_all_btn.setObjectName("secondaryButton")
        select_all_btn.clicked.connect(self.select_all)
        
        deselect_all_btn = QPushButton("❌ Deselect All")
        deselect_all_btn.setObjectName("secondaryButton")
        deselect_all_btn.clicked.connect(self.deselect_all)
        
        btn_layout.addWidget(select_all_btn)
        btn_layout.addWidget(deselect_all_btn)
        layout.addLayout(btn_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save Selection")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_selection)
        
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.setObjectName("secondaryButton")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        # Load running apps
        self.load_apps()
        
    def load_apps(self):
        """بارگذاری برنامه‌های در حال اجرا"""
        # پاک کردن لیست قبلی
        while self.apps_layout.count():
            child = self.apps_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.checkboxes = []
        
        # گرفتن لیست برنامه‌ها
        apps = self.killer.get_running_apps()
        
        if not apps:
            label = QLabel("No user apps running")
            label.setStyleSheet("color: #888; padding: 20px;")
            label.setAlignment(Qt.AlignCenter)
            self.apps_layout.addWidget(label)
            return
        
        # ساخت چک‌باکس برای هر برنامه
        for app in apps:
            checkbox = QCheckBox(f"{app['name']} ({app['count']} instance{'s' if app['count'] > 1 else ''})")
            checkbox.setObjectName("appCheckbox")
            checkbox.setFont(QFont("Segoe UI", 10))
            checkbox.app_name = app['name']
            
            self.checkboxes.append(checkbox)
            self.apps_layout.addWidget(checkbox)
        
        self.apps_layout.addStretch()
        
    def filter_apps(self, text):
        """فیلتر کردن برنامه‌ها"""
        text = text.lower()
        for checkbox in self.checkboxes:
            if text in checkbox.text().lower():
                checkbox.setVisible(True)
            else:
                checkbox.setVisible(False)
    
    def select_all(self):
        """انتخاب همه"""
        for checkbox in self.checkboxes:
            if checkbox.isVisible():
                checkbox.setChecked(True)
    
    def deselect_all(self):
        """لغو انتخاب همه"""
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)
    
    def save_selection(self):
        """ذخیره برنامه‌های انتخاب شده"""
        self.selected_apps = []
        
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                self.selected_apps.append(checkbox.app_name)
        
        if not self.selected_apps:
            QMessageBox.warning(self, "Warning", "Please select at least one app!")
            return
        
        self.accept()
    
    def get_selected_apps(self):
        """برگرداندن لیست برنامه‌های انتخاب شده"""
        return self.selected_apps
class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.network = NetworkManager()
        self.storage = Storage()
        self.killer = ProcessKiller()
        
        self.safe_ip = None
        self.monitoring = False
        
        self.init_ui()
        
        # بارگذاری تاریخچه
        self.populate_table(self.storage.load_history())
        
        # چک کن آیا قبلاً IP امن ست شده؟
        saved_ip = self.storage.get_safe_ip()
        if saved_ip:
            self.safe_ip = saved_ip
            self.safe_ip_label.setText(f"Safe IP: {self.safe_ip}")
            # شروع خودکار حفاظت
            QTimer.singleShot(500, self.start_monitoring)
        else:
            # اولین بار - بپرس
            QTimer.singleShot(500, self.ask_safe_ip)
        
    def init_ui(self):
        self.setWindowTitle("IP Protection - Kill Switch")
        self.setGeometry(100, 100, 1100, 750)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        header = self.create_header()
        layout.addWidget(header)
        
        self.protection_status = self.create_protection_status()
        layout.addWidget(self.protection_status)
        
        cards = self.create_info_cards()
        layout.addWidget(cards)
        
        buttons = self.create_buttons()
        layout.addWidget(buttons)
        
        self.table = self.create_table()
        layout.addWidget(self.table)
        
        footer = self.create_footer()
        layout.addWidget(footer)
        
    def create_header(self):
        header = QFrame()
        header.setObjectName("header")
        layout = QHBoxLayout(header)
        
        title = QLabel("🛡️ IP Protection - Kill Switch")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        
        self.status_label = QLabel("🔴 OFFLINE")
        self.status_label.setFont(QFont("Segoe UI", 12))
        
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.status_label)
        
        return header
    
    def create_protection_status(self):
        frame = QFrame()
        frame.setObjectName("protectionFrame")
        layout = QVBoxLayout(frame)
        
        self.protection_label = QLabel("🔒 Protection: OFF")
        self.protection_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.protection_label.setAlignment(Qt.AlignCenter)
        
        self.safe_ip_label = QLabel("Safe IP: Not Set")
        self.safe_ip_label.setFont(QFont("Segoe UI", 12))
        self.safe_ip_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.protection_label)
        layout.addWidget(self.safe_ip_label)
        
        return frame
    
    def create_info_cards(self):
        container = QFrame()
        container.setObjectName("cardsContainer")
        layout = QHBoxLayout(container)
        layout.setSpacing(15)
        
        self.cards = {
            "ip": self.create_card("Current IP", "---"),
            "country": self.create_card("Country", "---"),
            "city": self.create_card("City", "---"),
            "isp": self.create_card("ISP", "---"),
            "time": self.create_card("Last Check", "---")
        }
        
        for card in self.cards.values():
            layout.addWidget(card)
            
        return container
    
    def create_card(self, title, value):
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        title_label.setFont(QFont("Segoe UI", 10))
        
        value_label = QLabel(value)
        value_label.setObjectName("cardValue")
        value_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        value_label.setWordWrap(True)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        card.value_label = value_label
        return card
    
    def create_buttons(self):
        container = QFrame()
        layout = QHBoxLayout(container)
        layout.setSpacing(10)
        
        self.protect_btn = QPushButton("▶️ Start Protection")
        self.protect_btn.setObjectName("primaryButton")
        self.protect_btn.clicked.connect(self.toggle_protection)
        
        apps_btn = QPushButton("⚙️ Manage Apps")
        apps_btn.setObjectName("secondaryButton")
        apps_btn.clicked.connect(self.manage_apps)
        
        change_ip_btn = QPushButton("🔄 Change Safe IP")
        change_ip_btn.setObjectName("secondaryButton")
        change_ip_btn.clicked.connect(self.ask_safe_ip)
        
        export_btn = QPushButton("📤 Export CSV")
        export_btn.setObjectName("secondaryButton")
        export_btn.clicked.connect(self.export_history)
        
        clear_btn = QPushButton("🗑️ Clear History")
        clear_btn.setObjectName("secondaryButton")
        clear_btn.clicked.connect(self.clear_history)
        
        layout.addWidget(self.protect_btn)
        layout.addWidget(apps_btn)
        layout.addWidget(change_ip_btn)
        layout.addWidget(export_btn)
        layout.addWidget(clear_btn)
        layout.addStretch()
        
        return container
    
    def create_table(self):
        table = QTableWidget()
        table.setObjectName("historyTable")
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["Status", "Date", "IP Address", "Country", "City", "ISP"])
        table.horizontalHeader().setStretchLastSection(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setAlternatingRowColors(True)
        
        return table
    
    def create_footer(self):
        footer = QLabel("Developer: @msadeghkarimi | IP Kill Switch Protection")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignCenter)
        footer.setFont(QFont("Segoe UI", 9))
        
        return footer
    
    def ask_safe_ip(self):
        """تنظیم IP امن"""
        # توقف مانیتورینگ موقت
        if self.monitoring:
            self.stop_monitoring()
        
        data = self.network.get_network_info()
        
        if data["status"] == "offline":
            QMessageBox.critical(self, "Error", "No internet connection!\nConnect to VPN first.")
            return
        
        dialog = IPConfirmDialog(data["ip"], data["country"])
        
        if dialog.exec() == QDialog.Accepted:
            self.safe_ip = data["ip"]
            self.storage.save_safe_ip(self.safe_ip)
            self.safe_ip_label.setText(f"Safe IP: {self.safe_ip}")
            self.update_display(data)
            
            # ذخیره در تاریخچه
            data["status"] = "safe_ip_set"
            self.storage.add_history(data)
            self.populate_table(self.storage.load_history())
            
            # شروع خودکار
            self.start_monitoring()
        else:
            QMessageBox.warning(self, "Cancelled", "Protection not activated.")
            
    def toggle_protection(self):
        """روشن/خاموش کردن حفاظت"""
        if not self.safe_ip:
            QMessageBox.warning(self, "Warning", "Set Safe IP first!")
            return
            
        if not self.monitoring:
            self.start_monitoring()
        else:
            self.stop_monitoring()
            
    def start_monitoring(self):
        """شروع مانیتورینگ"""
        if not self.safe_ip:
            return
            
        self.monitoring = True
        self.protection_label.setText("🟢 Protection: ACTIVE")
        self.protection_label.setStyleSheet("color: #4CAF50;")
        self.protect_btn.setText("⏸️ Stop Protection")
        
        # چک هر 0.5 ثانیه (خیلی سریع)
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_ip)
        self.timer.start(500)  # 500ms = 0.5 second
        
    def stop_monitoring(self):
        """توقف مانیتورینگ"""
        self.monitoring = False
        self.protection_label.setText("🔴 Protection: OFF")
        self.protection_label.setStyleSheet("color: #f44336;")
        self.protect_btn.setText("▶️ Start Protection")
        
        if hasattr(self, 'timer'):
            self.timer.stop()
        
    def check_ip(self):
        """چک کردن IP هر 0.5 ثانیه"""
        current_ip = self.network.get_current_ip()
        
        if current_ip is None:
            self.status_label.setText("🔴 OFFLINE")
            return
            
        self.status_label.setText("🟢 ONLINE")
        
        # اگر IP تغییر کرد = بلافاصله Kill
        if current_ip != self.safe_ip:
            self.trigger_kill_switch(current_ip)
            
    def trigger_kill_switch(self, new_ip):
        """فعال‌سازی Kill Switch - بدون سوال"""
        # توقف مانیتورینگ
        self.stop_monitoring()
        
        # گرفتن اطلاعات کامل IP جدید
        data = self.network.get_network_info()
        self.update_display(data)
        
        # ذخیره در تاریخچه
        data["status"] = "ip_changed_kill"
        self.storage.add_history(data)
        self.populate_table(self.storage.load_history())
        
        # بستن برنامه‌های ذخیره شده
        protected_apps = self.storage.get_protected_apps()
        killed, failed = self.killer.kill_selected_apps(protected_apps)
        
        # پیام هشدار
        msg = f"🚨 IP CHANGED - KILL SWITCH ACTIVATED!\n\n"
        msg += f"Safe IP: {self.safe_ip}\n"
        msg += f"New IP: {new_ip}\n"
        msg += f"Country: {data['country']}\n\n"
        
        if killed:
            msg += f"🔒 {len(killed)} apps closed:\n"
            msg += "\n".join(f"• {app}" for app in killed[:10])
            if len(killed) > 10:
                msg += f"\n... and {len(killed)-10} more"
        else:
            msg += "No apps were running."
        
        if failed:
            msg += f"\n\n❌ Failed: {len(failed)} apps"
        
        QMessageBox.critical(self, "⚠️ KILL SWITCH ACTIVATED", msg)
    def update_display(self, data):
        """بروزرسانی نمایش"""
        self.status_label.setText("🟢 ONLINE")
        self.cards["ip"].value_label.setText(data["ip"])
        self.cards["country"].value_label.setText(data["country"])
        self.cards["city"].value_label.setText(data["city"])
        self.cards["isp"].value_label.setText(data["isp"])
        self.cards["time"].value_label.setText(data["date"])
        
    def manage_apps(self):
        """مدیریت برنامه‌ها"""
        dialog = ProcessManagerDialog(self.storage, self.killer)  # اضافه کردن killer
        dialog.exec()
        
    def populate_table(self, history):
        self.table.setRowCount(0)
        
        for record in reversed(history):
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # تشخیص وضعیت
            status_icon = "🟢"
            if record.get("status") == "ip_changed_kill":
                status_icon = "🔴"
            elif record.get("status") == "safe_ip_set":
                status_icon = "🔒"
            
            self.table.setItem(row, 0, QTableWidgetItem(status_icon))
            self.table.setItem(row, 1, QTableWidgetItem(record["date"]))
            self.table.setItem(row, 2, QTableWidgetItem(record["ip"]))
            self.table.setItem(row, 3, QTableWidgetItem(record["country"]))
            self.table.setItem(row, 4, QTableWidgetItem(record["city"]))
            self.table.setItem(row, 5, QTableWidgetItem(record["isp"]))
            
    def export_history(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv)")
        
        if filename:
            history = self.storage.load_history()
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["date", "ip", "country", "city", "isp", "status"])
                writer.writeheader()
                writer.writerows(history)
                
            QMessageBox.information(self, "Success", f"Exported {len(history)} records")
            
    def clear_history(self):
        reply = QMessageBox.question(self, "Confirm", "Clear all history?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.storage.clear_history()
            self.table.setRowCount(0)
            QMessageBox.information(self, "Success", "History cleared")