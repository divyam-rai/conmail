from flask import Flask

from app.db import db
from app.endpoints.v1.contact import contact_bp
from app.endpoints.v1.organization import organization_bp

from pytest import set_trace

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)

    app.register_blueprint(contact_bp)
    app.register_blueprint(organization_bp)

    return app