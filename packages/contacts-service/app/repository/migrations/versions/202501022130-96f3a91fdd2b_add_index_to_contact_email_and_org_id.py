"""add index to contact email and org id

Revision ID: 96f3a91fdd2b
Revises: 973cb2945295
Create Date: 2025-01-02 21:30:13.088467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '96f3a91fdd2b'
down_revision: Union[str, None] = '973cb2945295'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column(
        'contacts',
        sa.Column('organization_id', sa.UUID, nullable=False)
    )
    op.create_index('index_unique_on_email_organization_id', "contacts", ["email", "organization_id"], if_not_exists=True)


def downgrade() -> None:
    op.drop_index("index_unique_on_email_organization_id", "contacts", if_exists=True)
    op.drop_column('contacts', 'organization_id')