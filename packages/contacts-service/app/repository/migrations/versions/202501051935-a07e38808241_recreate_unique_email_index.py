"""recreate unique email index

Revision ID: a07e38808241
Revises: da737d2b010c
Create Date: 2025-01-05 19:35:11.381264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a07e38808241'
down_revision: Union[str, None] = 'da737d2b010c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index('index_unique_on_email_organization_id', "contacts", if_exists=True)
    op.create_index('index_unique_on_email_organization_id', "contacts", ["email", "organization_id"],  unique=True, if_not_exists=True)

def downgrade() -> None:
    op.drop_index('index_unique_on_email_organization_id', "contacts", if_exists=True)
    op.create_index('index_unique_on_email_organization_id', "contacts", ["email", "organization_id"], if_not_exists=True)
