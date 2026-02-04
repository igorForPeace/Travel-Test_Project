from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    places = relationship("ProjectPlace", back_populates="project", cascade="all, delete-orphan")


class ProjectPlace(Base):
    __tablename__ = "project_places"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    external_place_id = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
    is_visited = Column(Boolean, default=False, nullable=False)
    project = relationship("Project", back_populates="places")

    __table_args__ = (
        UniqueConstraint("project_id", "external_place_id", name="uq_project_external_place"),
    )
