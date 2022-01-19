"""test revert

Revision ID: af9dacd59be3
Revises: 706ea55f30ef
Create Date: 2022-01-18 21:22:38.205365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af9dacd59be3'
down_revision = '706ea55f30ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('first', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'first')
    # ### end Alembic commands ###