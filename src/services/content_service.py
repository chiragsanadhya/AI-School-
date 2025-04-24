from src.core.auth import supabase

class ContentService:
    def __init__(self):
        self.supabase = supabase

    async def get_subjects(self):
        response = await self.supabase.table('subjects').select('*').execute()
        return response.data

    async def get_chapters(self, subject_id: str):
        response = await self.supabase.table('chapters')\
            .select('*')\
            .eq('subject_id', subject_id)\
            .execute()
        return response.data

    async def get_chapter_content(self, chapter_id: str):
        response = await self.supabase.table('chapter_content')\
            .select('*')\
            .eq('chapter_id', chapter_id)\
            .single()\
            .execute()
        return response.data