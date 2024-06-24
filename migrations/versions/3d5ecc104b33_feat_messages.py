"""feat: messages

Revision ID: 3d5ecc104b33
Revises: 3dab9d3afa8d
Create Date: 2024-06-24 14:25:13.478412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d5ecc104b33'
down_revision = '3dab9d3afa8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('manager_id', sa.Integer(), nullable=False),
    sa.Column('merchandiser_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.ForeignKeyConstraint(['manager_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['merchandiser_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('notifications_')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications_',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('manager_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('merchandiser_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('message', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['manager_id'], ['users.id'], name='notifications__manager_id_fkey'),
    sa.ForeignKeyConstraint(['merchandiser_id'], ['users.id'], name='notifications__merchandiser_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='notifications__pkey')
    )
    op.drop_table('messages')
    # ### end Alembic commands ###