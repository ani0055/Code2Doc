from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.code import CodeAnalysisRequest, CodeAnalysisResponse
from app.services.code_parser import CodeParser
from app.services.llm_service import LLMService
from app.models.user import User
from app.models.project import Project
from app.models.documentation import Documentation
from app.utils.auth import get_current_user
from app.services.code_metrics import CodeMetricsService
import logging


code_metrics_service = CodeMetricsService()

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/analyze", tags=["Code Analysis"])

code_parser = CodeParser()
llm_service = LLMService()

@router.post("/code", response_model=CodeAnalysisResponse)
async def analyze_code(
    request: CodeAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze code and generate AI-powered documentation
    Saves the analysis to user's history
    """
    try:
        logger.info(f"Analyzing code for user {current_user.email}, file: {request.filename}")
        
        # Detect language
        language = code_parser.detect_language(request.filename)
        logger.info(f"Detected language: {language}")
        
        # Parse code structure
        code_structure = code_parser.parse_code(request.code, language)
        logger.info(f"Parsed structure: {len(code_structure['functions'])} functions, {len(code_structure['classes'])} classes")
        
        # Analyze code quality metrics NEW
        code_metrics = code_metrics_service.analyze_code_quality(request.code, language)
        


        # Generate documentation with Gemini AI
        ai_result = await llm_service.generate_documentation(
            code=request.code,
            code_structure=code_structure,
            language=language,
            include_diagram=request.include_diagram
        )
        
        # Save to database
        # Create project
        project = Project(
            user_id=current_user.id,
            name=request.filename.split('.')[0],  # Use filename without extension as name
            filename=request.filename,
            language=language,
            code=request.code
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        
        # Create documentation
        documentation = Documentation(
            project_id=project.id,
            markdown=ai_result['markdown'],
            diagram=ai_result.get('diagram'),
            has_diagram=request.include_diagram and ai_result.get('diagram') is not None
        )
        db.add(documentation)
        db.commit()
        
        logger.info(f"Documentation saved to history (Project ID: {project.id})")
        
        return CodeAnalysisResponse(
            markdown=ai_result['markdown'],
            diagram=ai_result.get('diagram'),
            language=language,
            structure=code_structure,
            metrics=code_metrics  
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error analyzing code: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing code: {str(e)}"
        )