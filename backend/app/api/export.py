from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.documentation import Documentation
# Project import is implicitly used via Documentation relationship, but good to include if needed elsewhere.
# from app.models.project import Project 
from app.utils.auth import get_current_user
from app.services.export_service import ExportService 
from pydantic import BaseModel
from typing import Optional

# Initialize the router and service
router = APIRouter(prefix="/export", tags=["Export"])
# Assuming ExportService handles document generation logic (e.g., using Pandoc, WeasyPrint, python-docx)
export_service = ExportService()

# Export Request Model
class ExportRequest(BaseModel):
    """
    Model for rich content export requests (where content is sent directly).
    """
    markdown: str
    filename: str = "documentation"
    diagram_image: Optional[str] = None # Base64 image data for an optional diagram

# --- Rich Content Export Endpoints (POST requests) ---

@router.post("/pdf")
async def export_pdf(
    request: ExportRequest,
    current_user: User = Depends(get_current_user) # Secured endpoint
):
    """
    Export documentation as professional PDF with optional diagram.
    """
    try:
        # Call ExportService to generate PDF bytes
        pdf_bytes = export_service.generate_pdf(
            markdown_text=request.markdown,
            diagram_image=request.diagram_image,
            filename=request.filename
        )
        
        # Return PDF bytes as a downloadable response
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={request.filename}.pdf"
            }
        )
    except Exception as e:
        print(f"PDF Generation Error for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate PDF."
        )

@router.post("/docx")
async def export_docx(
    request: ExportRequest,
    current_user: User = Depends(get_current_user) # Secured endpoint
):
    """
    Export documentation as professional DOCX with optional diagram.
    """
    try:
        # Call ExportService to generate DOCX bytes
        docx_bytes = export_service.generate_docx(
            markdown_text=request.markdown,
            diagram_image=request.diagram_image,
            filename=request.filename
        )
        
        # Return DOCX bytes as a downloadable response
        return Response(
            content=docx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename={request.filename}.docx"
            }
        )
    except Exception as e:
        print(f"DOCX Generation Error for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate DOCX."
        )


# --- Database Retrieval Export Endpoints (GET requests) ---

@router.get("/documentation/{doc_id}/pdf")
async def export_documentation_pdf(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db) # Database dependency
):
    """
    Export saved documentation by ID as PDF, retrieved from the database.
    Includes an authorization check.
    """
    try:
        # Query the database, ensuring the documentation belongs to a project the user has access to
        doc = db.query(Documentation).join(Documentation.project).filter(
            Documentation.id == doc_id,
            # CRUCIAL: Authorization check
            Documentation.project.has(user_id=current_user.id)
        ).first()
        
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Documentation not found or access denied."
            )
        
        filename = f"documentation_{doc_id}"
        
        # Generate PDF
        pdf_bytes = export_service.generate_pdf(
            markdown_text=doc.markdown,
            diagram=None,  # Assuming diagram data is not stored in the doc model for simplicity
            filename=filename
        )
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}.pdf"
            }
        )
    except HTTPException:
        # Re-raise explicit HTTP exceptions (404)
        raise
    except Exception as e:
        print(f"Database PDF Export Error for user {current_user.id} (Doc ID {doc_id}): {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export PDF."
        )

@router.get("/documentation/{doc_id}/docx")
async def export_documentation_docx(
    doc_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db) # Database dependency
):
    """
    Export saved documentation by ID as DOCX, retrieved from the database.
    Includes an authorization check.
    """
    try:
        # Query the database, ensuring the documentation belongs to a project the user has access to
        doc = db.query(Documentation).join(Documentation.project).filter(
            Documentation.id == doc_id,
            # CRUCIAL: Authorization check
            Documentation.project.has(user_id=current_user.id)
        ).first()
        
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Documentation not found or access denied."
            )

        filename = f"documentation_{doc_id}"
        
        # Generate DOCX
        docx_bytes = export_service.generate_docx(
            markdown_text=doc.markdown,
            diagram=None, # Assuming diagram data is not stored in the doc model for simplicity
            filename=filename
        )
        
        return Response(
            content=docx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename={filename}.docx"
            }
        )
    except HTTPException:
        # Re-raise explicit HTTP exceptions (404)
        raise
    except Exception as e:
        print(f"Database DOCX Export Error for user {current_user.id} (Doc ID {doc_id}): {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export DOCX."
        )


# --- Optional: Endpoint to test export service ---
@router.post("/test")
async def test_export(current_user: User = Depends(get_current_user)):
    """
    Test endpoint to verify export service is working by generating a sample PDF.
    """
    test_markdown = """
# Test Documentation

## Overview
This is a **test** document with `inline code`.

### Features
* Feature 1
* Feature 2

```python
def hello():
    print("Hello World")
```
"""
    
    try:
        pdf_bytes = export_service.generate_pdf(
            markdown_text=test_markdown,
            diagram=None,
            filename="test"
        )
        
        return {
            "status": "success",
            "message": "Export service is working (PDF generated successfully)",
            "pdf_size": len(pdf_bytes)
        }
    except Exception as e:
        print(f"Test Export Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Export service failed: {str(e)}"
        )