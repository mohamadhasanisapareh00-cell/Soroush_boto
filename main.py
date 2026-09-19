import asyncio
import json
import os
import random
import time

from splusthon import SoroushClient as SplusClient

# ============================================================
# تنظیمات
# ============================================================

CONFIG_FILE = "config.json"

DEFAULT_INTERVAL = 120
MIN_INTERVAL = 30

client = SplusClient("/tmp/mmd_sender")

stats = {
    "success": 0,
    "errors": 0,
    "last_message": "",
    "last_group": "",
    "last_time": 0
}


# ============================================================
# پیام‌های پیش‌فرض
# ============================================================

DEFAULT_MESSAGES = [

    # 🎬 فیلم
    "🎬 امشب چه فیلمی پیشنهاد میدید؟",
    "🍿 یه فیلم خوب برای امشب چی ببینیم؟",
    "🎥 بهترین فیلمی که اخیراً دیدید چی بوده؟",
    "🎬 کسی فیلم جذاب سراغ داره؟",
    "🍿 فیلم کمدی خوب چی پیشنهاد میدید؟",
    "🎥 یه فیلم اکشن خوب معرفی کنید.",
    "🎬 فیلم معمایی خوب می‌شناسید؟",
    "🍿 یه فیلم خانوادگی خوب چی پیشنهاد میدید؟",
    "🎥 کسی سریال جدید دیده؟",
    "🎬 فیلم ایرانی خوب چی پیشنهاد میدید؟",
    "🍿 فیلم خارجی خوب معرفی کنید.",
    "🎥 اهل فیلم و سریال هستید؟",
    "🎬 فیلم علمی‌تخیلی چی ببینیم؟",
    "🍿 یه فیلم برای آخر هفته معرفی کنید.",
    "🎥 فیلم هیجانی خوب سراغ دارید؟",
    "🎬 فیلم تاریخی خوب می‌شناسید؟",
    "🍿 یه فیلم قدیمی ولی جذاب معرفی کنید.",
    "🎥 بهترین سریالی که دیدید چی بوده؟",
    "🎬 فیلم‌بازا کجان؟ 😂",
    "🍿 امشب نوبت چه فیلمیه؟",
    "🎥 کسی پیشنهاد فیلم داره؟",
    "🎬 یه فیلم ارزش دیدن معرفی کنید.",
    "🍿 چه ژانری بیشتر دوست دارید؟",
    "🎥 فیلم مورد علاقه‌تون چیه؟",

    # 🎞️ سریال
    "📺 این روزا چه سریالی می‌بینید؟",
    "🎬 سریال کوتاه و جذاب چی پیشنهاد میدید؟",
    "🍿 سریال جدید و دیدنی سراغ دارید؟",
    "📺 کسی سریال معمایی خوب می‌شناسه؟",
    "🎥 سریال کمدی چی پیشنهاد میدید؟",
    "📺 سریال جنایی خوب چی داریم؟",
    "🎬 برای شروع یه سریال جدید چی پیشنهاد می‌کنید؟",
    "🍿 کسی سریال تموم کرده و پیشنهاد خوب داره؟",

    # 💬 تعاملی
    "💬 اگه فقط یک فیلم بخواید پیشنهاد بدید، چی انتخاب می‌کنید؟",
    "🎬 فیلم یا سریال؟",
    "🍿 کمدی یا اکشن؟",
    "🎥 فیلم قدیمی یا فیلم جدید؟",
    "📺 سریال کوتاه یا سریال طولانی؟",
    "🎬 ایرانی یا خارجی؟",
    "🍿 آخرین فیلمی که دیدید چی بود؟",
    "🎥 اهل فیلم دیدن شبانه هستید؟",
    "🎬 یه فیلم خوب معرفی کنید تا بقیه هم استفاده کنن.",
    "💬 بهترین ژانر از نظر شما چیه؟",

    # 🤝 تبادل
    "🤝 کسی برای تبادل دوستانه هست؟",
    "🔄 تبادل گپ با گپ انجام میدیم.",
    "🤝 کسی پایه تبادله؟",
    "🔄 برای تبادل هماهنگ کنیم؟",
    "📢 کسی دنبال تبادله؟",
    "🤝 تبادل دوطرفه کسی هست؟",
    "🔄 تبادل دوستانه داریم؟",
    "📢 دوستان، کسی برای همکاری و تبادل هست؟",
    "🤝 کسی مایل به تبادله؟",
    "🔄 تبادل با هماهنگی انجام میشه.",
    "📢 دنبال گپ برای تبادل هستیم.",
    "🤝 کسی آماده تبادله؟",
    "🔄 تبادل گپ به گپ کسی هست؟",
    "📢 تبادل دوستانه با گپ‌های فعال.",
    "🤝 کسی دنبال همکاری و تبادل هست؟",
    "🔄 امروز کسی برای تبادل هست؟",
    "📢 تبادل با هماهنگی دوستان.",
    "🤝 تبادل دوطرفه انجام میدیم.",

    # 😄 دوستانه
    "😄 بچه‌ها چه خبر؟",
    "👋 سلام به همه دوستان گپ.",
    "😊 امروز حالتون چطوره؟",
    "😂 یه گپ خوب بدون فیلم‌بازا نمیشه!",
    "🎬 فیلم‌بازا جمع شید 😂",
    "🍿 وقت فیلم دیدنه!",
    "😎 اهل فیلم و سریال کیه؟",
    "🎥 یه فیلم خوب، یه گپ خوب.",
    "😊 پیشنهاد خوب همیشه استقبال میشه.",
    "🎬 فیلم‌بازها نظر بدن.",

    # 🔄 ترکیبی
    "🎬 فیلم و سریال‌بازا کجان؟ راستی کسی پایه تبادله؟",
    "🍿 یه فیلم خوب معرفی کنید؛ برای تبادل هم پیام بدید.",
    "🎥 فیلم خوب سراغ دارید؟ دوستان تبادل هم می‌تونن هماهنگ کنن.",
    "🎬 معرفی فیلم و همکاری دوستانه.",
    "🤝 تبادل دوستانه + معرفی فیلم.",
    "🍿 فیلم خوب پیدا کنیم و گپ بزنیم.",
    "🎥 کسی فیلم جدید دیده؟ نظرتون رو بگید.",
    "🔄 کسی برای تبادل دوطرفه هست؟",
    "🎬 چه فیلمی ارزش دیدن داره؟",
    "🤝 برای همکاری و تبادل دوستانه هماهنگ کنیم.",

]


# ============================================================
# تنظیمات پیش‌فرض
# ============================================================

DEFAULT_CONFIG = {
    "owner_id": None,
    "link": "",
    "groups": [],
    "messages": DEFAULT_MESSAGES.copy(),
    "interval": DEFAULT_INTERVAL,
    "sending": True
}


# ============================================================
# ابزارها
# ============================================================

def load_config():

    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_CONFIG.copy()

    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError("config باید dictionary باشد")

        for key, value in DEFAULT_CONFIG.items():

            if key not in data:
                data[key] = value

        if not isinstance(data["groups"], list):
            data["groups"] = []
        else:
            data["groups"] = [
                str(g) for g in data["groups"]
            ]

        if not isinstance(data["messages"], list):
            data["messages"] = DEFAULT_MESSAGES.copy()

        try:
            data["interval"] = int(data["interval"])
        except (TypeError, ValueError):
            data["interval"] = DEFAULT_INTERVAL

        if data["interval"] < MIN_INTERVAL:
            data["interval"] = MIN_INTERVAL

        return data

    except Exception as e:

        print(
            "⚠️ خطا در config:",
            repr(e)
        )

        return DEFAULT_CONFIG.copy()


config = load_config()


def save_config():

    try:

        temp_file = CONFIG_FILE + ".tmp"

        with open(
            temp_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                config,
                f,
                ensure_ascii=False,
                indent=2
            )

        os.replace(
            temp_file,
            CONFIG_FILE
        )

        return True

    except Exception as e:

        print(
            "❌ خطا در ذخیره config:",
            repr(e)
        )

        return False


def is_owner(sender_id):

    owner = config.get("owner_id")

    if owner is None:
        return False

    return str(owner) == str(sender_id)


def looks_like_group_link(text):

    text = text.strip().lower()

    if not text.startswith(
        ("http://", "https://")
    ):
        return False

    return (
        "splus.ir" in text
        or
        "soroushplus.ir" in text
    )


def now_string():

    return time.strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def choose_message():

    messages = config.get(
        "messages",
        []
    )

    if not messages:
        return "🎬 کسی فیلم خوب سراغ داره؟"

    previous = stats.get(
        "last_message",
        ""
    )

    if len(messages) == 1:
        return messages[0]

    choices = [
        x for x in messages
        if x != previous
    ]

    if not choices:
        return random.choice(messages)

    return random.choice(choices)


# ============================================================
# لیست گپ‌ها
# ============================================================

def get_groups_list():

    groups = config.get(
        "groups",
        []
    )

    if not groups:
        return "📋 لیست گپ‌ها خالیه."

    result = [
        "📋 لیست گپ‌ها\n"
    ]

    for i, group_id in enumerate(
        groups,
        1
    ):

        result.append(
            f"🟢 {i}. {group_id}"
        )

    return "\n".join(result)


# ============================================================
# وضعیت
# ============================================================

def get_status():

    groups = len(
        config.get(
            "groups",
            []
        )
    )

    messages = len(
        config.get(
            "messages",
            []
        )
    )

    sending = (
        "🟢 روشن"
        if config.get("sending")
        else
        "🔴 خاموش"
    )

    last_time = stats.get(
        "last_time",
        0
    )

    if last_time:
        last = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime(last_time)
        )
    else:
        last = "هنوز ارسال نشده"

    return (
        "📊 وضعیت ربات\n\n"
        f"⚙️ ارسال: {sending}\n"
        f"👥 تعداد گپ‌ها: {groups}\n"
        f"💬 تعداد پیام‌ها: {messages}\n"
        f"⏱ فاصله: {config['interval']} ثانیه\n"
        f"✅ ارسال موفق: {stats['success']}\n"
        f"❌ خطا: {stats['errors']}\n"
        f"🕐 آخرین ارسال: {last}"
    )


# ============================================================
# آمار
# ============================================================

def get_stats():

    return (
        "📊 آمار ربات\n\n"
        f"✅ موفق: {stats['success']}\n"
        f"❌ خطا: {stats['errors']}\n"
        f"👥 گپ‌ها: {len(config['groups'])}\n"
        f"💬 پیام‌ها: {len(config['messages'])}\n"
        f"⏱ فاصله: {config['interval']} ثانیه"
    )


# ============================================================
# راهنما
# ============================================================

def get_help():

    return """
👑 دستورات مالک

━━━━━━━━━━━━━━
👥 مدیریت گپ
━━━━━━━━━━━━━━

.add
➜ افزودن گپ فعلی

.remove
➜ حذف گپ فعلی

لیست گپ ها
➜ نمایش گپ‌ها

.clear
➜ پاک کردن لیست گپ‌ها

━━━━━━━━━━━━━━
📤 ارسال
━━━━━━━━━━━━━━

.on
➜ روشن کردن ارسال

.off
➜ خاموش کردن ارسال

.interval 120
➜ تغییر فاصله ارسال

.test
➜ ارسال آزمایشی در گپ فعلی

━━━━━━━━━━━━━━
💬 پیام‌ها
━━━━━━━━━━━━━━

.addmsg متن
➜ اضافه کردن پیام

.delmsg متن
➜ حذف پیام

.msgs
➜ تعداد پیام‌ها

.clearmsgs
➜ حذف پیام‌های سفارشی

━━━━━━━━━━━━━━
🔗 لینک
━━━━━━━━━━━━━━

.setlink لینک
➜ تنظیم لینک

.link
➜ نمایش لینک

.dellink
➜ حذف لینک

━━━━━━━━━━━━━━
📊 آمار
━━━━━━━━━━━━━━

.stats
➜ آمار ارسال

.status
➜ وضعیت ربات

.resetstats
➜ صفر کردن آمار

━━━━━━━━━━━━━━

.help
➜ همین راهنما
"""


# ============================================================
# ورود با لینک
# ============================================================

async def join_and_register(link):

    try:

        print(
            "🔗 تلاش برای ورود:",
            link
        )

        result = await client.join_group_by_invite(
            link
        )

        print(
            "📦 نتیجه:",
            repr(result)
        )

        group_id = None

        if isinstance(result, dict):

            group_id = (
                result.get("chat_id")
                or
                result.get("id")
            )

            chat = result.get("chat")

            if isinstance(chat, dict):

                group_id = (
                    chat.get("id")
                    or
                    chat.get("chat_id")
                    or
                    group_id
                )

        if group_id is not None:

            group_id = str(group_id)

            if group_id not in config["groups"]:

                config["groups"].append(
                    group_id
                )

                save_config()

            return (
                True,
                group_id,
                "✅ ورود موفق بود و گپ ثبت شد."
            )

        return (
            True,
            None,
            "✅ ورود انجام شد، ولی آیدی گپ دریافت نشد."
        )

    except Exception as e:

        print(
            "❌ خطای ورود:",
            repr(e)
        )

        return (
            False,
            None,
            f"❌ ورود انجام نشد:\n{e}"
        )


# ============================================================
# پردازش دستورات مالک
# ============================================================

async def owner_command(
    event,
    text
):

    chat_id = event.chat_id

    chat_id_str = str(chat_id) if chat_id is not None else None

    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    if text == ".help":

        await event.respond(
            get_help()
        )

        return True

    # --------------------------------------------------------
    # ADD
    # --------------------------------------------------------

    if text == ".add":

        if chat_id_str is None:

            await event.respond(
                "❌ آیدی گپ پیدا نشد."
            )

            return True

        if chat_id_str not in config["groups"]:

            config["groups"].append(
                chat_id_str
            )

            save_config()

            await event.respond(
                "✅ این گپ به لیست اضافه شد."
            )

        else:

            await event.respond(
                "⚠️ این گپ قبلاً ثبت شده."
            )

        return True

    # --------------------------------------------------------
    # REMOVE
    # --------------------------------------------------------

    if text == ".remove":

        if chat_id_str in config["groups"]:

            config["groups"].remove(
                chat_id_str
            )

            save_config()

            await event.respond(
                "✅ این گپ حذف شد."
            )

        else:

            await event.respond(
                "⚠️ این گپ در لیست نیست."
            )

        return True

    # --------------------------------------------------------
    # CLEAR GROUPS
    # --------------------------------------------------------

    if text == ".clear":

        config["groups"] = []

        save_config()

        await event.respond(
            "🧹 لیست گپ‌ها پاک شد."
        )

        return True

    # --------------------------------------------------------
    # GROUPS
    # --------------------------------------------------------

    if (
        text == "لیست گپ ها"
        or
        text == "لیست گپ‌ها"
        or
        text == ".groups"
    ):

        await event.respond(
            get_groups_list()
        )

        return True

    # --------------------------------------------------------
    # ON
    # --------------------------------------------------------

    if text == ".on":

        config["sending"] = True

        save_config()

        await event.respond(
            "🟢 ارسال خودکار روشن شد."
        )

        return True

    # --------------------------------------------------------
    # OFF
    # --------------------------------------------------------

    if text == ".off":

        config["sending"] = False

        save_config()

        await event.respond(
            "🔴 ارسال خودکار خاموش شد."
        )

        return True

    # --------------------------------------------------------
    # INTERVAL
    # --------------------------------------------------------

    if text.lower().startswith(
        ".interval"
    ):

        value = text[
            len(".interval"):
        ].strip()

        try:

            seconds = int(value)

            if seconds < MIN_INTERVAL:

                await event.respond(
                    f"❌ حداقل فاصله "
                    f"{MIN_INTERVAL} ثانیه است."
                )

                return True

            config["interval"] = seconds

            save_config()

            await event.respond(
                f"✅ فاصله ارسال شد "
                f"{seconds} ثانیه."
            )

        except (TypeError, ValueError):

            await event.respond(
                "❌ مثال:\n"
                ".interval 120"
            )

        return True

    # --------------------------------------------------------
    # ADD MESSAGE
    # --------------------------------------------------------

    if text.lower().startswith(
        ".addmsg "
    ):

        message = text[
            len(".addmsg "):
        ].strip()

        if not message:

            await event.respond(
                "❌ متن پیام خالیه."
            )

            return True

        if message in config["messages"]:

            await event.respond(
                "⚠️ این پیام قبلاً وجود داره."
            )

            return True

        config["messages"].append(
            message
        )

        save_config()

        await event.respond(
            "✅ پیام اضافه شد."
        )

        return True

    # --------------------------------------------------------
    # DELETE MESSAGE
    # --------------------------------------------------------

    if text.lower().startswith(
        ".delmsg "
    ):

        message = text[
            len(".delmsg "):
        ].strip()

        if message in config["messages"]:

            config["messages"].remove(
                message
            )

            save_config()

            await event.respond(
                "✅ پیام حذف شد."
            )

        else:

            await event.respond(
                "❌ چنین پیامی پیدا نشد."
            )

        return True

    # --------------------------------------------------------
    # MESSAGES
    # --------------------------------------------------------

    if text == ".msgs":

        await event.respond(
            f"💬 تعداد پیام‌ها: "
            f"{len(config['messages'])}"
        )

        return True

    # --------------------------------------------------------
    # CLEAR MESSAGES
    # --------------------------------------------------------

    if text == ".clearmsgs":

        config["messages"] = []

        save_config()

        await event.respond(
            "🧹 تمام پیام‌ها پاک شدند."
        )

        return True

    # --------------------------------------------------------
    # SETLINK
    # --------------------------------------------------------

    if text.lower().startswith(
        ".setlink"
    ):

        new_link = text[
            len(".setlink"):
        ].strip()

        if not new_link:

            await event.respond(
                "❌ لینک وارد نشده."
            )

            return True

        config["link"] = new_link

        save_config()

        await event.respond(
            "✅ لینک ذخیره شد."
        )

        return True

    # --------------------------------------------------------
    # LINK
    # --------------------------------------------------------

    if text.lower() == ".link":

        link = str(
            config.get(
                "link",
                ""
            )
        ).strip()

        if link:

            await event.respond(
                f"🔗 لینک فعلی:\n{link}"
            )

        else:

            await event.respond(
                "❌ هنوز لینکی تنظیم نشده."
            )

        return True

    # --------------------------------------------------------
    # DELETE LINK
    # --------------------------------------------------------

    if text.lower() == ".dellink":

        config["link"] = ""

        save_config()

        await event.respond(
            "🗑️ لینک حذف شد."
        )

        return True

    # --------------------------------------------------------
    # STATS
    # --------------------------------------------------------

    if text == ".stats":

        await event.respond(
            get_stats()
        )

        return True

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if text == ".status":

        await event.respond(
            get_status()
        )

        return True

    # --------------------------------------------------------
    # RESET STATS
    # --------------------------------------------------------

    if text == ".resetstats":

        stats["success"] = 0
        stats["errors"] = 0
        stats["last_message"] = ""
        stats["last_group"] = ""
        stats["last_time"] = 0

        await event.respond(
            "♻️ آمار صفر شد."
        )

        return True

    # --------------------------------------------------------
    # TEST
    # --------------------------------------------------------

    if text == ".test":

        if not chat_id:

            await event.respond(
                "❌ آیدی گپ پیدا نشد."
            )

            return True

        try:

            message = choose_message()

            await client.send_message(
                chat_id,
                message
            )

            await event.respond(
                "✅ پیام آزمایشی ارسال شد."
            )

        except Exception as e:

            await event.respond(
                f"❌ خطا:\n{e}"
            )

        return True

    return False


# ============================================================
# دریافت پیام
# ============================================================

@client.on_message(
    incoming=True
)
async def message_handler(event):

    try:

        if getattr(
            event,
            "is_me",
            False
        ):
            return

        sender_id = event.sender_id
        chat_id = event.chat_id

        text = (
            getattr(
                event,
                "raw_text",
                ""
            )
            or
            ""
        ).strip()

        is_private = getattr(
            event,
            "is_private",
            False
        )

        is_group = getattr(
            event,
            "is_group",
            False
        )

        print(
            f"📩 پیام | "
            f"sender={sender_id} | "
            f"private={is_private} | "
            f"group={is_group} | "
            f"text={text!r}"
        )

        # ====================================================
        # PV
        # ====================================================

        if is_private:

            if (
                config.get("owner_id") is None
                and
                text == "m0m0d9"
            ):

                config["owner_id"] = sender_id

                save_config()

                await event.respond(
                    "👑 شما مالک ربات شدید."
                )

                print(
                    "👑 مالک:",
                    sender_id
                )

                return

            if is_owner(sender_id):

                handled = await owner_command(
                    event,
                    text
                )

                if handled:
                    return

                if looks_like_group_link(text):

                    await event.respond(
                        "⏳ لینک دریافت شد.\n"
                        "در حال بررسی..."
                    )

                    success, group_id, message = (
                        await join_and_register(text)
                    )

                    await event.respond(
                        message
                    )

                    return

                return

            if looks_like_group_link(text):

                print(
                    "🚫 لینک از کاربر عادی دریافت شد."
                )

                return

            link = str(
                config.get(
                    "link",
                    ""
                )
            ).strip()

            if link:

                await event.respond(
                    f"🔗 لینک من:\n"
                    f"{link}\n\n"
                    f"👤 مالک:\n"
                    f"@mr_mmd909"
                )

            else:

                await event.respond(
                    "⏳ هنوز لینکی تنظیم نشده."
                )

            return

        # ====================================================
        # گپ
        # ====================================================

        if is_group:

            if not is_owner(sender_id):
                return

            await owner_command(
                event,
                text
            )

            return

    except Exception as e:

        print(
            "❌ خطای message_handler:",
            repr(e)
        )


# ============================================================
# ارسال خودکار
# ============================================================

async def auto_sender():

    print(
        "📤 سیستم ارسال خودکار فعال شد."
    )

    while True:

        try:

            if not config.get(
                "sending",
                True
            ):

                await asyncio.sleep(5)
                continue

            groups = list(
                config.get(
                    "groups",
                    []
                )
            )

            if not groups:

                await asyncio.sleep(10)
                continue

            for group_id in groups:

                if not config.get(
                    "sending",
                    True
                ):
                    break

                try:

                    message = choose_message()

                    await client.send_message(
                        group_id,
                        message
                    )

                    stats["success"] += 1
                    stats["last_message"] = message
                    stats["last_group"] = str(
                        group_id
                    )
                    stats["last_time"] = time.time()

                    print(
                        f"📤 {group_id}: "
                        f"{message}"
                    )

                except Exception as e:

                    stats["errors"] += 1

                    print(
                        f"❌ خطا در گپ "
                        f"{group_id}:",
                        repr(e)
                    )

                await asyncio.sleep(
                    random.uniform(3, 7)
                )

            await asyncio.sleep(
                max(
                    MIN_INTERVAL,
                    int(
                        config.get(
                            "interval",
                            DEFAULT_INTERVAL
                        )
                    )
                )

            )

        except Exception as e:

            print(
                "❌ خطای auto_sender:",
                repr(e)
            )

            await asyncio.sleep(10)


# ============================================================
# اجرای اصلی
# ============================================================

async def main():

    print(
        "🔌 در حال اتصال به سروش..."
    )

    phone = os.getenv("PHONE", "").strip()

    if not phone:

        phone = input(
            "📱 شماره سروش را با کد کشور وارد کن: "
        ).strip()

    if not phone:

        print(
            "❌ شماره وارد نشده."
        )

        return

    while True:

        try:

            await client.start(
                phone
            )

            break

        except Exception as e:

            print(
                "❌ اتصال ناموفق:",
                repr(e)
            )

            print(
                "🔄 تلاش مجدد تا 10 ثانیه دیگر..."
            )

            await asyncio.sleep(10)

    try:

        me = await client.get_me()

        print()
        print(
            "✅ ورود موفق بود"
        )

        print(
            "👤 حساب:",
            me.get(
                "first_name",
                ""
            )
        )

        print(
            "🆔 ID:",
            me.get(
                "id",
                ""
            )
        )

    except Exception as e:

        print(
            "⚠️ اطلاعات حساب دریافت نشد:",
            repr(e)
        )

    if config.get(
        "owner_id"
    ) is None:

        print()
        print(
            "🔐 مالک هنوز تعیین نشده."
        )

        print(
            "در PV عبارت m0m0d9 را بفرست."
        )

    else:

        print(
            "👑 مالک قبلاً تعیین شده."
        )

    print(
        "🚀 ربات فعال شد."
    )

    await asyncio.gather(
        client.run_until_disconnected(),
        auto_sender(),
        return_exceptions=True
    )


# ============================================================
# شروع
# ============================================================

if __name__ == "__main__":

    try:

        asyncio.run(
            main()
        )

    except KeyboardInterrupt:

        print(
            "\n⛔ برنامه متوقف شد."
        )

    except Exception as e:

        print(
            "\n❌ خطای اصلی:",
            repr(e)
)
