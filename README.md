# 🧹 Auto Remove Channel Members with Telethon | حذف خودکار اعضای چنل با Telethon

> 🇬🇧 A fast, professional, and safe utility for removing Telegram channel/supergroup members with full control and a dry-run mode.
>
> 🇮🇷 ابزاری سریع، حرفه‌ای و ایمن برای حذف اعضای چنل یا سوپرگروه تلگرام، با کنترل کامل و امکان تست قبل از حذف واقعی.

---

## ✨ Features | امکانات

### 🇬🇧 English

- Remove all members except your Telegram contacts
- Keep your own account and administrators by default
- Dry-Run mode (preview without removing anyone)
- Ban instead of Kick
- Configurable delay for large channels/groups
- Clear and readable output

### 🇮🇷 فارسی

- حذف تمام اعضا به‌جز مخاطبین تلگرام شما
- نگه داشتن خود اکانت و ادمین‌ها (به‌صورت پیش‌فرض)
- حالت **Dry-Run** برای تست بدون حذف واقعی
- امکان **Ban** به‌جای **Kick**
- تنظیم **Delay** برای چنل‌ها و گروه‌های بزرگ
- خروجی کاملاً شفاف و قابل فهم

---

## 🚀 Installation | نصب

```bash
python3 -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🔐 Get API ID & API Hash | دریافت API ID و API Hash

Visit:

https://my.telegram.org

Open **API Development Tools** and obtain:

- `api_id`
- `api_hash`

---

## ▶️ Usage | استفاده

### 🧪 Dry Run (No members will be removed)
### تست بدون حذف واقعی

```bash
python purge_channel_members.py @your_channel \
    --api-id 12345 \
    --api-hash abcdef
```

> No members will be removed until you add `--execute`.
>
> تا زمانی که `--execute` را اضافه نکنید، هیچ عضوی حذف نخواهد شد.

---

### ✅ Execute Removal
### حذف واقعی

```bash
python purge_channel_members.py @your_channel \
    --api-id 12345 \
    --api-hash abcdef \
    --execute
```

---

### 🐢 Large Channels / Groups
### برای چنل‌ها و گروه‌های بزرگ

```bash
python purge_channel_members.py @your_channel \
    --execute \
    --delay 3
```

---

### 🚫 Ban Instead of Kick
### Ban به‌جای Kick

```bash
python purge_channel_members.py @your_channel \
    --execute \
    --ban-instead-of-kick
```

---

### 👮 Remove Non-Contact Admins
### حذف ادمین‌های غیرمخاطب

```bash
python purge_channel_members.py @your_channel \
    --execute \
    --no-keep-admins
```

---

## 🌐 Environment Variables | متغیرهای محیطی

```bash
export TG_API_ID=12345
export TG_API_HASH=abcdef
export TG_PHONE=+98912xxxxxxx
```

---

## ⚠️ Warning | هشدار

**English**

This tool is intended for Telegram accounts with **Owner/Admin** privileges.

Always test with **Dry-Run** before performing an actual removal.

**فارسی**

این ابزار برای حساب‌هایی طراحی شده که دسترسی **Owner** یا **Admin** دارند.

قبل از اجرای واقعی، حتماً ابتدا حالت **Dry-Run** را امتحان کنید.
