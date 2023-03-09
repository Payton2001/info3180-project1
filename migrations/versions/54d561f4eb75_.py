"""empty message

Revision ID: 54d561f4eb75
Revises: 319ef2d56e4e
Create Date: 2023-03-09 12:18:51.421063

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '54d561f4eb75'
down_revision = '319ef2d56e4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('property_profiles', schema=None) as batch_op:
        batch_op.alter_column('property_photo',
               existing_type=postgresql.BYTEA(),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('property_profiles', schema=None) as batch_op:
        batch_op.alter_column('property_photo',
               existing_type=sa.String(length=255),
               type_=postgresql.BYTEA(),
               existing_nullable=True)

    # ### end Alembic commands ###
