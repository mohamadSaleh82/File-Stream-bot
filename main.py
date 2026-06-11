import streamlit as st
import asyncio
import logging
from telethon import TelegramClient
from telethon.sessions import StringSession
import os
import nest_asyncio

# Apply nest_asyncio to allow running async code in Streamlit
nest_asyncio.apply()

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
        loop = asyncio.get_event_loop()
        loop.run_until_complete(client.start(bot_token=BOT_TOKEN))
        logger.info("Telegram client started successfully")
    except Exception as e:
        st.error(f"Failed to start Telegram client: {e}")
        return None
    
    return client

def get_messages(client, limit=20):
    """Get recent messages from channel"""
    if not client:
        return []
    
    try:
        loop = asyncio.get_event_loop()
        messages = loop.run_until_complete(client.get_messages(CHANNEL_ID, limit=limit))
        return messages
    except Exception as e:
        logger.error(f"Error getting messages: {e}")
        return []

def download_file(client, message_id):
    """Download file from Telegram"""
    if not client:
        return None, None
    
    try:
        loop = asyncio.get_event_loop()
        message = loop.run_until_complete(client.get_messages(CHANNEL_ID, ids=message_id))
        if not message or not message.file:
            return None, None
        
        file_name = message.file.name or f"file{message.file.ext or ''}"
        
        # Download file to memory
        file_data = loop.run_until_complete(message.download_media())
        
        with open(file_data, 'rb') as f:
            file_bytes = f.read()
        
        # Clean up downloaded file
        os.remove(file_data)
        
        return file_bytes, file_name
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
    messages = get_messages(client)
    
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
                            file_bytes, fname = download_file(client, msg.id)
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