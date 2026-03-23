import os
import re
from pathlib import Path
from typing import List, Dict
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
from services.graph_generator import graph_generator
from services.image_searcher import image_searcher

class AdvancedVideoService:
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
        """Generate ADVANCED multi-slide video with images and graphs"""
        
        try:
            print("🎬 ADVANCED Video Generation Started...")
            
            if not os.path.exists(audio_path):
                return None
            
            audio_clip = AudioFileClip(audio_path)
            total_duration = audio_clip.duration
            
            # Generate multiple slides
            slides = self._create_all_slides(content_sections[0] if content_sections else {})
            
            if not slides:
                return None
            
            # Calculate timing per slide
            time_per_slide = total_duration / len(slides)
            
            # Create video clips for each slide
            video_clips = []
            
            for i, slide_data in enumerate(slides):
                print(f"🎬 Creating slide {i+1}/{len(slides)}: {slide_data['type']}")
                
                clip = self._create_slide_clip(slide_data, time_per_slide)
                if clip:
                    video_clips.append(clip)
            
            # Concatenate with transitions
            final_video = concatenate_videoclips(video_clips, method="compose")
            final_video = final_video.set_audio(audio_clip)
            
            # Export
            output_path = self.output_dir / output_filename
            print("💾 Exporting final video...")
            
            final_video.write_videofile(
                str(output_path),
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                preset='medium',
                threads=4,
                logger=None
            )
            
            print("✅ ADVANCED Video Complete!")
            return str(output_path)
            
        except Exception as e:
            print(f"❌ Advanced video error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _create_all_slides(self, section: Dict) -> List[Dict]:
        """Create multiple slides from content"""
        
        slides = []
        
        # 1. TITLE SLIDE
        if section.get('heading'):
            slides.append({
                'type': 'title',
                'heading': section['heading']
            })
        
        # 2. DEFINITION SLIDE (with concept image)
        if section.get('definition'):
            slides.append({
                'type': 'definition',
                'heading': section['heading'],
                'definition': section['definition'],
                'image_query': section['heading']  # Search image for topic
            })
        
        # 3. POINT SLIDES (2 points per slide)
        points = section.get('points', [])
        
        for i in range(0, len(points), 2):
            slide_points = points[i:i+2]
            
            # Check if point contains equation
            has_equation = any(
                p.get('type') == 'equation' for p in slide_points
            )
            
            if has_equation:
                # Equation slide with graph
                equation_point = next(p for p in slide_points if p.get('type') == 'equation')
                slides.append({
                    'type': 'equation_graph',
                    'heading': section['heading'],
                    'points': slide_points,
                    'equation': equation_point.get('text', '')
                })
            else:
                # Regular points slide
                slides.append({
                    'type': 'points',
                    'heading': section['heading'],
                    'points': slide_points
                })
        
        # 4. SUMMARY SLIDE (if more than 4 points)
        if len(points) > 4:
            slides.append({
                'type': 'summary',
                'heading': section['heading'],
                'summary_points': [p.get('text', '')[:60] for p in points[:4]]
            })
        
        print(f"📊 Created {len(slides)} slides")
        return slides
    
    def _create_slide_clip(self, slide_data: Dict, duration: float):
        """Create video clip for a slide"""
        
        slide_type = slide_data.get('type')
        
        if slide_type == 'title':
            return self._create_title_slide(slide_data, duration)
        elif slide_type == 'definition':
            return self._create_definition_slide(slide_data, duration)
        elif slide_type == 'equation_graph':
            return self._create_equation_slide(slide_data, duration)
        elif slide_type == 'points':
            return self._create_points_slide(slide_data, duration)
        elif slide_type == 'summary':
            return self._create_summary_slide(slide_data, duration)
        
        return None
    
    def _create_title_slide(self, data: Dict, duration: float):
        """Create animated title slide"""
        
        img = Image.new('RGB', self.resolution, color='#1E40AF')  # Blue background
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 100)
        except:
            font = ImageFont.load_default()
        
        heading = data['heading']
        
        # Center text
        bbox = draw.textbbox((0, 0), heading, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (1920 - text_width) // 2
        y = (1080 - text_height) // 2
        
        draw.text((x, y), heading, fill='white', font=font)
        
        # Save and create clip
        path = self.output_dir / f"title_{id(data)}.png"
        img.save(path)
        
        clip = ImageClip(str(path)).set_duration(duration)
        clip = clip.fadein(0.5).fadeout(0.5)
        
        return clip
    
    def _create_definition_slide(self, data: Dict, duration: float):
        """Create definition slide with image"""
        
        # Download relevant image
        image_query = data.get('image_query', 'education')
        image_path = image_searcher.search_and_download(
            image_query,
            f"concept_{id(data)}.jpg"
        )
        
        # Create slide
        img = Image.new('RGB', self.resolution, color='white')
        draw = ImageDraw.Draw(img)
        
        # Insert image (top half)
        if image_path and os.path.exists(image_path):
            concept_img = Image.open(image_path)
            concept_img = concept_img.resize((1600, 500))
            img.paste(concept_img, (160, 100))
        
        # Add definition text (bottom half)
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        definition = self._clean_text(data['definition'])
        lines = self._wrap_text(definition, 80)
        
        y = 650
        for line in lines[:3]:
            draw.text((100, y), line, fill=(31, 41, 55), font=font)
            y += 60
        
        # Save
        path = self.output_dir / f"def_{id(data)}.png"
        img.save(path)
        
        clip = ImageClip(str(path)).set_duration(duration)
        clip = clip.fadein(0.5).fadeout(0.5)
        
        return clip
    
    def _create_equation_slide(self, data: Dict, duration: float):
        """Create equation slide with graph"""
        
        # Generate graph
        equation = data.get('equation', '')
        graph_path = graph_generator.generate_graph_from_equation(
            equation,
            f"graph_{id(data)}.png"
        )
        
        # Create slide
        img = Image.new('RGB', self.resolution, color='white')
        draw = ImageDraw.Draw(img)
        
        # Title
        try:
            title_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 60)
            text_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 35)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        draw.text((100, 50), data['heading'], fill=(30, 64, 175), font=title_font)
        
        # Insert graph (right side)
        if graph_path and os.path.exists(graph_path):
            graph_img = Image.open(graph_path)
            graph_img = graph_img.resize((850, 500))
            img.paste(graph_img, (970, 150))
        
        # Points (left side)
        y = 200
        for point in data['points']:
            text = self._clean_text(point.get('text', ''))
            lines = self._wrap_text(f"• {text}", 40)
            
            for line in lines[:2]:
                draw.text((100, y), line, fill=(55, 65, 81), font=text_font)
                y += 50
            y += 20
        
        # Save
        path = self.output_dir / f"eq_{id(data)}.png"
        img.save(path)
        
        clip = ImageClip(str(path)).set_duration(duration)
        clip = clip.fadein(0.5).fadeout(0.5)
        
        return clip
    
    def _create_points_slide(self, data: Dict, duration: float):
        """Create slide with points"""
        
        img = Image.new('RGB', self.resolution, color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 60)
            text_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 45)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        # Title
        draw.text((100, 80), data['heading'], fill=(30, 64, 175), font=title_font)
        
        # Points
        y = 250
        for point in data['points']:
            text = self._clean_text(point.get('text', ''))
            lines = self._wrap_text(f"• {text}", 70)
            
            for line in lines[:2]:
                draw.text((150, y), line, fill=(31, 41, 55), font=text_font)
                y += 70
            y += 30
        
        # Save
        path = self.output_dir / f"points_{id(data)}.png"
        img.save(path)
        
        clip = ImageClip(str(path)).set_duration(duration)
        clip = clip.fadein(0.5).fadeout(0.5)
        
        return clip
    
    def _create_summary_slide(self, data: Dict, duration: float):
        """Create summary slide"""
        
        img = Image.new('RGB', self.resolution, color='#F0F9FF')
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 70)
            text_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 40)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        draw.text((100, 100), "Key Takeaways", fill=(30, 64, 175), font=title_font)
        
        y = 300
        for i, point in enumerate(data['summary_points'], 1):
            text = self._clean_text(point)
            draw.text((150, y), f"{i}. {text}", fill=(31, 41, 55), font=text_font)
            y += 100
        
        # Save
        path = self.output_dir / f"summary_{id(data)}.png"
        img.save(path)
        
        clip = ImageClip(str(path)).set_duration(duration)
        clip = clip.fadein(0.5).fadeout(0.5)
        
        return clip
    
    def _clean_text(self, text: str) -> str:
        """Remove Hindi characters"""
        text = re.sub(r'[\u0900-\u097F]+', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Wrap text to width"""
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

advanced_video_service = AdvancedVideoService()