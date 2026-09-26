from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.data_source import DataSource
from app.schemas.data_source import (
    DataSourceCreate,
    DataSourceRead,
    DataSourceUpdate,
)
from app.services import data_sources as data_source_service
from app.services import projects as project_service


router = APIRouter(
    prefix="/projects/{project_id}/data-sources",
    tags=["data-sources"],
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


def get_data_source_or_404(
    db: Session,
    project_id: int,
    data_source_id: int,
) -> DataSource:
    data_source = data_source_service.get_data_source_by_id(
        db=db,
        project_id=project_id,
        data_source_id=data_source_id,
    )

    if data_source is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found",
        )

    return data_source


@router.post(
    "",
    response_model=DataSourceRead,
    status_code=status.HTTP_201_CREATED,
)
def create_data_source(
    project_id: int,
    payload: DataSourceCreate,
    db: Session = Depends(get_db),
):
    ensure_project_exists(db=db, project_id=project_id)

    try:
        return data_source_service.create_data_source(
            db=db,
            project_id=project_id,
            payload=payload,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[DataSourceRead],
)
def list_data_sources(
    project_id: int,
    db: Session = Depends(get_db),
):
    ensure_project_exists(db=db, project_id=project_id)

    return data_source_service.list_data_sources(
        db=db,
        project_id=project_id,
    )


@router.get(
    "/{data_source_id}",
    response_model=DataSourceRead,
)
def get_data_source(
    project_id: int,
    data_source_id: int,
    db: Session = Depends(get_db),
):
    ensure_project_exists(db=db, project_id=project_id)

    return get_data_source_or_404(
        db=db,
        project_id=project_id,
        data_source_id=data_source_id,
    )


@router.patch(
    "/{data_source_id}",
    response_model=DataSourceRead,
)
def update_data_source(
    project_id: int,
    data_source_id: int,
    payload: DataSourceUpdate,
    db: Session = Depends(get_db),
):
    ensure_project_exists(db=db, project_id=project_id)

    data_source = get_data_source_or_404(
        db=db,
        project_id=project_id,
        data_source_id=data_source_id,
    )

    try:
        return data_source_service.update_data_source(
            db=db,
            data_source=data_source,
            payload=payload,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{data_source_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_data_source(
    project_id: int,
    data_source_id: int,
    db: Session = Depends(get_db),
):
    ensure_project_exists(db=db, project_id=project_id)

    data_source = get_data_source_or_404(
        db=db,
        project_id=project_id,
        data_source_id=data_source_id,
    )

    data_source_service.delete_data_source(
        db=db,
        data_source=data_source,
    )