import streamlit as st
import asyncio
import logging
from telethon import TelegramClient
from telethon.sessions import StringSession
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load config from secrets
API_ID = int(os.getenv("api_id", "1234"))
API_HASH = os.getenv("api_hash", "")
CHANNEL_ID = int(os.getenv("channel_files_chat_id", "-1001601419165"))
BOT_TOKEN = os.getenv("token", "")

@st.cache_resource
def init_telegram_client():
    """Initialize Telegram client"""
    if not BOT_TOKEN:
        st.error("Bot token is not set. Please add 'token' to your Streamlit secrets.")
        return None
    
    client = TelegramClient(
        StringSession(),
        API_ID,
        API_HASH
    )
    
    # Start the client with bot token
    try:
        # Use asyncio.run() for clean event loop management
        async def start_client():
            await client.start(bot_token=BOT_TOKEN)
            return client
        
        # Create a new event loop for initialization
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(start_client())
        loop.close()
        logger.info("Telegram client started successfully")
        return result
    except Exception as e:
        st.error(f"Failed to start Telegram client: {e}")
        return None

def get_messages_sync(client, limit=20):
    """Get recent messages from channel (synchronous wrapper)"""
    if not client:
        return []
    
    try:
        async def fetch_messages():
            return await client.get_messages(CHANNEL_ID, limit=limit)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        messages = loop.run_until_complete(fetch_messages())
        loop.close()
        return messages
    except Exception as e:
        logger.error(f"Error getting messages: {e}")
        return []

def download_file_sync(client, message_id):
    """Download file from Telegram (synchronous wrapper)"""
    if not client:
        return None, None
    
    try:
        async def fetch_and_download():
            message = await client.get_messages(CHANNEL_ID, ids=message_id)
            if not message or not message.file:
                return None, None
            
            file_name = message.file.name or f"file{message.file.ext or ''}"
            
            # Download file to memory
            file_data = await message.download_media()
            
            with open(file_data, 'rb') as f:
                file_bytes = f.read()
            
            # Clean up downloaded file
            os.remove(file_data)
            
            return file_bytes, file_name
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(fetch_and_download())
        loop.close()
        return result
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return None, None

# Main app
st.title("File Stream Bot")

# Initialize client
client = init_telegram_client()

if client:
    st.success("✅ Bot is connected!")
    
    # Get messages
    messages = get_messages_sync(client)
    
    if messages:
        st.subheader("Available Files")
        
        for msg in messages:
            if msg.file:
                file_name = msg.file.name or f"file{msg.file.ext or 'unknown'}"
                file_size = msg.file.size
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"📄 **{file_name}** ({file_size / 1024 / 1024:.2f} MB)")
                with col2:
                    if st.button("Download", key=f"dl_{msg.id}"):
                        with st.spinner("Downloading..."):
                            file_bytes, fname = download_file_sync(client, msg.id)
                            if file_bytes:
                                st.download_button(
                                    label="Save File",
                                    data=file_bytes,
                                    file_name=fname,
                                    mime=msg.file.mime_type or "application/octet-stream",
                                    key=f"save_{msg.id}"
                                )
                            else:
                                st.error("Failed to download file")
                st.divider()
    else:
        st.info("No files found in the channel.")
else:
    st.error("❌ Failed to connect to Telegram. Please check your bot token and credentials.")
    st.stop()