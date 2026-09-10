from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services import projects as project_service
from app.models.project import Project

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


def get_project_or_404(
        db: Session,
        project_id:int,

) -> Project:
    project=project_service.get_project_by_id(
        db=db,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project


@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED
)

def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
):
    return project_service.create_project(
        db=db,
        payload=payload,
    )
    

@router.get(
    "",
    response_model=list[ProjectRead],

)

def list_projects(

    db:Session = Depends(get_db),
):
    return project_service.list_project(db)



@router.get(
    "/{project_id}",
    response_model=ProjectRead,
)
def get_project(
    project_id:int,
    db:Session=Depends(get_db),

):
    return get_project_or_404(
        db=db,
        project_id=project_id,
    )



@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,

)
def delete_project(
    project_id:int,
    db:Session=Depends(get_db),
):
    project = get_project_or_404(
        db=db,
        project_id=project_id,
    )
    
    project_service.delete_project(
        db=db,
        project=project,
    )

    


@router.patch(
    "/{project_id}",
    response_model=ProjectRead,
)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
):
    project = get_project_or_404(
        db=db,
        project_id=project_id,
    )

    return project_service.update_project(
        db=db,
        project=project,
        payload=payload,
    )