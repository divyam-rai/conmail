"""add index on contacts organization id

Revision ID: b0640a5cdb73
Revises: 96f3a91fdd2b
Create Date: 2025-01-02 21:35:43.718346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0640a5cdb73'
down_revision: Union[str, None] = '96f3a91fdd2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('index_contacts_on_organization_id', 'contacts', ["organization_id"], if_not_exists=True)


def downgrade() -> None:
    op.drop_index('index_contacts_on_organization_id', 'contacts', if_exists=True)
