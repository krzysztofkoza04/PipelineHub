from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectRead

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)



@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED
)

def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
):
    project = Project(
        name=payload.name,
        description=payload.description,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project

@router.get(
    "",
    response_model=list[ProjectRead],

)

def list_projects(

    db:Session = Depends(get_db),
):
    statement = select(Project).order_by(Project.id)

    return db.scalars(statement).all()

