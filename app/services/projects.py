from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def create_project(
    db: Session,
    payload: ProjectCreate,
) -> Project:
    project = Project(
        name=payload.name,
        description=payload.description,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def list_projects(
    db: Session,
) -> list[Project]:
    statement = select(Project).order_by(Project.id)

    return list(db.scalars(statement).all())


def get_project_by_id(
    db: Session,
    project_id: int,
) -> Project | None:
    return db.get(Project, project_id)


def update_project(
    db: Session,
    project: Project,
    payload: ProjectUpdate,
) -> Project:
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


def delete_project(
    db: Session,
    project: Project,
) -> None:
    db.delete(project)
    db.commit()