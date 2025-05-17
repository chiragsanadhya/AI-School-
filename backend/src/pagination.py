from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')

class PageInfo(BaseModel):
    """Pagination metadata."""
    total: int
    page: int
    size: int
    pages: int

class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response model."""
    items: List[T]
    page_info: PageInfo

def get_page_info(total: int, page: int, size: int) -> PageInfo:
    """Calculate pagination metadata."""
    pages = (total + size - 1) // size  # Ceiling division
    return PageInfo(
        total=total,
        page=page,
        size=size,
        pages=pages
    )

def paginate_query(query, page: int = 1, size: int = 10):
    """Apply pagination to a SQLAlchemy query."""
    if page < 1:
        page = 1
    if size < 1:
        size = 10
    
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    return items, get_page_info(total, page, size)
