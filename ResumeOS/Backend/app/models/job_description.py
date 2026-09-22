from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Index,
    JSON,
    String,
    Text,
    UniqueConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.application_workspace import ApplicationWorkspace


class JobDescription(BaseModel):
    """
    Parsed Job Description.

    One Job Description belongs to exactly one
    Application Workspace.
    """

    __tablename__ = "job_descriptions"

    __table_args__ = (
        UniqueConstraint(
            "workspace_id",
            name="uq_job_description_workspace",
        ),
        Index(
            "ix_job_description_workspace",
            "workspace_id",
        ),
    )

    # ------------------------------------------------------
    # Relationship
    # ------------------------------------------------------

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey(
            "application_workspaces.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # ------------------------------------------------------
    # Original Job Description
    # ------------------------------------------------------

    original_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # ------------------------------------------------------
    # Parsed Information
    # ------------------------------------------------------

    company_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    role_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
    )

    employment_type: Mapped[str | None] = mapped_column(
        String(100),
    )

    experience_required: Mapped[str | None] = mapped_column(
        String(255),
    )

    education_required: Mapped[str | None] = mapped_column(
        String(255),
    )

    salary_range: Mapped[str | None] = mapped_column(
        String(255),
    )

    # ------------------------------------------------------
    # AI Extracted Data
    # ------------------------------------------------------

    required_skills: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    preferred_skills: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    responsibilities: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    qualifications: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    parsed_json: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    # ------------------------------------------------------
    # Relationship
    # ------------------------------------------------------

    workspace: Mapped["ApplicationWorkspace"] = relationship(
        "ApplicationWorkspace",
        back_populates="job_description",
    )

    # ------------------------------------------------------
    # Helpers
    # ------------------------------------------------------

    @property
    def total_required_skills(self) -> int:
        return len(self.required_skills)

    @property
    def total_preferred_skills(self) -> int:
        return len(self.preferred_skills)

    def __repr__(self) -> str:
        return (
            f"<JobDescription("
            f"workspace_id={self.workspace_id}, "
            f"role='{self.role_name}')>"
        )