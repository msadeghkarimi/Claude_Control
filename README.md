
# 🛡️ NetworkLauncher - ابزار محافظت از IP و Kill Switch

<div dir="rtl">

یک ابزار سبک و قدرتمند برای ویندوز که IP عمومی شما را به صورت real-time مانیتور می‌کند و در صورت قطع VPN یا تغییر IP، به صورت خودکار برنامه‌های حساس را می‌بندد.

</div>

---

## ✨ ویژگی‌ها

<div dir="rtl">

- ⚡ **مانیتورینگ لحظه‌ای**: چک کردن IP هر 0.5 ثانیه
- 🔒 **تایید IP امن**: در اولین اجرا IP فعلی را تایید کنید
- 💀 **Kill Switch خودکار**: بستن فوری مرورگرها، تلگرام، VS Code و ...
- 📊 **تاریخچه کامل**: ثبت تمام اتصالات و تغییرات IP
- 🎨 **رابط کاربری مدرن**: طراحی Dark Mode شبیه VSCode و Discord
- 🔐 **حریم خصوصی کامل**: بدون دیتابیس، بدون Cloud - همه چیز Local
- ⚙️ **انتخاب دستی برنامه‌ها**: خودتان مشخص کنید کدام برنامه‌ها بسته شوند

</div>

---

## 📥 دانلود

<div dir="rtl">

### برای کاربران عادی (بدون نیاز به برنامه‌نویسی)

فایل اجرایی آماده را از بخش [Releases](https://github.com/msadeghkarimi/Claude_Control/releases/latest) دانلود کنید.

**مراحل نصب:**
1. فایل `NetworkLauncher.zip` را دانلود کنید
2. فایل را Extract کنید
3. روی `NetworkLauncher.exe` **راست کلیک** کرده و **Run as Administrator** را انتخاب کنید
4. در اولین اجرا، IP فعلی خود (VPN) را تایید کنید
5. دکمه **Start Protection** را بزنید

⚠️ **نکته مهم**: حتماً برنامه را به عنوان Administrator اجرا کنید تا بتواند برنامه‌ها را ببندد.

</div>

---

## 💻 برای برنامه‌نویسان

<div dir="rtl">

### پیش‌نیازها

- Python 3.10 یا بالاتر
- ویندوز 10/11
- دسترسی Administrator (برای بستن پروسس‌ها)

### نصب و اجرا

#### 1️⃣ کلون کردن پروژه

</div>

```bash
git clone https://github.com/msadeghkarimi/Claude_Control.git
cd Claude_Control
```

<div dir="rtl">

#### 2️⃣ نصب کتابخانه‌ها

</div>

```bash
pip install -r requirements.txt
```

<div dir="rtl">

#### 3️⃣ اجرای برنامه

</div>

```bash
python main.py
```

<div dir="rtl">

#### 4️⃣ ساخت فایل اجرایی (EXE)

برای توزیع برنامه بدون نیاز به نصب پایتون:

</div>

```bash
# نصب PyInstaller
pip install pyinstaller

# ساخت فایل exe (تک فایلی)
python -m PyInstaller --onefile --windowed --name="NetworkLauncher" --icon="assets/icon.ico" --clean main.py

# یا ساخت به صورت پوشه (پایدارتر)
python -m PyInstaller --windowed --name="NetworkLauncher" --icon="assets/icon.ico" --add-data="styles;styles" --add-data="config;config" --collect-all PySide6 --clean main.py
```

<div dir="rtl">

فایل نهایی در پوشه `dist/` قرار می‌گیرد.

</div>

---

## 📂 ساختار پروژه

```
NetworkLauncher/
├── main.py                      # فایل اصلی اجرا
├── requirements.txt             # لیست کتابخانه‌ها
├── assets/                      # آیکون‌ها و تصاویر
│   ├── icon.ico
│   └── logo.png
├── config/                      # فایل‌های تنظیمات (JSON)
│   ├── history.json            # تاریخچه اتصالات
│   ├── settings.json           # تنظیمات برنامه
│   └── protected_apps.json     # لیست برنامه‌های محافظت شده
├── gui/                        # رابط کاربری
│   ├── __init__.py
│   └── dashboard.py            # پنجره اصلی
├── utils/                      # ماژول‌های کمکی
│   ├── __init__.py
│   ├── network.py              # مدیریت شبکه و IP
│   ├── storage.py              # ذخیره‌سازی داده‌ها
│   └── process_killer.py       # بستن پروسس‌ها
└── styles/                     # استایل‌های UI
    └── dark.qss                # تم Dark Mode
```

---

## 🎯 نحوه استفاده

<div dir="rtl">

### راه‌اندازی اولیه

1. **اتصال به VPN**: قبل از اجرا، VPN خود را وصل کنید
2. **اجرای برنامه**: `NetworkLauncher.exe` را به عنوان Administrator اجرا کنید
3. **تایید IP**: پنجره‌ای باز می‌شود که IP فعلی و کشور را نشان می‌دهد
4. اگر این IP امن است (VPN)، دکمه **"✅ Confirm & Start Protection"** را بزنید

### تنظیم برنامه‌های محافظت شده

1. روی دکمه **"⚙️ Manage Apps"** کلیک کنید
2. دو تب خواهید دید:
   - **💾 Saved Apps**: برنامه‌هایی که قبلاً ذخیره کرده‌اید
   - **▶️ Running Apps**: برنامه‌های در حال اجرا که می‌توانید انتخاب کنید

3. در تب **Running Apps**:
   - برنامه‌های مورد نظر (مثل Chrome, Telegram, ...) را تیک بزنید
   - دکمه **"➕ Add Selected to Saved"** را بزنید
4. برنامه‌های انتخاب شده، در صورت تغییر IP بسته خواهند شد

### فعال کردن حفاظت

روی دکمه **"▶️ Start Protection"** کلیک کنید. برنامه هر 0.5 ثانیه IP شما را چک می‌کند.

### در صورت تغییر IP

اگر VPN قطع شود یا IP تغییر کند:
- ✅ تمام برنامه‌های انتخاب شده **بلافاصله بسته می‌شوند**
- ✅ یک پیام هشدار نمایش داده می‌شود
- ✅ رخداد در تاریخچه ثبت می‌شود

</div>

---

## 🔧 تنظیمات پیشرفته

<div dir="rtl">

### فایل‌های JSON

تمام تنظیمات در پوشه `config/` به صورت JSON ذخیره می‌شوند:

**`settings.json`** - تنظیمات اصلی:
</div>

```json
{
  "theme": "dark",
  "developer": "@msadeghkarimi",
  "safe_ip": "185.xxx.xxx.xxx"
}
```

<div dir="rtl">

**`protected_apps.json`** - برنامه‌های محافظت شده:
</div>

```json
[
  "chrome.exe",
  "firefox.exe",
  "telegram.exe",
  "Code.exe"
]
```

<div dir="rtl">

**`history.json`** - تاریخچه اتصالات:
</div>

```json
[
  {
    "date": "2025-01-15 14:30",
    "ip": "185.xxx.xxx.xxx",
    "country": "Germany",
    "city": "Berlin",
    "isp": "Hetzner",
    "status": "safe_ip_set"
  }
]
```

---

## ⚠️ نکات مهم

<div dir="rtl">

### برای کاربران

- 🔴 **حتماً به عنوان Administrator اجرا کنید** وگرنه نمی‌تواند برنامه‌ها را ببندد
- 🔴 **قبل از اجرا VPN را وصل کنید** تا IP صحیح را ثبت کند
- 🟡 اگر Windows Defender برنامه را بلاک کرد، آن را به Exclusions اضافه کنید
- 🟢 برای تست، می‌توانید Notepad باز کنید و آن را به لیست اضافه کنید

### برای برنامه‌نویسان

- استفاده از **PySide6** برای UI
- **psutil** برای مدیریت پروسس‌ها
- **requests** برای درخواست‌های شبکه
- ذخیره‌سازی با **JSON** بدون نیاز به دیتابیس
- معماری **OOP** و **ماژولار**

</div>

---

## 🐛 عیب‌یابی

<div dir="rtl">

### برنامه‌ها بسته نمی‌شوند
- به عنوان Administrator اجرا کنید
- برنامه را از لیست Protected Apps حذف و دوباره اضافه کنید

### IP تشخیص داده نمی‌شود
- اتصال اینترنت را چک کنید
- فایروال ممکن است درخواست‌ها را بلاک کند

### فایل exe اجرا نمی‌شود
- Microsoft Visual C++ Redistributable را نصب کنید: [دانلود](https://aka.ms/vs/17/release/vc_redist.x64.exe)
- Windows Defender را موقتاً غیرفعال کنید

</div>

---

## 📊 تکنولوژی‌های استفاده شده

<div dir="rtl">

| تکنولوژی | نسخه | کاربرد |
|---------|------|--------|
| Python | 3.13+ | زبان اصلی |
| PySide6 | 6.7.0 | رابط کاربری |
| psutil | 5.9.8 | مدیریت پروسس‌ها |
| requests | 2.32.3 | درخواست‌های شبکه |
| PyInstaller | 6.13.0 | ساخت فایل اجرایی |

</div>

---

## 🤝 مشارکت

<div dir="rtl">

برای مشارکت در پروژه:

1. فورک کنید
2. یک برنچ جدید بسازید: `git checkout -b feature/amazing-feature`
3. تغییرات را کامیت کنید: `git commit -m 'Add some feature'`
4. پوش کنید: `git push origin feature/amazing-feature`
5. Pull Request باز کنید

</div>

---

## 📜 لایسنس

<div dir="rtl">

این پروژه تحت لایسنس MIT منتشر شده است. برای اطلاعات بیشتر فایل [LICENSE](LICENSE) را مطالعه کنید.

</div>

---

## 👨‍💻 توسعه‌دهنده

<div dir="rtl">

**محمدصادق کریمی**  
GitHub: [@msadeghkarimi](https://github.com/msadeghkarimi)

اگر این پروژه برایتان مفید بود، حتماً یک ⭐ بدهید!

</div>

---

## 🔗 لینک‌های مرتبط

<div dir="rtl">
## 📦 دانلود

برای دریافت آخرین نسخه فایل اجرایی، از لینک زیر استفاده کنید:

- 📥 [دریافت فایل نصبی (Windows)](https://t.me/msadeghkarimi/3098)
</div>

---

## 📸 تصاویر

<div dir="rtl">

### صفحه اصلی
![Dashboard](screenshots/dashboard.png)

### مدیریت برنامه‌ها
![Manage Apps](screenshots/manage-apps.png)

### Kill Switch فعال
![Kill Switch](screenshots/kill-switch.png)

*تصاویر به زودی اضافه می‌شوند*

</div>

---

## ❓ سوالات متداول

<div dir="rtl">

**س: آیا برنامه رایگان است؟**  
ج: بله، کاملاً رایگان و Open Source.

**س: آیا اطلاعات من ارسال می‌شود؟**  
ج: خیر، هیچ اطلاعاتی ارسال نمی‌شود. همه چیز Local است.

**س: چرا به Administrator نیاز دارد؟**  
ج: برای بستن اجباری برنامه‌هایی مثل Chrome و VS Code به دسترسی Administrator نیاز است.

**س: آیا برای لینوکس یا مک هم کار می‌کند؟**  
ج: خیر، فعلاً فقط برای ویندوز طراحی شده است.

</div>

---

<div align="center" dir="rtl">

ساخته شده با ❤️ در ایران

**اگر این پروژه مفید بود، حتماً Star بدهید! ⭐**

</div>
