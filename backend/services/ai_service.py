# from openai import OpenAI
# from google import genai
# from google.genai import types
# import os
# from typing import List, Dict
# from dotenv import load_dotenv

# load_dotenv()

# # OpenAI for TTS/STT only
# openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Gemini client
# genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# class AIService:
#     @staticmethod
#     def get_teaching_response(question: str, conversation_history: List[Dict], subject: str = "general"):
#         """Get AI teacher response using Gemini (FREE)"""
        
#         system_prompt = f"""You are a friendly and patient teacher teaching {subject}.

# Instructions:
# - Explain concepts clearly with examples
# - Use simple language
# - If student interrupts with a doubt, answer it first
# - Then ask if they want you to continue the previous topic
# - Keep responses concise (3-4 sentences max)
# - Use analogies and real-world examples
# - Be encouraging and supportive
# - Respond in Hindi-English mix (Hinglish) for better understanding
# """
        
#         # Build conversation context
#         full_prompt = system_prompt + "\n\n"
        
#         for msg in conversation_history:
#             if msg["role"] == "user":
#                 full_prompt += f"Student: {msg['content']}\n"
#             elif msg["role"] == "assistant":
#                 full_prompt += f"Teacher: {msg['content']}\n"
        
#         full_prompt += f"\nStudent: {question}\nTeacher:"
        
#         # Use Gemini API with correct model
#         response = genai_client.models.generate_content(
#             model='gemini-2.5-flash',  # ✅ CORRECTED!
#             contents=full_prompt
#         )
        
#         return response.text
    
#     @staticmethod
#     def text_to_speech(text: str, output_file: str = "temp/speech.mp3"):
#         """Convert text to speech using OpenAI"""
        
#         try:
#             response = openai_client.audio.speech.create(
#                 model="tts-1",
#                 voice="alloy",
#                 input=text
#             )
            
#             response.stream_to_file(output_file)
#             return output_file
#         except Exception as e:
#             print(f"⚠️ TTS Error (quota issue - will skip audio): {e}")
#             return None
    
#     @staticmethod
#     def speech_to_text(audio_file_path: str, language: str = "hi"):
#         """Convert speech to text using OpenAI"""
        
#         try:
#             with open(audio_file_path, 'rb') as audio_file:
#                 transcript = openai_client.audio.transcriptions.create(
#                     model="whisper-1",
#                     file=audio_file,
#                     language=language
#                 )
            
#             return transcript.text
#         except Exception as e:
#             print(f"⚠️ STT Error: {e}")
#             return None















# from openai import OpenAI
# from google import genai
# from google.genai import types
# import os
# from typing import List, Dict
# from dotenv import load_dotenv

# load_dotenv()

# # OpenAI client (optional - may not have credits)
# try:
#     openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#     openai_available = True
# except:
#     openai_client = None
#     openai_available = False

# # Gemini client (FREE!)
# genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# class AIService:
#     @staticmethod
#     def get_teaching_response(question: str, conversation_history: List[Dict], subject: str = "general"):
#         """Get AI teacher response using Gemini (FREE)"""
        
#         system_prompt = f"""You are a friendly and patient teacher teaching {subject}.

# Instructions:
# - Explain concepts clearly with examples
# - Use simple language
# - If student interrupts with a doubt, answer it first
# - Then ask if they want you to continue the previous topic
# - Keep responses concise (3-4 sentences max)
# - Use analogies and real-world examples
# - Be encouraging and supportive
# - Respond in Hindi-English mix (Hinglish) for better understanding
# """
        
#         # Build conversation context
#         full_prompt = system_prompt + "\n\n"
        
#         for msg in conversation_history:
#             if msg["role"] == "user":
#                 full_prompt += f"Student: {msg['content']}\n"
#             elif msg["role"] == "assistant":
#                 full_prompt += f"Teacher: {msg['content']}\n"
        
#         full_prompt += f"\nStudent: {question}\nTeacher:"
        
#         # Use Gemini API
#         response = genai_client.models.generate_content(
#             model='gemini-2.5-flash',
#             contents=full_prompt
#         )
        
#         return response.text
    

    

#     @staticmethod
#     def text_to_speech(text: str, output_file: str = "temp/speech.mp3"):
#         """Convert text to speech - FREE with gTTS"""
        
#         # Try OpenAI first (if available)
#         if openai_available:
#             try:
#                 response = openai_client.audio.speech.create(
#                     model="tts-1",
#                     voice="alloy",
#                     input=text
#                 )
#                 response.stream_to_file(output_file)
#                 print(f"✅ Audio (OpenAI): {output_file}")
#                 return output_file
#             except Exception as e:
#                 print(f"⚠️ OpenAI TTS failed: {e}")
#                 # Fall through to gTTS
        
#         # Use FREE gTTS as fallback
#         try:
#             from gtts import gTTS
            
#             # Generate speech
#             tts = gTTS(text=text, lang='hi', slow=False)
#             tts.save(output_file)
            
#             print(f"✅ Audio (gTTS - FREE): {output_file}")
#             return output_file
            
#         except ImportError:
#             print("⚠️ gTTS not installed. Run: pip install gtts")
#             return None
            
#         except Exception as e:
#             print(f"⚠️ TTS Error: {e}")
#             return None
    
#     @staticmethod
#     def speech_to_text(audio_file_path: str, language: str = "hi"):
#         """Convert speech to text using OpenAI Whisper"""
        
#         if not openai_available:
#             print("⚠️ OpenAI not available for STT")
#             return None
        
#         try:
#             with open(audio_file_path, 'rb') as audio_file:
#                 transcript = openai_client.audio.transcriptions.create(
#                     model="whisper-1",
#                     file=audio_file,
#                     language=language
#                 )
            
#             return transcript.text
            
#         except Exception as e:
#             print(f"⚠️ STT Error: {e}")
#             return None

















# from openai import OpenAI
# from google import genai
# from google.genai import types
# import os
# from typing import List, Dict
# from dotenv import load_dotenv

# load_dotenv()

# # OpenAI client (optional)
# try:
#     openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#     openai_available = True
# except:
#     openai_client = None
#     openai_available = False

# # Gemini client
# genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# class AIService:
#     @staticmethod
#     def get_teaching_response(question: str, conversation_history: List[Dict], subject: str = "general"):
#         """Get AI teacher response - STRUCTURED FORMAT"""
        
#         system_prompt = f"""You are an educational content generator for {subject}.

# CRITICAL: Provide content in this EXACT STRUCTURED format:

# [TOPIC NAME]

# Definition: [2-3 sentence clear definition]

# Key Points:
# 1. [First important point]
# 2. [Second important point]  
# 3. [Third important point]
# 4. [Fourth important point]
# 5. [Fifth important point]

# Formula/Equation: [If applicable, write mathematical formula]

# Example: [Practical example with explanation]

# RULES:
# - NO greetings (Namaste, Hello)
# - NO conversational words (Arre wah, Bahut accha, Chaliye, Dekho)
# - NO questions at the end
# - MINIMUM 5 key points
# - Include formula if topic has one
# - Include practical example
# - Write in clear Hindi-English mix
# - Be concise but complete

# EXAMPLE:

# Photosynthesis

# Definition: Photosynthesis is the process by which green plants convert light energy into chemical energy. This process takes place in chloroplasts and produces glucose and oxygen.

# Key Points:
# 1. Requires three main inputs: sunlight, water, and carbon dioxide
# 2. Takes place in chloroplasts containing green pigment chlorophyll
# 3. Occurs in two stages: light reactions and dark reactions (Calvin cycle)
# 4. Produces glucose (food) and releases oxygen as byproduct
# 5. Essential for all life on Earth as primary source of oxygen

# Formula/Equation: 6CO₂ + 6H₂O + Light Energy → C₆H₁₂O₆ + 6O₂

# Example: When a plant is kept in sunlight, its leaves absorb CO₂ from air and water from roots. Using sunlight energy, it makes glucose for growth and releases oxygen that we breathe.

# Now provide content for the student's question following this format:"""
        
#         # Build full prompt
#         full_prompt = system_prompt + f"\n\nStudent Question: {question}\n\nYour Response:"
        
#         # Get structured response
#         response = genai_client.models.generate_content(
#             model='gemini-2.5-flash',
#             contents=full_prompt
#         )
        
#         return response.text
    
#     @staticmethod
#     def text_to_speech(text: str, output_file: str = "temp/speech.mp3"):
#         """Convert text to speech - FREE with gTTS"""
        
#         # Try OpenAI first
#         if openai_available:
#             try:
#                 response = openai_client.audio.speech.create(
#                     model="tts-1",
#                     voice="alloy",
#                     input=text
#                 )
#                 response.stream_to_file(output_file)
#                 print(f"✅ Audio (OpenAI): {output_file}")
#                 return output_file
#             except Exception as e:
#                 print(f"⚠️ OpenAI TTS failed: {e}")
        
#         # Use gTTS
#         try:
#             from gtts import gTTS
#             tts = gTTS(text=text, lang='hi', slow=False)
#             tts.save(output_file)
#             print(f"✅ Audio (gTTS): {output_file}")
#             return output_file
#         except Exception as e:
#             print(f"⚠️ TTS Error: {e}")
#             return None
    
#     @staticmethod
#     def speech_to_text(audio_file_path: str, language: str = "hi"):
#         """Convert speech to text"""
        
#         if not openai_available:
#             return None
        
#         try:
#             with open(audio_file_path, 'rb') as audio_file:
#                 transcript = openai_client.audio.transcriptions.create(
#                     model="whisper-1",
#                     file=audio_file,
#                     language=language
#                 )
#             return transcript.text
#         except Exception as e:
#             print(f"⚠️ STT Error: {e}")
#             return None

















# import google.generativeai as genai
# from dotenv import load_dotenv 
# from gtts import gTTS
# import os
# import time
# import re

# class AIService:
#     def __init__(self):
#         genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#         self.model = genai.GenerativeModel('gemini-1.5-flash')
    
#     def generate_answer(self, question, subject="general"):
#         """Generate structured answer with EXAMPLES, FORMULAS, GRAPHS"""
        
#         prompt = f"""You are an expert teacher. Explain the following topic in a clear, structured way.

# TOPIC: {question}
# SUBJECT: {subject}

# STRICT FORMAT TO FOLLOW:

# [TOPIC NAME]
# Brief definition (2 sentences max)

# Key Concepts:
# 1. [First concept]
# 2. [Second concept]
# 3. [Third concept]

# Formula (if applicable):
# [Write the formula clearly]

# Derivation (if applicable):
# Step 1: [First step]
# Step 2: [Second step]
# Step 3: [Final step]

# EXAMPLE 1:
# Problem: [State a clear example problem]
# Solution:
# Step 1: [First step with calculation]
# Step 2: [Second step with calculation]
# Answer: [Final answer]

# EXAMPLE 2:
# Problem: [Another example]
# Solution:
# [Step by step solution]
# Answer: [Final answer]

# Real-World Application:
# [How is this used in real life?]

# IMPORTANT RULES:
# 1. ALWAYS include at least 2 worked examples with step-by-step solutions
# 2. For math topics: Show formula → derivation → numerical example
# 3. For science topics: Show concept → example → real-world use
# 4. Keep each point short (1-2 lines max)
# 5. Use simple English, avoid Hindi/Devanagari
# 6. Include numbers, calculations, and specific values
# 7. Make examples practical and easy to understand

# DO NOT USE:
# - No "Namaste", "Bahut accha", "Arre wah", "Chaliye" 
# - No greetings or filler words
# - No Hindi/Devanagari characters
# - No vague explanations

# START NOW:"""

#         try:
#             response = self.model.generate_content(prompt)
#             answer = response.text
            
#             # Clean answer
#             answer = self._clean_answer(answer)
            
#             print(f"✅ AI Answer generated ({len(answer)} chars)")
#             return answer
            
#         except Exception as e:
#             print(f"❌ AI Error: {e}")
#             raise
    
#     def _clean_answer(self, text):
#         """Remove unwanted characters"""
#         # Remove Hindi/Devanagari
#         text = re.sub(r'[\u0900-\u097F]+', '', text)
        
#         # Remove common Hindi phrases
#         hindi_phrases = ['Namaste', 'Bahut accha', 'Arre wah', 'Chaliye', 
#                         'Dekho', 'Acha', 'Theek hai']
#         for phrase in hindi_phrases:
#             text = text.replace(phrase, '')
        
#         # Clean extra whitespace
#         text = re.sub(r'\n\s*\n', '\n\n', text)
#         text = text.strip()
        
#         return text
    
#     def generate_audio(self, text, output_dir="temp/audio"):
#         """Generate audio from text"""
#         try:
#             os.makedirs(output_dir, exist_ok=True)
            
#             # Clean text for speech
#             clean_text = self._clean_answer(text)
            
#             # Generate audio
#             tts = gTTS(text=clean_text, lang='en', slow=False)
            
#             filename = f"lesson_{int(time.time())}.mp3"
#             filepath = os.path.join(output_dir, filename)
            
#             tts.save(filepath)
            
#             print(f"✅ Audio generated: {filepath}")
#             return filepath
            
#         except Exception as e:
#             print(f"❌ Audio generation error: {e}")
#             raise

# ai_service = AIService()











# from google import genai
# from google.genai import types
# from gtts import gTTS
# from dotenv import load_dotenv
# import os
# import time
# import re

# # ✅ Load .env file automatically
# load_dotenv()

# class AIService:
#     def __init__(self):
#         # ✅ Get API key with clear error message
#         api_key = os.getenv("GEMINI_API_KEY")
#         if not api_key:
#             raise ValueError(
#                 "❌ GEMINI_API_KEY not found!\n"
#                 "➡️  Create a .env file in your backend folder with:\n"
#                 "    GEMINI_API_KEY=your_key_here\n"
#                 "➡️  Get your key from: https://aistudio.google.com/app/apikey"
#             )

#         # ✅ New google-genai client (not deprecated)
#         self.client = genai.Client(api_key=api_key)
#         self.model = "gemini-2.0-flash"

#         print("✅ AIService initialized successfully")

#     # ─────────────────────────────────────────────
#     # MAIN: Generate Answer
#     # ─────────────────────────────────────────────
#     def generate_answer(self, question: str, subject: str = "general") -> str:
#         """Generate structured answer with examples, formulas, steps"""

#         prompt = f"""You are an expert teacher. Explain the following topic clearly and structurally.

# TOPIC: {question}
# SUBJECT: {subject}

# STRICT FORMAT TO FOLLOW:

# [TOPIC NAME]
# Brief definition (2 sentences max)

# Key Concepts:
# 1. [First concept]
# 2. [Second concept]
# 3. [Third concept]

# Formula (if applicable):
# [Write the formula clearly]

# Derivation (if applicable):
# Step 1: [First step]
# Step 2: [Second step]
# Step 3: [Final step]

# EXAMPLE 1:
# Problem: [State a clear example problem]
# Solution:
# Step 1: [First step with calculation]
# Step 2: [Second step with calculation]
# Answer: [Final answer]

# EXAMPLE 2:
# Problem: [Another example]
# Solution:
# [Step by step solution]
# Answer: [Final answer]

# Real-World Application:
# [How is this used in real life?]

# IMPORTANT RULES:
# 1. ALWAYS include at least 2 worked examples with step-by-step solutions
# 2. For math topics: Show formula → derivation → numerical example
# 3. For science topics: Show concept → example → real-world use
# 4. Keep each point short (1-2 lines max)
# 5. Use simple English only
# 6. Include numbers, calculations, and specific values
# 7. Make examples practical and easy to understand

# DO NOT USE:
# - No greetings or filler words
# - No Hindi/Devanagari characters
# - No vague explanations

# START NOW:"""

#         try:
#             response = self.client.models.generate_content(
#                 model=self.model,
#                 contents=prompt,
#             )

#             answer = response.text
#             answer = self._clean_answer(answer)

#             print(f"✅ AI Answer generated ({len(answer)} chars)")
#             return answer

#         except Exception as e:
#             print(f"❌ AI Error: {e}")
#             raise RuntimeError(f"Failed to generate answer: {e}") from e

#     # ─────────────────────────────────────────────
#     # Generate answer with custom system instruction
#     # ─────────────────────────────────────────────
#     def generate_answer_with_system(
#         self, question: str, subject: str = "general", system_instruction: str = None
#     ) -> str:
#         """Generate answer with optional system instruction"""

#         if system_instruction is None:
#             system_instruction = (
#                 "You are an expert teacher who explains topics clearly, "
#                 "with examples and step-by-step solutions. Use simple English only."
#             )

#         user_prompt = f"Explain this topic clearly:\n\nTOPIC: {question}\nSUBJECT: {subject}"

#         try:
#             response = self.client.models.generate_content(
#                 model=self.model,
#                 contents=user_prompt,
#                 config=types.GenerateContentConfig(
#                     system_instruction=system_instruction,
#                     max_output_tokens=2048,
#                     temperature=0.7,
#                 ),
#             )

#             answer = response.text
#             answer = self._clean_answer(answer)

#             print(f"✅ AI Answer (with system) generated ({len(answer)} chars)")
#             return answer

#         except Exception as e:
#             print(f"❌ AI Error (system): {e}")
#             raise RuntimeError(f"Failed to generate answer: {e}") from e

#     # ─────────────────────────────────────────────
#     # Generate Quiz Questions
#     # ─────────────────────────────────────────────
#     def generate_quiz(self, topic: str, num_questions: int = 5) -> list[dict]:
#         """Generate MCQ quiz questions for a topic"""

#         prompt = f"""Generate {num_questions} multiple choice questions about: {topic}

# Return ONLY this exact format for each question, nothing else:

# Q1: [Question text]
# A) [Option A]
# B) [Option B]
# C) [Option C]
# D) [Option D]
# Answer: [A/B/C/D]
# Explanation: [Why this answer is correct]

# Q2: ...and so on"""

#         try:
#             response = self.client.models.generate_content(
#                 model=self.model,
#                 contents=prompt,
#             )

#             raw = response.text
#             questions = self._parse_quiz(raw)

#             print(f"✅ Quiz generated: {len(questions)} questions")
#             return questions

#         except Exception as e:
#             print(f"❌ Quiz generation error: {e}")
#             raise RuntimeError(f"Failed to generate quiz: {e}") from e

#     def _parse_quiz(self, raw_text: str) -> list[dict]:
#         """Parse raw quiz text into structured list"""
#         questions = []
#         blocks = re.split(r'\nQ\d+:', '\n' + raw_text)

#         for block in blocks:
#             block = block.strip()
#             if not block:
#                 continue
#             try:
#                 lines = block.split('\n')
#                 question_text = lines[0].strip()
#                 options = {}
#                 answer = ""
#                 explanation = ""

#                 for line in lines[1:]:
#                     line = line.strip()
#                     if line.startswith('A)'):
#                         options['A'] = line[2:].strip()
#                     elif line.startswith('B)'):
#                         options['B'] = line[2:].strip()
#                     elif line.startswith('C)'):
#                         options['C'] = line[2:].strip()
#                     elif line.startswith('D)'):
#                         options['D'] = line[2:].strip()
#                     elif line.startswith('Answer:'):
#                         answer = line.replace('Answer:', '').strip()
#                     elif line.startswith('Explanation:'):
#                         explanation = line.replace('Explanation:', '').strip()

#                 if question_text and options and answer:
#                     questions.append({
#                         "question": question_text,
#                         "options": options,
#                         "answer": answer,
#                         "explanation": explanation,
#                     })
#             except Exception:
#                 continue  # Skip malformed blocks

#         return questions

#     # ─────────────────────────────────────────────
#     # Generate Audio (Text-to-Speech)
#     # ─────────────────────────────────────────────
#     def generate_audio(self, text: str, output_dir: str = "temp/audio") -> str:
#         """Convert text to speech and save as MP3"""
#         try:
#             os.makedirs(output_dir, exist_ok=True)

#             clean_text = self._clean_answer(text)

#             # Limit text length for gTTS (avoids timeout on huge texts)
#             if len(clean_text) > 3000:
#                 clean_text = clean_text[:3000] + "..."

#             tts = gTTS(text=clean_text, lang='en', slow=False)

#             filename = f"lesson_{int(time.time())}.mp3"
#             filepath = os.path.join(output_dir, filename)

#             tts.save(filepath)

#             print(f"✅ Audio generated: {filepath}")
#             return filepath

#         except Exception as e:
#             print(f"❌ Audio generation error: {e}")
#             raise RuntimeError(f"Failed to generate audio: {e}") from e

#     # ─────────────────────────────────────────────
#     # Clean Text Helper
#     # ─────────────────────────────────────────────
#     def _clean_answer(self, text: str) -> str:
#         """Remove Hindi characters, filler words, extra whitespace"""

#         # Remove Hindi/Devanagari script
#         text = re.sub(r'[\u0900-\u097F]+', '', text)

#         # Remove common unwanted phrases
#         filler_phrases = [
#             'Namaste', 'Bahut accha', 'Arre wah', 'Chaliye',
#             'Dekho', 'Acha', 'Theek hai', 'Bilkul', 'Haan',
#         ]
#         for phrase in filler_phrases:
#             text = text.replace(phrase, '')

#         # Collapse multiple blank lines into one
#         text = re.sub(r'\n{3,}', '\n\n', text)

#         # Remove leading/trailing whitespace
#         text = text.strip()

#         return text

#     # ─────────────────────────────────────────────
#     # Health Check
#     # ─────────────────────────────────────────────
#     def health_check(self) -> dict:
#         """Quick check that the API is working"""
#         try:
#             response = self.client.models.generate_content(
#                 model=self.model,
#                 contents="Say 'OK' and nothing else.",
#             )
#             return {"status": "ok", "response": response.text.strip()}
#         except Exception as e:
#             return {"status": "error", "error": str(e)}
        


    


# # ─────────────────────────────────────────────
# # Singleton instance
# # ─────────────────────────────────────────────
# ai_service = AIService()




























# from google import genai
# from google.genai import types
# from gtts import gTTS
# from dotenv import load_dotenv
# import os
# import time
# import re

# # ✅ Load .env file automatically
# load_dotenv()


# class AIService:
#     def __init__(self):
#         api_key = os.getenv("GEMINI_API_KEY")
#         if not api_key:
#             raise ValueError(
#                 "❌ GEMINI_API_KEY not found!\n"
#                 "➡️  Create a .env file in your backend folder with:\n"
#                 "    GEMINI_API_KEY=your_key_here\n"
#                 "➡️  Get your key from: https://aistudio.google.com/app/apikey"
#             )

#         self.client = genai.Client(api_key=api_key)
#         self.model = "gemini-2.0-flash-lite"
#         print("✅ AIService initialized successfully")

#     # ─────────────────────────────────────────────
#     # MAIN: Generate Answer
#     # ─────────────────────────────────────────────
#     def generate_answer(self, question: str, subject: str = "general") -> str:
#         """Generate structured answer with examples, formulas, steps"""

#         prompt = f"""You are an expert teacher. Explain the following topic clearly and structurally.

# TOPIC: {question}
# SUBJECT: {subject}

# STRICT FORMAT TO FOLLOW:

# [TOPIC NAME]
# Brief definition (2 sentences max)

# Key Concepts:
# 1. [First concept]
# 2. [Second concept]
# 3. [Third concept]

# Formula (if applicable):
# [Write the formula clearly]

# Derivation (if applicable):
# Step 1: [First step]
# Step 2: [Second step]
# Step 3: [Final step]

# EXAMPLE 1:
# Problem: [State a clear example problem]
# Solution:
# Step 1: [First step with calculation]
# Step 2: [Second step with calculation]
# Answer: [Final answer]

# EXAMPLE 2:
# Problem: [Another example]
# Solution:
# [Step by step solution]
# Answer: [Final answer]

# Real-World Application:
# [How is this used in real life?]

# IMPORTANT RULES:
# 1. ALWAYS include at least 2 worked examples with step-by-step solutions
# 2. For math topics: Show formula -> derivation -> numerical example
# 3. For science topics: Show concept -> example -> real-world use
# 4. Keep each point short (1-2 lines max)
# 5. Use simple English only
# 6. Include numbers, calculations, and specific values
# 7. Make examples practical and easy to understand

# DO NOT USE:
# - No greetings or filler words
# - No Hindi/Devanagari characters
# - No vague explanations

# START NOW:"""

#         try:
#             response = self.client.models.generate_content(
#                 model=self.model,
#                 contents=prompt,
#             )
#             answer = self._clean_answer(response.text)
#             print(f"✅ AI Answer generated ({len(answer)} chars)")
#             return answer

#         except Exception as e:
#             print(f"❌ AI Error: {e}")
#             raise RuntimeError(f"Failed to generate answer: {e}") from e

#     # ─────────────────────────────────────────────
#     # Generate Answer with System Instruction
#     # ─────────────────────────────────────────────
#     def generate_answer_with_system(
#         self, question: str, subject: str = "general", system_instruction: str = None
#     ) -> str:
#         """Generate answer with optional system instruction"""

#         if system_instruction is None:
#             system_instruction = (
#                 "You are an expert teacher who explains topics clearly, "
#                 "with examples and step-by-step solutions. Use simple English only."
#             )

#         user_prompt = f"Explain this topic clearly:\n\nTOPIC: {question}\nSUBJECT: {subject}"

#         try:
#             response = self.client.models.generate_content(
#                 model=self.model,
#                 contents=user_prompt,
#                 config=types.GenerateContentConfig(
#                     system_instruction=system_instruction,
#                     max_output_tokens=2048,
#                     temperature=0.7,
#                 ),
#             )
#             answer = self._clean_answer(response.text)
#             print(f"✅ AI Answer (with system) generated ({len(answer)} chars)")
#             return answer

#         except Exception as e:
#             print(f"❌ AI Error (system): {e}")
#             raise RuntimeError(f"Failed to generate answer: {e}") from e

#     # ─────────────────────────────────────────────
#     # Text to Speech (used by main.py)
#     # ─────────────────────────────────────────────
#     def text_to_speech(self, text: str, output_path: str) -> str:
#         """Convert text to speech and save to specific path"""
#         try:
#             output_dir = os.path.dirname(output_path)
#             if output_dir:
#                 os.makedirs(output_dir, exist_ok=True)

#             clean_text = self._clean_answer(text)

#             if len(clean_text) > 3000:
#                 clean_text = clean_text[:3000] + "..."

#             tts = gTTS(text=clean_text, lang='en', slow=False)
#             tts.save(output_path)

#             print(f"✅ Audio saved: {output_path}")
#             return output_path

#         except Exception as e:
#             print(f"❌ TTS error: {e}")
#             raise RuntimeError(f"Failed to generate audio: {e}") from e

#     # ─────────────────────────────────────────────
#     # Generate Audio (alternate method)
#     # ─────────────────────────────────────────────
#     def generate_audio(self, text: str, output_dir: str = "temp/audio") -> str:
#         """Convert text to speech and save in output_dir"""
#         try:
#             os.makedirs(output_dir, exist_ok=True)

#             clean_text = self._clean_answer(text)

#             if len(clean_text) > 3000:
#                 clean_text = clean_text[:3000] + "..."

#             tts = gTTS(text=clean_text, lang='en', slow=False)

#             filename = f"lesson_{int(time.time())}.mp3"
#             filepath = os.path.join(output_dir, filename)
#             tts.save(filepath)

#             print(f"✅ Audio generated: {filepath}")
#             return filepath

#         except Exception as e:
#             print(f"❌ Audio generation error: {e}")
#             raise RuntimeError(f"Failed to generate audio: {e}") from e

#     # ─────────────────────────────────────────────
#     # Speech to Text
#     # ─────────────────────────────────────────────
#     def speech_to_text(self, audio_path: str, language: str = "en") -> str:
#         """Transcribe audio to text"""
#         # Placeholder — integrate Whisper if needed
#         return "Transcription not available"

#     # ─────────────────────────────────────────────
#     # Teaching Response (for doubts/interruptions)
#     # ─────────────────────────────────────────────
#     def get_teaching_response(
#         self, question: str, conversation_history: list, subject: str = "general"
#     ) -> str:
#         """Generate teaching response with conversation context"""

#         history_text = ""
#         for msg in conversation_history[-5:]:
#             role = "Student" if msg.get("role") == "user" else "Teacher"
#             history_text += f"{role}: {msg.get('content', '')}\n"

#         prompt = f"""You are an expert teacher. Answer this student doubt clearly.

# Previous conversation:
# {history_text}

# Student's doubt: {question}
# Subject: {subject}

# Give a clear, concise answer in 3-5 sentences."""

#         try:
#             response = self.client.models.generate_content(
#                 model=self.model,
#                 contents=prompt,
#             )
#             return self._clean_answer(response.text)

#         except Exception as e:
#             raise RuntimeError(f"Failed to get teaching response: {e}") from e

#     # ─────────────────────────────────────────────
#     # Generate Quiz
#     # ─────────────────────────────────────────────
#     def generate_quiz(self, topic: str, num_questions: int = 5) -> list:
#         """Generate MCQ quiz questions for a topic"""

#         prompt = f"""Generate {num_questions} multiple choice questions about: {topic}

# Return ONLY this exact format for each question, nothing else:

# Q1: [Question text]
# A) [Option A]
# B) [Option B]
# C) [Option C]
# D) [Option D]
# Answer: [A/B/C/D]
# Explanation: [Why this answer is correct]

# Q2: ...and so on"""

#         try:
#             response = self.client.models.generate_content(
#                 model=self.model,
#                 contents=prompt,
#             )
#             questions = self._parse_quiz(response.text)
#             print(f"✅ Quiz generated: {len(questions)} questions")
#             return questions

#         except Exception as e:
#             print(f"❌ Quiz generation error: {e}")
#             raise RuntimeError(f"Failed to generate quiz: {e}") from e

#     def _parse_quiz(self, raw_text: str) -> list:
#         """Parse raw quiz text into structured list"""
#         questions = []
#         blocks = re.split(r'\nQ\d+:', '\n' + raw_text)

#         for block in blocks:
#             block = block.strip()
#             if not block:
#                 continue
#             try:
#                 lines = block.split('\n')
#                 question_text = lines[0].strip()
#                 options = {}
#                 answer = ""
#                 explanation = ""

#                 for line in lines[1:]:
#                     line = line.strip()
#                     if line.startswith('A)'):
#                         options['A'] = line[2:].strip()
#                     elif line.startswith('B)'):
#                         options['B'] = line[2:].strip()
#                     elif line.startswith('C)'):
#                         options['C'] = line[2:].strip()
#                     elif line.startswith('D)'):
#                         options['D'] = line[2:].strip()
#                     elif line.startswith('Answer:'):
#                         answer = line.replace('Answer:', '').strip()
#                     elif line.startswith('Explanation:'):
#                         explanation = line.replace('Explanation:', '').strip()

#                 if question_text and options and answer:
#                     questions.append({
#                         "question": question_text,
#                         "options": options,
#                         "answer": answer,
#                         "explanation": explanation,
#                     })
#             except Exception:
#                 continue

#         return questions

#     # ─────────────────────────────────────────────
#     # Clean Text Helper
#     # ─────────────────────────────────────────────
#     def _clean_answer(self, text: str) -> str:
#         """Remove Hindi characters, filler words, extra whitespace"""

#         text = re.sub(r'[\u0900-\u097F]+', '', text)

#         filler_phrases = [
#             'Namaste', 'Bahut accha', 'Arre wah', 'Chaliye',
#             'Dekho', 'Acha', 'Theek hai', 'Bilkul', 'Haan',
#         ]
#         for phrase in filler_phrases:
#             text = text.replace(phrase, '')

#         text = re.sub(r'\n{3,}', '\n\n', text)
#         text = text.strip()

#         return text

#     # ─────────────────────────────────────────────
#     # Health Check
#     # ─────────────────────────────────────────────
#     def health_check(self) -> dict:
#         """Quick check that the API is working"""
#         try:
#             response = self.client.models.generate_content(
#                 model=self.model,
#                 contents="Say 'OK' and nothing else.",
#             )
#             return {"status": "ok", "response": response.text.strip()}
#         except Exception as e:
#             return {"status": "error", "error": str(e)}


# # ─────────────────────────────────────────────
# # Singleton instance
# # ─────────────────────────────────────────────
# ai_service = AIService()













from groq import Groq
from gtts import gTTS
from dotenv import load_dotenv
import os
import time
import re

# ✅ Load .env file automatically
load_dotenv()


class AIService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ GROQ_API_KEY not found!\n"
                "➡️  Create a .env file in your backend folder with:\n"
                "    GROQ_API_KEY=your_key_here\n"
                "➡️  Get your key from: https://console.groq.com/keys"
            )

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"  # Free + very powerful
        print("✅ AIService initialized successfully (Groq)")

    # ─────────────────────────────────────────────
    # Helper: Call Groq API
    # ─────────────────────────────────────────────
    def _call_groq(self, prompt: str, max_tokens: int = 2048) -> str:
        """Internal helper to call Groq API"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content

    # ─────────────────────────────────────────────
    # MAIN: Generate Answer
    # ─────────────────────────────────────────────
    def generate_answer(self, question: str, subject: str = "general") -> str:
        """Generate structured answer with examples, formulas, steps"""

        prompt = f"""You are an expert teacher. Explain the following topic clearly and structurally.

TOPIC: {question}
SUBJECT: {subject}

STRICT FORMAT TO FOLLOW:

[TOPIC NAME]
Brief definition (2 sentences max)

Key Concepts:
1. [First concept]
2. [Second concept]
3. [Third concept]

Formula (if applicable):
[Write the formula clearly]

Derivation (if applicable):
Step 1: [First step]
Step 2: [Second step]
Step 3: [Final step]

EXAMPLE 1:
Problem: [State a clear example problem]
Solution:
Step 1: [First step with calculation]
Step 2: [Second step with calculation]
Answer: [Final answer]

EXAMPLE 2:
Problem: [Another example]
Solution:
[Step by step solution]
Answer: [Final answer]

Real-World Application:
[How is this used in real life?]

IMPORTANT RULES:
1. ALWAYS include at least 2 worked examples with step-by-step solutions
2. For math topics: Show formula -> derivation -> numerical example
3. For science topics: Show concept -> example -> real-world use
4. Keep each point short (1-2 lines max)
5. Use simple English only
6. Include numbers, calculations, and specific values
7. Make examples practical and easy to understand

DO NOT USE:
- No greetings or filler words
- No Hindi/Devanagari characters
- No vague explanations

START NOW:"""

        try:
            answer = self._call_groq(prompt)
            answer = self._clean_answer(answer)
            print(f"✅ AI Answer generated ({len(answer)} chars)")
            return answer

        except Exception as e:
            print(f"❌ AI Error: {e}")
            raise RuntimeError(f"Failed to generate answer: {e}") from e

    # ─────────────────────────────────────────────
    # Generate Answer with System Instruction
    # ─────────────────────────────────────────────
    def generate_answer_with_system(
        self, question: str, subject: str = "general", system_instruction: str = None
    ) -> str:
        """Generate answer with optional system instruction"""

        if system_instruction is None:
            system_instruction = (
                "You are an expert teacher who explains topics clearly, "
                "with examples and step-by-step solutions. Use simple English only."
            )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"Explain this topic clearly:\n\nTOPIC: {question}\nSUBJECT: {subject}"}
                ],
                max_tokens=2048,
                temperature=0.7,
            )
            answer = self._clean_answer(response.choices[0].message.content)
            print(f"✅ AI Answer (with system) generated ({len(answer)} chars)")
            return answer

        except Exception as e:
            print(f"❌ AI Error (system): {e}")
            raise RuntimeError(f"Failed to generate answer: {e}") from e

    # ─────────────────────────────────────────────
    # Text to Speech (used by main.py)
    # ─────────────────────────────────────────────
    def text_to_speech(self, text: str, output_path: str) -> str:
        """Convert text to speech and save to specific path"""
        try:
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            clean_text = self._clean_answer(text)

            if len(clean_text) > 3000:
                clean_text = clean_text[:3000] + "..."

            tts = gTTS(text=clean_text, lang='en', slow=False)
            tts.save(output_path)

            print(f"✅ Audio saved: {output_path}")
            return output_path

        except Exception as e:
            print(f"❌ TTS error: {e}")
            raise RuntimeError(f"Failed to generate audio: {e}") from e

    # ─────────────────────────────────────────────
    # Generate Audio (alternate method)
    # ─────────────────────────────────────────────
    def generate_audio(self, text: str, output_dir: str = "temp/audio") -> str:
        """Convert text to speech and save in output_dir"""
        try:
            os.makedirs(output_dir, exist_ok=True)

            clean_text = self._clean_answer(text)

            if len(clean_text) > 3000:
                clean_text = clean_text[:3000] + "..."

            tts = gTTS(text=clean_text, lang='en', slow=False)

            filename = f"lesson_{int(time.time())}.mp3"
            filepath = os.path.join(output_dir, filename)
            tts.save(filepath)

            print(f"✅ Audio generated: {filepath}")
            return filepath

        except Exception as e:
            print(f"❌ Audio generation error: {e}")
            raise RuntimeError(f"Failed to generate audio: {e}") from e

    # ─────────────────────────────────────────────
    # Speech to Text
    # ─────────────────────────────────────────────
    def speech_to_text(self, audio_path: str, language: str = "en") -> str:
        """Transcribe audio to text"""
        return "Transcription not available"

    # ─────────────────────────────────────────────
    # Teaching Response (for doubts/interruptions)
    # ─────────────────────────────────────────────
    def get_teaching_response(
        self, question: str, conversation_history: list, subject: str = "general"
    ) -> str:
        """Generate teaching response with conversation context"""

        messages = [
            {
                "role": "system",
                "content": "You are an expert teacher. Answer student doubts clearly in 3-5 sentences. Use simple English only."
            }
        ]

        # Add last 5 messages for context
        for msg in conversation_history[-5:]:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        # Add current question
        messages.append({
            "role": "user",
            "content": f"Student's doubt: {question}\nSubject: {subject}"
        })

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=512,
                temperature=0.7,
            )
            return self._clean_answer(response.choices[0].message.content)

        except Exception as e:
            raise RuntimeError(f"Failed to get teaching response: {e}") from e

    # ─────────────────────────────────────────────
    # Generate Quiz
    # ─────────────────────────────────────────────
    def generate_quiz(self, topic: str, num_questions: int = 5) -> list:
        """Generate MCQ quiz questions for a topic"""

        prompt = f"""Generate {num_questions} multiple choice questions about: {topic}

Return ONLY this exact format for each question, nothing else:

Q1: [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Answer: [A/B/C/D]
Explanation: [Why this answer is correct]

Q2: ...and so on"""

        try:
            raw = self._call_groq(prompt)
            questions = self._parse_quiz(raw)
            print(f"✅ Quiz generated: {len(questions)} questions")
            return questions

        except Exception as e:
            print(f"❌ Quiz generation error: {e}")
            raise RuntimeError(f"Failed to generate quiz: {e}") from e

    def _parse_quiz(self, raw_text: str) -> list:
        """Parse raw quiz text into structured list"""
        questions = []
        blocks = re.split(r'\nQ\d+:', '\n' + raw_text)

        for block in blocks:
            block = block.strip()
            if not block:
                continue
            try:
                lines = block.split('\n')
                question_text = lines[0].strip()
                options = {}
                answer = ""
                explanation = ""

                for line in lines[1:]:
                    line = line.strip()
                    if line.startswith('A)'):
                        options['A'] = line[2:].strip()
                    elif line.startswith('B)'):
                        options['B'] = line[2:].strip()
                    elif line.startswith('C)'):
                        options['C'] = line[2:].strip()
                    elif line.startswith('D)'):
                        options['D'] = line[2:].strip()
                    elif line.startswith('Answer:'):
                        answer = line.replace('Answer:', '').strip()
                    elif line.startswith('Explanation:'):
                        explanation = line.replace('Explanation:', '').strip()

                if question_text and options and answer:
                    questions.append({
                        "question": question_text,
                        "options": options,
                        "answer": answer,
                        "explanation": explanation,
                    })
            except Exception:
                continue

        return questions

    # ─────────────────────────────────────────────
    # Clean Text Helper
    # ─────────────────────────────────────────────
    def _clean_answer(self, text: str) -> str:
        """Remove Hindi characters, filler words, extra whitespace"""

        text = re.sub(r'[\u0900-\u097F]+', '', text)

        filler_phrases = [
            'Namaste', 'Bahut accha', 'Arre wah', 'Chaliye',
            'Dekho', 'Acha', 'Theek hai', 'Bilkul', 'Haan',
        ]
        for phrase in filler_phrases:
            text = text.replace(phrase, '')

        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()

        return text

    # ─────────────────────────────────────────────
    # Health Check
    # ─────────────────────────────────────────────
    def health_check(self) -> dict:
        """Quick check that the API is working"""
        try:
            result = self._call_groq("Say 'OK' and nothing else.", max_tokens=10)
            return {"status": "ok", "response": result.strip()}
        except Exception as e:
            return {"status": "error", "error": str(e)}


# ─────────────────────────────────────────────
# Singleton instance
# ─────────────────────────────────────────────
ai_service = AIService()