from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DocumentationBase(BaseModel):
    markdown: str
    diagram: Optional[str] = None
    has_diagram: bool = False

class DocumentationResponse(DocumentationBase):
    id: int
    project_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    filename: str
    language: str

class ProjectCreate(ProjectBase):
    code: str

class ProjectResponse(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProjectWithDocs(ProjectResponse):
    documentations: List[DocumentationResponse] = []
    
    class Config:
        from_attributes = True