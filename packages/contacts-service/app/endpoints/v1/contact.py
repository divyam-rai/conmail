from flask import Blueprint, request
from app.core.schemas.contact import CreateContactRequest, CreateContactImportRequest
from uuid import UUID

from app.core.errors.not_found import NotFound
from app.core.errors.validation_error import ValidationError
from app.core.helpers.utils import response

from app.core.schemas import contact
from app.services.contact import ContactService

contact_bp = Blueprint("contact_bp", __name__, url_prefix="/contacts")
contact_service = ContactService()

@contact_bp.route("/<id>", methods=["GET"])
def get_contact(id: UUID):
    contact = contact_service.get(id)
    if contact is None:
        raise NotFound('contact')
    return response(200, contact.to_dict())

@contact_bp.route("/", methods=["POST"])
def create_contact():
    contact_request = CreateContactRequest.from_request(request.json)
    contact = contact_service.create(contact_request)
    return response(201, contact.to_dict())

@contact_bp.route("/<id>", methods=["DELETE"])
def delete_contact(id: UUID):
    row_deleted = contact_service.delete(id)
    if not row_deleted:
        return response(409, { "error": "failed to delete organization" })
    return response(204)

@contact_bp.route("/import/request", methods=["POST"])
def request_contacts_import():    
    contact_import_request = CreateContactImportRequest.from_request(request.json)
    contact_import = contact_service.request_import(contact_import_request)
    return response(200, contact_import.to_dict())
