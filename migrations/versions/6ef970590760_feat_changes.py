"""feat: changes

Revision ID: 6ef970590760
Revises: 99ec2a529fa0
Create Date: 2024-06-18 15:25:43.262780

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6ef970590760'
down_revision = '99ec2a529fa0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assigned_merchandisers', schema=None) as batch_op:
        batch_op.alter_column('merchandisers_id',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               type_=postgresql.JSONB(astext_type=sa.Text()),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assigned_merchandisers', schema=None) as batch_op:
        batch_op.alter_column('merchandisers_id',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               type_=postgresql.JSON(astext_type=sa.Text()),
               existing_nullable=False)

    # ### end Alembic commands ###
