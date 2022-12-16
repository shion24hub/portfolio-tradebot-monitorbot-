from dotenv import load_dotenv
import os

load_dotenv()
CHANNEL_ACCESS_TOKEN : str = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET : str = os.getenv("CHANNEL_SECRET")
API_SECRET : str = os.getenv("API_SECRET")