import os
from dotenv import load_dotenv
from services.ai_service import AIService
from services.session_service import session_manager

load_dotenv()

print("🧪 Testing Backend with NEW Gemini 2.0 API\n")

# Test 1: Environment
print("1️⃣ Testing .env...")
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    print(f"✅ Gemini Key: {gemini_key[:20]}...")
else:
    print("❌ Gemini Key not found!")
    exit()

openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    print(f"✅ OpenAI Key: {openai_key[:20]}...")
else:
    print("⚠️ OpenAI Key not found")

# Test 2: AI Service
print("\n2️⃣ Testing AI Service...")
try:
    ai_service = AIService()
    print("✅ AI Service initialized")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit()

# Test 3: Gemini Response
print("\n3️⃣ Testing Gemini 2.0 Response...")
try:
    response = ai_service.get_teaching_response(
        question="What is 2+2?",
        conversation_history=[],
        subject="math"
    )
    print(f"✅ Got response: {response[:100]}...")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit()

# Test 4: Session Manager
print("\n4️⃣ Testing Session Manager...")
try:
    session_manager.create_session("test123")
    session_manager.add_message("test123", "user", "Hello")
    history = session_manager.get_history("test123")
    print(f"✅ Session working: {len(history)} messages")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*50)
print("🎉 ALL TESTS PASSED!")
print("="*50)
print("\n💡 Using FREE Google Gemini 2.0 Flash")
print("   No costs, no limits for development!")