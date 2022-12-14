"""empty message

Revision ID: 1572fb6b53a5
Revises: 0fdf8235cfed
Create Date: 2022-11-30 20:38:25.417743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1572fb6b53a5'
down_revision = '0fdf8235cfed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbl_rounds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('round_name', sa.String(), nullable=False),
    sa.Column('round_start_datetime', sa.String(), nullable=False),
    sa.Column('round_start_timestamp', sa.Integer(), nullable=False),
    sa.Column('round_end_datetime', sa.String(), nullable=False),
    sa.Column('round_end_timestamp', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('tbl_games', schema=None) as batch_op:
        batch_op.add_column(sa.Column('round_id', sa.Integer(), nullable=True))
        batch_op.alter_column('match_date_timestamp',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.create_index(batch_op.f('ix_tbl_games_round_id'), ['round_id'], unique=False)
        batch_op.create_foreign_key(None, 'tbl_rounds', ['round_id'], ['id'])

    with op.batch_alter_table('tbl_predictions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prediction_insert_date', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('prediction_modified_date', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tbl_predictions', schema=None) as batch_op:
        batch_op.drop_column('prediction_modified_date')
        batch_op.drop_column('prediction_insert_date')

    with op.batch_alter_table('tbl_games', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_tbl_games_round_id'))
        batch_op.alter_column('match_date_timestamp',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('round_id')

    op.drop_table('tbl_rounds')
    # ### end Alembic commands ###
