# def parse_content(text: str):
#     """Parse AI response into sections"""
    
#     lines = text.split('\n')
#     sections = []
    
#     current_section = {
#         'heading': 'Lesson',
#         'definition': None,
#         'points': []
#     }
    
#     for line in lines:
#         line = line.strip()
#         if not line:
#             continue
        
#         # Simple parsing
#         if len(line) < 60 and line[0].isupper() and ':' in line:
#             # Save previous section
#             if current_section['definition'] or current_section['points']:
#                 sections.append(current_section)
            
#             # New section
#             current_section = {
#                 'heading': line.replace(':', ''),
#                 'definition': None,
#                 'points': []
#             }
#         elif len(line) > 20 and not current_section['definition']:
#             current_section['definition'] = line
#         else:
#             current_section['points'].append({'text': line})
    
#     # Add last section
#     if current_section['definition'] or current_section['points']:
#         sections.append(current_section)
    
#     return sections












# import re

# def parse_content(text: str):
#     """Parse structured AI response"""
    
#     print(f"📝 Parsing text length: {len(text)} chars")
    
#     # Clean up text
#     text = text.strip()
    
#     # Extract heading (first line or bracketed topic)
#     heading = _extract_heading(text)
    
#     # Extract definition
#     definition = _extract_definition(text)
    
#     # Extract all points (key points, examples, formulas)
#     points = _extract_all_points(text)
    
#     section = {
#         'heading': heading,
#         'definition': definition,
#         'points': points
#     }
    
#     print(f"✅ Parsed: Heading='{heading}', Def={len(definition) if definition else 0} chars, Points={len(points)}")
    
#     return [section]


# def _extract_heading(text: str) -> str:
#     """Extract topic heading"""
    
#     # Look for bracketed heading [TOPIC]
#     bracket_match = re.search(r'\[(.*?)\]', text)
#     if bracket_match:
#         return bracket_match.group(1).strip()
    
#     # First line before "Definition:"
#     if 'Definition:' in text:
#         heading = text.split('Definition:')[0].strip()
#         # Clean up heading
#         heading = re.sub(r'\n+', ' ', heading)
#         heading = heading.split('\n')[0]  # First line
#         if len(heading) < 60 and len(heading) > 3:
#             return heading
    
#     # First substantial line
#     lines = text.split('\n')
#     for line in lines[:3]:
#         line = line.strip()
#         if 10 < len(line) < 60 and not line.startswith(('Definition', 'Key', 'Formula', 'Example')):
#             return line
    
#     return "Lesson"


# def _extract_definition(text: str) -> str:
#     """Extract definition"""
    
#     # Look for "Definition:" section
#     def_match = re.search(r'Definition:\s*(.+?)(?=Key Points:|Formula:|Example:|\n\n|\Z)', text, re.DOTALL | re.IGNORECASE)
    
#     if def_match:
#         definition = def_match.group(1).strip()
#         # Clean up
#         definition = re.sub(r'\n+', ' ', definition)
#         definition = definition[:300]  # Max length
#         return definition
    
#     # Look for sentence with "is", "are", "means"
#     sentences = text.split('.')
#     for sentence in sentences[:5]:
#         sentence = sentence.strip()
#         if any(word in sentence.lower() for word in [' is ', ' are ', ' means ', ' refers ']):
#             if 30 < len(sentence) < 200:
#                 return sentence + '.'
    
#     return None


# def _extract_all_points(text: str) -> list:
#     """Extract ALL points from text"""
    
#     points = []
    
#     # 1. Extract numbered points (1. 2. 3. etc.)
#     numbered = re.findall(r'\d+\.\s+([^\n]+)', text)
#     for point in numbered:
#         point = point.strip()
#         if len(point) > 15:
#             points.append({'type': 'bullet', 'text': point})
    
#     # 2. Extract bullet points (• - *)
#     bullets = re.findall(r'[•\-\*]\s+([^\n]+)', text)
#     for point in bullets:
#         point = point.strip()
#         if len(point) > 15:
#             points.append({'type': 'bullet', 'text': point})
    
#     # 3. Extract formulas/equations
#     formulas = re.findall(r'(?:Formula|Equation):\s*([^\n]+)', text, re.IGNORECASE)
#     for formula in formulas:
#         formula = formula.strip()
#         if len(formula) > 5:
#             points.append({'type': 'equation', 'text': formula})
    
#     # 4. Extract examples
#     examples = re.findall(r'Example:\s*(.+?)(?=\n\n|\Z)', text, re.DOTALL | re.IGNORECASE)
#     for example in examples:
#         example = example.strip()
#         example = re.sub(r'\n+', ' ', example)
#         if len(example) > 20:
#             # Split long examples into sentences
#             sentences = example.split('.')
#             for sent in sentences[:2]:  # Max 2 sentences
#                 sent = sent.strip()
#                 if len(sent) > 15:
#                     points.append({'type': 'text', 'text': sent + '.'})
    
#     # 5. If not enough points, extract from "Key Points:" section
#     if len(points) < 3:
#         key_section = re.search(r'Key Points?:\s*(.+?)(?=Formula:|Example:|\n\n|\Z)', text, re.DOTALL | re.IGNORECASE)
#         if key_section:
#             key_text = key_section.group(1)
#             lines = key_text.split('\n')
#             for line in lines:
#                 line = line.strip()
#                 # Remove numbering
#                 line = re.sub(r'^\d+[\.\)]\s*', '', line)
#                 if len(line) > 15:
#                     points.append({'type': 'bullet', 'text': line})
    
#     print(f"📊 Extracted {len(points)} points")
    
#     return points[:10]  # Max 10 points



import re

class ContentParser:
    """Parse AI-generated content into structured format"""
    
    def parse_content(self, text):
        """
        Parse AI response into structured sections
        
        Returns list of sections with:
        - heading
        - definition
        - points (list of dicts with type and text)
        """
        
        sections = []
        lines = text.split('\n')
        
        current_section = {
            'heading': '',
            'definition': '',
            'points': []
        }
        
        in_definition = False
        in_points = False
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            # Clean Hindi/special characters
            line = self._clean_text(line)
            
            # Detect heading (usually in brackets or all caps)
            if line.startswith('[') and line.endswith(']'):
                if current_section['heading']:
                    sections.append(current_section)
                    current_section = {'heading': '', 'definition': '', 'points': []}
                
                current_section['heading'] = line.strip('[]')
                in_definition = True
                in_points = False
                continue
            
            # Detect numbered points
            if re.match(r'^\d+\.', line):
                in_points = True
                in_definition = False
                point_text = re.sub(r'^\d+\.\s*', '', line)
                current_section['points'].append({
                    'type': 'numbered',
                    'text': point_text
                })
                continue
            
            # Detect bullet points
            if line.startswith('•') or line.startswith('-'):
                in_points = True
                in_definition = False
                point_text = line.lstrip('•-').strip()
                current_section['points'].append({
                    'type': 'bullet',
                    'text': point_text
                })
                continue
            
            # Detect formula/equation
            if 'formula' in line.lower() or 'equation' in line.lower() or '=' in line:
                current_section['points'].append({
                    'type': 'formula',
                    'text': line
                })
                continue
            
            # Detect example
            if 'example' in line.lower():
                current_section['points'].append({
                    'type': 'example',
                    'text': line
                })
                continue
            
            # Add to definition or points
            if in_definition and not current_section['definition']:
                current_section['definition'] = line
            elif in_points:
                if current_section['points']:
                    # Append to last point
                    current_section['points'][-1]['text'] += ' ' + line
                else:
                    current_section['points'].append({
                        'type': 'text',
                        'text': line
                    })
            else:
                # First line after heading is definition
                if not current_section['definition']:
                    current_section['definition'] = line
                    in_definition = False
        
        # Add last section
        if current_section['heading'] or current_section['definition'] or current_section['points']:
            sections.append(current_section)
        
        # If no sections found, create a basic one
        if not sections:
            sections.append({
                'heading': 'Lesson',
                'definition': text[:200] if len(text) > 200 else text,
                'points': [{'type': 'text', 'text': text}]
            })
        
        return sections
    
    def _clean_text(self, text):
        """Remove Hindi/Devanagari and special characters"""
        # Remove Devanagari script (Hindi)
        text = re.sub(r'[\u0900-\u097F]+', '', text)
        
        # Remove other non-ASCII characters
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        
        # Remove common Hindi phrases
        hindi_phrases = [
            'Namaste', 'Bahut accha', 'Arre wah', 'Chaliye',
            'Dekho', 'Acha', 'Theek hai', 'Sahi', 'Bilkul'
        ]
        
        for phrase in hindi_phrases:
            text = text.replace(phrase, '')
        
        # Clean extra spaces
        text = ' '.join(text.split())
        
        return text.strip()

# Export instance
content_parser = ContentParser()

# Also export the parse function directly
def parse_content(text):
    """Direct parse function for backward compatibility"""
    return content_parser.parse_content(text)