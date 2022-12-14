"""empty message

Revision ID: d2ff47f0f95e
Revises: a9a5ce9eaaf4
Create Date: 2022-11-21 17:23:07.399152

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd2ff47f0f95e'
down_revision = 'a9a5ce9eaaf4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tbl_games', schema=None) as batch_op:
        batch_op.add_column(sa.Column('match_date_timestamp', sa.TIMESTAMP(), nullable=True))
        batch_op.drop_column('match_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tbl_games', schema=None) as batch_op:
        batch_op.add_column(sa.Column('match_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
        batch_op.drop_column('match_date_timestamp')

    # ### end Alembic commands ###
