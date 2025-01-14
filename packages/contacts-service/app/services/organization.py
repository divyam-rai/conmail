from uuid import UUID
from typing import Optional
from conmail.v1.organization_pb2 import OrganizationEvent
from app.config import Config

from app.core.helpers.kafka import produce
from app.core.helpers.utils import get_logger
from app.core.errors.not_found import NotFound
from app.repository.organization import OrganizationRepository
from app.core.schemas.organization import Organization as OrganizationSchema

logger = get_logger("ORGANIZATION_SERVICE")

class OrganizationService:
    def __init__(self):
        self._repository = OrganizationRepository()
        self.topic = Config.KAFKA_TOPIC_ORGANIZATIONS

    def get(self, id: UUID) -> Optional[OrganizationSchema]:
        return self._repository.get(id)

    def create(self, organization: OrganizationSchema):
        organization = self._repository.create(organization)

        organization_event = OrganizationEvent(
            type=OrganizationEvent.Type.CREATED,
            organization= organization.to_protobuf()
        )

        produce(self.topic, organization_event, organization.id)

        return organization
    
    def delete(self, id: UUID) -> bool:
        organization = self._repository.get(id)
        if organization is None:
            raise NotFound('organization')

        rows_deleted = self._repository.delete(id)
        if rows_deleted <= 0:
            return False

        organization_event = OrganizationEvent(
            type= OrganizationEvent.Type.DELETED,
            organization= organization.to_protobuf()
        )

        produce(self.topic, organization_event, organization.id)

        return True