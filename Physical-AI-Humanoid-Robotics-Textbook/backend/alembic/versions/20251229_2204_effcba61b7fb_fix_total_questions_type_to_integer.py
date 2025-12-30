"""fix_total_questions_type_to_integer

Revision ID: effcba61b7fb
Revises: a5b38b6b02e4
Create Date: 2025-12-29 22:04:49.793530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'effcba61b7fb'
down_revision: Union[str, None] = 'a5b38b6b02e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Change total_questions column type from VARCHAR to INTEGER
    # Using USING clause to cast existing string values to integers
    op.execute("""
        ALTER TABLE user_profiles
        ALTER COLUMN total_questions
        TYPE INTEGER
        USING total_questions::INTEGER
    """)

    # Update default value to 0 (integer)
    op.alter_column(
        'user_profiles',
        'total_questions',
        server_default='0'
    )


def downgrade() -> None:
    # Revert back to VARCHAR if needed (not recommended)
    op.execute("""
        ALTER TABLE user_profiles
        ALTER COLUMN total_questions
        TYPE VARCHAR
    """)

    op.alter_column(
        'user_profiles',
        'total_questions',
        server_default="'0'"
    )
