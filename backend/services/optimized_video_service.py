from moviepy.editor import *
from moviepy.video.fx.all import fadein, fadeout
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import os
import re
from services.fast_image_service import fast_image_service

class OptimizedVideoService:
    """
    FAST video generation with:
    - Dynamic slide count (based on content)
    - Smooth animations
    - Real images from Unsplash
    - 3x faster rendering
    """
    
    def __init__(self):
        self.width = 1920
        self.height = 1080
        self.fps = 24  # Lower FPS = faster rendering
        
        # Load fonts (with fallback)
        self.fonts = self._load_fonts()
        
    def _load_fonts(self):
        """Load fonts with fallbacks"""
        font_paths = [
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ]
        
        fonts = {}
        for path in font_paths:
            try:
                fonts['title'] = ImageFont.truetype(path, 90)
                fonts['heading'] = ImageFont.truetype(path, 70)
                fonts['body'] = ImageFont.truetype(path, 45)
                fonts['small'] = ImageFont.truetype(path, 35)
                print(f"✅ Fonts loaded from: {path}")
                break
            except:
                continue
        
        if not fonts:
            fonts = {
                'title': ImageFont.load_default(),
                'heading': ImageFont.load_default(),
                'body': ImageFont.load_default(),
                'small': ImageFont.load_default()
            }
        
        return fonts
    
    def _clean_text(self, text):
        """Remove Hindi/special characters"""
        text = re.sub(r'[\u0900-\u097F]+', '', text)
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        return text.strip()
    
    def _create_animated_text_clip(self, text, duration, font, color, position, animation="fade"):
        """Create text with fade animation"""
        
        # Create text image
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calculate text position
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (self.width - text_width) // 2 if position[0] == 'center' else position[0]
        y = position[1]
        
        # Draw text
        draw.text((x, y), text, font=font, fill=color)
        
        # Convert to numpy
        img_array = np.array(img)
        
        # Create clip
        clip = ImageClip(img_array, duration=duration)
        
        # Add animations
        if animation == "fade":
            clip = fadein(clip, 0.3).fadeout(0.3)
        
        return clip
    
    def _create_slide_with_image(self, heading, points, topic, slide_index):
        """
        Create single slide with:
        - Background image (from Unsplash)
        - Animated text overlay
        - Smooth transitions
        """
        duration = 6  # 6 seconds per slide
        
        # 1. Get background image (FAST - Unsplash)
        bg_image_path = fast_image_service.get_image_for_topic(topic, slide_index)
        
        if bg_image_path and os.path.exists(bg_image_path):
            # Load and darken image for text readability
            bg_img = Image.open(bg_image_path)
            bg_img = bg_img.filter(ImageFilter.GaussianBlur(2))
            
            # Add dark overlay
            overlay = Image.new('RGBA', bg_img.size, (0, 0, 0, 120))
            bg_img = Image.alpha_composite(bg_img.convert('RGBA'), overlay)
            
            bg_clip = ImageClip(np.array(bg_img), duration=duration)
        else:
            # Fallback: gradient background
            bg_clip = ColorClip(size=(self.width, self.height), color=(30, 30, 60), duration=duration)
        
        # 2. Create text overlays with animations
        clips = [bg_clip]
        
        # Heading (animated fade in)
        heading_clip = self._create_animated_text_clip(
            self._clean_text(heading),
            duration=duration,
            font=self.fonts['heading'],
            color=(255, 255, 255),
            position=('center', 150),
            animation="fade"
        )
        clips.append(heading_clip)
        
        # Points (staggered fade in)
        y_offset = 400
        for i, point in enumerate(points[:4]):  # Max 4 points per slide
            point_text = f"• {self._clean_text(point['text'])}"
            
            # Staggered animation (each point appears slightly after previous)
            point_clip = self._create_animated_text_clip(
                point_text,
                duration=duration - (i * 0.2),  # Slight delay
                font=self.fonts['body'],
                color=(220, 220, 220),
                position=(200, y_offset + (i * 120)),
                animation="fade"
            )
            
            # Delay start of each point
            point_clip = point_clip.set_start(i * 0.2)
            
            clips.append(point_clip)
        
        # Composite all layers
        final_clip = CompositeVideoClip(clips, size=(self.width, self.height))
        
        # Add fade transition between slides
        final_clip = fadein(final_clip, 0.5).fadeout(0.5)
        
        return final_clip
    
    def create_dynamic_video(self, parsed_content, audio_path, output_path, topic):
        """
        Create video with DYNAMIC slide count based on content length
        
        Logic:
        - 1-3 points = 1 slide
        - 4-7 points = 2 slides
        - 8-12 points = 3 slides
        - 12+ points = 4 slides
        """
        
        print(f"🎬 Creating optimized video for: {topic}")
        
        try:
            # Calculate optimal number of slides
            total_points = sum(len(section.get('points', [])) for section in parsed_content)
            
            if total_points <= 3:
                num_slides = 1
            elif total_points <= 7:
                num_slides = 2
            elif total_points <= 12:
                num_slides = 3
            else:
                num_slides = 4
            
            print(f"📊 Content: {total_points} points → {num_slides} slides")
            
            # Distribute content across slides
            slides_data = self._distribute_content(parsed_content, num_slides)
            
            # Create slide clips
            slide_clips = []
            for i, slide_data in enumerate(slides_data):
                print(f"  Creating slide {i+1}/{num_slides}...")
                
                slide_clip = self._create_slide_with_image(
                    heading=slide_data['heading'],
                    points=slide_data['points'],
                    topic=topic,
                    slide_index=i
                )
                
                slide_clips.append(slide_clip)
            
            # Concatenate all slides
            video = concatenate_videoclips(slide_clips, method="compose")
            
            # Add audio
            if os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                
                # Match video length to audio
                if video.duration < audio.duration:
                    # Loop video if needed
                    n_loops = int(np.ceil(audio.duration / video.duration))
                    video = concatenate_videoclips([video] * n_loops)
                
                video = video.set_duration(audio.duration)
                video = video.set_audio(audio)
            
            # Write video with OPTIMIZED settings (3x faster)
            print(f"💾 Rendering video... ({num_slides} slides)")
            
            video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                preset='ultrafast',  # FAST rendering
                threads=4,
                logger=None  # Disable verbose logging
            )
            
            print(f"✅ Video created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Video creation error: {e}")
            raise
    
    def _distribute_content(self, parsed_content, num_slides):
        """Distribute content points across slides evenly"""
        
        all_points = []
        heading = "Topic Overview"
        
        # Collect all points
        for section in parsed_content:
            if section.get('heading'):
                heading = section['heading']
            all_points.extend(section.get('points', []))
        
        # Distribute points across slides
        points_per_slide = max(1, len(all_points) // num_slides)
        
        slides_data = []
        for i in range(num_slides):
            start_idx = i * points_per_slide
            end_idx = start_idx + points_per_slide if i < num_slides - 1 else len(all_points)
            
            slides_data.append({
                'heading': heading if i == 0 else f"{heading} (Part {i+1})",
                'points': all_points[start_idx:end_idx]
            })
        
        return slides_data

optimized_video_service = OptimizedVideoService()