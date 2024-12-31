"""additional columns TBL_USER_INFO

Revision ID: 156ea44e90de
Revises: 0fa747e970a7
Create Date: 2024-12-31 11:42:52.516457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '156ea44e90de'
down_revision = '0fa747e970a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('TBL_USER_INFO', schema=None) as batch_op:
        batch_op.add_column(sa.Column('diet_description', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('nutrion_knowledge', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('guidance_needed', sa.String(), nullable=True))
        batch_op.drop_column('deit_description')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('TBL_USER_INFO', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deit_description', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('guidance_needed')
        batch_op.drop_column('nutrion_knowledge')
        batch_op.drop_column('diet_description')

    # ### end Alembic commands ###