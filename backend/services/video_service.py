# # import os
# # import json
# # import subprocess
# # from pathlib import Path
# # from typing import List, Dict
# # import tempfile
# # from moviepy import (
# #     VideoFileClip, AudioFileClip, CompositeVideoClip,
# #     ImageClip, TextClip, concatenate_videoclips
# # )
# # from PIL import Image, ImageDraw, ImageFont
# # import numpy as np

# # class VideoGenerationService:
# #     def __init__(self):
# #         self.output_dir = Path("temp/videos")
# #         self.output_dir.mkdir(parents=True, exist_ok=True)
# #         self.fps = 30
# #         self.resolution = (1920, 1080)
        
# #     def generate_educational_video(
# #         self,
# #         content_sections: List[Dict],
# #         audio_path: str,
# #         output_filename: str
# #     ) -> str:
# #         """
# #         Main function to generate complete educational video
        
# #         Args:
# #             content_sections: Parsed content with headings, definitions, points
# #             audio_path: Path to audio file
# #             output_filename: Name for output video
            
# #         Returns:
# #             Path to generated video file
# #         """
# #         try:
# #             print("🎬 Starting video generation...")
            
# #             # Get audio duration
# #             audio_clip = AudioFileClip(audio_path)
# #             total_duration = audio_clip.duration
            
# #             # Calculate timing for each section
# #             sections_with_timing = self._calculate_section_timings(
# #                 content_sections, 
# #                 total_duration
# #             )
            
# #             # Generate video clips for each section
# #             video_clips = []
            
# #             for section in sections_with_timing:
# #                 clip = self._create_section_clip(section)
# #                 if clip:
# #                     video_clips.append(clip)
            
# #             # Concatenate all clips
# #             print("📹 Combining video clips...")
# #             final_video = concatenate_videoclips(video_clips, method="compose")
            
# #             # Add audio
# #             print("🎵 Adding audio...")
# #             final_video = final_video.set_audio(audio_clip)
            
# #             # Export
# #             output_path = self.output_dir / output_filename
# #             print(f"💾 Exporting to {output_path}...")
            
# #             final_video.write_videofile(
# #                 str(output_path),
# #                 fps=self.fps,
# #                 codec='libx264',
# #                 audio_codec='aac',
# #                 temp_audiofile='temp-audio.m4a',
# #                 remove_temp=True
# #             )
            
# #             print("✅ Video generation complete!")
# #             return str(output_path)
            
# #         except Exception as e:
# #             print(f"❌ Video generation error: {e}")
# #             import traceback
# #             traceback.print_exc()
# #             return None
    
# #     def _calculate_section_timings(
# #         self, 
# #         sections: List[Dict], 
# #         total_duration: float
# #     ) -> List[Dict]:
# #         """Calculate when each section should appear"""
        
# #         if not sections:
# #             return []
        
# #         # Distribute time evenly across sections
# #         time_per_section = total_duration / len(sections)
        
# #         timed_sections = []
# #         current_time = 0
        
# #         for section in sections:
# #             timed_section = section.copy()
# #             timed_section['start_time'] = current_time
# #             timed_section['duration'] = time_per_section
# #             timed_sections.append(timed_section)
# #             current_time += time_per_section
        
# #         return timed_sections
    
# #     def _create_section_clip(self, section: Dict) -> VideoFileClip:
# #         """Create video clip for a single section"""
        
# #         try:
# #             # Create white background
# #             img = Image.new('RGB', self.resolution, color='white')
# #             draw = ImageDraw.Draw(img)
            
# #             # Try to load fonts
# #             try:
# #                 heading_font = ImageFont.truetype("arial.ttf", 80)
# #                 text_font = ImageFont.truetype("arial.ttf", 50)
# #                 small_font = ImageFont.truetype("arial.ttf", 40)
# #             except:
# #                 heading_font = ImageFont.load_default()
# #                 text_font = ImageFont.load_default()
# #                 small_font = ImageFont.load_default()
            
# #             y_position = 100
            
# #             # Draw heading
# #             if section.get('heading'):
# #                 heading = f"📌 {section['heading']}"
# #                 # Draw text (simplified - actual would need text wrapping)
# #                 draw.text(
# #                     (100, y_position),
# #                     heading,
# #                     fill='#1E40AF',
# #                     font=heading_font
# #                 )
# #                 y_position += 120
                
# #                 # Draw underline
# #                 draw.line(
# #                     [(100, y_position), (1820, y_position)],
# #                     fill='#3B82F6',
# #                     width=5
# #                 )
# #                 y_position += 60
            
# #             # Draw definition
# #             if section.get('definition'):
# #                 # Simplified - actual would need word wrapping
# #                 def_text = f"Definition: {section['definition']}"
# #                 lines = self._wrap_text(def_text, 80)
                
# #                 for line in lines[:3]:  # Max 3 lines
# #                     draw.text(
# #                         (120, y_position),
# #                         line,
# #                         fill='#1F2937',
# #                         font=text_font
# #                     )
# #                     y_position += 70
                
# #                 y_position += 40
            
# #             # Draw points
# #             if section.get('points'):
# #                 for i, point in enumerate(section['points'][:5]):  # Max 5 points
# #                     point_text = f"• {point.get('text', '')}"
# #                     lines = self._wrap_text(point_text, 90)
                    
# #                     for line in lines[:2]:  # Max 2 lines per point
# #                         draw.text(
# #                             (150, y_position),
# #                             line,
# #                             fill='#374151',
# #                             font=small_font
# #                         )
# #                         y_position += 60
                    
# #                     y_position += 20
            
# #             # Save frame as temporary image
# #             temp_img_path = self.output_dir / f"temp_frame_{id(section)}.png"
# #             img.save(temp_img_path)
            
# #             # Create video clip from image
# #             clip = ImageClip(str(temp_img_path))
# #             clip = clip.set_duration(section['duration'])
            
# #             # Add fade in/out
# #             clip = clip.fadein(0.5).fadeout(0.5)
            
# #             return clip
            
# #         except Exception as e:
# #             print(f"❌ Error creating section clip: {e}")
# #             return None


    
# #     def _wrap_text(self, text: str, width: int) -> List[str]:
# #         """Simple text wrapping"""
# #         words = text.split()
# #         lines = []
# #         current_line = []
        
# #         for word in words:
# #             if len(' '.join(current_line + [word])) <= width:
# #                 current_line.append(word)
# #             else:
# #                 if current_line:
# #                     lines.append(' '.join(current_line))
# #                 current_line = [word]
        
# #         if current_line:
# #             lines.append(' '.join(current_line))
        
# #         return lines

# # # Global instance
# # video_service = VideoGenerationService()













# import os
# import json
# import subprocess
# from pathlib import Path
# from typing import List, Dict
# import tempfile
# from moviepy.editor import (
#     VideoFileClip, AudioFileClip, CompositeVideoClip,
#     ImageClip, TextClip, concatenate_videoclips
# )
# from PIL import Image, ImageDraw, ImageFont
# import numpy as np

# class VideoGenerationService:
#     def __init__(self):
#         self.output_dir = Path("temp/videos")
#         self.output_dir.mkdir(parents=True, exist_ok=True)
#         self.fps = 30
#         self.resolution = (1920, 1080)
        
#     def generate_educational_video(
#         self,
#         content_sections: List[Dict],
#         audio_path: str,
#         output_filename: str
#     ) -> str:
#         """
#         Main function to generate complete educational video
        
#         Args:
#             content_sections: Parsed content with headings, definitions, points
#             audio_path: Path to audio file
#             output_filename: Name for output video
            
#         Returns:
#             Path to generated video file
#         """
#         try:
#             print("🎬 Starting video generation...")
#             print(f"📝 Sections: {len(content_sections)}")
#             print(f"🎵 Audio: {audio_path}")
            
#             # Check audio exists
#             if not os.path.exists(audio_path):
#                 print(f"❌ Audio file not found: {audio_path}")
#                 return None
            
#             # Get audio duration
#             audio_clip = AudioFileClip(audio_path)
#             total_duration = audio_clip.duration
#             print(f"⏱️ Audio duration: {total_duration}s")
            
#             if not content_sections:
#                 print("⚠️ No content sections to render")
#                 return None
            
#             # Calculate timing for each section
#             sections_with_timing = self._calculate_section_timings(
#                 content_sections, 
#                 total_duration
#             )
            
#             # Generate video clips for each section
#             video_clips = []
            
#             for i, section in enumerate(sections_with_timing):
#                 print(f"🎬 Creating clip {i+1}/{len(sections_with_timing)}...")
#                 clip = self._create_section_clip(section)
#                 if clip:
#                     video_clips.append(clip)
#                 else:
#                     print(f"⚠️ Clip {i+1} failed, skipping")
            
#             if not video_clips:
#                 print("❌ No video clips created")
#                 return None
            
#             print(f"✅ Created {len(video_clips)} clips")
            
#             # Concatenate all clips
#             print("📹 Combining video clips...")
#             final_video = concatenate_videoclips(video_clips, method="compose")
            
#             # Add audio
#             print("🎵 Adding audio...")
#             final_video = final_video.set_audio(audio_clip)
            
#             # Export
#             output_path = self.output_dir / output_filename
#             print(f"💾 Exporting to {output_path}...")
            
#             final_video.write_videofile(
#                 str(output_path),
#                 fps=self.fps,
#                 codec='libx264',
#                 audio_codec='aac',
#                 preset='ultrafast',  # Faster rendering
#                 threads=4,
#                 logger=None  # Less verbose
#             )
            
#             print("✅ Video generation complete!")
#             return str(output_path)
            
#         except Exception as e:
#             print(f"❌ Video generation error: {e}")
#             import traceback
#             traceback.print_exc()
#             return None
    
#     def _calculate_section_timings(
#         self, 
#         sections: List[Dict], 
#         total_duration: float
#     ) -> List[Dict]:
#         """Calculate when each section should appear"""
        
#         if not sections:
#             return []
        
#         # Distribute time evenly across sections
#         time_per_section = total_duration / len(sections)
        
#         timed_sections = []
#         current_time = 0
        
#         for section in sections:
#             timed_section = section.copy()
#             timed_section['start_time'] = current_time
#             timed_section['duration'] = time_per_section
#             timed_sections.append(timed_section)
#             current_time += time_per_section
        
#         return timed_sections
    
#     def _create_section_clip(self, section: Dict):
#     """Create video clip for a single section"""
    
#     try:
#         # Create white background
#         img = Image.new('RGB', self.resolution, color='white')
#         draw = ImageDraw.Draw(img)
        
#         # Load fonts
#         try:
#             heading_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 70)
#             text_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 45)
#             small_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 35)
#         except Exception as e:
#             print(f"⚠️ Using default font: {e}")
#             heading_font = ImageFont.load_default()
#             text_font = ImageFont.load_default()
#             small_font = ImageFont.load_default()
        
#         y_position = 100
#         margin_left = 100
#         max_width = 1720
        
#         # Draw heading
#         if section.get('heading'):
#             heading_text = f"📌 {section['heading']}"
            
#             try:
#                 bbox = draw.textbbox((0, 0), heading_text, font=heading_font)
#                 text_width = bbox[2] - bbox[0]
#             except:
#                 text_width = len(heading_text) * 40
            
#             draw.text(
#                 (margin_left, y_position),
#                 heading_text,
#                 fill=(30, 64, 175),
#                 font=heading_font
#             )
#             y_position += 100
            
#             draw.line(
#                 [(margin_left, y_position), (margin_left + min(text_width, max_width), y_position)],
#                 fill=(59, 130, 246),
#                 width=4
#             )
#             y_position += 50
        
#         # Draw definition
#         if section.get('definition'):
#             def_text = f"📖 {section['definition']}"
#             lines = self._wrap_text_smart(draw, def_text, text_font, max_width)
            
#             for line in lines[:4]:
#                 draw.text(
#                     (margin_left + 20, y_position),
#                     line,
#                     fill=(31, 41, 55),
#                     font=text_font
#                 )
#                 y_position += 60
            
#             y_position += 30
        
#         # Draw points
#         if section.get('points'):
#             for i, point in enumerate(section['points'][:6]):
#                 point_text = f"• {point.get('text', '')}"
#                 lines = self._wrap_text_smart(draw, point_text, small_font, max_width - 100)
                
#                 for line in lines[:2]:
#                     draw.text(
#                         (margin_left + 50, y_position),
#                         line,
#                         fill=(55, 65, 81),
#                         font=small_font
#                     )
#                     y_position += 50
                
#                 y_position += 15
                
#                 if y_position > 950:
#                     break
        
#         # Save frame
#         temp_img_path = self.output_dir / f"temp_frame_{id(section)}.png"
#         img.save(temp_img_path)
#         print(f"✅ Frame saved: {temp_img_path}")
        
#         # Create clip
#         clip = ImageClip(str(temp_img_path))
        
#         # ✅ FIX: Try both duration methods
#         duration = section.get('duration', 3)
#         try:
#             clip = clip.set_duration(duration)  # Old MoviePy API
#         except AttributeError:
#             try:
#                 clip = clip.with_duration(duration)  # New MoviePy API
#             except:
#                 # Manual duration setting
#                 clip.duration = duration
        
#         # Add fade effects
#         clip = clip.fadein(0.3).fadeout(0.3)
        
#         print(f"✅ Clip created: {duration}s")
        
#         return clip
        
#     except Exception as e:
#         print(f"❌ Error creating section clip: {e}")
#         import traceback
#         traceback.print_exc()
#         return None
    
#     def _wrap_text_smart(self, draw, text: str, font, max_width: int) -> List[str]:
#         """Smart text wrapping using actual font measurements"""
        
#         words = text.split()
#         lines = []
#         current_line = []
        
#         for word in words:
#             test_line = ' '.join(current_line + [word])
            
#             try:
#                 bbox = draw.textbbox((0, 0), test_line, font=font)
#                 line_width = bbox[2] - bbox[0]
#             except:
#                 # Fallback if textbbox fails
#                 line_width = len(test_line) * 20
            
#             if line_width <= max_width:
#                 current_line.append(word)
#             else:
#                 if current_line:
#                     lines.append(' '.join(current_line))
#                 current_line = [word]
        
#         if current_line:
#             lines.append(' '.join(current_line))
        
#         return lines

# # Global instance
# video_service = VideoGenerationService()
















# import os
# from pathlib import Path
# from typing import List, Dict

# try:
#     from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips
#     print("✅ Using MoviePy")
# except ImportError:
#     print("❌ MoviePy not installed")

# from PIL import Image, ImageDraw, ImageFont
# import numpy as np

# class VideoGenerationService:
#     def __init__(self):
#         self.output_dir = Path("temp/videos")
#         self.output_dir.mkdir(parents=True, exist_ok=True)
#         self.fps = 30
#         self.resolution = (1920, 1080)
        
#     def generate_educational_video(
#         self,
#         content_sections: List[Dict],
#         audio_path: str,
#         output_filename: str
#     ) -> str:
#         """Generate complete educational video"""
        
#         try:
#             print("🎬 Starting video generation...")
#             print(f"📝 Sections: {len(content_sections)}")
            
#             if not os.path.exists(audio_path):
#                 print(f"❌ Audio not found: {audio_path}")
#                 return None
            
#             audio_clip = AudioFileClip(audio_path)
#             total_duration = audio_clip.duration
#             print(f"⏱️ Audio: {total_duration}s")
            
#             if not content_sections:
#                 print("⚠️ No sections")
#                 return None
            
#             sections_with_timing = self._calculate_section_timings(
#                 content_sections, 
#                 total_duration
#             )
            
#             video_clips = []
            
#             for i, section in enumerate(sections_with_timing):
#                 print(f"🎬 Clip {i+1}/{len(sections_with_timing)}...")
#                 clip = self._create_section_clip(section)
#                 if clip:
#                     video_clips.append(clip)
            
#             if not video_clips:
#                 print("❌ No clips created")
#                 return None
            
#             print(f"✅ {len(video_clips)} clips ready")
#             print("📹 Combining...")
            
#             final_video = concatenate_videoclips(video_clips, method="compose")
#             final_video = final_video.set_audio(audio_clip)
            
#             output_path = self.output_dir / output_filename
#             print(f"💾 Exporting...")
            
#             final_video.write_videofile(
#                 str(output_path),
#                 fps=self.fps,
#                 codec='libx264',
#                 audio_codec='aac',
#                 preset='ultrafast',
#                 threads=4,
#                 logger=None
#             )
            
#             print("✅ Video done!")
#             return str(output_path)
            
#         except Exception as e:
#             print(f"❌ Video error: {e}")
#             import traceback
#             traceback.print_exc()
#             return None
    
#     def _calculate_section_timings(self, sections: List[Dict], total_duration: float) -> List[Dict]:
#         """Calculate timing for sections"""
        
#         if not sections:
#             return []
        
#         time_per_section = total_duration / len(sections)
#         timed_sections = []
#         current_time = 0
        
#         for section in sections:
#             timed_section = section.copy()
#             timed_section['start_time'] = current_time
#             timed_section['duration'] = time_per_section
#             timed_sections.append(timed_section)
#             current_time += time_per_section
        
#         return timed_sections
    
#     def _create_section_clip(self, section: Dict):
#         """Create video clip for section"""
        
#         try:
#             img = Image.new('RGB', self.resolution, color='white')
#             draw = ImageDraw.Draw(img)
            
#             try:
#                 heading_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 70)
#                 text_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 45)
#                 small_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 35)
#             except:
#                 heading_font = ImageFont.load_default()
#                 text_font = ImageFont.load_default()
#                 small_font = ImageFont.load_default()
            
#             y_position = 100
#             margin_left = 100
#             max_width = 1720
            
#             # Heading
#             if section.get('heading'):
#                 heading_text = f"📌 {section['heading']}"
#                 draw.text(
#                     (margin_left, y_position),
#                     heading_text,
#                     fill=(30, 64, 175),
#                     font=heading_font
#                 )
#                 y_position += 100
#                 draw.line(
#                     [(margin_left, y_position), (margin_left + 800, y_position)],
#                     fill=(59, 130, 246),
#                     width=4
#                 )
#                 y_position += 50
            
#             # Definition
#             if section.get('definition'):
#                 def_text = f"📖 {section['definition']}"
#                 lines = self._wrap_text(def_text, 70)
                
#                 for line in lines[:4]:
#                     draw.text(
#                         (margin_left + 20, y_position),
#                         line,
#                         fill=(31, 41, 55),
#                         font=text_font
#                     )
#                     y_position += 60
                
#                 y_position += 30
            
#             # Points
#             if section.get('points'):
#                 for point in section['points'][:6]:
#                     point_text = f"• {point.get('text', '')}"
#                     lines = self._wrap_text(point_text, 80)
                    
#                     for line in lines[:2]:
#                         draw.text(
#                             (margin_left + 50, y_position),
#                             line,
#                             fill=(55, 65, 81),
#                             font=small_font
#                         )
#                         y_position += 50
                    
#                     y_position += 15
                    
#                     if y_position > 950:
#                         break
            
#             temp_img_path = self.output_dir / f"frame_{id(section)}.png"
#             img.save(temp_img_path)
#             print(f"✅ Frame: {temp_img_path}")
            
#             clip = ImageClip(str(temp_img_path))
#             duration = section.get('duration', 3)
#             clip = clip.set_duration(duration)
#             clip = clip.fadein(0.3).fadeout(0.3)
            
#             print(f"✅ Clip: {duration}s")
#             return clip
            
#         except Exception as e:
#             print(f"❌ Clip error: {e}")
#             import traceback
#             traceback.print_exc()
#             return None
    

    
#     def _wrap_text(self, text: str, width: int) -> List[str]:
#         """Simple text wrapping"""
        
#         words = text.split()
#         lines = []
#         current_line = []
        
#         for word in words:
#             if len(' '.join(current_line + [word])) <= width:
#                 current_line.append(word)
#             else:
#                 if current_line:
#                     lines.append(' '.join(current_line))
#                 current_line = [word]
        
#         if current_line:
#             lines.append(' '.join(current_line))
        
#         return lines

# video_service = VideoGenerationService()













import os
import re
from pathlib import Path
from typing import List, Dict

try:
    from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips
    print("✅ Using MoviePy")
except ImportError:
    print("❌ MoviePy not installed")

from PIL import Image, ImageDraw, ImageFont
import numpy as np

class VideoGenerationService:
    def __init__(self):
        self.output_dir = Path("temp/videos")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.fps = 30
        self.resolution = (1920, 1080)
        
    def generate_educational_video(
        self,
        content_sections: List[Dict],
        audio_path: str,
        output_filename: str
    ) -> str:
        """Generate complete educational video"""
        
        try:
            print("🎬 Starting video generation...")
            print(f"📝 Sections: {len(content_sections)}")
            
            if not os.path.exists(audio_path):
                print(f"❌ Audio not found: {audio_path}")
                return None
            
            audio_clip = AudioFileClip(audio_path)
            total_duration = audio_clip.duration
            print(f"⏱️ Audio: {total_duration}s")
            
            if not content_sections:
                print("⚠️ No sections")
                return None
            
            sections_with_timing = self._calculate_section_timings(
                content_sections, 
                total_duration
            )
            
            video_clips = []
            
            for i, section in enumerate(sections_with_timing):
                print(f"🎬 Clip {i+1}/{len(sections_with_timing)}...")
                clip = self._create_section_clip(section)
                if clip:
                    video_clips.append(clip)
            
            if not video_clips:
                print("❌ No clips created")
                return None
            
            print(f"✅ {len(video_clips)} clips ready")
            print("📹 Combining...")
            
            final_video = concatenate_videoclips(video_clips, method="compose")
            final_video = final_video.set_audio(audio_clip)
            
            output_path = self.output_dir / output_filename
            print(f"💾 Exporting...")
            
            final_video.write_videofile(
                str(output_path),
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                preset='ultrafast',
                threads=4,
                logger=None
            )
            
            print("✅ Video done!")
            return str(output_path)
            
        except Exception as e:
            print(f"❌ Video error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _calculate_section_timings(self, sections: List[Dict], total_duration: float) -> List[Dict]:
        """Calculate timing for sections"""
        
        if not sections:
            return []
        
        time_per_section = total_duration / len(sections)
        timed_sections = []
        current_time = 0
        
        for section in sections:
            timed_section = section.copy()
            timed_section['start_time'] = current_time
            timed_section['duration'] = time_per_section
            timed_sections.append(timed_section)
            current_time += time_per_section
        
        return timed_sections
    
    def _create_section_clip(self, section: Dict):
        """Create video clip for section"""
        
        try:
            # ✅ CLEAN Hindi characters from section before rendering
            section = self._clean_section_unicode(section)
            
            img = Image.new('RGB', self.resolution, color='white')
            draw = ImageDraw.Draw(img)
            
            # Try multiple fonts with Unicode support
            heading_font = None
            text_font = None
            small_font = None
            
            font_paths = [
                "C:/Windows/Fonts/segoeui.ttf",    # Best Unicode support
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/calibri.ttf",
                "C:/Windows/Fonts/verdana.ttf",
            ]
            
            for font_path in font_paths:
                try:
                    heading_font = ImageFont.truetype(font_path, 70)
                    text_font = ImageFont.truetype(font_path, 45)
                    small_font = ImageFont.truetype(font_path, 35)
                    print(f"✅ Font: {os.path.basename(font_path)}")
                    break
                except:
                    continue
            
            # Fallback to default
            if not heading_font:
                print("⚠️ Using default font")
                heading_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            y_position = 100
            margin_left = 100
            max_width = 1720
            
            # HEADING
            if section.get('heading'):
                heading_text = f"📌 {section['heading']}"
                
                try:
                    draw.text(
                        (margin_left, y_position),
                        heading_text,
                        fill=(30, 64, 175),
                        font=heading_font
                    )
                except Exception as e:
                    # Remove emoji and try again
                    heading_text = section['heading']
                    draw.text(
                        (margin_left, y_position),
                        heading_text,
                        fill=(30, 64, 175),
                        font=heading_font
                    )
                
                y_position += 100
                draw.line(
                    [(margin_left, y_position), (margin_left + 800, y_position)],
                    fill=(59, 130, 246),
                    width=4
                )
                y_position += 50
            
            # DEFINITION
            if section.get('definition'):
                def_text = f"📖 {section['definition']}"
                lines = self._wrap_text(def_text, 70)
                
                for line in lines[:4]:
                    try:
                        draw.text(
                            (margin_left + 20, y_position),
                            line,
                            fill=(31, 41, 55),
                            font=text_font
                        )
                    except:
                        # Clean and retry
                        line = self._clean_text(line)
                        draw.text(
                            (margin_left + 20, y_position),
                            line,
                            fill=(31, 41, 55),
                            font=text_font
                        )
                    y_position += 60
                
                y_position += 30
            
            # POINTS (increased to 8)
            if section.get('points'):
                for point in section['points'][:8]:  # ✅ Show up to 8 points
                    point_text = f"• {point.get('text', '')}"
                    lines = self._wrap_text(point_text, 80)
                    
                    for line in lines[:2]:
                        try:
                            draw.text(
                                (margin_left + 50, y_position),
                                line,
                                fill=(55, 65, 81),
                                font=small_font
                            )
                        except:
                            # Clean and retry
                            line = self._clean_text(line)
                            draw.text(
                                (margin_left + 50, y_position),
                                line,
                                fill=(55, 65, 81),
                                font=small_font
                            )
                        y_position += 50
                    
                    y_position += 15
                    
                    # Stop if running out of space
                    if y_position > 950:
                        break
            
            # Save frame
            temp_img_path = self.output_dir / f"frame_{id(section)}.png"
            img.save(temp_img_path)
            print(f"✅ Frame: {temp_img_path}")
            
            # Create clip
            clip = ImageClip(str(temp_img_path))
            duration = section.get('duration', 3)
            clip = clip.set_duration(duration)
            clip = clip.fadein(0.3).fadeout(0.3)
            
            print(f"✅ Clip: {duration}s")
            return clip
            
        except Exception as e:
            print(f"❌ Clip error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _clean_section_unicode(self, section: Dict) -> Dict:
        """Remove Hindi/Devanagari characters that cause boxes"""
        
        cleaned = section.copy()
        
        if cleaned.get('heading'):
            cleaned['heading'] = self._clean_text(cleaned['heading'])
        
        if cleaned.get('definition'):
            cleaned['definition'] = self._clean_text(cleaned['definition'])
        
        if cleaned.get('points'):
            cleaned['points'] = [
                {**p, 'text': self._clean_text(p.get('text', ''))}
                for p in cleaned['points']
            ]
        
        return cleaned
    
    def _clean_text(self, text: str) -> str:
        """Remove Hindi/Devanagari characters and clean text"""
        
        # Remove Devanagari Unicode range (Hindi characters)
        text = re.sub(r'[\u0900-\u097F]+', '', text)
        
        # Remove other problematic Unicode
        text = re.sub(r'[\u0080-\u08FF\u0980-\uFFFF]+', '', text)
        
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove trailing/leading spaces
        text = text.strip()
        
        return text
    
    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Simple text wrapping"""
        
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            if len(' '.join(current_line + [word])) <= width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

video_service = VideoGenerationService()