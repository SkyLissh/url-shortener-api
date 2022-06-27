"""Create URL table

Revision ID: 046fb539753a
Revises: 
Create Date: 2022-06-26 00:50:16.277236

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '046fb539753a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('urls',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('url', sa.String(length=10), nullable=True),
    sa.Column('admin_url', sa.String(length=10), nullable=True),
    sa.Column('target_url', sa.String(length=255), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('clicks', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_urls_admin_url'), 'urls', ['admin_url'], unique=True)
    op.create_index(op.f('ix_urls_target_url'), 'urls', ['target_url'], unique=True)
    op.create_index(op.f('ix_urls_url'), 'urls', ['url'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_urls_url'), table_name='urls')
    op.drop_index(op.f('ix_urls_target_url'), table_name='urls')
    op.drop_index(op.f('ix_urls_admin_url'), table_name='urls')
    op.drop_table('urls')
    # ### end Alembic commands ###