"""make_job_description_recruiter_id_nullable

Revision ID: abe0a993c883
Revises: 1408cd60169a
Create Date: 2026-07-12 16:03:06.587905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abe0a993c883'
down_revision: Union[str, Sequence[str], None] = '1408cd60169a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('job_descriptions', schema=None) as batch_op:
        batch_op.alter_column('recruiter_id',
               existing_type=sa.INTEGER(),
               nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('job_descriptions', schema=None) as batch_op:
        batch_op.alter_column('recruiter_id',
               existing_type=sa.INTEGER(),
               nullable=False)
