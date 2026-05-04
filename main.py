import asyncio
from pyrogram import idle
from client import app
import modules

@app.on_message()
async def debug(client, message):
    print("📩", message.text)

async def main():
    print("BOT START")

    await app.start()
    print("CONNECTED")

    modules.load(app)

    await idle()
    await app.stop()

asyncio.run(main())
