import streamlit as st
import api
import asyncio
import logging
logging.basicConfig(level=logging.INFO)

async def init_client():
    server = api.Client()
    await server.client.start(bot_token=server.bot_token)
    return server

if 'client' not in st.session_state:
    st.session_state.client = None

if st.session_state.client is None:
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        st.session_state.client = loop.run_until_complete(init_client())
    except Exception as e:
        st.error(f"Error initializing client: {e}")
        st.stop()

st.title("File Stream Bot")
st.write("Bot is running!")

# Note: For actual file streaming, you need to use st.download_button or similar
# The aiohttp routes cannot be used directly in Streamlit