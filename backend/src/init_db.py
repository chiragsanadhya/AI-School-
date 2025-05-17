import logging
from sqlalchemy import text
from .database import engine, Base, init_db
from .models import User, Chapter, DocumentEmbedding, LearningProgress
from .exceptions import DatabaseError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_vector_index():
    """Create vector similarity search index."""
    try:
        with engine.connect() as conn:
            # Create vector similarity search index
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_document_embeddings_vector 
                ON document_embeddings 
                USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100);
            """))
            conn.commit()
            logger.info("Vector similarity search index created successfully")
    except Exception as e:
        logger.error(f"Error creating vector index: {str(e)}")
        raise DatabaseError(f"Failed to create vector index: {str(e)}")

def create_updated_at_trigger():
    """Create trigger function for updating timestamps."""
    try:
        with engine.connect() as conn:
            # Create updated_at trigger function
            conn.execute(text("""
                CREATE OR REPLACE FUNCTION update_updated_at_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = NOW();
                    RETURN NEW;
                END;
                $$ language 'plpgsql';
            """))
            
            # Add updated_at triggers to tables
            tables = ['users', 'chapters', 'learning_progress']
            for table in tables:
                conn.execute(text(f"""
                    DROP TRIGGER IF EXISTS update_{table}_updated_at ON {table};
                    CREATE TRIGGER update_{table}_updated_at
                        BEFORE UPDATE ON {table}
                        FOR EACH ROW
                        EXECUTE FUNCTION update_updated_at_column();
                """))
            
            conn.commit()
            logger.info("Updated at triggers created successfully")
    except Exception as e:
        logger.error(f"Error creating updated_at triggers: {str(e)}")
        raise DatabaseError(f"Failed to create updated_at triggers: {str(e)}")

def create_indexes():
    """Create additional indexes for better performance."""
    try:
        with engine.connect() as conn:
            # Create indexes
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
                CREATE INDEX IF NOT EXISTS idx_chapters_title ON chapters(title);
                CREATE INDEX IF NOT EXISTS idx_document_embeddings_chapter_id ON document_embeddings(chapter_id);
                CREATE INDEX IF NOT EXISTS idx_learning_progress_user_id ON learning_progress(user_id);
                CREATE INDEX IF NOT EXISTS idx_learning_progress_chapter_id ON learning_progress(chapter_id);
            """))
            conn.commit()
            logger.info("Additional indexes created successfully")
    except Exception as e:
        logger.error(f"Error creating indexes: {str(e)}")
        raise DatabaseError(f"Failed to create indexes: {str(e)}")

def initialize_database():
    """Initialize the database with all necessary components."""
    try:
        logger.info("Starting database initialization...")
        
        # Initialize base tables and extensions
        init_db()
        
        # Create vector index
        create_vector_index()
        
        # Create updated_at triggers
        create_updated_at_trigger()
        
        # Create additional indexes
        create_indexes()
        
        logger.info("Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise DatabaseError(f"Database initialization failed: {str(e)}")

if __name__ == "__main__":
    initialize_database() 