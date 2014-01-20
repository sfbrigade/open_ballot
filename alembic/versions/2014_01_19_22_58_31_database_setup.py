"""Database setup

Revision ID: 7417382a3f1
Revises: None
Create Date: 2014-01-19 22:58:31.952424

"""

# revision identifiers, used by Alembic.
revision = '7417382a3f1'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')


def downgrade():
    pass
