"""
ResumeOS Models Package

Import every SQLAlchemy model here.

Alembic imports this package to discover
all ORM models automatically.
"""

from app.models.application_workspace import ApplicationWorkspace
from app.models.generated_resume import GeneratedResume
from app.models.job_description import JobDescription
from app.models.master_resume import MasterResume
from app.models.user import User
from app.models.recruiter_message import RecruiterMessage
from app.models.interview_note import InterviewNote
__all__ = [
    "ApplicationWorkspace",
    "GeneratedResume",
    "JobDescription",
    "MasterResume",
    "CoverLetter",
    "RecruiterMessage",
    "InterviewNote",
    "User",
]