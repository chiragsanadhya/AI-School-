from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres.riehvfvowzyqkuvgcvgy:piqxix-xamze8-kohwiD@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
