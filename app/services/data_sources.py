from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.data_source import DataSource
from app.schemas.data_source import DataSourceCreate, DataSourceUpdate
from app.schemas.source_config import validate_source_config


def create_data_source(
    db: Session,
    project_id: int,
    payload: DataSourceCreate,
) -> DataSource:

    validated_config = validate_source_config(
        source_type=payload.source_type,
        config=payload.config,
    )

    data_source = DataSource(
        project_id=project_id,
        name=payload.name,
        source_type=payload.source_type,
        config=validated_config,
    )

    db.add(data_source)
    db.commit()
    db.refresh(data_source)

    return data_source


def list_data_sources(
    db: Session,
    project_id: int,
) -> list[DataSource]:
    statement = (
        select(DataSource)
        .where(DataSource.project_id == project_id)
        .order_by(DataSource.id)
    )

    return list(db.scalars(statement).all())


def get_data_source_by_id(
    db: Session,
    project_id: int,
    data_source_id: int,
) -> DataSource | None:
    statement = select(DataSource).where(
        DataSource.id == data_source_id,
        DataSource.project_id == project_id,
    )

    return db.scalar(statement)


def update_data_source(
    db: Session,
    data_source: DataSource,
    payload: DataSourceUpdate,
) -> DataSource:
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(data_source, field, value)

    db.commit()
    db.refresh(data_source)

    return data_source


def delete_data_source(
    db: Session,
    data_source: DataSource,
) -> None:
    db.delete(data_source)
    db.commit()