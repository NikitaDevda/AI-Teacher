import requests
from PIL import Image
from io import BytesIO
import os
import time

class FastImageService:
    """Fast image fetching from Unsplash API"""
    
    def __init__(self):
        # Free Unsplash API - No key needed for demo
        self.unsplash_url = "https://source.unsplash.com/800x600/"
        
    def get_image_for_topic(self, topic, index=0):
        """
        Get relevant image from Unsplash
        Ultra fast - no API key needed
        """
        try:
            # Clean topic for search
            search_query = topic.replace(" ", "-").lower()
            
            # Unsplash source URL (instant redirect to image)
            image_url = f"{self.unsplash_url}?{search_query}"
            
            # Download image (< 1 second)
            response = requests.get(image_url, timeout=5)
            
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                
                # Resize to standard size
                img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
                
                # Save locally
                filename = f"temp/images/topic_{index}_{int(time.time())}.jpg"
                os.makedirs("temp/images", exist_ok=True)
                img.save(filename, "JPEG", quality=85)
                
                print(f"✅ Image downloaded: {search_query}")
                return filename
            
            return None
            
        except Exception as e:
            print(f"❌ Image fetch error: {e}")
            return None
    
    def get_fallback_gradient(self, color="blue"):
        """Create simple gradient background if image fails"""
        from PIL import ImageDraw
        
        img = Image.new('RGB', (1920, 1080), color=color)
        filename = f"temp/images/gradient_{int(time.time())}.jpg"
        img.save(filename)
        return filename

fast_image_service = FastImageService()