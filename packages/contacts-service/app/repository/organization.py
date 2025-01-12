from uuid import UUID
from typing import Optional

from app.db import db
from app.core.schemas.organization import Organization as OrganizationSchema
from app.repository.models.organization import Organization as OrganizationDb

class OrganizationRepository:
    @staticmethod
    def get(id: UUID) -> Optional[OrganizationSchema]:
        organization = db.session.query(OrganizationDb).get(id)        
        if organization is None:
            return None
        return OrganizationSchema.from_db(organization)

    @staticmethod
    def create(organization: OrganizationSchema) -> OrganizationSchema:
        organization_db = organization.to_db()

        db.session.add(organization_db)
        db.session.commit()

        organization.id = organization_db.id

        return organization
    
    @staticmethod
    def delete(id: UUID) -> int:
        row_count = db.session.query(OrganizationDb).filter(OrganizationDb.id == id).delete()
        db.session.commit()

        return row_count