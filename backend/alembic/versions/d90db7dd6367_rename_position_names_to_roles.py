"""rename position_names to roles

Revision ID: d90db7dd6367
Revises: e25885fc4401
Create Date: 2026-07-12 09:52:06.392173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd90db7dd6367'
down_revision: Union[str, None] = 'e25885fc4401'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('position_names', 'roles')
    op.alter_column('users', 'position_id', new_column_name='role_id')
    op.drop_constraint('users_position_id_fkey', 'users', type_='foreignkey')
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.alter_column('users', 'role_id', new_column_name='position_id')
    op.create_foreign_key('users_position_id_fkey', 'users', 'position_names', ['position_id'], ['id'])
    op.rename_table('roles', 'position_names')
