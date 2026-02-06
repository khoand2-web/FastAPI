"""add_created_at_to_cart_items

Revision ID: c7830ace38a4
Revises: 
Create Date: 2026-02-06 10:13:17.849687

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'c7830ace38a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add created_at column to cart_items table
    op.add_column('cart_items', 
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('NOW()'))
    )


def downgrade() -> None:
    # Remove created_at column from cart_items table
    op.drop_column('cart_items', 'created_at')
