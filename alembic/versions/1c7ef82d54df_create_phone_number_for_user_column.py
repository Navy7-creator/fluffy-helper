"""Create phone number for user column

Revision ID: 1c7ef82d54df
Revises: 
Create Date: 2026-08-30 19:06:51.860970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c7ef82d54df'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(length=20), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')


