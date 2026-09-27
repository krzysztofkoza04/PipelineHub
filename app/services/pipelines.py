from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pipeline import Pipeline
from app.schemas.pipeline import (
    PipelineCreate,
    PipelineUpdate,
)


def create_pipeline(
    db: Session,
    project_id: int,
    payload: PipelineCreate,
) -> Pipeline:
    pipeline = Pipeline(
        project_id=project_id,
        name=payload.name,
        description=payload.description,
    )

    db.add(pipeline)
    db.commit()
    db.refresh(pipeline)

    return pipeline


def list_pipelines(
    db: Session,
    project_id: int,
) -> list[Pipeline]:
    statement = (
        select(Pipeline)
        .where(Pipeline.project_id == project_id)
        .order_by(Pipeline.id)
    )

    return list(db.scalars(statement).all())


def get_pipeline_by_id(
    db: Session,
    project_id: int,
    pipeline_id: int,
) -> Pipeline | None:
    statement = select(Pipeline).where(
        Pipeline.id == pipeline_id,
        Pipeline.project_id == project_id,
    )

    return db.scalar(statement)


def update_pipeline(
    db: Session,
    pipeline: Pipeline,
    payload: PipelineUpdate,
) -> Pipeline:
    update_data = payload.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(pipeline, field, value)

    db.commit()
    db.refresh(pipeline)

    return pipeline


def delete_pipeline(
    db: Session,
    pipeline: Pipeline,
) -> None:
    db.delete(pipeline)
    db.commit()