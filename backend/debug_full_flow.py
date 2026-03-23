from services.ai_service import AIService
from services.avatar_service import AvatarService
import os

print("="*50)
print("TESTING COMPLETE FLOW")
print("="*50)

# Test 1: AI Response
print("\n1️⃣ Testing AI Response...")
ai_service = AIService()
answer = ai_service.get_teaching_response(
    question="What is photosynthesis?",
    conversation_history=[],
    subject="science"
)
print(f"✅ AI Answer: {answer[:100]}...")

# Test 2: Audio
print("\n2️⃣ Testing Audio (gTTS)...")
os.makedirs("temp", exist_ok=True)
audio_file = ai_service.text_to_speech(answer, "temp/test_audio.mp3")
if audio_file:
    print(f"✅ Audio generated: {audio_file}")
else:
    print("❌ Audio failed")

# Test 3: Video
print("\n3️⃣ Testing Video (D-ID)...")
avatar_service = AvatarService()
video_url = avatar_service.create_talking_video(answer[:200])  # Short text
if video_url:
    print(f"✅ Video URL: {video_url}")
    print("\n📺 OPEN THIS URL IN BROWSER:")
    print(video_url)
else:
    print("❌ Video failed")

print("\n" + "="*50)
print("TEST COMPLETE")
print("="*50)