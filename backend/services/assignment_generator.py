# from google import genai
# import os
# from pathlib import Path
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_LEFT
# from reportlab.lib import colors
# from dotenv import load_dotenv

# load_dotenv()
# genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# class AssignmentGenerator:
#     def __init__(self):
#         self.output_dir = Path("temp/assignments")
#         self.output_dir.mkdir(parents=True, exist_ok=True)
    
#     def generate_assignment(self, topic: str, difficulty: str = "medium") -> tuple:
#         """Generate assignment questions and answers"""
        
#         try:
#             print(f"📝 Generating assignment for: {topic}")
            
#             # Generate questions using AI
#             questions_data = self._generate_questions_ai(topic, difficulty)
            
#             # Create PDF files
#             questions_pdf = self._create_questions_pdf(topic, questions_data, difficulty)
#             answers_pdf = self._create_answers_pdf(topic, questions_data, difficulty)
            
#             print(f"✅ Assignment created")
#             return questions_pdf, answers_pdf
            
#         except Exception as e:
#             print(f"❌ Assignment generation error: {e}")
#             import traceback
#             traceback.print_exc()
#             return None, None
    
#     def _generate_questions_ai(self, topic: str, difficulty: str) -> dict:
#         """Use AI to generate questions"""
        
#         prompt = f"""Generate a practice assignment for the topic: {topic}

# Difficulty Level: {difficulty}

# Create exactly 10 questions in the following format:

# Question 1: [Multiple Choice Question]
# A) [Option A]
# B) [Option B]
# C) [Option C]
# D) [Option D]
# Answer: [Correct option letter]
# Explanation: [Brief explanation]

# Question 2: [Short Answer Question]
# Answer: [Expected answer]
# Explanation: [Brief explanation]

# Question 3: [True/False]
# Answer: [True/False]
# Explanation: [Brief explanation]

# Include mix of:
# - 4 Multiple Choice Questions
# - 3 Short Answer Questions
# - 3 True/False Questions

# Make questions educational and test understanding of key concepts.
# """
        
#         response = genai_client.models.generate_content(
#             model='gemini-2.5-flash',
#             contents=prompt
#         )
        
#         # Parse response
#         questions = self._parse_questions(response.text)
#         return questions
    
#     def _parse_questions(self, text: str) -> dict:
#         """Parse AI response into structured questions"""
        
#         import re
        
#         questions = []
        
#         # Split by "Question N:"
#         question_blocks = re.split(r'Question \d+:', text)[1:]  # Skip first empty split
        
#         for block in question_blocks[:10]:  # Max 10 questions
#             lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
            
#             if not lines:
#                 continue
            
#             question_text = lines[0]
            
#             # Find answer and explanation
#             answer = ""
#             explanation = ""
#             options = []
            
#             for line in lines[1:]:
#                 if line.startswith(('A)', 'B)', 'C)', 'D)')):
#                     options.append(line)
#                 elif line.startswith('Answer:'):
#                     answer = line.replace('Answer:', '').strip()
#                 elif line.startswith('Explanation:'):
#                     explanation = line.replace('Explanation:', '').strip()
            
#             questions.append({
#                 'question': question_text,
#                 'options': options,
#                 'answer': answer,
#                 'explanation': explanation
#             })
        
#         return {'questions': questions}
    
#     def _create_questions_pdf(self, topic: str, data: dict, difficulty: str) -> str:
#         """Create questions PDF (without answers)"""
        
#         filename = f"assignment_{topic.replace(' ', '_')}.pdf"
#         output_path = self.output_dir / filename
        
#         doc = SimpleDocTemplate(str(output_path), pagesize=A4)
#         story = []
#         styles = getSampleStyleSheet()
        
#         # Custom styles
#         title_style = ParagraphStyle(
#             'Title',
#             parent=styles['Heading1'],
#             fontSize=20,
#             textColor=colors.HexColor('#1E40AF'),
#             spaceAfter=20,
#             fontName='Helvetica-Bold'
#         )
        
#         question_style = ParagraphStyle(
#             'Question',
#             parent=styles['Normal'],
#             fontSize=12,
#             spaceAfter=10,
#             fontName='Helvetica-Bold'
#         )
        
#         # Header
#         story.append(Paragraph(f"Practice Assignment: {topic}", title_style))
#         story.append(Paragraph(f"Difficulty: {difficulty.capitalize()}", styles['Normal']))
#         story.append(Spacer(1, 20))
        
#         # Instructions
#         instructions = """
#         <b>Instructions:</b><br/>
#         • Read each question carefully<br/>
#         • Show all your work for calculations<br/>
#         • Answer all questions to the best of your ability<br/>
#         • Check your answers with the answer key after completion
#         """
#         story.append(Paragraph(instructions, styles['Normal']))
#         story.append(Spacer(1, 20))
        
#         # Questions
#         for i, q in enumerate(data.get('questions', []), 1):
#             story.append(Paragraph(f"<b>Question {i}:</b> {q['question']}", question_style))
            
#             # Options if present
#             for option in q.get('options', []):
#                 story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;{option}", styles['Normal']))
            
#             story.append(Spacer(1, 15))
        
#         doc.build(story)
#         return str(output_path)
    
#     def _create_answers_pdf(self, topic: str, data: dict, difficulty: str) -> str:
#         """Create answer key PDF"""
        
#         filename = f"answers_{topic.replace(' ', '_')}.pdf"
#         output_path = self.output_dir / filename
        
#         doc = SimpleDocTemplate(str(output_path), pagesize=A4)
#         story = []
#         styles = getSampleStyleSheet()
        
#         # Title
#         title_style = ParagraphStyle(
#             'Title',
#             parent=styles['Heading1'],
#             fontSize=20,
#             textColor=colors.HexColor('#059669'),
#             spaceAfter=20,
#             fontName='Helvetica-Bold'
#         )
        
#         story.append(Paragraph(f"Answer Key: {topic}", title_style))
#         story.append(Spacer(1, 20))
        
#         # Answers
#         for i, q in enumerate(data.get('questions', []), 1):
#             # Question
#             story.append(Paragraph(f"<b>Question {i}:</b> {q['question']}", styles['Heading3']))
            
#             # Answer
#             answer_text = f"<b>Answer:</b> <font color='green'>{q['answer']}</font>"
#             story.append(Paragraph(answer_text, styles['Normal']))
            
#             # Explanation
#             if q.get('explanation'):
#                 exp_text = f"<b>Explanation:</b> {q['explanation']}"
#                 story.append(Paragraph(exp_text, styles['Italic']))
            
#             story.append(Spacer(1, 15))
        
#         doc.build(story)
#         return str(output_path)

# assignment_generator = AssignmentGenerator()







# from groq import Groq
# import os
# import re
# from pathlib import Path
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_LEFT, TA_CENTER
# from reportlab.lib import colors
# from dotenv import load_dotenv

# load_dotenv()

# # ✅ Groq client
# groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# class AssignmentGenerator:
#     def __init__(self):
#         self.output_dir = Path("temp/assignments")
#         self.output_dir.mkdir(parents=True, exist_ok=True)

#     # ─────────────────────────────────────────────
#     # MAIN: Generate Assignment
#     # ─────────────────────────────────────────────
#     def generate_assignment(self, topic: str, difficulty: str = "medium") -> tuple:
#         """Generate assignment questions and answers PDFs"""

#         try:
#             print(f"📝 Generating assignment for: {topic}")

#             questions_data = self._generate_questions_ai(topic, difficulty)

#             questions_pdf = self._create_questions_pdf(topic, questions_data, difficulty)
#             answers_pdf = self._create_answers_pdf(topic, questions_data, difficulty)

#             print(f"✅ Assignment created: {len(questions_data.get('questions', []))} questions")
#             return questions_pdf, answers_pdf

#         except Exception as e:
#             print(f"❌ Assignment generation error: {e}")
#             import traceback
#             traceback.print_exc()
#             return None, None

#     # ─────────────────────────────────────────────
#     # Generate Questions using Groq
#     # ─────────────────────────────────────────────
#     def _generate_questions_ai(self, topic: str, difficulty: str) -> dict:
#         """Use Groq AI to generate 10 proper MCQ questions"""

#         prompt = f"""You are a teacher creating a multiple choice assignment.
# Topic: {topic}
# Difficulty: {difficulty}

# Generate EXACTLY 10 multiple choice questions. Each question MUST have 4 options (A, B, C, D).

# Use this EXACT format for ALL 10 questions, no exceptions:

# Q1: [Question text here?]
# A) [Option A text]
# B) [Option B text]
# C) [Option C text]
# D) [Option D text]
# Answer: [A or B or C or D]
# Explanation: [One sentence explanation]

# Q2: [Question text here?]
# A) [Option A text]
# B) [Option B text]
# C) [Option C text]
# D) [Option D text]
# Answer: [A or B or C or D]
# Explanation: [One sentence explanation]

# Q3: [Question text here?]
# A) [Option A text]
# B) [Option B text]
# C) [Option C text]
# D) [Option D text]
# Answer: [A or B or C or D]
# Explanation: [One sentence explanation]

# Q4: [Question text here?]
# A) [Option A text]
# B) [Option B text]
# C) [Option C text]
# D) [Option D text]
# Answer: [A or B or C or D]
# Explanation: [One sentence explanation]

# Q5: [Question text here?]
# A) [Option A text]
# B) [Option B text]
# C) [Option C text]
# D) [Option D text]
# Answer: [A or B or C or D]
# Explanation: [One sentence explanation]

# Q6: [Question text here?]
# A) [Option A text]
# B) [Option B text]
# C) [Option C text]
# D) [Option D text]
# Answer: [A or B or C or D]
# Explanation: [One sentence explanation]

# Q7: [Question text here?]
# A) [Option A text]
# B) [Option B text]
# C) [Option C text]
# D) [Option D text]
# Answer: [A or B or C or D]
# Explanation: [One sentence explanation]

# Q8: [Question text here?]
# A) [Option A text]
# B) [Option B text]
# C) [Option C text]
# D) [Option D text]
# Answer: [A or B or C or D]
# Explanation: [One sentence explanation]

# Q9: [Question text here?]
# A) [Option A text]
# B) [Option B text]
# C) [Option C text]
# D) [Option D text]
# Answer: [A or B or C or D]
# Explanation: [One sentence explanation]

# Q10: [Question text here?]
# A) [Option A text]
# B) [Option B text]
# C) [Option C text]
# D) [Option D text]
# Answer: [A or B or C or D]
# Explanation: [One sentence explanation]

# RULES:
# - Every question MUST have exactly 4 options A, B, C, D
# - Answer MUST be only A, B, C, or D
# - No True/False questions
# - No short answer questions
# - Questions must test understanding of {topic}
# - Use simple, clear English"""

#         response = groq_client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=3000,
#             temperature=0.5,
#         )

#         raw_text = response.choices[0].message.content
#         questions = self._parse_questions(raw_text)
#         return {"questions": questions}

#     # ─────────────────────────────────────────────
#     # Parse Questions from AI Response
#     # ─────────────────────────────────────────────
#     def _parse_questions(self, text: str) -> list:
#         """Parse AI response into structured questions list"""

#         questions = []

#         # Split by Q1:, Q2:, etc.
#         blocks = re.split(r'\nQ\d+:', '\n' + text)

#         for block in blocks:
#             block = block.strip()
#             if not block:
#                 continue

#             lines = [l.strip() for l in block.split('\n') if l.strip()]
#             if not lines:
#                 continue

#             question_text = lines[0].strip()
#             # Remove leading colon or number if present
#             question_text = re.sub(r'^[\d\.\:\)]+\s*', '', question_text).strip()

#             if not question_text or len(question_text) < 5:
#                 continue

#             options = {}
#             answer = ""
#             explanation = ""

#             for line in lines[1:]:
#                 line = line.strip()
#                 if re.match(r'^A[\)\.]', line):
#                     options['A'] = re.sub(r'^A[\)\.\s]+', '', line).strip()
#                 elif re.match(r'^B[\)\.]', line):
#                     options['B'] = re.sub(r'^B[\)\.\s]+', '', line).strip()
#                 elif re.match(r'^C[\)\.]', line):
#                     options['C'] = re.sub(r'^C[\)\.\s]+', '', line).strip()
#                 elif re.match(r'^D[\)\.]', line):
#                     options['D'] = re.sub(r'^D[\)\.\s]+', '', line).strip()
#                 elif line.lower().startswith('answer:'):
#                     answer = line.split(':', 1)[1].strip().upper()
#                     # Extract only the letter
#                     match = re.search(r'[ABCD]', answer)
#                     answer = match.group(0) if match else answer[0] if answer else "A"
#                 elif line.lower().startswith('explanation:'):
#                     explanation = line.split(':', 1)[1].strip()

#             # Only add if we have question + all 4 options + answer
#             if (question_text and
#                     len(options) == 4 and
#                     answer in ['A', 'B', 'C', 'D']):
#                 questions.append({
#                     'question': question_text,
#                     'options': options,
#                     'answer': answer,
#                     'explanation': explanation or "Review the topic for more details."
#                 })

#         print(f"✅ Parsed {len(questions)} valid questions")
#         return questions

#     # ─────────────────────────────────────────────
#     # Create Questions PDF
#     # ─────────────────────────────────────────────
#     def _create_questions_pdf(self, topic: str, data: dict, difficulty: str) -> str:
#         """Create questions PDF (without answers)"""

#         filename = f"assignment_{topic.replace(' ', '_')}.pdf"
#         output_path = self.output_dir / filename

#         doc = SimpleDocTemplate(str(output_path), pagesize=A4,
#                                 rightMargin=50, leftMargin=50,
#                                 topMargin=60, bottomMargin=40)
#         story = []
#         styles = getSampleStyleSheet()

#         # Styles
#         title_style = ParagraphStyle(
#             'Title',
#             parent=styles['Heading1'],
#             fontSize=22,
#             textColor=colors.HexColor('#1E40AF'),
#             spaceAfter=6,
#             alignment=TA_CENTER,
#             fontName='Helvetica-Bold'
#         )
#         subtitle_style = ParagraphStyle(
#             'Subtitle',
#             parent=styles['Normal'],
#             fontSize=11,
#             textColor=colors.HexColor('#6B7280'),
#             spaceAfter=20,
#             alignment=TA_CENTER,
#         )
#         question_style = ParagraphStyle(
#             'Question',
#             parent=styles['Normal'],
#             fontSize=12,
#             spaceAfter=6,
#             spaceBefore=14,
#             fontName='Helvetica-Bold',
#             textColor=colors.HexColor('#111827'),
#         )
#         option_style = ParagraphStyle(
#             'Option',
#             parent=styles['Normal'],
#             fontSize=11,
#             spaceAfter=3,
#             leftIndent=20,
#             textColor=colors.HexColor('#374151'),
#         )

#         # Header
#         story.append(Paragraph(f"Practice Assignment: {topic}", title_style))
#         story.append(Paragraph(f"Difficulty: {difficulty.capitalize()}  |  Total Questions: {len(data.get('questions', []))}  |  Each question carries equal marks", subtitle_style))

#         # Instructions
#         instructions = (
#             "<b>Instructions:</b> "
#             "Read each question carefully and choose the BEST answer from the options given (A, B, C, or D). "
#             "Write the letter of your answer clearly."
#         )
#         story.append(Paragraph(instructions, styles['Normal']))
#         story.append(Spacer(1, 16))

#         # Questions
#         questions = data.get('questions', [])
#         if not questions:
#             story.append(Paragraph("No questions generated. Please try again.", styles['Normal']))
#         else:
#             for i, q in enumerate(questions, 1):
#                 # Question text
#                 story.append(Paragraph(f"Q{i}. {q['question']}", question_style))

#                 # Options
#                 for letter in ['A', 'B', 'C', 'D']:
#                     option_text = q['options'].get(letter, '')
#                     if option_text:
#                         story.append(Paragraph(f"{letter})  {option_text}", option_style))

#                 story.append(Spacer(1, 8))

#         doc.build(story)
#         print(f"✅ Questions PDF: {output_path}")
#         return str(output_path)

#     # ─────────────────────────────────────────────
#     # Create Answers PDF
#     # ─────────────────────────────────────────────
#     def _create_answers_pdf(self, topic: str, data: dict, difficulty: str) -> str:
#         """Create answer key PDF"""

#         filename = f"answers_{topic.replace(' ', '_')}.pdf"
#         output_path = self.output_dir / filename

#         doc = SimpleDocTemplate(str(output_path), pagesize=A4,
#                                 rightMargin=50, leftMargin=50,
#                                 topMargin=60, bottomMargin=40)
#         story = []
#         styles = getSampleStyleSheet()

#         # Styles
#         title_style = ParagraphStyle(
#             'Title',
#             parent=styles['Heading1'],
#             fontSize=22,
#             textColor=colors.HexColor('#059669'),
#             spaceAfter=6,
#             alignment=TA_CENTER,
#             fontName='Helvetica-Bold'
#         )
#         subtitle_style = ParagraphStyle(
#             'Subtitle',
#             parent=styles['Normal'],
#             fontSize=11,
#             textColor=colors.HexColor('#6B7280'),
#             spaceAfter=20,
#             alignment=TA_CENTER,
#         )
#         question_style = ParagraphStyle(
#             'Question',
#             parent=styles['Normal'],
#             fontSize=12,
#             spaceAfter=4,
#             spaceBefore=14,
#             fontName='Helvetica-Bold',
#             textColor=colors.HexColor('#111827'),
#         )
#         answer_style = ParagraphStyle(
#             'Answer',
#             parent=styles['Normal'],
#             fontSize=12,
#             spaceAfter=3,
#             leftIndent=20,
#             textColor=colors.HexColor('#059669'),
#             fontName='Helvetica-Bold',
#         )
#         explanation_style = ParagraphStyle(
#             'Explanation',
#             parent=styles['Normal'],
#             fontSize=11,
#             spaceAfter=4,
#             leftIndent=20,
#             textColor=colors.HexColor('#374151'),
#         )

#         # Header
#         story.append(Paragraph(f"Answer Key: {topic}", title_style))
#         story.append(Paragraph(f"Difficulty: {difficulty.capitalize()}", subtitle_style))

#         # Answers
#         questions = data.get('questions', [])
#         if not questions:
#             story.append(Paragraph("No answers available.", styles['Normal']))
#         else:
#             for i, q in enumerate(questions, 1):
#                 # Question
#                 story.append(Paragraph(f"Q{i}. {q['question']}", question_style))

#                 # Correct answer with option text
#                 correct_letter = q['answer']
#                 correct_text = q['options'].get(correct_letter, '')
#                 story.append(Paragraph(
#                     f"✓ Correct Answer: {correct_letter})  {correct_text}",
#                     answer_style
#                 ))

#                 # Explanation
#                 if q.get('explanation'):
#                     story.append(Paragraph(
#                         f"Explanation: {q['explanation']}",
#                         explanation_style
#                     ))

#                 story.append(Spacer(1, 8))

#         doc.build(story)
#         print(f"✅ Answers PDF: {output_path}")
#         return str(output_path)


# # ─────────────────────────────────────────────
# # Singleton instance
# # ─────────────────────────────────────────────
# assignment_generator = AssignmentGenerator()















from groq import Groq
import os
import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class AssignmentGenerator:
    def __init__(self):
        self.output_dir = Path("temp/assignments")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ─────────────────────────────────────────────
    # MAIN: Generate Assignment
    # ─────────────────────────────────────────────
    def generate_assignment(self, topic: str, difficulty: str = "medium") -> tuple:
        try:
            print(f"📝 Generating assignment for: {topic}")
            questions_data = self._generate_questions_ai(topic, difficulty)
            questions_pdf = self._create_questions_pdf(topic, questions_data, difficulty)
            answers_pdf = self._create_answers_pdf(topic, questions_data, difficulty)
            print(f"✅ Assignment created: {len(questions_data.get('questions', []))} questions")
            return questions_pdf, answers_pdf
        except Exception as e:
            print(f"❌ Assignment error: {e}")
            import traceback
            traceback.print_exc()
            return None, None

    # ─────────────────────────────────────────────
    # Generate Questions using Groq
    # ─────────────────────────────────────────────
    def _generate_questions_ai(self, topic: str, difficulty: str) -> dict:
        prompt = f"""You are a teacher. Create a multiple choice quiz about: {topic}
Difficulty: {difficulty}

Generate EXACTLY 10 MCQ questions. Every question MUST have 4 options.

STRICT FORMAT — follow exactly:

Q1: What is [question about {topic}]?
A) [option 1]
B) [option 2]
C) [option 3]
D) [option 4]
Answer: A
Explanation: [one line reason]

Q2: Which of the following [question about {topic}]?
A) [option 1]
B) [option 2]
C) [option 3]
D) [option 4]
Answer: B
Explanation: [one line reason]

Q3: How does [question about {topic}]?
A) [option 1]
B) [option 2]
C) [option 3]
D) [option 4]
Answer: C
Explanation: [one line reason]

Q4: Why is [question about {topic}]?
A) [option 1]
B) [option 2]
C) [option 3]
D) [option 4]
Answer: D
Explanation: [one line reason]

Q5: What happens when [question about {topic}]?
A) [option 1]
B) [option 2]
C) [option 3]
D) [option 4]
Answer: A
Explanation: [one line reason]

Q6: Which statement about {topic} is correct?
A) [option 1]
B) [option 2]
C) [option 3]
D) [option 4]
Answer: B
Explanation: [one line reason]

Q7: What is the formula/definition of [part of {topic}]?
A) [option 1]
B) [option 2]
C) [option 3]
D) [option 4]
Answer: C
Explanation: [one line reason]

Q8: In which situation is [aspect of {topic}] used?
A) [option 1]
B) [option 2]
C) [option 3]
D) [option 4]
Answer: A
Explanation: [one line reason]

Q9: What is the result of [calculation or concept in {topic}]?
A) [option 1]
B) [option 2]
C) [option 3]
D) [option 4]
Answer: D
Explanation: [one line reason]

Q10: Which of these is a real-world application of {topic}?
A) [option 1]
B) [option 2]
C) [option 3]
D) [option 4]
Answer: B
Explanation: [one line reason]

RULES:
- All 10 questions MUST be about {topic} specifically
- Every question MUST have exactly A) B) C) D) options
- Answer must be one letter: A, B, C, or D
- NO True/False, NO short answer
- Options must be realistic and educational
- Simple clear English only"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3500,
            temperature=0.4,
        )

        raw_text = response.choices[0].message.content
        questions = self._parse_questions(raw_text)
        return {"questions": questions, "topic": topic}

    # ─────────────────────────────────────────────
    # Parse Questions
    # ─────────────────────────────────────────────
    def _parse_questions(self, text: str) -> list:
        questions = []
        blocks = re.split(r'\nQ\d+:', '\n' + text)

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            lines = [l.strip() for l in block.split('\n') if l.strip()]
            if not lines:
                continue

            question_text = lines[0].strip()
            question_text = re.sub(r'^[\d\.\:\)]+\s*', '', question_text).strip()

            if not question_text or len(question_text) < 8:
                continue

            options = {}
            answer = ""
            explanation = ""

            for line in lines[1:]:
                line = line.strip()
                if re.match(r'^A[\)\.]', line):
                    options['A'] = re.sub(r'^A[\)\.\s]+', '', line).strip()
                elif re.match(r'^B[\)\.]', line):
                    options['B'] = re.sub(r'^B[\)\.\s]+', '', line).strip()
                elif re.match(r'^C[\)\.]', line):
                    options['C'] = re.sub(r'^C[\)\.\s]+', '', line).strip()
                elif re.match(r'^D[\)\.]', line):
                    options['D'] = re.sub(r'^D[\)\.\s]+', '', line).strip()
                elif line.lower().startswith('answer:'):
                    raw_ans = line.split(':', 1)[1].strip().upper()
                    match = re.search(r'[ABCD]', raw_ans)
                    answer = match.group(0) if match else "A"
                elif line.lower().startswith('explanation:'):
                    explanation = line.split(':', 1)[1].strip()

            if question_text and len(options) == 4 and answer in ['A', 'B', 'C', 'D']:
                questions.append({
                    'question': question_text,
                    'options': options,
                    'answer': answer,
                    'explanation': explanation or "Refer to your lesson notes."
                })

        print(f"✅ Parsed {len(questions)} questions")
        return questions

    # ─────────────────────────────────────────────
    # Create Questions PDF — with bubble sheet style
    # ─────────────────────────────────────────────
    def _create_questions_pdf(self, topic: str, data: dict, difficulty: str) -> str:
        filename = f"assignment_{topic.replace(' ', '_')}.pdf"
        output_path = self.output_dir / filename

        doc = SimpleDocTemplate(str(output_path), pagesize=A4,
                                rightMargin=50, leftMargin=50,
                                topMargin=50, bottomMargin=40)
        story = []
        styles = getSampleStyleSheet()

        # ── Styles ──
        title_style = ParagraphStyle('T', parent=styles['Heading1'],
            fontSize=22, textColor=colors.HexColor('#1E3A8A'),
            spaceAfter=4, alignment=TA_CENTER, fontName='Helvetica-Bold')

        sub_style = ParagraphStyle('S', parent=styles['Normal'],
            fontSize=10, textColor=colors.HexColor('#6B7280'),
            spaceAfter=16, alignment=TA_CENTER)

        instr_style = ParagraphStyle('I', parent=styles['Normal'],
            fontSize=11, textColor=colors.HexColor('#374151'),
            spaceAfter=16, backColor=colors.HexColor('#EFF6FF'),
            borderPadding=8)

        q_style = ParagraphStyle('Q', parent=styles['Normal'],
            fontSize=12, spaceAfter=6, spaceBefore=14,
            fontName='Helvetica-Bold', textColor=colors.HexColor('#111827'))

        opt_style = ParagraphStyle('O', parent=styles['Normal'],
            fontSize=11, spaceAfter=4, leftIndent=24,
            textColor=colors.HexColor('#1F2937'))

        # ── Header ──
        story.append(Paragraph(f"📚 Assignment: {topic}", title_style))
        story.append(Paragraph(
            f"Difficulty: {difficulty.capitalize()}  ·  Total: {len(data.get('questions', []))} Questions  ·  Marks: {len(data.get('questions', []))} × 1 = {len(data.get('questions', []))}",
            sub_style))

        story.append(Paragraph(
            "📌 Instructions: Read each question carefully. "
            "Choose the BEST answer (A, B, C, or D) and circle or write the letter in the blank provided. "
            "Each correct answer = 1 mark.",
            instr_style))

        # ── Answer Blank Table at top ──
        questions = data.get('questions', [])
        if questions:
            blank_data = [["Q.No.", "Answer", "Q.No.", "Answer", "Q.No.", "Answer"]]
            row = []
            for i in range(1, len(questions) + 1):
                row.append(str(i))
                row.append("______")
                if len(row) == 6:
                    blank_data.append(row)
                    row = []
            if row:
                while len(row) < 6:
                    row.append("")
                blank_data.append(row)

            blank_table = Table(blank_data, colWidths=[45, 55, 45, 55, 45, 55])
            blank_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(blank_table)
            story.append(Spacer(1, 20))

        # ── Questions ──
        for i, q in enumerate(questions, 1):
            story.append(Paragraph(f"Q{i}.  {q['question']}", q_style))

            for letter in ['A', 'B', 'C', 'D']:
                opt_text = q['options'].get(letter, '')
                if opt_text:
                    story.append(Paragraph(f"○  {letter})  {opt_text}", opt_style))

            story.append(Spacer(1, 6))

        doc.build(story)
        print(f"✅ Questions PDF: {output_path}")
        return str(output_path)

    # ─────────────────────────────────────────────
    # Create Answers PDF — with score sheet
    # ─────────────────────────────────────────────
    def _create_answers_pdf(self, topic: str, data: dict, difficulty: str) -> str:
        filename = f"answers_{topic.replace(' ', '_')}.pdf"
        output_path = self.output_dir / filename

        doc = SimpleDocTemplate(str(output_path), pagesize=A4,
                                rightMargin=50, leftMargin=50,
                                topMargin=50, bottomMargin=40)
        story = []
        styles = getSampleStyleSheet()

        # ── Styles ──
        title_style = ParagraphStyle('T', parent=styles['Heading1'],
            fontSize=22, textColor=colors.HexColor('#065F46'),
            spaceAfter=4, alignment=TA_CENTER, fontName='Helvetica-Bold')

        sub_style = ParagraphStyle('S', parent=styles['Normal'],
            fontSize=10, textColor=colors.HexColor('#6B7280'),
            spaceAfter=16, alignment=TA_CENTER)

        q_style = ParagraphStyle('Q', parent=styles['Normal'],
            fontSize=12, spaceAfter=4, spaceBefore=12,
            fontName='Helvetica-Bold', textColor=colors.HexColor('#111827'))

        correct_style = ParagraphStyle('C', parent=styles['Normal'],
            fontSize=12, spaceAfter=3, leftIndent=20,
            textColor=colors.HexColor('#065F46'), fontName='Helvetica-Bold')

        wrong_style = ParagraphStyle('W', parent=styles['Normal'],
            fontSize=11, spaceAfter=3, leftIndent=20,
            textColor=colors.HexColor('#9CA3AF'))

        exp_style = ParagraphStyle('E', parent=styles['Normal'],
            fontSize=10, spaceAfter=4, leftIndent=20,
            textColor=colors.HexColor('#4B5563'))

        # ── Header ──
        questions = data.get('questions', [])
        story.append(Paragraph(f"✅ Answer Key: {topic}", title_style))
        story.append(Paragraph(
            f"Total Questions: {len(questions)}  ·  Total Marks: {len(questions)}",
            sub_style))

        # ── Quick Answer Table ──
        if questions:
            ans_data = [["Q", "Ans", "Q", "Ans", "Q", "Ans", "Q", "Ans", "Q", "Ans"]]
            row = []
            for i, q in enumerate(questions, 1):
                row.append(str(i))
                row.append(q['answer'])
                if len(row) == 10:
                    ans_data.append(row)
                    row = []
            if row:
                while len(row) < 10:
                    row.append("")
                ans_data.append(row)

            ans_table = Table(ans_data, colWidths=[30, 30, 30, 30, 30, 30, 30, 30, 30, 30])
            ans_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#065F46')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1FAE5')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0FDF4')]),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                # Highlight answer rows
                ('FONTNAME', (1, 1), (1, -1), 'Helvetica-Bold'),
                ('TEXTCOLOR', (1, 1), (-1, -1), colors.HexColor('#065F46')),
            ]))
            story.append(ans_table)
            story.append(Spacer(1, 20))

        # ── Score Sheet ──
        score_data = [
            ["Student Name:", "________________________", "Date:", "____________"],
            ["Total Correct:", "_____ / " + str(len(questions)), "Score %:", "________%"],
        ]
        score_table = Table(score_data, colWidths=[100, 160, 80, 100])
        score_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 20))

        # ── Grading Scale ──
        grade_data = [
            ["Marks", "9-10", "7-8", "5-6", "3-4", "0-2"],
            ["Grade", "A+ 🌟", "A ✅", "B 👍", "C ⚠️", "D ❌"],
        ]
        grade_table = Table(grade_data, colWidths=[60, 60, 60, 60, 60, 60])
        grade_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BFDBFE')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#EFF6FF')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(grade_table)
        story.append(Spacer(1, 24))

        # ── Detailed Answers ──
        story.append(Paragraph("📋 Detailed Explanations", ParagraphStyle('H',
            parent=styles['Heading2'], fontSize=14,
            textColor=colors.HexColor('#1E3A8A'), spaceAfter=12)))

        for i, q in enumerate(questions, 1):
            story.append(Paragraph(f"Q{i}. {q['question']}", q_style))

            for letter in ['A', 'B', 'C', 'D']:
                opt_text = q['options'].get(letter, '')
                if not opt_text:
                    continue
                if letter == q['answer']:
                    story.append(Paragraph(f"✓  {letter})  {opt_text}  ← CORRECT", correct_style))
                else:
                    story.append(Paragraph(f"✗  {letter})  {opt_text}", wrong_style))

            if q.get('explanation'):
                story.append(Paragraph(f"💡 {q['explanation']}", exp_style))

            story.append(Spacer(1, 8))

        doc.build(story)
        print(f"✅ Answers PDF: {output_path}")
        return str(output_path)


# ─────────────────────────────────────────────
# Singleton instance
# ─────────────────────────────────────────────
assignment_generator = AssignmentGenerator()