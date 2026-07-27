"""refine_data_models

Revision ID: 29f28f934f49
Revises: abe0a993c883
Create Date: 2026-07-12 16:21:20.302405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29f28f934f49'
down_revision: Union[str, Sequence[str], None] = 'abe0a993c883'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Add new columns to resumes as nullable first
    with op.batch_alter_table('resumes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('original_filename', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('file_type', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('uploaded_at', sa.DateTime(), nullable=True))

    # 2. Add new JSON column to scan_results
    with op.batch_alter_table('scan_results', schema=None) as batch_op:
        batch_op.add_column(sa.Column('analysis_metadata', sa.JSON(), nullable=True))

    # 3. Backfill resumes data
    conn = op.get_bind()
    conn.execute(sa.text("UPDATE resumes SET uploaded_at = created_at WHERE uploaded_at IS NULL"))
    conn.execute(sa.text("UPDATE resumes SET original_filename = 'legacy_resume.pdf' WHERE original_filename IS NULL"))
    conn.execute(sa.text("UPDATE resumes SET file_type = 'pdf' WHERE file_type IS NULL"))

    # 4. Enforce nullable=False on resumes.uploaded_at
    with op.batch_alter_table('resumes', schema=None) as batch_op:
        batch_op.alter_column('uploaded_at',
               existing_type=sa.DateTime(),
               nullable=False)

    # 5. Migrate candidate-created job descriptions (recruiter_id IS NULL)
    conn.execute(sa.text("""
        UPDATE job_descriptions
        SET recruiter_id = COALESCE(
            (
                SELECT r.candidate_id
                FROM scan_results sr
                JOIN resumes r ON sr.resume_id = r.id
                WHERE sr.job_description_id = job_descriptions.id
                LIMIT 1
            ),
            (SELECT id FROM users LIMIT 1)
        )
        WHERE recruiter_id IS NULL
    """))

    # 6. Rename recruiter_id to owner_id on job_descriptions and set nullable=False
    with op.batch_alter_table('job_descriptions', schema=None) as batch_op:
        batch_op.alter_column('recruiter_id',
               new_column_name='owner_id',
               existing_type=sa.INTEGER(),
               nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Rename owner_id back to recruiter_id and set nullable=True
    with op.batch_alter_table('job_descriptions', schema=None) as batch_op:
        batch_op.alter_column('owner_id',
               new_column_name='recruiter_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # 2. Drop JSON column from scan_results
    with op.batch_alter_table('scan_results', schema=None) as batch_op:
        batch_op.drop_column('analysis_metadata')

    # 3. Drop columns from resumes
    with op.batch_alter_table('resumes', schema=None) as batch_op:
        batch_op.drop_column('uploaded_at')
        batch_op.drop_column('file_type')
        batch_op.drop_column('original_filename')
