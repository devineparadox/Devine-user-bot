import asyncio
import sys
from pyrogram import Client, filters

# User credentials
API_ID = 21048424  # Replace with your actual API ID
API_HASH = ""  # Replace with your actual API Hash
PHONE_NUMBER = ""  # Replace with your actual phone number

# Create a Pyrogram client
app = Client("user_bot", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

# Command to check if the bot is alive
@app.on_message(filters.command(["alive", ".alive"]) & filters.group)
async def alive_command(client, message):
    python_version = sys.version.split(" ")[0]
    pyrogram_version = await app.get_version()
    ping = await app.get_me().then.user.status

    response = (
        "✨ Ꭰᴇᴠɪɴᴇ User bot ɪs ᴀʟɪᴠᴇ.\n\n"
        "‣ ᴍᴀᴅᴇ ʙʏ ᴅᴇᴠɪɴᴇ ɴᴇᴛᴡᴏʀᴋ\n"
        "‣ ᴅᴇᴠʟᴏᴘᴇʀ : Ꭰᴇᴠɪɴᴇ Ꭰᴀʀᴋ 々\n"
        f"‣ ᴘɪɴɢ : {ping} ms\n"
        f"‣ ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ : {python_version}\n"
        f"‣ ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ : {pyrogram_version}\n"
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

    # Ensure proper database connection handling
    await asyncio.sleep(2)  # Increase delay to 2 seconds
    try:
        async for member in client.iter_chat_members(chat_id):
            user_id = member.user.id

            # Skip banning admins and the user bot itself
            if user_id not in admins and user_id != (await client.get_me()).id:
                try:
                    await client.kick_chat_member(chat_id, user_id)
                    await message.reply_text(f"Banned user: {user_id}")
                    await asyncio.sleep(1)  # Add delay to handle rate limits
                except Exception as e:
                    await message.reply_text(f"Failed to ban user {user_id}: {e}")
                    print(f"Failed to ban user {user_id}: {e}")

        await message.reply_text("Finished banning all users.")
    except Exception as ex:
        await message.reply_text(f"Error: {ex}")

# Start the bot
app.run()
