class AppException(Exception):
    """Base exception for the application."""
    pass

class DatabaseError(AppException):
    """Database related errors."""
    pass

class VectorDBError(DatabaseError):
    """Vector database specific errors."""
    pass

class AuthenticationError(AppException):
    """Authentication related errors."""
    pass

class ValidationError(AppException):
    """Data validation errors."""
    pass

class FileProcessingError(AppException):
    """File processing related errors."""
    pass

class LearningError(AppException):
    """Learning module specific errors."""
    pass

class PDFProcessingError(LearningError):
    """PDF processing specific errors."""
    pass

class EmbeddingError(LearningError):
    """Embedding generation errors."""
    pass

class NarrationError(LearningError):
    """Text-to-speech and narration errors."""
    pass

class RAGError(LearningError):
    """RAG (Retrieval-Augmented Generation) errors."""
    pass

class TestGenerationError(LearningError):
    """Test generation errors."""
    pass
