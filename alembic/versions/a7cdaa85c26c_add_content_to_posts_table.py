"""add content to posts table

Revision ID: a7cdaa85c26c
Revises: 71a9cea82dd7
Create Date: 2023-02-03 23:10:28.003321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7cdaa85c26c'
down_revision = 'f3cdcf71df32'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
