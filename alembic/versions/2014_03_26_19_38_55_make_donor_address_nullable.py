"""Make donor address nullable

Revision ID: 579070c00568
Revises: 1f2296edbc75
Create Date: 2014-03-26 19:38:55.053479

"""

# revision identifiers, used by Alembic.
revision = '579070c00568'
down_revision = '1f2296edbc75'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('donor', 'address', nullable=True)


def downgrade():
    op.alter_column('donor', 'address', nullable=False)
