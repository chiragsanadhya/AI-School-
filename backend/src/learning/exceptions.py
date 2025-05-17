class LearningError(Exception):
    """Base exception for learning module."""
    pass

class PDFProcessingError(LearningError):
    pass

class EmbeddingError(LearningError):
    pass

class NarrationError(LearningError):
    pass

class RAGError(LearningError):
    pass

class TestGenerationError(LearningError):
    pass
