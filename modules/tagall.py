import asyncio
import random
import time
import html
from collections import deque

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait

from utils.state import manual_setup, stop_flag, auto_data
from utils.files import save_autotag
from utils.helpers import fancy_name

# ================= DEBUG =================
print("🔥 TAGALL MODULE ACTIVE")


# ================= TAGALL COMMAND =================
def register(app):

    @app.on_message(filters.command("tagall") & filters.group)
    async def tagall_cmd(client, message):

        print("📌 TAGALL TRIGGERED")

        chat = message.chat

        if not message.from_user:
            return await message.reply("❌ anonymous user")

        user = message.from_user

        # ================= DEBUG ADMIN CHECK =================
        try:
            member = await client.get_chat_member(chat.id, user.id)
            print("👤 STATUS:", member.status)

            if member.status not in (
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.OWNER
            ):
                return await message.reply(f"❌ bukan admin: {member.status}")

        except Exception as e:
            print("❌ ADMIN CHECK ERROR:", e)
            return await message.reply(f"ERROR ADMIN CHECK:\n{e}")

        # ================= SAVE GROUP =================
        user_id = str(user.id)

        if user_id not in auto_data:
            auto_data[user_id] = {}

        auto_data[user_id]["chat_id"] = chat.id
        await save_autotag(auto_data)

        # ================= INPUT =================
        text = " ".join(message.command[1:])

        if text:
            manual_setup[chat.id] = {"msg": text, "mode": "text"}

        elif message.reply_to_message:
            manual_setup[chat.id] = {
                "msg": message.reply_to_message.id,
                "mode": "reply"
            }
        else:
            return await message.reply("❌ isi text / reply")

        # ================= DEBUG =================
        print("⚡ TAGALL DATA SET:", manual_setup.get(chat.id))

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("2 menit", callback_data="dur_2"),
                InlineKeyboardButton("5 menit", callback_data="dur_5")
            ],
            [
                InlineKeyboardButton("10 menit", callback_data="dur_10"),
                InlineKeyboardButton("30 menit", callback_data="dur_30")
            ],
            [
                InlineKeyboardButton("60 menit", callback_data="dur_60"),
                InlineKeyboardButton("Unlimited", callback_data="dur_unli")
            ]
        ])

        await message.reply("⏱ pilih durasi:", reply_markup=keyboard)


# ================= CANCEL =================
def register_cancel(app):

    @app.on_message(filters.command("cancel") & filters.group)
    async def cancel_cmd(client, message):

        print("🛑 CANCEL TRIGGERED")

        chat = message.chat

        if not message.from_user:
            return await message.reply("❌ invalid user")

        stop_flag[chat.id] = True
        await message.reply("⛔ STOPPED")


# ================= CALLBACK =================
def register_callback(app):

    @app.on_callback_query(filters.regex(r"^dur_(.+)$"))
    async def handle_durasi(client, query):

        print("📍 CALLBACK:", query.data)

        chat_id = query.message.chat.id
        await query.answer()

        if chat_id not in manual_setup:
            print("❌ NO SESSION")
            return await query.edit_message_text("session hilang")

        data = query.data.split("_")[1]

        durasi_map = {
            "2": 120,
            "5": 300,
            "10": 600,
            "30": 1800,
            "60": 3600,
            "unli": None
        }

        duration = durasi_map.get(data)

        setup = manual_setup[chat_id]
        msg = setup["msg"]

        print("🚀 START TAGALL:", chat_id, msg)

        await query.edit_message_text("🚀 start tagall...")

        asyncio.create_task(
            run_tagall_manual(client, chat_id, msg, duration)
        )


# ================= WORKER =================
async def run_tagall_manual(client, chat_id, msg, duration):

    print("⚙️ WORKER START")

    stop_flag[chat_id] = False

    members = {}

    try:
        async for m in client.get_chat_members(chat_id):
            if m.user:
                members[m.user.id] = m.user.first_name
    except Exception as e:
        print("❌ GET MEMBERS ERROR:", e)
        return

    if not members:
        print("❌ NO MEMBERS")
        return

    queue = deque(list(members.keys()))
    random.shuffle(queue)

    print("👥 MEMBERS LOADED:", len(queue))

    while queue:

        if stop_flag.get(chat_id):
            print("🛑 STOP FLAG")
            break

        batch = [queue.popleft() for _ in range(min(3, len(queue)))]

        mention = []
        for uid in batch:
            name = html.escape(members.get(uid, "user"))
            fancy = fancy_name(name)
            mention.append(f'<a href="tg://user?id={uid}">{fancy}</a>')

        text = f"TAGALL:\n{' '.join(mention)}"

        try:
            await client.send_message(chat_id, text)
        except FloodWait as e:
            print("⚠️ FLOOD:", e.value)
            await asyncio.sleep(e.value)

        await asyncio.sleep(2)

    print("✅ DONE TAGALL")
