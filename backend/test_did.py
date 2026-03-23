import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("D_ID_API_KEY")

print("Testing D-ID Key...")
print(f"Key: {api_key[:20]}...")

# Try Method 1: Basic auth
headers1 = {
    "Authorization": f"Basic {api_key}",
}

response = requests.get(
    "https://api.d-id.com/credits",
    headers=headers1
)

print("\nMethod 1 (Basic):", response.status_code)
print(response.text)

# Try Method 2: Direct key
headers2 = {
    "Authorization": api_key,
}

response2 = requests.get(
    "https://api.d-id.com/credits",
    headers=headers2
)

print("\nMethod 2 (Direct):", response2.status_code)
print(response2.text)