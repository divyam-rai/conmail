"""add contact import requests

Revision ID: 905b1ee44bb6
Revises: a07e38808241
Create Date: 2025-01-15 22:10:54.432675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '905b1ee44bb6'
down_revision: Union[str, None] = 'a07e38808241'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'contact_imports',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('file_name', sa.String(50), nullable=False),
        sa.Column('status', sa.Enum('CREATED', 'UPLOADED', 'PROCESSING', 'ERRED', name='ContactImportStatus'), nullable=False, default='CREATED'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)),
    )

def downgrade() -> None:
    op.drop_table('contact_imports')
