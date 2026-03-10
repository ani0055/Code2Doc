from pydantic import BaseModel
from typing import Optional, Dict, List

class CodeAnalysisRequest(BaseModel):
    code: str
    filename: Optional[str] = "file.py"
    include_diagram: bool = False

class CodeAnalysisResponse(BaseModel):
    markdown: str
    diagram: Optional[str] = None
    language: str
    structure: Dict
    metrics: Optional[Dict] = None  