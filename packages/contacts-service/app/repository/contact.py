from app.repository.models.contact import Contact
from app.core.schemas import contact as schema
from uuid import UUID
from app.db import db

class ContactRepository:
    @staticmethod
    def get(id: UUID) -> schema.Contact:
        contact = db.session.query(Contact).get(id)
        if contact is None:
            return None
        return schema.Contact.from_model(contact)

    @staticmethod
    def create(contact: schema.Contact) -> schema.Contact:
        db_contact = contact.to_model()
        db.session.add(db_contact)
        db.session.commit()
        return schema.Contact.from_model(db_contact)

    @staticmethod
    def delete_by_id(id: UUID) -> int:
        row_count = db.session.query(Contact).filter(Contact.id == id).delete()
        db.session.commit()

        return row_count