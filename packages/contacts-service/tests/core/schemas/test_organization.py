import pytest
import random
import string
from uuid import uuid4

from app.core.schemas.organization import Organization, CreateOrganizationRequest
from app.repository.models.organization import Organization as OrganizationDb
from conmail.v1.organization_pb2 import Organization as OrganizationProto
from app.core.errors.validation_error import ValidationError

class TestOrganization:
    @staticmethod
    def test_init_valid_payload():
        payload = {
            "id": uuid4(),
            "name": "test",
            "description": "this is a test"
        }
        
        organization = Organization(**payload)

        assert type(organization) == Organization
        assert organization.id == payload["id"]
        assert organization.string_id() == str(payload["id"])
        assert organization.name ==  payload["name"] and organization.description == payload["description"]

    @staticmethod
    def test_init_missing_id():
        payload = {
            "name": "test",
            "description": "this is a test"
        }
        
        organization = Organization(**payload)

        assert type(organization) == Organization
        assert organization.id == None
        assert organization.string_id() == None
        assert organization.name ==  payload["name"] and organization.description == payload["description"]
    
    @staticmethod
    def test_init_missing_name():
        with pytest.raises(TypeError) as exc:
            payload = {
                "id": uuid4(),
                "description": "this is a test"
            }
            
            Organization(**payload)

        assert exc.value.args[0] == "Organization.__init__() missing 1 required positional argument: 'name'"
    
    @staticmethod
    def test_init_missing_description():
        with pytest.raises(TypeError) as exc:
            payload = {
                "id": uuid4(),
                "name": "test"
            }
            
            Organization(**payload)

        assert exc.value.args[0] == "Organization.__init__() missing 1 required positional argument: 'description'"

    @staticmethod
    def test_from_db():
        organization_db = OrganizationDb(
            id = uuid4(),
            name = "test",
            description = "this is a test"
        )

        organization = Organization.from_db(organization_db)

        assert type(organization) == Organization
        assert organization.id == organization_db.id
        assert organization.name == organization_db.name and organization.description == organization_db.description

    @staticmethod
    def test_to_dict_valid_id():
        payload = {
            "id": str(uuid4()),
            "name": "test",
            "description": "this is a test"
        }

        organization = Organization(**payload)

        assert organization.to_dict() == payload

    @staticmethod
    def test_to_dict_missing_id():
        payload = {
            "name": "test",
            "description": "this is a test"
        }

        organization = Organization(**payload)
        org_as_dict = organization.to_dict()

        assert org_as_dict["id"] == None
        assert org_as_dict["name"] == payload["name"] and org_as_dict["description"] == payload["description"]

    @staticmethod
    def test_to_protobuf_valid_id():
        payload = {
            "id": str(uuid4()),
            "name": "test",
            "description": "this is a test"
        }

        organization = Organization(**payload)

        assert organization.to_protobuf() == OrganizationProto(**payload)

    @staticmethod
    def test_to_protobuf_missing_id():
        payload = {
            "name": "test",
            "description": "this is a test"
        }

        organization = Organization(**payload)

        assert organization.to_protobuf() == OrganizationProto(**payload)

class TestCreateOrganizationRequest:
    @staticmethod
    def test_init_valid_payload():
        attrs = {
            "name": "test",
            "description": "this is a test",
        }
        request = CreateOrganizationRequest(**attrs)
        
        assert issubclass(request.__class__, Organization)
        assert request.id == None
        assert request.name == attrs["name"] and request.description == attrs["description"]


    TABLE_CREATE_ORGANIZATION_FROM_REQUEST_VALID_CASES = [
        pytest.param(
            {
                "name": "test",
                "description": "this is a test",
            },
            id="valid_payload",        
        ),
        pytest.param(
            {
                "id": uuid4(),
                "name": "test",
                "description": "this is a test",
            },
            id="payload_with_id",        
        ),
    ]
        
    @staticmethod
    @pytest.mark.parametrize(("attrs"), TABLE_CREATE_ORGANIZATION_FROM_REQUEST_VALID_CASES)
    def test_from_request(attrs):
        request = CreateOrganizationRequest.from_request(attrs)

        assert request.id == None
        assert request.name == attrs["name"] and request.description == attrs["description"]
    

    TABLE_CREATE_ORGANIZATION_REQUEST_VALIDATION_CASES = [
        pytest.param(
            {
                "description": "this is a test",
            },
            "missing fields in request payload",
            id="missing_description",        
        ),
        pytest.param(
            {
                "name": "test",
            },
            "missing fields in request payload",
            id="missing_name",        
        ),
        pytest.param(
            {},
            "missing fields in request payload",
            id="empty_payload",        
        ),
        pytest.param(
            {
                "name": "",
                "description": "this is a test"
            },
            "name does not meet length validations",
            id="name_empty",        
        ),
        pytest.param(
            {
                "name": "a-very-very-very-long-name",
                "description": "this is a test"
            },
            "name does not meet length validations",
            id="name_too_long",        
        ),
        pytest.param(
            {
                "name": "test",
                "description": ""
            },
            "description does not meet length validations",
            id="description_empty",        
        ),
        pytest.param(
            {
                "name": "test",
                "description": ''.join(random.choices(string.ascii_lowercase, k=105)),
            },
            "description does not meet length validations",
            id="description_too_long",        
        ),
    ]

    @staticmethod
    @pytest.mark.parametrize(("attrs", "expected_error_message"), TABLE_CREATE_ORGANIZATION_REQUEST_VALIDATION_CASES)
    def test_validations(attrs, expected_error_message):
        with pytest.raises(ValidationError) as exc:
            CreateOrganizationRequest.from_request(attrs)
        assert exc.value.description == expected_error_message