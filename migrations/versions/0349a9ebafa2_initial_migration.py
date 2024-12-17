"""Initial migration

Revision ID: 0349a9ebafa2
Revises: 
Create Date: 2024-12-16 23:09:54.124148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0349a9ebafa2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('TBL_APP_USERS',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=70), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('TBL_STAGING',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=70), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('TBL_TOKENS',
    sa.Column('token_id', sa.Integer(), nullable=False),
    sa.Column('request_type', sa.String(), nullable=True),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['TBL_APP_USERS.user_id'], name=op.f('fk_TBL_TOKENS_user_id_TBL_APP_USERS')),
    sa.PrimaryKeyConstraint('token_id'),
    sa.UniqueConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('TBL_TOKENS')
    op.drop_table('TBL_STAGING')
    op.drop_table('TBL_APP_USERS')
    # ### end Alembic commands ###
