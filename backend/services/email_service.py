import os

class EmailService:
    
    @staticmethod
    def send_verification_email(email: str, token: str, username: str):
        """Send verification email (development mode - prints to console)"""
        
        verification_link = f"http://localhost:5173/verify-email?token={token}"
        
        print(f"""
╔════════════════════════════════════════════════════════════════╗
║                    📧 EMAIL VERIFICATION                       ║
╠════════════════════════════════════════════════════════════════╣
║  To: {email:<57} ║
║  Username: {username:<51} ║
║                                                                ║
║  Click to verify:                                              ║
║  {verification_link:<59} ║
║                                                                ║
║  (In production, this will be sent via email service)         ║
╚════════════════════════════════════════════════════════════════╝
        """)
        
        return True
    
    @staticmethod
    def send_password_reset_email(email: str, token: str):
        """Send password reset email"""
        
        reset_link = f"http://localhost:5173/reset-password?token={token}"
        
        print(f"""
╔════════════════════════════════════════════════════════════════╗
║                    🔐 PASSWORD RESET                           ║
╠════════════════════════════════════════════════════════════════╣
║  To: {email:<57} ║
║                                                                ║
║  Click to reset password:                                      ║
║  {reset_link:<59} ║
╚════════════════════════════════════════════════════════════════╝
        """)
        
        return True


email_service = EmailService()