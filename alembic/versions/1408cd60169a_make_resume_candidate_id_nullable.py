"""Make Resume candidate_id nullable

Revision ID: 1408cd60169a
Revises: 0a92b2217e1e
Create Date: 2026-07-11 23:01:04.482366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1408cd60169a'
down_revision: Union[str, Sequence[str], None] = '0a92b2217e1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('resumes', schema=None) as batch_op:
        batch_op.alter_column('candidate_id',
               existing_type=sa.INTEGER(),
               nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('resumes', schema=None) as batch_op:
        batch_op.alter_column('candidate_id',
               existing_type=sa.INTEGER(),
               nullable=False)
