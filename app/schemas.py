from datetime import date
from pydantic import BaseModel, Field
from typing import Optional, List


class PlaceCreate(BaseModel):
    external_place_id: int
    notes: Optional[str] = None


class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    is_visited: Optional[bool] = None


class PlaceResponse(BaseModel):
    id: int
    project_id: int
    external_place_id: int
    notes: Optional[str] = None
    is_visited: bool

    model_config = {"from_attributes": True}


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: Optional[date] = None
    places: Optional[List[PlaceCreate]] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    completed: bool
    places: List[PlaceResponse] = []

    model_config = {"from_attributes": True}