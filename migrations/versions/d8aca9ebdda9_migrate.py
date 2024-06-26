"""migrate

Revision ID: d8aca9ebdda9
Revises: 3b14489646c2
Create Date: 2024-06-24 21:31:42.692251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8aca9ebdda9'
down_revision = '3b14489646c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('replies_',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('manager_id', sa.Integer(), nullable=False),
    sa.Column('merchandiser_id', sa.Integer(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('reply', sa.Text(), nullable=False),
    sa.Column('sender', sa.String(length=10), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.ForeignKeyConstraint(['manager_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['merchandiser_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('replies')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('replies',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('manager_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('merchandiser_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('message_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('reply', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['manager_id'], ['users.id'], name='replies_manager_id_fkey'),
    sa.ForeignKeyConstraint(['merchandiser_id'], ['users.id'], name='replies_merchandiser_id_fkey'),
    sa.ForeignKeyConstraint(['message_id'], ['messages.id'], name='replies_message_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='replies_pkey')
    )
    op.drop_table('replies_')
    # ### end Alembic commands ###
