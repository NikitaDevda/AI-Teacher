from services.avatar_service import AvatarService

avatar = AvatarService()

print("🎬 Testing video generation...")
video_url = avatar.create_talking_video(
    "Hello student! Main tumhari AI teacher hoon. Aaj kya seekhna hai?"
)

if video_url:
    print(f"\n✅ VIDEO GENERATED!")
    print(f"🔗 URL: {video_url}")
    print(f"\n📺 Browser mein open karo ye URL:")
    print(video_url)
else:
    print("❌ Video generation failed")