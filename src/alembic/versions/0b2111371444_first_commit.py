"""first commit

Revision ID: 0b2111371444
Revises: 
Create Date: 2022-01-18 21:20:43.865439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b2111371444'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teachers',
    sa.Column('tid', sa.String(length=16), nullable=False),
    sa.Column('first', sa.String(length=255), nullable=True),
    sa.Column('last', sa.String(length=255), nullable=True),
    sa.Column('school', sa.String(length=4), nullable=True),
    sa.PrimaryKeyConstraint('tid'),
    mysql_engine='InnoDB'
    )
    op.create_table('users',
    sa.Column('uid', sa.String(length=36), nullable=False),
    sa.Column('gid', sa.String(length=255), nullable=True),
    sa.Column('first', sa.String(length=255), nullable=True),
    sa.Column('last', sa.String(length=255), nullable=True),
    sa.Column('school', sa.String(length=4), nullable=True),
    sa.Column('grade', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('gid'),
    mysql_engine='InnoDB'
    )
    op.create_table('classes',
    sa.Column('tid', sa.String(length=16), nullable=False),
    sa.Column('block', sa.String(length=8), nullable=False),
    sa.Column('uid', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['tid'], ['teachers.tid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['uid'], ['users.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('tid', 'block', 'uid')
    )
    op.create_table('sessions',
    sa.Column('sid', sa.String(length=16), nullable=False),
    sa.Column('uid', sa.String(length=36), nullable=False),
    sa.Column('last_accessed', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['users.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('sid', 'uid'),
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sessions')
    op.drop_table('classes')
    op.drop_table('users')
    op.drop_table('teachers')
    # ### end Alembic commands ###