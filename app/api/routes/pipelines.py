from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.pipeline import Pipeline
from app.schemas.pipeline import (
    PipelineCreate,
    PipelineRead,
    PipelineUpdate,
)
from app.services import pipelines as pipeline_service
from app.services import projects as project_service


router = APIRouter(
    prefix="/projects/{project_id}/pipelines",
    tags=["pipelines"],
)


def ensure_project_exists(
    db: Session,
    project_id: int,
) -> None:
    project = project_service.get_project_by_id(
        db=db,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )


def get_pipeline_or_404(
    db: Session,
    project_id: int,
    pipeline_id: int,
) -> Pipeline:
    pipeline = pipeline_service.get_pipeline_by_id(
        db=db,
        project_id=project_id,
        pipeline_id=pipeline_id,
    )

    if pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pipeline not found",
        )

    return pipeline


@router.post(
    "",
    response_model=PipelineRead,
    status_code=status.HTTP_201_CREATED,
)
def create_pipeline(
    project_id: int,
    payload: PipelineCreate,
    db: Session = Depends(get_db),
):
    ensure_project_exists(
        db=db,
        project_id=project_id,
    )

    return pipeline_service.create_pipeline(
        db=db,
        project_id=project_id,
        payload=payload,
    )


@router.get(
    "",
    response_model=list[PipelineRead],
)
def list_pipelines(
    project_id: int,
    db: Session = Depends(get_db),
):
    ensure_project_exists(
        db=db,
        project_id=project_id,
    )

    return pipeline_service.list_pipelines(
        db=db,
        project_id=project_id,
    )


@router.get(
    "/{pipeline_id}",
    response_model=PipelineRead,
)
def get_pipeline(
    project_id: int,
    pipeline_id: int,
    db: Session = Depends(get_db),
):
    ensure_project_exists(
        db=db,
        project_id=project_id,
    )

    return get_pipeline_or_404(
        db=db,
        project_id=project_id,
        pipeline_id=pipeline_id,
    )


@router.patch(
    "/{pipeline_id}",
    response_model=PipelineRead,
)
def update_pipeline(
    project_id: int,
    pipeline_id: int,
    payload: PipelineUpdate,
    db: Session = Depends(get_db),
):
    ensure_project_exists(
        db=db,
        project_id=project_id,
    )

    pipeline = get_pipeline_or_404(
        db=db,
        project_id=project_id,
        pipeline_id=pipeline_id,
    )

    return pipeline_service.update_pipeline(
        db=db,
        pipeline=pipeline,
        payload=payload,
    )


@router.delete(
    "/{pipeline_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_pipeline(
    project_id: int,
    pipeline_id: int,
    db: Session = Depends(get_db),
):
    ensure_project_exists(
        db=db,
        project_id=project_id,
    )

    pipeline = get_pipeline_or_404(
        db=db,
        project_id=project_id,
        pipeline_id=pipeline_id,
    )

    pipeline_service.delete_pipeline(
        db=db,
        pipeline=pipeline,
    )