"""initialise contacts table

Revision ID: 973cb2945295
Revises: 
Create Date: 2025-01-01 14:37:19.030164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '973cb2945295'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;')

    op.create_table(
        'contacts',
        sa.Column('id', sa.UUID, primary_key=True, default="public.uuid_generate_v4()"),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True)),
        sa.Column('name_first', sa.String(50)),
        sa.Column('name_middle', sa.String(50)),
        sa.Column('name_last', sa.String(50)),
        sa.Column('address_street', sa.String(500)),
        sa.Column('address_city', sa.String(50)),
        sa.Column('address_country', sa.String(50)),
        sa.Column('address_zip', sa.Integer),
        if_not_exists= True,
    )

def downgrade() -> None:
    op.drop_table('contacts', if_exists= True)
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
