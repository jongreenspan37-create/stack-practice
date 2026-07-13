"""test ownership

Revision ID: 00e35e71ea01
Revises: d90db7dd6367
Create Date: 2026-07-12 10:37:05.669948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00e35e71ea01'
down_revision: Union[str, None] = 'd90db7dd6367'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
