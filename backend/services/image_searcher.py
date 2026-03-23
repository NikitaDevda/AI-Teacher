import requests
from pathlib import Path
import os

class ImageSearcher:
    def __init__(self):
        self.output_dir = Path("temp/images")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Unsplash API (free tier)
        # Get key from: https://unsplash.com/developers
        self.unsplash_access_key = os.getenv("UNSPLASH_ACCESS_KEY", "")
    
    def search_and_download(self, query: str, filename: str) -> str:
        """Search for relevant image and download"""
        
        try:
            print(f"🖼️ Searching image for: {query}")
            
            # Try Unsplash first
            if self.unsplash_access_key:
                image_path = self._search_unsplash(query, filename)
                if image_path:
                    return image_path
            
            # Fallback to placeholder
            return self._create_placeholder(query, filename)
            
        except Exception as e:
            print(f"❌ Image search error: {e}")
            return self._create_placeholder(query, filename)
    
    def _search_unsplash(self, query: str, filename: str) -> str:
        """Search Unsplash for images"""
        
        try:
            url = "https://api.unsplash.com/search/photos"
            headers = {"Authorization": f"Client-ID {self.unsplash_access_key}"}
            params = {"query": query, "per_page": 1, "orientation": "landscape"}
            
            response = requests.get(url, headers=headers, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    image_url = data['results'][0]['urls']['regular']
                    
                    # Download image
                    img_response = requests.get(image_url, timeout=10)
                    output_path = self.output_dir / filename
                    
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    
                    print(f"✅ Image downloaded: {output_path}")
                    return str(output_path)
            
            return None
            
        except Exception as e:
            print(f"⚠️ Unsplash search failed: {e}")
            return None
    
    def _create_placeholder(self, text: str, filename: str) -> str:
        """Create placeholder image with text"""
        
        from PIL import Image, ImageDraw, ImageFont
        
        img = Image.new('RGB', (1200, 675), color='#E8F4F8')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Draw centered text
        text = text[:50]  # Limit length
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (1200 - text_width) // 2
        y = (675 - text_height) // 2
        
        draw.text((x, y), text, fill='#1E40AF', font=font)
        
        output_path = self.output_dir / filename
        img.save(output_path)
        
        return str(output_path)

image_searcher = ImageSearcher()