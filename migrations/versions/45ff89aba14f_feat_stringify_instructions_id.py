"""feat: stringify instructions id

Revision ID: 45ff89aba14f
Revises: dc6b05e3b6d4
Create Date: 2024-06-20 13:14:36.793631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45ff89aba14f'
down_revision = 'dc6b05e3b6d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('responses', schema=None) as batch_op:
        batch_op.alter_column('instruction_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=200),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('responses', schema=None) as batch_op:
        batch_op.alter_column('instruction_id',
               existing_type=sa.String(length=200),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
