from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserDeactivated, BotBlocked
import asyncio

api_id = "TG_API_ID"
api_hash = "TG_API_HASH"

app = Client("my_account", api_id=api_id, api_hash=api_hash)

stop_words = ["прекрасно", "ожидать"]

@app.on_message(filters.text & filters.private)
async def handle_message(client, message):
    async with async_session() as session:
        user_id = message.from_user.id
        user = await session.get(User, user_id)

        if user and user.status == "finished":
            return

        for word in stop_words:
            if word in message.text:
                await update_user_status(session, user_id, "finished")
                return

        if user is None:
            new_user = User(id=user_id)
            session.add(new_user)
            await session.commit()

async def message_loop():
    while True:
        async with async_session() as session:
            users = await get_alive_users(session)

        for user in users:
            try:
                await app.send_message(user.id, "Ваше сообщение")
                await asyncio.sleep(1)  # Pausing between sends to prevent flooding
            except (BotBlocked, UserDeactivated):
                async with async_session() as session:
                    await update_user_status(session, user.id, "dead")
            await asyncio.sleep(5)



if __name__ == "__main__":
    app.start()
    asyncio.run(message_loop())
    app.idle()