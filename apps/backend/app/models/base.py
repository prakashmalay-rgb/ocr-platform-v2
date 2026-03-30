from sqlalchemy.orm import declarative_base

# Unified Registry Base for all backend models
Base = declarative_base()

# Import all models here to register them with the Base.metadata automatically
# This solves the NoReferencedTableError and Circular dependency issues.
from .user import User
from .job import Job
from .upload import Upload
from .audit import AuditLog

__all__ = ["Base", "User", "Job", "Upload", "AuditLog"]
