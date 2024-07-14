import asyncio
from pyrogram import Client, filters

# User credentials
API_ID = 10803194
API_HASH = "e09f0ed31c8a5e4a1362d4257210d972"
PHONE_NUMBER = "+917003729439"

# Create a Pyrogram client
app = Client("user_bot", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

# Command to ban all users
@app.on_message(filters.command("banall") & filters.group)
async def ban_all_users(client, message):
    chat_id = message.chat.id
    admins = [admin.user.id for admin in await client.get_chat_members(chat_id, filter="administrators")]
    
    # Check if the user has admin privileges
    if message.from_user.id not in admins:
        await message.reply_text("You need to be an admin to use this command.")
        return

    # Fetch all members in the group
    async for member in app.get_chat_members(chat_id):
        user_id = member.user.id
        
        # Skip banning admins and the user bot itself
        if user_id not in admins and user_id != (await client.get_me()).id:
            try:
                await app.kick_chat_member(chat_id, user_id)
                await message.reply_text(f"Banned user: {user_id}")
            except Exception as e:
                await message.reply_text(f"Failed to ban user {user_id}: {e}")

# Start the bot
app.run()
