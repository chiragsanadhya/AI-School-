from src.core.auth import supabase
from src.core.config import settings
from datetime import timedelta

class AuthService:
    def __init__(self):
        self.supabase = supabase

    async def signup(self, email: str, password: str, full_name: str):
        return await self.supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "full_name": full_name
                }
            }
        })

    async def login(self, email: str, password: str):
        return await self.supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

    async def verify_email(self, token: str):
        return await self.supabase.auth.verify_email(token)