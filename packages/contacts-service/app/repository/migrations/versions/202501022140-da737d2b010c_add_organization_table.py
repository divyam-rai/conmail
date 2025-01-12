"""add_organization_table

Revision ID: da737d2b010c
Revises: b0640a5cdb73
Create Date: 2025-01-02 21:40:40.124785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da737d2b010c'
down_revision: Union[str, None] = 'b0640a5cdb73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'organizations',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.String(2000))
    )

    op.create_foreign_key('fk_contacts_organization_id', 'contacts', 'organizations', ["organization_id"], ["id"], ondelete="CASCADE")

def downgrade() -> None:
    op.drop_index('fk_contacts_organization_id', 'contacts')
    op.drop_table('organizations')
