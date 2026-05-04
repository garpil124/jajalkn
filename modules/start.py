import asyncio
import os
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.files import load_setting, save_setting

# ================= DEBUG =================
print("🔥 START MODULE ACTIVE")

# ================= REGISTER =================
def register(app):

    @app.on_message(filters.command("start"))
    async def start_cmd(client, message):

        data = await load_setting()
        user_id = message.from_user.id

        users = data.get("users", [])

        if user_id not in users:
            users.append(user_id)
            data["users"] = users
            await save_setting(data)

        msg = await message.reply("⚡ Initializing...")

        # ================= RGB GLITCH =================
        glitch = [
            "💜 𝑵𝑶𝑰𝑹𝑭𝑳𝑼𝑬𝑹 💜",
            "💙 𝗡𝗢𝗜𝗥𝗙𝗟𝗨𝗘𝗥 💙",
            "💚 𝙉𝙊𝙄𝙍𝙁𝙇𝙐𝙀𝙍 💚",
            "💛 𝐍𝐎𝐈𝐑𝐅𝐋𝐔𝐄𝐑 💛",
            "🧡 𝒩𝒪ℐℛ𝒻𝓁𝓊ℯ𝓇 🧡",
            "❤️ ＮＯＩＲＦＬＵＥＲ ❤️"
        ]

        for g in glitch:
            await asyncio.sleep(0.12)
            try:
                await msg.edit(g)
            except:
                pass

        # ================= TYPING =================
        hacker_lines = [
            "⌬ connecting to core...",
            "⌬ bypass firewall...",
            "⌬ injecting payload...",
            "⌬ decrypting system...",
            "⌬ syncing modules..."
        ]

        for line in hacker_lines:
            words = line.split(" ")
            typed = ""

            for w in words:
                typed += w + " "
                try:
                    await msg.edit(typed)
                except:
                    pass
                await asyncio.sleep(0.03)

            await asyncio.sleep(0.05)

        # ================= PROGRESS =================
        for i in range(0, 101, 20):
            bar = "■" * (i // 20) + "□" * (5 - i // 20)
            await asyncio.sleep(0.12)
            try:
                await msg.edit(f"⚡ Booting System...\n[{bar}] {i}%")
            except:
                pass

        # ================= FINAL TEXT =================
        text = (
            "𓊆 ✨ 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝗕𝗢𝗧 𝗡𝗢𝗜𝗥𝗙𝗟𝗨𝗘𝗥 ✨ 𓊇\n\n"
            "╭───────────────╮\n"
            "│ sistem tagall otomatis & cepat.\n"
            "│ baca dulu biar paham.\n"
            "╰───────────────╯\n\n"
            "✦ CARA PAKAI ✦\n"
            "⟡ kirim pesan untuk tagall\n"
            "⟡ bot akan proses otomatis\n"
        )

        # ================= BUTTON =================
        buttons = []

        if "pj" in data:
            buttons.append([
                InlineKeyboardButton(
                    "📩 REQUEST PARTNER",
                    url=f"https://t.me/{data['pj']}"
                )
            ])

        if "rules" in data:
            buttons.append([
                InlineKeyboardButton(
                    "📜 RULES",
                    callback_data="rules"
                )
            ])

        if data.get("livechat"):
            buttons.append([
                InlineKeyboardButton(
                    "💬 LIVE CHAT",
                    url=data["livechat"]
                )
            ])

        markup = InlineKeyboardMarkup(buttons) if buttons else None

        await asyncio.sleep(0.2)

        try:
            await msg.delete()
        except:
            pass

        # ================= FOTO =================
        photo_path = "database9/start.jpg"

        if data.get("start_pict"):
            await client.send_photo(
                chat_id=message.chat.id,
                photo=data["start_pict"],
                caption=text,
                reply_markup=markup
            )

        elif os.path.exists(photo_path):
            await client.send_photo(
                chat_id=message.chat.id,
                photo=photo_path,
                caption=text,
                reply_markup=markup
            )

        else:
            await message.reply(text, reply_markup=markup)
