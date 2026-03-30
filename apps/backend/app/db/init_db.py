from app.db.session import engine, Base
# Import all models to register them with Base.metadata
from app.models.user import User
from app.models.upload import Upload
from app.models.job import Job
from app.models.audit import AuditLog

def init_db():
    """ Initialize database tables before the app starts. """
    # Run in a synchronous context
    Base.metadata.create_all(bind=engine)
