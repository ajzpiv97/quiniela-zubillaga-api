"""empty message

Revision ID: 0fdf8235cfed
Revises: d2ff47f0f95e
Create Date: 2022-11-21 18:17:24.516311

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0fdf8235cfed'
down_revision = 'd2ff47f0f95e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tbl_games', schema=None) as batch_op:
        batch_op.drop_column('match_date_timestamp')
        batch_op.add_column(sa.Column('match_date_timestamp', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tbl_games', schema=None) as batch_op:
        batch_op.alter_column('match_date_timestamp',
               existing_type=sa.Integer(),
               type_=postgresql.TIMESTAMP(),
               nullable=True)

    # ### end Alembic commands ###