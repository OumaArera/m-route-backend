"""update models

Revision ID: 3c8727d2e7ed
Revises: 549d2cc2223c
Create Date: 2024-06-11 17:10:35.038237

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3c8727d2e7ed'
down_revision = '549d2cc2223c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('periodic_performances')
    with op.batch_alter_table('assigned_merchandisers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('year', sa.Integer(), nullable=False))

    with op.batch_alter_table('responses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=10), nullable=False))
        batch_op.add_column(sa.Column('kpi_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'key_performance_indicators', ['kpi_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('responses', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('kpi_id')
        batch_op.drop_column('status')

    with op.batch_alter_table('assigned_merchandisers', schema=None) as batch_op:
        batch_op.drop_column('year')

    op.create_table('periodic_performances',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('merchandiser_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('merchandiser_performance_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('day', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.Column('week', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.Column('month', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.Column('year', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['merchandiser_id'], ['users.id'], name='periodic_performances_merchandiser_id_fkey'),
    sa.ForeignKeyConstraint(['merchandiser_performance_id'], ['merchandiser_performances.id'], name='periodic_performances_merchandiser_performance_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='periodic_performances_pkey')
    )
    # ### end Alembic commands ###
