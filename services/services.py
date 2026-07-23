from core.db import get_session
from sqlalchemy import delete
from core.models.base import T


def save_object(obj: T) -> None:
    with get_session() as session:
        session.add(obj)
        session.commit()


def delete_object(obj: T) -> None:
    with get_session() as session:
        session.delete(obj)
        session.commit()


def delete_by_id(model: type[T], ids: int | list[int]) -> None:
    if isinstance(ids, int):
        ids = [ids]
    with get_session() as session:
        session.execute(delete(model).where(model.id.in_(ids)))
        session.commit()