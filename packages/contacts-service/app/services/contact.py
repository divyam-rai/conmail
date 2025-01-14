import sqlalchemy

from uuid import UUID
from conmail.v1.contact_pb2 import ContactEvent

from app.config import Config
from app.core.helpers.kafka import produce
from app.core.helpers.utils import raise_error, get_logger
from app.core.errors.not_found import NotFound
from app.core.errors.not_unique import NotUnique
from app.repository.contact import ContactRepository
from app.services.organization import OrganizationService

from app.core.schemas import contact as schema

logger = get_logger("CONTACT_SERVICE")
organization_service = OrganizationService()

class ContactService:
    def __init__(self):
        self._repository = ContactRepository()
        self.topic = Config.KAFKA_TOPIC_CONTACTS
    
    def get(self, id: UUID) -> schema.Contact:
        return self._repository.get(id)
    
    def create(self, contact_request: schema.CreateContactRequest) -> schema.Contact:
        try:
            organization = organization_service.get(contact_request.organization_id)
            if organization is None:
                raise NotFound('organization')

            contact = self._repository.create(contact_request)

            contact_event = ContactEvent(
                type= ContactEvent.Type.CREATED,
                contact= contact.to_protobuf()
            )

            produce(topic= self.topic, key= contact.id, proto_value= contact_event)

            return contact
        except sqlalchemy.exc.IntegrityError:
            raise NotUnique()


    def delete(self, id: UUID) -> bool:
        contact = self._repository.get(id)
        if contact is None:
            raise NotFound('contact')

        rows_deleted = self._repository.delete_by_id(id)
        if rows_deleted <= 0:
            return False

        contact_event = ContactEvent(
            type= ContactEvent.Type.DELETED,
            contact= contact.to_protobuf()
        )

        produce(self.topic, contact_event, contact.id)

        return True