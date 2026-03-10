from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Documentation(Base):
    __tablename__ = "documentations"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    markdown = Column(Text, nullable=False)
    diagram = Column(Text, nullable=True)
    has_diagram = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="documentations")