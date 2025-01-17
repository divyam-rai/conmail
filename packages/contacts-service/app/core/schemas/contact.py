from uuid import UUID
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.core.errors.validation_error import ValidationError
from conmail.v1.contact_pb2 import Contact as ContactProto
from app.repository.models.contact import Contact as ContactModel
from app.repository.models.contact_import import ContactImport as ContactImportModel, ContactImportStatus


@dataclass
class ContactName:
    first: str
    last: str
    middle: Optional[str] = None

    def __post_init__(self):
        for name in [self.first, self.last, self.middle]:
            if name is None:
                continue

            name_length = len(name)

            if name_length < 3 or name_length > 10:
                raise ValidationError('name does not meet length validations')
            
    def to_protobuf(self) -> ContactProto.Name:
        return ContactProto.Name(
            first= self.first,
            last= self.last,
            middle= self.middle
        )

@dataclass
class ContactAddress:
    street: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[int] = None

    def __post_init__(self):
        for address in [self.street, self.city, self.country]:
            if address is None:
                continue

            address_length = len(address)

            if address_length < 2 or address_length > 500:
                raise ValidationError('address does not meet length validations')

    def to_protobuf(self) -> ContactProto.Address:
        return ContactProto.Address(
            street= self.street,
            city= self.city,
            country= self.country,
            zip= self.zip
        )

@dataclass
class Contact:
    email: str
    name: ContactName
    organization_id: UUID

    updated_at: datetime = datetime.now(timezone.utc)
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    address: Optional[ContactAddress] = field(default_factory=ContactAddress)
    id: Optional[UUID] = None

    def to_protobuf(self):
        return ContactProto(
            id= str(self.id),
            email= self.email,
            name= self.name.to_protobuf(),
            address= self.address.to_protobuf(),
            organization_id= str(self.organization_id),
            create_time= self.created_at,
            update_time= self.updated_at,
            delete_time= self.deleted_at,
        )
    
    @classmethod
    def from_model(cls, model: ContactModel):
        return cls(
            id= model.id,
            email= model.email,
            name= ContactName(
                first= model.name_first,
                middle= model.name_middle,
                last= model.name_last,
            ),
            address= ContactAddress(
                street= model.address_street,
                city= model.address_city,
                country= model.address_country,
                zip= model.address_zip
            ),
            organization_id= model.organization_id,
            created_at= model.created_at,
            updated_at= model.updated_at,
            deleted_at= model.deleted_at
        )
    
    @staticmethod
    def format_timestamp_as_string(timestamp):
        if timestamp is None:
            return timestamp
        
        return datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "created_at": self.format_timestamp_as_string(self.created_at),
            "updated_at": self.format_timestamp_as_string(self.updated_at),
            "deleted_at": self.format_timestamp_as_string(self.deleted_at),
            "name": {
                "first": self.name.first,
                "middle": self.name.middle,
                "last": self.name.last,
            },
            "address": {
                "street": self.address.street,
                "city": self.address.city,
                "country": self.address.country,
                "zip": self.address.zip,
            },
            "organization_id": str(self.organization_id)
        }

    def to_model(self):
        return ContactModel(
            id= self.id,
            email= self.email,
            created_at= self.created_at,
            updated_at= self.updated_at,
            deleted_at= self.deleted_at,
            name_first= self.name.first,
            name_middle= self.name.middle,
            name_last= self.name.last,
            address_street= self.address.street,
            address_city= self.address.city,
            address_country= self.address.country,
            address_zip= self.address.zip,
            organization_id= self.organization_id
        )

@dataclass
class CreateContactRequest(Contact):
    @classmethod
    def from_request(cls, request):
        if 'organization_id' not in request:
            raise ValidationError('missing organization from request')

        if 'name' not in request or 'email' not in request:
            raise ValidationError('missing required attributes from request')
        
        contact_name = ContactName(**request['name'])

        contact_address = ContactAddress()
        if 'address' in request:
            contact_address = ContactAddress(**request['address'])

        return Contact(
            email= request['email'],
            name= contact_name,
            address= contact_address,
            organization_id= request['organization_id'],
        )

@dataclass
class ContactImport:
    organization_id: UUID
    file_name: str

    updated_at: datetime = datetime.now(timezone.utc)
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    id: Optional[UUID] = None
    status: Optional[ContactImportStatus] = ContactImportStatus.CREATED

    @staticmethod
    def format_timestamp_as_string(timestamp):
        if timestamp is None:
            return timestamp
        
        return datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return {
            "id": str(self.id),
            "file_name": self.file_name,
            "status": self.status.value,
            "organization_id": str(self.organization_id),
            "created_at": self.format_timestamp_as_string(self.created_at),
            "updated_at": self.format_timestamp_as_string(self.updated_at),
        }
    
    def to_model(self):
        return ContactImportModel(
            id= self.id,
            file_name= self.file_name,
            status= self.status,
            organization_id= self.organization_id,
            created_at= self.created_at,
            updated_at= self.updated_at,
            deleted_at= self.deleted_at,
        )
    
    @classmethod
    def from_model(cls, model: ContactImportModel):
        return cls(
            id= model.id,
            file_name= model.file_name,
            status= model.status,
            organization_id= model.organization_id,
            created_at= model.created_at,
            updated_at= model.updated_at,
            deleted_at= model.deleted_at,
        )

@dataclass
class CreateContactImportRequest(ContactImport):
    @classmethod
    def from_request(cls, payload: dict):
        if 'organization_id' not in payload or 'file_name' not in payload:
            raise ValidationError('missing fields in request payload')

        return cls(
            organization_id= payload['organization_id'],
            file_name= payload['file_name']
        )

    def __post_init__(self):
        # TODO: sanitize file_name and check for extension
        name_length = len(self.file_name)

        if name_length < 3 or name_length > 10:
            raise ValidationError('file_name does not meet length requirements')

@dataclass
class CreateContactImportResponse(ContactImport):
    upload_url: Optional[str] = None

    def to_dict(self):
        return { **super().to_dict(), "upload_url": self.upload_url }
    
    @classmethod
    def from_contact_import(cls, contact_import: ContactImport):
        return cls(
            id= contact_import.id,
            file_name= contact_import.file_name,
            status= contact_import.status,
            organization_id= contact_import.organization_id,
            created_at= contact_import.created_at,
            updated_at= contact_import.updated_at,
            deleted_at= contact_import.deleted_at,
        )