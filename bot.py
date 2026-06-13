import os
import random
import asyncio
import re
from telethon import TelegramClient, events, errors
from telethon.errors import FloodWaitError

API_ID = 27029926
API_HASH = "6963d3bf5f8a776f5139d71cfc707abc"
PHONE_NUMBER = "+989053716748"

OWNERS = {"usernames": ["DevilWillCryBitch","MY_FALAH_M", "PV_KiTANAM","Pxcio"]}

BOT_DIR = "downloads_bot1"
if not os.path.exists(BOT_DIR):
    os.mkdir(BOT_DIR)

files_defaults = {
    "Kheshab.txt": "ONLINE",
    "targetid.txt": "1",
    "Caption.txt": "",
    "time.txt": "2",
    "fwd_source_channel.txt": "",
    "fwd_source_msg_id.txt": "0",
    "fwd_active.txt": "False",
    "fwd_delay_min.txt": "2",
    "fwd_delay_max.txt": "5",
    "fwd_extra_text.txt": "",
    "fwd_extra_position.txt": "after"
}

for filename, content in files_defaults.items():
    path = os.path.join(BOT_DIR, filename)
    if not os.path.exists(path):
        with open(path, 'w', encoding="utf-8") as f:
            f.write(content)

Spammer = [False]
ForwardSpammer = [False]
client = None

async def spam_function():
    global client
    print("Text spam thread started")
    while Spammer[0]:
        try:
            with open(os.path.join(BOT_DIR, 'targetid.txt'), 'r') as f:
                target_id = int(f.read().strip())
            with open(os.path.join(BOT_DIR, 'Kheshab.txt'), 'r', encoding="utf-8") as f:
                messages = f.readlines()
            with open(os.path.join(BOT_DIR, 'Caption.txt'), 'r', encoding="utf-8") as f:
                caption = f.read().strip()
            with open(os.path.join(BOT_DIR, 'time.txt'), 'r') as f:
                delay = int(f.read().strip())
        except Exception as e:
            print(f"Config error: {e}")
            delay = 2
            messages = []

        if messages and target_id != 1:
            try:
                text = random.choice(messages).strip()
                if text:
                    print(f"📤 Sending: {text[:30]}...")
                    msg = f"{text}\n\n{caption}" if caption else text
                    await client.send_message(target_id, msg)
            except Exception as e:
                print(f"Send error: {e}")
        await asyncio.sleep(delay)
    print("Text spam stopped")

async def forward_spam_function():
    global client
    print("Forward spam thread started")
    while ForwardSpammer[0]:
        try:
            with open(os.path.join(BOT_DIR, 'targetid.txt'), 'r') as f:
                target_id = int(f.read().strip())
            with open(os.path.join(BOT_DIR, 'fwd_source_channel.txt'), 'r', encoding="utf-8") as f:
                source_channel = f.read().strip()
            with open(os.path.join(BOT_DIR, 'fwd_source_msg_id.txt'), 'r') as f:
                source_msg_id = int(f.read().strip())
            with open(os.path.join(BOT_DIR, 'fwd_delay_min.txt'), 'r') as f:
                delay_min = float(f.read().strip())
            with open(os.path.join(BOT_DIR, 'fwd_delay_max.txt'), 'r') as f:
                delay_max = float(f.read().strip())
            with open(os.path.join(BOT_DIR, 'fwd_extra_text.txt'), 'r', encoding="utf-8") as f:
                extra_text = f.read().strip()
            with open(os.path.join(BOT_DIR, 'fwd_extra_position.txt'), 'r', encoding="utf-8") as f:
                extra_pos = f.read().strip()
        except Exception as e:
            print(f"Config read error: {e}")
            await asyncio.sleep(5)
            continue

        if target_id == 1:
            print("⚠️ No target set. Use /setgp <chatid>")
            ForwardSpammer[0] = False
            break
            
        if not source_channel or source_msg_id == 0:
            print("⚠️ No source set. Use /setfwd <message_link>")
            ForwardSpammer[0] = False
            break

        try:
            source_message = await client.get_messages(source_channel, ids=source_msg_id)
            if not source_message:
                print(f"❌ Message {source_msg_id} not found in {source_channel}")
                ForwardSpammer[0] = False
                break

            await client.forward_messages(target_id, source_message)

            if extra_text:
                if extra_pos == "before":
                    await client.send_message(target_id, f"{extra_text}\n\n")
                else:
                    await client.send_message(target_id, f"\n\n{extra_text}")

            print(f"📨 Forwarded to {target_id}")

            delay = random.uniform(delay_min, delay_max)
            await asyncio.sleep(delay)

        except FloodWaitError as e:
            print(f"⏳ Flood wait: {e.seconds}s")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"Forward error: {e}")
            await asyncio.sleep(5)

    print("Forward spam stopped")

# ========== اصلاح شده: دیگه هیچی به دیگران نمیگه ==========
async def check_owner(event):
    sender = await event.get_sender()
    if sender and sender.username and sender.username in OWNERS["usernames"]:
        return True
    # کاملاً نادیده گرفته میشه - هیچ خروجی نمیاد
    return False

@events.register(events.NewMessage(pattern=re.compile(r'^/help$', re.IGNORECASE)))
async def help_command(event):
    if not await check_owner(event): return
    await event.reply("""*help list**

**Setup (One Time):**
/chatid - Get current chat/group ID
/setgp <id> - Set TARGET chat ID (where messages go)

**Forward Spam**
/setfwd <message_link> - Set SOURCE (any message link from Telegram)
/setfwd_delay <min> <max> - Random delay (seconds)
/setfwd_text <text> - Extra text before/after forward
/setfwd_pos before/after - Position of extra text
/fwdspam_on - Start forwarding to target
/fwdspam_off - Stop
/showfwd - Show current config

**Text Spam **
/cap <text> - Global caption
/speed <n> - Delay seconds
/spam_on - Start text spam
/spam_off - Stop

/ping - Bot status

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Coded by BrianMoser - MERGED BY JUST LISA**

**OWNER CHANNEL** → https://t.me/nahuhnothinghere/4
""")

@events.register(events.NewMessage(pattern=re.compile(r'^/setfwd (https?://t\.me/[^\s]+)$', re.IGNORECASE)))
async def set_forward_from_link(event):
    if not await check_owner(event): return
    link = event.pattern_match.group(1).strip()
    
    try:
        parts = link.replace("https://t.me/", "").split("/")
        
        if parts[0] == "c":
            channel_id = int("-100" + parts[1])
            msg_id = int(parts[2])
            channel_username = str(channel_id)
        else:
            channel_username = parts[0]
            msg_id = int(parts[1])
            
        with open(os.path.join(BOT_DIR, 'fwd_source_channel.txt'), 'w', encoding="utf-8") as f:
            f.write(channel_username)
        with open(os.path.join(BOT_DIR, 'fwd_source_msg_id.txt'), 'w') as f:
            f.write(str(msg_id))
            
        await event.reply(f"✅ Source set!\n📢 Channel: {channel_username}\n🔢 Message ID: {msg_id}")
        
    except Exception as e:
        await event.reply(f"❌ Failed to parse link: {e}\nUse format: https://t.me/username/message_id")

# بقیه هندلرها همگی به همین شکل اولش check_owner دارن
# (بقیه کد دقیقاً به همان صورتی که بود میمونه)
# فقط تابع check_owner عوض شد

async def main():
    global client
    client = TelegramClient('userbot_session', API_ID, API_HASH)

    print("🔐 Connecting...")
    await client.start(phone=PHONE_NUMBER)

    me = await client.get_me()
    print(f"✅ Logged in as: @{me.username}")

    client.add_event_handler(help_command)
    client.add_event_handler(set_caption)
    client.add_event_handler(get_caption)
    client.add_event_handler(set_speed)
    client.add_event_handler(get_speed)
    client.add_event_handler(get_chat_id)
    client.add_event_handler(get_user_id)
    client.add_event_handler(set_group)
    client.add_event_handler(spam_on)
    client.add_event_handler(spam_off)
    client.add_event_handler(ping)
    client.add_event_handler(set_forward_from_link)
    client.add_event_handler(set_forward_delay)
    client.add_event_handler(set_forward_text)
    client.add_event_handler(set_forward_pos)
    client.add_event_handler(forward_spam_on)
    client.add_event_handler(forward_spam_off)
    client.add_event_handler(show_forward_config)

    print("="*40)
    print("🔥 Bot running - Just-Lisa edition")
    print("Commands: /help")
    print("="*40)

    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped")
