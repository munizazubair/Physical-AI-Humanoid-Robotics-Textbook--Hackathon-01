"""recreate_user_profiles_with_correct_types

Revision ID: 104c72557adf
Revises: effcba61b7fb
Create Date: 2025-12-29 22:14:49.740758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '104c72557adf'
down_revision: Union[str, None] = 'effcba61b7fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the existing user_profiles table (no data loss since table is empty)
    op.execute("DROP INDEX IF EXISTS ix_user_profiles_session_id")
    op.drop_table('user_profiles')

    # Recreate with correct types
    # Create enum type if it doesn't exist
    from sqlalchemy.dialects.postgresql import ENUM
    knowledge_level_enum = ENUM('BEGINNER', 'INTERMEDIATE', 'ADVANCED', name='knowledgelevel', create_type=False)

    op.create_table(
        'user_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('interests', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('knowledge_level', knowledge_level_enum, nullable=False),
        sa.Column('visited_chapters', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('total_questions', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['user_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_profiles_session_id'), 'user_profiles', ['session_id'], unique=True)


def downgrade() -> None:
    # Revert to old schema if needed
    op.drop_index(op.f('ix_user_profiles_session_id'), table_name='user_profiles')
    op.drop_table('user_profiles')

    # Recreate with old VARCHAR type
    op.create_table(
        'user_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('interests', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('knowledge_level', sa.Enum('BEGINNER', 'INTERMEDIATE', 'ADVANCED', name='knowledgelevel'), nullable=False),
        sa.Column('visited_chapters', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('total_questions', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['user_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_profiles_session_id'), 'user_profiles', ['session_id'], unique=True)
