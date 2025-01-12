import os
from dotenv import load_dotenv

# Load dotenv files for local configuration
basedir = os.path.abspath(os.getcwd())
envfile_path = os.path.join(basedir, '.env')
if os.path.exists(envfile_path):
    load_dotenv(envfile_path)

# Configuration definition.
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_SCHEMA_REGISTRY_URL = os.environ.get("KAFKA_SCHEMA_REGISTRY_URL")
    KAFKA_TOPIC_CONTACTS = os.environ.get("KAFKA_TOPIC_CONTACTS")
    KAFKA_TOPIC_ORGANIZATIONS = os.environ.get("KAFKA_TOPIC_ORGANIZATIONS")

# class TestConfig(Config):
#     SQLALCHEMY_DATABASE_URI = "sqlite:///memory"
#     TESTING = True
#     PROPAGATE_EXCEPTIONS = True