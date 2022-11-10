"""empty message

Revision ID: 8f8a5308a749
Revises: 
Create Date: 2022-11-09 22:22:10.913881

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8f8a5308a749'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbl_games',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('team_a', sa.String(), nullable=False),
    sa.Column('team_b', sa.String(), nullable=False),
    sa.Column('score', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tbl_games_date'), 'tbl_games', ['date'], unique=False)
    op.create_index(op.f('ix_tbl_games_id'), 'tbl_games', ['id'], unique=False)
    op.create_table('tbl_users',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.Column('total_points', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_tbl_users_id'), 'tbl_users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tbl_users_id'), table_name='tbl_users')
    op.drop_table('tbl_users')
    op.drop_index(op.f('ix_tbl_games_id'), table_name='tbl_games')
    op.drop_index(op.f('ix_tbl_games_date'), table_name='tbl_games')
    op.drop_table('tbl_games')
    # ### end Alembic commands ###