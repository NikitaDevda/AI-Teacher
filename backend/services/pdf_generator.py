from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from pathlib import Path
import os
from datetime import datetime

class PDFNotesGenerator:
    def __init__(self):
        self.output_dir = Path("temp/notes")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_notes(self, content_data: dict, filename: str) -> str:
        """Generate comprehensive PDF notes"""
        
        try:
            print(f"📄 Generating PDF notes...")
            
            output_path = self.output_dir / filename
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18,
            )
            
            # Container for elements
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1E40AF'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=18,
                textColor=colors.HexColor('#1E40AF'),
                spaceAfter=12,
                spaceBefore=12,
                fontName='Helvetica-Bold'
            )
            
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['Normal'],
                fontSize=12,
                leading=18,
                spaceAfter=12,
                alignment=TA_LEFT
            )
            
            # Title
            title = Paragraph(content_data.get('heading', 'Study Notes'), title_style)
            story.append(title)
            story.append(Spacer(1, 0.3*inch))
            
            # Date
            date_text = f"<i>Generated on: {datetime.now().strftime('%B %d, %Y')}</i>"
            story.append(Paragraph(date_text, styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Definition Section
            if content_data.get('definition'):
                story.append(Paragraph("📖 Definition", heading_style))
                definition = Paragraph(content_data['definition'], body_style)
                story.append(definition)
                story.append(Spacer(1, 0.2*inch))
            
            # Key Points Section
            points = content_data.get('points', [])
            if points:
                story.append(Paragraph("📌 Key Points", heading_style))
                
                for i, point in enumerate(points, 1):
                    point_text = point.get('text', '')
                    point_type = point.get('type', 'bullet')
                    
                    if point_type == 'equation':
                        # Highlight equations
                        equation_text = f"<b>Formula:</b> <font color='#059669'>{point_text}</font>"
                        story.append(Paragraph(equation_text, body_style))
                    else:
                        bullet_text = f"• {point_text}"
                        story.append(Paragraph(bullet_text, body_style))
                    
                    story.append(Spacer(1, 0.1*inch))
            
            # Additional Notes Section
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph("📝 Additional Notes", heading_style))
            story.append(Paragraph("Use this space for your own notes and observations.", styles['Italic']))
            
            # Build PDF
            doc.build(story)
            
            print(f"✅ PDF notes created: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"❌ PDF generation error: {e}")
            import traceback
            traceback.print_exc()
            return None

pdf_generator = PDFNotesGenerator()