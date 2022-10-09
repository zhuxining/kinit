"""update

Revision ID: 203b11efd025
Revises: 1d13c64e1444
Create Date: 2022-10-05 21:43:34.894121

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '203b11efd025'
down_revision = '1d13c64e1444'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vadmin_system_dict_details', sa.Column('label', sa.String(length=50), nullable=False, comment='字典标签'))
    op.add_column('vadmin_system_dict_details', sa.Column('value', sa.String(length=50), nullable=False, comment='字典键值'))
    op.drop_index('ix_vadmin_system_dict_details_dict_label', table_name='vadmin_system_dict_details')
    op.drop_index('ix_vadmin_system_dict_details_dict_value', table_name='vadmin_system_dict_details')
    op.create_index(op.f('ix_vadmin_system_dict_details_label'), 'vadmin_system_dict_details', ['label'], unique=False)
    op.create_index(op.f('ix_vadmin_system_dict_details_value'), 'vadmin_system_dict_details', ['value'], unique=False)
    op.drop_column('vadmin_system_dict_details', 'dict_label')
    op.drop_column('vadmin_system_dict_details', 'dict_value')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vadmin_system_dict_details', sa.Column('dict_value', mysql.VARCHAR(length=50), nullable=False, comment='字典键值'))
    op.add_column('vadmin_system_dict_details', sa.Column('dict_label', mysql.VARCHAR(length=50), nullable=False, comment='字典标签'))
    op.drop_index(op.f('ix_vadmin_system_dict_details_value'), table_name='vadmin_system_dict_details')
    op.drop_index(op.f('ix_vadmin_system_dict_details_label'), table_name='vadmin_system_dict_details')
    op.create_index('ix_vadmin_system_dict_details_dict_value', 'vadmin_system_dict_details', ['dict_value'], unique=False)
    op.create_index('ix_vadmin_system_dict_details_dict_label', 'vadmin_system_dict_details', ['dict_label'], unique=False)
    op.drop_column('vadmin_system_dict_details', 'value')
    op.drop_column('vadmin_system_dict_details', 'label')
    # ### end Alembic commands ###