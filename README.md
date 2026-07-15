# 🧹 حذف خودکار اعضای چنل با Telethon

> یک ابزار حرفه‌ای و سریع برای پاک‌سازی اعضای چنل/سوپرگروپ، با کنترل کامل و امکان تست قبل از حذف واقعی.

## ✨ امکانات

- حذف اعضا به‌جز مخاطبین تلگرام شما
- نگه‌داشتن خود اکانت و ادمین‌ها (به‌صورت پیش‌فرض)
- حالت Dry-Run برای تست بدون حذف واقعی
- امکان Ban به‌جای Kick
- تنظیم Delay برای چنل‌های بزرگ
- خروجی کاملا شفاف و قابل‌درک

---

## 🚀 نصب سریع

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🔐 گرفتن API ID و API Hash

از این لینک استفاده کنید:

https://my.telegram.org

در بخش API development tools، مقدارهای زیر را بگیرید:

- `api_id`
- `api_hash`

---

## ▶️ استفاده

### 1) تست بدون حذف واقعی

```bash
python purge_channel_members.py @your_channel --api-id 12345 --api-hash abcdef
```

تا زمانی که `--execute` را نداده باشید، هیچ عضوی حذف نخواهد شد.

### 2) حذف واقعی

```bash
python purge_channel_members.py @your_channel --api-id 12345 --api-hash abcdef --execute
```

### 3) برای چنل‌های بزرگ

```bash
python purge_channel_members.py @your_channel --execute --delay 3
```

### 4) Ban به‌جای Kick

```bash
python purge_channel_members.py @your_channel --execute --ban-instead-of-kick
```

### 5) حذف کردن ادمین‌های غیرمخاطب هم

```bash
python purge_channel_members.py @your_channel --execute --no-keep-admins
```

---

## 🌐 تنظیم متغیرهای محیطی

برای استفاده راحت‌تر:

```bash
export TG_API_ID=12345
export TG_API_HASH=abcdef
export TG_PHONE=+98912xxxxxxx
```

---

## ⚠️ نکته مهم

این ابزار برای حساب‌های دارای دسترسی owner/admin طراحی شده و باید با دقت و مسئولانه استفاده شود. قبل از اجرای واقعی، حتماً حالت dry-run را امتحان کنید.


