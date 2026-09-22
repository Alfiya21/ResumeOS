from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


# ==========================================================
# Naming Convention
# ==========================================================

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


metadata = MetaData(
    naming_convention=NAMING_CONVENTION,
)


# ==========================================================
# Base Class
# ==========================================================


class Base(DeclarativeBase):
    """
    Base declarative class for all ORM models.
    """

    metadata = metadata

    type_annotation_map: dict[Any, Any] = {}


# ==========================================================
# Common Audit Model
# ==========================================================


class BaseModel(Base):
    """
    Abstract model inherited by every database table.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Automatically generate table names.

        Example:
            User -> users
            Resume -> resumes
            ATSReport -> atsreports
        """

        return cls.__name__.lower() + "s"

    def to_dict(self) -> dict[str, Any]:
        """
        Convert ORM object into dictionary.
        """

        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}"
            f"(id={self.id})>"
        )