import pymongo
import sys
import asyncio
from pyrogram import Client, filters

# MongoDB connection URL
mongo_url = "mongodb+srv://borobo1625:wxLvRG2iMty7l8wp@cluster0.41tusdj.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB
client = pymongo.MongoClient(mongo_url)
db = client.get_database()  # Replace with your database name if needed
collection = db["user_bot_data"]  # MongoDB collection name for bot data

# User credentials
API_ID = 21048424  # Replace with your actual API ID
API_HASH = "1ad8c57a3e3906ee82f5ccbc9aeffb4a"  # Replace with your actual API Hash
PHONE_NUMBER = "+917003729439"  # Replace with your actual phone number

# Create a Pyrogram client
app = Client("user_bot", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

# Command to check if the bot is alive
@app.on_message(filters.command(["alive", ".alive"]) & filters.group)
async def alive_command(client, message):
    python_version = sys.version.split(" ")[0]
    pyrogram_version = await app.get_version()
    ping = (await app.get_me()).status.expires

    response = (
        "<b>✨ Ꭰᴇᴠɪɴᴇ ᴜsᴇʀ ʙᴏᴛ ɪs ᴀʟɪᴠᴇ.</b>\n\n"
        "<b>‣ ᴍᴀᴅᴇ ʙʏ [ᴅᴇᴠɪɴᴇ ɴᴇᴛᴡᴏʀᴋ](https://t.me/Devine_Network)</b>\n"
        "<b>‣ ᴅᴇᴠʟᴏᴘᴇʀ : [Ꭰᴇᴠɪɴᴇ Ꭰᴀʀᴋ](https://t.me/devine_dark)</b>\n"
        f"<b>‣ ᴘɪɴɢ : {ping} ms</b>\n"
        f"<b>‣ ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ : {python_version}</b>\n"
        f"<b>‣ ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ : {pyrogram_version}</b>\n"
    )
    await message.reply_text(response)

# Command to ban all users
@app.on_message(filters.command("banall") & filters.group)
async def ban_all_users(client, message):
    chat_id = message.chat.id
    admins = []

    async for admin in client.iter_chat_members(chat_id, filter="administrators"):
        admins.append(admin.user.id)

    # Check if the user has admin privileges
    if message.from_user.id not in admins:
        await message.reply_text("You need to be an admin to use this command.")
        return

    await message.reply_text("Starting to ban all users...")

    async for member in client.get_chat_members(chat_id):
        user_id = member.user.id

        # Skip banning admins and the user bot itself
        if user_id not in admins and user_id != (await client.get_me()).id:
            try:
                await client.kick_chat_member(chat_id, user_id)
                await message.reply_text(f"Banned user: {user_id}")
                await asyncio.sleep(1)  # Add delay to handle rate limits

                # Store banned user in MongoDB for logging purposes
                collection.insert_one({"user_id": user_id, "action": "banned"})

            except Exception as e:
                await message.reply_text(f"Failed to ban user {user_id}: {e}")
                print(f"Failed to ban user {user_id}: {e}")

    await message.reply_text("Finished banning all users.")

# Start the bot
app.run()
