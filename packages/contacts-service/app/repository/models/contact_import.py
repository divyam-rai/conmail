import enum

from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4
from datetime import datetime, timezone

from app.repository.models.base import Base

class ContactImportStatus(enum.Enum):
    CREATED = "CREATED"
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    ERRED = "ERRED"

class ContactImport(Base):
    __tablename__ = "contact_imports"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    file_name: Mapped[str] = mapped_column()
    
    status: Mapped[ContactImportStatus] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(timezone.utc))
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)
    organization_id: Mapped[UUID] = mapped_column()