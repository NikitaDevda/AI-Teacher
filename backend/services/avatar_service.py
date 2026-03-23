# import requests
# import time
# import os
# from dotenv import load_dotenv  # ✅ ADD THIS

# # ✅ LOAD .env
# load_dotenv()

# class AvatarService:
#     def __init__(self):
#         self.api_key = os.getenv("D_ID_API_KEY")
#         self.base_url = "https://api.d-id.com"
    
#     def create_talking_video(self, text: str, avatar_url: str = None):
#         """Generate talking avatar video using D-ID"""
        
#         if not avatar_url:
#             # Default avatar image
#             avatar_url = "https://create-images-results.d-id.com/default_presenter.jpg"
        
#         headers = {
#             "Authorization": f"Basic {self.api_key}",
#             "Content-Type": "application/json"
#         }
        
#         payload = {
#             "script": {
#                 "type": "text",
#                 "input": text,
#                 "provider": {
#                     "type": "microsoft",
#                     "voice_id": "hi-IN-SwaraNeural"  # Hindi voice
#                 }
#             },
#             "source_url": avatar_url,
#             "config": {
#                 "fluent": True,
#                 "stitch": True
#             }
#         }
        
#         # Create talk
#         response = requests.post(
#             f"{self.base_url}/talks",
#             json=payload,
#             headers=headers
#         )
        
#         if response.status_code != 201:
#             print(f"D-ID Error: {response.text}")
#             return None
        
#         talk_id = response.json()["id"]
        
#         # Wait for video generation (polling)
#         video_url = self._wait_for_video(talk_id)
        
#         return video_url
    
#     def _wait_for_video(self, talk_id: str, max_wait: int = 30):
#         """Poll D-ID API until video is ready"""
        
#         headers = {
#             "Authorization": f"Basic {self.api_key}"
#         }
        
#         for _ in range(max_wait):
#             response = requests.get(
#                 f"{self.base_url}/talks/{talk_id}",
#                 headers=headers
#             )
            
#             if response.status_code == 200:
#                 data = response.json()
                
#                 if data["status"] == "done":
#                     return data["result_url"]
#                 elif data["status"] == "error":
#                     print(f"Video generation error: {data}")
#                     return None
            
#             time.sleep(1)  # Wait 1 second before next check
        
#         return None

















import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

class AvatarService:
    def __init__(self):
        self.api_key = os.getenv("D_ID_API_KEY")
        self.base_url = "https://api.d-id.com"
        self.headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def create_talking_video(self, text: str):
        """Generate talking avatar video"""
        
        if not self.api_key:
            print("⚠️ D-ID key not found")
            return None
        
        try:
            # Limit text length for faster generation
            text = text[:500] if len(text) > 500 else text
            
            # Step 1: Create talk with built-in presenter
            payload = {
                "script": {
                    "type": "text",
                    "input": text,
                    "provider": {
                        "type": "microsoft",
                        "voice_id": "hi-IN-SwaraNeural"  # Hindi voice
                    }
                },
                # ✅ Use D-ID's built-in presenter (no URL needed!)
                "presenter_id": "amy-jcwCkr1grs",  # Professional woman presenter
                "config": {
                    "fluent": True,
                    "stitch": True
                }
            }
            
            print("🎬 Creating video...")
            response = requests.post(
                f"{self.base_url}/talks",
                json=payload,
                headers=self.headers
            )
            
            print(f"Response Status: {response.status_code}")
            
            if response.status_code != 201:
                print(f"❌ Error: {response.text}")
                return None
            
            talk_id = response.json()["id"]
            print(f"✅ Video ID: {talk_id}")
            
            # Step 2: Wait for video
            return self._wait_for_video(talk_id)
            
        except Exception as e:
            print(f"❌ Exception: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _wait_for_video(self, talk_id: str, max_wait: int = 60):
        """Poll until video is ready"""
        
        print("⏳ Waiting for video generation...")
        
        for i in range(max_wait):
            time.sleep(2)  # Check every 2 seconds
            
            try:
                response = requests.get(
                    f"{self.base_url}/talks/{talk_id}",
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")
                    
                    if status == "done":
                        video_url = data.get("result_url")
                        print(f"✅ Video ready!")
                        return video_url
                    elif status == "error":
                        error_msg = data.get("error", {}).get("description", "Unknown error")
                        print(f"❌ Video generation error: {error_msg}")
                        return None
                    else:
                        print(f"⏳ Status: {status}... ({i*2}s elapsed)")
                else:
                    print(f"⚠️ Status check failed: {response.status_code}")
                    
            except Exception as e:
                print(f"⚠️ Error checking status: {e}")
        
        print("❌ Video generation timeout!")
        return None