from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate

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

@router.get(
    "/{project_id}",
    response_model=ProjectRead,
)
def get_project(
    project_id:int,
    db:Session=Depends(get_db),

):
    project = db.get(Project,project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,

)
def delete_project(
    project_id:int,
    db:Session=Depends(get_db),
):
    project = db.get(Project,project_id)
    if project is None:
        raise HTTPExceeption(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeect not found",
        )
    db.delete(project)
    db.commit()



@router.patch(
    "/{project_id}",
    response_model=ProjectRead,
)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
):
    project = db.get(Project, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project