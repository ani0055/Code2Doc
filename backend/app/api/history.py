from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.documentation import Documentation
from app.schemas.project import ProjectResponse, ProjectWithDocs, DocumentationResponse
from app.utils.auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/history", tags=["History"])

@router.get("/projects", response_model=List[ProjectResponse])
def get_user_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get all projects for the current user"""
    projects = db.query(Project).filter(
        Project.user_id == current_user.id
    ).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    
    return projects

@router.get("/projects/{project_id}", response_model=ProjectWithDocs)
def get_project_details(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get project with all its documentation versions"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return project

@router.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a project and all its documentation"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()
    
    return {"message": "Project deleted successfully"}

@router.get("/recent", response_model=List[ProjectResponse])
def get_recent_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get recent projects for quick access"""
    projects = db.query(Project).filter(
        Project.user_id == current_user.id
    ).order_by(Project.created_at.desc()).limit(limit).all()
    
    return projects

class ProjectUpdate(BaseModel):
    name: str

@router.patch("/projects/{project_id}")
def update_project_name(
    project_id: int,
    update: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update project name"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    project.name = update.name
    db.commit()
    db.refresh(project)
    
    return project