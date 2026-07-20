from core.db import get_session
from core.models.base import T

def save_object(model: T):
    session = get_session()
    with session:
        session.add(model)
        session.commit()
    