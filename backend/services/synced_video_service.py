# from moviepy.editor import *
# from moviepy.video.fx.all import fadein, fadeout
# from PIL import Image, ImageDraw, ImageFont
# import numpy as np
# import os
# import re
# from mutagen.mp3 import MP3
# from services.fast_image_service import fast_image_service
# from services.graph_generator import graph_generator

# class SyncedVideoService:
#     """
#     PERFECTLY SYNCED audio-video with:
#     - Audio duration = Video duration (EXACT MATCH)
#     - Dynamic slides based on audio length
#     - Graphs for math topics
#     - Fast rendering
#     """
    
#     def __init__(self):
#         self.width = 1920
#         self.height = 1080
#         self.fps = 24
#         self.fonts = self._load_fonts()
    
#     def _load_fonts(self):
#         """Load fonts"""
#         font_paths = [
#             "C:/Windows/Fonts/segoeui.ttf",
#             "C:/Windows/Fonts/arial.ttf",
#         ]
        
#         fonts = {}
#         for path in font_paths:
#             try:
#                 fonts['title'] = ImageFont.truetype(path, 90)
#                 fonts['heading'] = ImageFont.truetype(path, 70)
#                 fonts['body'] = ImageFont.truetype(path, 45)
#                 fonts['small'] = ImageFont.truetype(path, 35)
#                 break
#             except:
#                 continue
        
#         if not fonts:
#             fonts = {k: ImageFont.load_default() for k in ['title', 'heading', 'body', 'small']}
        
#         return fonts
    
#     def _get_audio_duration(self, audio_path):
#         """Get exact audio duration"""
#         try:
#             audio = MP3(audio_path)
#             return audio.info.length
#         except:
#             # Fallback
#             audio = AudioFileClip(audio_path)
#             duration = audio.duration
#             audio.close()
#             return duration
    
#     def _clean_text(self, text):
#         """Remove special characters"""
#         text = re.sub(r'[\u0900-\u097F]+', '', text)
#         text = re.sub(r'[^\x00-\x7F]+', '', text)
#         return text.strip()
    
#     def _create_text_image(self, text, font, color=(255, 255, 255), max_width=1700):
#         """Create text image with word wrapping"""
#         img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
#         draw = ImageDraw.Draw(img)
        
#         # Word wrap
#         words = text.split()
#         lines = []
#         current_line = []
        
#         for word in words:
#             test_line = ' '.join(current_line + [word])
#             bbox = draw.textbbox((0, 0), test_line, font=font)
#             width = bbox[2] - bbox[0]
            
#             if width <= max_width:
#                 current_line.append(word)
#             else:
#                 if current_line:
#                     lines.append(' '.join(current_line))
#                 current_line = [word]
        
#         if current_line:
#             lines.append(' '.join(current_line))
        
#         # Draw lines
#         y = 100
#         for line in lines:
#             bbox = draw.textbbox((0, 0), line, font=font)
#             text_width = bbox[2] - bbox[0]
#             x = (self.width - text_width) // 2
            
#             # Text shadow for better readability
#             draw.text((x+2, y+2), line, font=font, fill=(0, 0, 0, 180))
#             draw.text((x, y), line, font=font, fill=color)
            
#             y += bbox[3] - bbox[1] + 20
        
#         return np.array(img)
    
#     def _create_slide(self, heading, points, duration, bg_image_path=None, graph_path=None):
#         """Create single slide with perfect timing"""
        
#         # Background
#         if graph_path and os.path.exists(graph_path):
#             # Use graph as background
#             bg_img = Image.open(graph_path).resize((self.width, self.height))
#             bg_clip = ImageClip(np.array(bg_img), duration=duration)
#         elif bg_image_path and os.path.exists(bg_image_path):
#             # Use topic image as background
#             bg_img = Image.open(bg_image_path).resize((self.width, self.height))
#             # Darken
#             darken = Image.new('RGBA', bg_img.size, (0, 0, 0, 150))
#             bg_img = Image.alpha_composite(bg_img.convert('RGBA'), darken)
#             bg_clip = ImageClip(np.array(bg_img), duration=duration)
#         else:
#             # Gradient background
#             bg_clip = ColorClip(size=(self.width, self.height), color=(20, 30, 50), duration=duration)
        
#         clips = [bg_clip]
        
#         # Heading
#         heading_text = self._clean_text(heading)
#         heading_img = self._create_text_image(heading_text, self.fonts['heading'])
#         heading_clip = ImageClip(heading_img, duration=duration)
#         heading_clip = fadein(heading_clip, 0.5).fadeout(0.5)
#         clips.append(heading_clip)
        
#         # Points
#         y_start = 350
#         for i, point in enumerate(points[:5]):  # Max 5 points
#             point_text = f"• {self._clean_text(point['text'])}"
            
#             # Create point image
#             img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
#             draw = ImageDraw.Draw(img)
            
#             # Word wrap for long points
#             words = point_text.split()
#             lines = []
#             current_line = []
            
#             for word in words:
#                 test_line = ' '.join(current_line + [word])
#                 bbox = draw.textbbox((0, 0), test_line, font=self.fonts['body'])
#                 if (bbox[2] - bbox[0]) <= 1600:
#                     current_line.append(word)
#                 else:
#                     if current_line:
#                         lines.append(' '.join(current_line))
#                     current_line = [word]
            
#             if current_line:
#                 lines.append(' '.join(current_line))
            
#             # Draw lines
#             y = y_start + (i * 130)
#             for line in lines:
#                 draw.text((102, y+2), line, font=self.fonts['body'], fill=(0, 0, 0, 200))
#                 draw.text((100, y), line, font=self.fonts['body'], fill=(230, 230, 230))
#                 y += 60
            
#             point_img = np.array(img)
#             point_clip = ImageClip(point_img, duration=duration)
            
#             # Staggered fade in
#             point_clip = point_clip.set_start(i * 0.3)
#             point_clip = fadein(point_clip, 0.5)
            
#             clips.append(point_clip)
        
#         # Composite
#         final = CompositeVideoClip(clips, size=(self.width, self.height))
#         final = fadein(final, 0.5).fadeout(0.5)
        
#         return final
    
#     def create_synced_video(self, parsed_content, audio_path, output_path, topic, answer_text):
#         """
#         Create video that PERFECTLY matches audio duration
#         """
        
#         print(f"🎬 Creating synced video for: {topic}")
        
#         try:
#             # 1. Get exact audio duration
#             audio_duration = self._get_audio_duration(audio_path)
#             print(f"🎵 Audio duration: {audio_duration:.2f} seconds")
            
#             # 2. Check if we need a graph
#             graph_path = graph_generator.detect_and_generate_graph(answer_text)
#             if graph_path:
#                 print(f"📊 Graph generated: {graph_path}")
            
#             # 3. Calculate optimal slide count and duration
#             # Aim for 5-7 seconds per slide
#             ideal_slide_duration = 6
#             num_slides = max(2, min(6, int(audio_duration / ideal_slide_duration)))
#             slide_duration = audio_duration / num_slides
            
#             print(f"📊 Creating {num_slides} slides, {slide_duration:.2f}s each")
            
#             # 4. Distribute content
#             all_points = []
#             heading = topic
            
#             for section in parsed_content:
#                 if section.get('heading'):
#                     heading = section['heading']
#                 all_points.extend(section.get('points', []))
            
#             # 5. Get background image
#             bg_image = fast_image_service.get_image_for_topic(topic, 0)
            
#             # 6. Create slides
#             slide_clips = []
#             points_per_slide = max(1, len(all_points) // num_slides)
            
#             for i in range(num_slides):
#                 start_idx = i * points_per_slide
#                 end_idx = start_idx + points_per_slide if i < num_slides - 1 else len(all_points)
                
#                 slide_points = all_points[start_idx:end_idx]
                
#                 slide_heading = heading if i == 0 else f"{heading} ({i+1}/{num_slides})"
                
#                 # Use graph only on first slide (if available)
#                 use_graph = graph_path if i == 0 else None
                
#                 slide = self._create_slide(
#                     heading=slide_heading,
#                     points=slide_points,
#                     duration=slide_duration,
#                     bg_image_path=bg_image,
#                     graph_path=use_graph
#                 )
                
#                 slide_clips.append(slide)
            
#             # 7. Concatenate slides
#             video = concatenate_videoclips(slide_clips, method="compose")
            
#             # 8. CRITICAL: Set exact duration to match audio
#             video = video.set_duration(audio_duration)
            
#             # 9. Add audio
#             audio = AudioFileClip(audio_path)
#             video = video.set_audio(audio)
            
#             # 10. Write video
#             print(f"💾 Rendering video... (Duration: {audio_duration:.2f}s)")
            
#             video.write_videofile(
#                 output_path,
#                 fps=self.fps,
#                 codec='libx264',
#                 audio_codec='aac',
#                 preset='ultrafast',
#                 threads=4,
#                 logger=None
#             )
            
#             # Cleanup
#             video.close()
#             audio.close()
            
#             print(f"✅ Video created: {output_path}")
#             print(f"✅ Audio-Video perfectly synced!")
            
#             return output_path
            
#         except Exception as e:
#             print(f"❌ Video error: {e}")
#             raise

# synced_video_service = SyncedVideoService()










from moviepy.editor import (
    ImageClip, AudioFileClip, concatenate_videoclips,
    CompositeVideoClip, ColorClip
)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import os
import re
from mutagen.mp3 import MP3
from services.graph_generator import graph_generator

class SyncedVideoService:
    """
    FAST + GOOD QUALITY video generation
    - 720p instead of 1080p (3x faster render)
    - ultrafast preset
    - No Unsplash image download (saves 2-3 sec per slide)
    - Beautiful gradient backgrounds
    - Minimal compositing
    """

    def __init__(self):
        # ✅ 720p — 3x faster than 1080p, still looks great
        self.width = 1280
        self.height = 720
        self.fps = 24
        self.fonts = self._load_fonts()

        # Color themes per slide
        self.themes = [
            {"bg": (15, 32, 80),   "accent": (99, 179, 237),  "text": (255, 255, 255)},
            {"bg": (20, 60, 40),   "accent": (72, 199, 142),  "text": (255, 255, 255)},
            {"bg": (60, 20, 60),   "accent": (232, 121, 249), "text": (255, 255, 255)},
            {"bg": (60, 30, 10),   "accent": (251, 191, 36),  "text": (255, 255, 255)},
            {"bg": (10, 40, 60),   "accent": (56, 189, 248),  "text": (255, 255, 255)},
            {"bg": (50, 10, 20),   "accent": (251, 113, 133), "text": (255, 255, 255)},
        ]

    # ─────────────────────────────────────────────
    # Load Fonts
    # ─────────────────────────────────────────────
    def _load_fonts(self):
        font_paths = [
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
        ]
        fonts = {}
        for path in font_paths:
            try:
                fonts['heading'] = ImageFont.truetype(path, 52)
                fonts['body']    = ImageFont.truetype(path, 32)
                fonts['small']   = ImageFont.truetype(path, 24)
                fonts['title']   = ImageFont.truetype(path, 68)
                print(f"✅ Fonts loaded: {path}")
                break
            except:
                continue

        if not fonts:
            default = ImageFont.load_default()
            fonts = {k: default for k in ['heading', 'body', 'small', 'title']}

        return fonts

    # ─────────────────────────────────────────────
    # Audio Duration
    # ─────────────────────────────────────────────
    def _get_audio_duration(self, audio_path):
        try:
            audio = MP3(audio_path)
            return audio.info.length
        except:
            audio = AudioFileClip(audio_path)
            dur = audio.duration
            audio.close()
            return dur

    # ─────────────────────────────────────────────
    # Clean Text
    # ─────────────────────────────────────────────
    def _clean_text(self, text):
        text = re.sub(r'[\u0900-\u097F]+', '', text)
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        text = re.sub(r'\*+', '', text)
        return text.strip()

    # ─────────────────────────────────────────────
    # Word Wrap
    # ─────────────────────────────────────────────
    def _wrap_text(self, draw, text, font, max_width):
        words = text.split()
        lines = []
        current = []

        for word in words:
            test = ' '.join(current + [word])
            bbox = draw.textbbox((0, 0), test, font=font)
            if (bbox[2] - bbox[0]) <= max_width:
                current.append(word)
            else:
                if current:
                    lines.append(' '.join(current))
                current = [word]
        if current:
            lines.append(' '.join(current))
        return lines

    # ─────────────────────────────────────────────
    # Create Beautiful Gradient Background
    # ─────────────────────────────────────────────
    def _create_gradient_bg(self, theme):
        """Create gradient background — no internet needed, instant"""
        img = Image.new('RGB', (self.width, self.height))
        pixels = img.load()

        bg = theme['bg']
        accent = theme['accent']

        for y in range(self.height):
            ratio = y / self.height
            r = int(bg[0] + (accent[0] - bg[0]) * ratio * 0.3)
            g = int(bg[1] + (accent[1] - bg[1]) * ratio * 0.3)
            b = int(bg[2] + (accent[2] - bg[2]) * ratio * 0.3)
            for x in range(self.width):
                pixels[x, y] = (
                    max(0, min(255, r)),
                    max(0, min(255, g)),
                    max(0, min(255, b))
                )

        # Add subtle diagonal light effect
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        for i in range(0, self.width + self.height, 40):
            draw.line([(i, 0), (0, i)], fill=(255, 255, 255, 8), width=2)

        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        return img

    # ─────────────────────────────────────────────
    # Create Slide Image (PIL — fast, no moviepy overhead)
    # ─────────────────────────────────────────────
    def _create_slide_image(self, heading, points, theme, slide_num, total_slides, graph_path=None):
        """Create complete slide as PIL image — very fast"""

        # Background
        if graph_path and os.path.exists(graph_path):
            bg = Image.open(graph_path).resize((self.width, self.height), Image.LANCZOS)
            # Darken for text readability
            dark = Image.new('RGBA', bg.size, (0, 0, 0, 160))
            bg = Image.alpha_composite(bg.convert('RGBA'), dark).convert('RGB')
        else:
            bg = self._create_gradient_bg(theme)

        draw = ImageDraw.Draw(bg)
        accent = theme['accent']
        text_color = theme['text']

        # ── Top accent bar ──
        draw.rectangle([(0, 0), (self.width, 6)], fill=accent)

        # ── Slide counter (top right) ──
        counter = f"{slide_num}/{total_slides}"
        draw.text((self.width - 80, 16), counter,
                  font=self.fonts['small'], fill=(*accent, 200))

        # ── Heading ──
        heading_clean = self._clean_text(heading)
        heading_lines = self._wrap_text(draw, heading_clean, self.fonts['heading'], self.width - 100)

        y = 50
        for line in heading_lines[:2]:
            # Shadow
            draw.text((52, y + 2), line, font=self.fonts['heading'], fill=(0, 0, 0, 120))
            draw.text((50, y), line, font=self.fonts['heading'], fill=accent)
            bbox = draw.textbbox((0, 0), line, font=self.fonts['heading'])
            y += (bbox[3] - bbox[1]) + 8

        # ── Divider line ──
        y += 10
        draw.rectangle([(50, y), (self.width - 50, y + 2)], fill=(*accent, 100))
        y += 20

        # ── Points ──
        for i, point in enumerate(points[:5]):
            pt = self._clean_text(point.get('text', ''))
            if not pt:
                continue

            pt_lines = self._wrap_text(draw, f"  {pt}", self.fonts['body'], self.width - 130)

            # Bullet circle
            circle_y = y + 8
            draw.ellipse([(50, circle_y), (66, circle_y + 16)], fill=accent)

            for j, line in enumerate(pt_lines[:2]):
                prefix = "      " if j == 0 else "        "
                draw.text((72, y + 1), line, font=self.fonts['body'], fill=(0, 0, 0, 80))
                draw.text((70, y), line, font=self.fonts['body'], fill=text_color)
                bbox = draw.textbbox((0, 0), line, font=self.fonts['body'])
                y += (bbox[3] - bbox[1]) + 4

            y += 16

            if y > self.height - 80:
                break

        # ── Bottom bar ──
        draw.rectangle([(0, self.height - 4), (self.width, self.height)], fill=accent)

        return np.array(bg)

    # ─────────────────────────────────────────────
    # MAIN: Create Synced Video
    # ─────────────────────────────────────────────
    def create_synced_video(self, parsed_content, audio_path, output_path, topic, answer_text):
        """Create video that PERFECTLY matches audio — fast version"""

        print(f"🎬 Creating fast video for: {topic}")

        try:
            # 1. Audio duration
            audio_duration = self._get_audio_duration(audio_path)
            print(f"🎵 Audio: {audio_duration:.1f}s")

            # 2. Graph (only if needed)
            graph_path = None
            try:
                graph_path = graph_generator.detect_and_generate_graph(answer_text)
                if graph_path:
                    print(f"📊 Graph: {graph_path}")
            except:
                pass

            # 3. Slide count — aim for 6-8s per slide
            ideal_dur = 7
            num_slides = max(2, min(8, int(audio_duration / ideal_dur)))
            slide_dur = audio_duration / num_slides
            print(f"📊 {num_slides} slides × {slide_dur:.1f}s each")

            # 4. Collect content
            all_points = []
            heading = topic
            for section in parsed_content:
                if section.get('heading'):
                    heading = section['heading']
                all_points.extend(section.get('points', []))

            # 5. Create slides
            slide_clips = []
            points_per_slide = max(1, len(all_points) // num_slides) if all_points else 1

            for i in range(num_slides):
                theme = self.themes[i % len(self.themes)]

                start = i * points_per_slide
                end = start + points_per_slide if i < num_slides - 1 else len(all_points)
                slide_points = all_points[start:end]

                slide_heading = heading if i == 0 else f"{heading} — Part {i + 1}"
                use_graph = graph_path if (i == 0 and graph_path) else None

                # Create PIL image (fast!)
                slide_img = self._create_slide_image(
                    heading=slide_heading,
                    points=slide_points,
                    theme=theme,
                    slide_num=i + 1,
                    total_slides=num_slides,
                    graph_path=use_graph
                )

                clip = ImageClip(slide_img, duration=slide_dur)
                slide_clips.append(clip)

                print(f"  ✅ Slide {i+1}/{num_slides} ready")

            # 6. Concatenate
            video = concatenate_videoclips(slide_clips, method="chain")  # chain = faster than compose
            video = video.set_duration(audio_duration)

            # 7. Add audio
            audio = AudioFileClip(audio_path)
            video = video.set_audio(audio)

            # 8. Render — ultrafast settings
            print(f"💾 Rendering {audio_duration:.1f}s video at 720p...")
            video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                preset='ultrafast',   # ✅ Fastest encoding
                ffmpeg_params=[
                    '-crf', '28',     # ✅ Good quality, smaller file
                    '-tune', 'fastdecode',
                ],
                threads=os.cpu_count() or 4,  # ✅ Use all CPU cores
                logger=None
            )

            video.close()
            audio.close()

            print(f"✅ Video done: {output_path}")
            return output_path

        except Exception as e:
            print(f"❌ Video error: {e}")
            import traceback
            traceback.print_exc()
            raise


synced_video_service = SyncedVideoService()