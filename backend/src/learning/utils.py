import os
from pathlib import Path

def ensure_dir(path: str | Path):
    """Ensure a directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)


def safe_remove(path: str | Path):
    """Remove a file if it exists."""
    try:
        os.remove(path)
    except FileNotFoundError:
        pass

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_service_role_key
