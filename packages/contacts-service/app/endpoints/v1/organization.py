from flask import Blueprint, request
from uuid import UUID

from app.core.schemas.organization import CreateOrganizationRequest
from app.services.organization import OrganizationService
from app.core.helpers.utils import response
from app.core.errors.not_found import NotFound

organization_bp = Blueprint('organization_bp', __name__, url_prefix='/organizations')
organization_service = OrganizationService()

@organization_bp.route('/<id>', methods=["GET"])
def get_organization(id: UUID):
    organization = organization_service.get(id)
    if organization is None:
        raise NotFound('organization')
    return response(200, organization.to_dict())

@organization_bp.route('/', methods=["POST"])
def create_organization():
    body = request.json
    organization_request = CreateOrganizationRequest.from_request(body)
    organization = organization_service.create(organization_request)
    return response(201, organization.to_dict())

@organization_bp.route('/<id>', methods=["DELETE"])
def delete_organization(id: UUID):
    row_deleted = organization_service.delete(id)
    if not row_deleted:
        return response(409, { "error": "failed to delete organization" })
    return response(204)