from dotenv import load_dotenv
import os

load_dotenv()
API_KEY : str = os.getenv("API_KEY")
SECRET_KEY : str = os.getenv("SECRET_KEY")
ENDPOINT_PUBLIC : str = "https://api.coin.z.com/public"
ENDPOINT_PRIVATE : str = "https://api.coin.z.com/private"

