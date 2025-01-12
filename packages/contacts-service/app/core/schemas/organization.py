from dataclasses import dataclass
from uuid import UUID
from typing import Optional

from app.core.errors.validation_error import ValidationError
from app.repository.models.organization import Organization as OrganizationDb
from conmail.v1.organization_pb2 import Organization as OrganizationProto

@dataclass
class Organization:
    name: str
    description: str

    id: Optional[UUID] = None

    @classmethod
    def from_db(cls, model: OrganizationDb):
        return cls(
            id= model.id,
            name= model.name,
            description= model.description
        )

    def string_id(self):
        if self.id is None:
            return self.id
        
        return str(self.id)

    def to_db(self):
        return OrganizationDb(
            id= self.id,
            name= self.name,
            description= self.description,
        )

    def to_dict(self):
        return {
            "id": self.string_id(),
            "name": self.name,
            "description": self.description,
        }

    def to_protobuf(self):
        return OrganizationProto(
            id = self.string_id(),
            name= self.name,
            description= self.description
        )

@dataclass
class CreateOrganizationRequest(Organization):
    @classmethod
    def from_request(cls, request: dict):
        if "name" not in request or "description" not in request:
            raise ValidationError('missing fields in request payload')
        
        return cls(
            name= request["name"],
            description= request["description"]
        )

    def validate_name(self, name: Optional[str]) -> str:
        name_length = len(name)

        if name_length < 3 or name_length > 10:
            raise ValidationError('name does not meet length validations')

        return name
    
    def validate_description(self, description: str) -> str:
        description_length = len(description)

        if description_length < 3 or description_length > 100:
            raise ValidationError('description does not meet length validations')

        return description
    
    def __post_init__(self):
        self.validate_name(name=self.name)
        self.validate_description(description=self.description)