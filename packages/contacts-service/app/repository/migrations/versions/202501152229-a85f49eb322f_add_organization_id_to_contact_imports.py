"""add organization id to contact imports

Revision ID: a85f49eb322f
Revises: 905b1ee44bb6
Create Date: 2025-01-15 22:29:56.372181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a85f49eb322f'
down_revision: Union[str, None] = '905b1ee44bb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('contact_imports', sa.Column('organization_id', sa.UUID, nullable=False))
    op.create_index('idx_contact_imports_on_organization_id', 'contact_imports', ['organization_id'], if_not_exists=True)


def downgrade() -> None:
    op.drop_index('idx_contact_imports_on_organization_id', 'contact_imports')
    op.drop_column('contact_imports', 'organization_id')
