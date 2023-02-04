"""add user table

Revision ID: 818baba08c05
Revises: a7cdaa85c26c
Create Date: 2023-02-03 23:23:31.228043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '818baba08c05'
down_revision = 'a7cdaa85c26c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
