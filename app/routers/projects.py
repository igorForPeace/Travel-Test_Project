from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db import get_db
from app.models import Project, ProjectPlace
from app.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    PlaceCreate,
    PlaceUpdate,
    PlaceResponse,
)

from app.services.ex_places import place_exists

router = APIRouter()

def is_project_completed(project: Project):
    if not project.places:
        return False
    return all(p.is_visited for p in project.places)


def project_response(project: Project):
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        start_date=project.start_date,
        completed=is_project_completed(project),
        places=project.places,
    )


def get_project(db: Session, project_id: int):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id #{project_id} is not found")
    return project


def get_place(db: Session, project_id: int, place_id: int):
    place = db.get(ProjectPlace, place_id)
    if not place or place.project_id != project_id:
        raise HTTPException(status_code=404, detail=f"Place with id #{place_id} is not found")
    return place


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(payload_data: ProjectCreate, db: Session = Depends(get_db)):
    project_places = payload_data.places or []
    if len(project_places) < 1:
        raise HTTPException(status_code=400, detail="Project must have at least 1 place")
    if len(project_places) > 10:
        raise HTTPException(status_code=400, detail="Project cannot have more than 10 places")
    
    ext_ids = [p.external_place_id for p in project_places]
    for ext_id in ext_ids:
        if not await place_exists(ext_id):
            raise HTTPException(status_code=400, detail=f"Place {ext_id} not found in external API")
        
    project = Project(name=payload_data.name, description=payload_data.description, start_date=payload_data.start_date)
    db.add(project)
    db.flush()

    for p in project_places:
        db.add(
            ProjectPlace(
                project_id=project.id,
                external_place_id=p.external_place_id,
                notes=p.notes,
                is_visited=False,
            )
        )

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Place already exists in this project")
    
    db.refresh(project)
    project.places 
    return project_response(project)


@router.get("/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.id.desc()).all()
    for project in projects:
        project.places
    return [project_response(project) for project in projects]


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_by_id(project_id: int, db: Session = Depends(get_db)):
    project = get_project(db, project_id)
    project.places
    return project_response(project)


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    project = get_project(db, project_id)

    if payload.name is not None:
        project.name = payload.name
    if payload.description is not None:
        project.description = payload.description
    if payload.start_date is not None:
        project.start_date = payload.start_date

    db.commit()
    db.refresh(project)
    project.places
    return project_response(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = get_project(db, project_id)

    visited_place = (
    db.query(ProjectPlace).filter(
        ProjectPlace.project_id == project_id, 
        ProjectPlace.is_visited == True).first())

    if visited_place:
        raise HTTPException(status_code=400, detail="Cannot delete project with visited places")

    db.delete(project)
    db.commit()
    return


@router.get("/{project_id}/places", response_model=list[PlaceResponse])
def list_places(project_id: int, db: Session = Depends(get_db)):
    get_project(db, project_id)
    places = db.execute(
        select(ProjectPlace).where(ProjectPlace.project_id == project_id).order_by(ProjectPlace.id.desc())
    ).scalars().all()
    return places


@router.get("/{project_id}/places/{place_id}", response_model=PlaceResponse)
def get_place_by_id(project_id: int, place_id: int, db: Session = Depends(get_db)):
    place = get_place(db, project_id, place_id)
    return place


@router.post("/{project_id}/places", response_model=PlaceResponse, status_code=status.HTTP_201_CREATED)
async def add_place(project_id: int, payload: PlaceCreate, db: Session = Depends(get_db)):
    get_project(db, project_id)

    count_places = db.query(ProjectPlace).filter(ProjectPlace.project_id == project_id).count()
    if count_places >= 7:
        raise HTTPException(status_code=400, detail="Project cannot have more than 7 places")

    if not await place_exists(payload.external_place_id):
        raise HTTPException(status_code=400, detail=f"Place {payload.external_place_id} not found in ArtIC API")

    place = ProjectPlace(
        project_id=project_id,
        external_place_id=payload.external_place_id,
        notes=payload.notes,
        is_visited=False,
    )
    db.add(place)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Place already exists in this project")

    db.refresh(place)
    return place


@router.patch("/{project_id}/places/{place_id}", response_model=PlaceResponse)
def update_place(project_id: int, place_id: int, payload: PlaceUpdate, db: Session = Depends(get_db)):
    place = get_place(db, project_id, place_id)

    if payload.notes is not None:
        place.notes = payload.notes
    if payload.is_visited is not None:
        place.is_visited = payload.is_visited

    db.commit()
    db.refresh(place)
    return place