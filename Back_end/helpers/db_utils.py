from contextlib import contextmanager
from helpers.database import db

@contextmanager
def session_scope():
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    finally:
        db.session.remove()