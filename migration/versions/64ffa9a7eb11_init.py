"""init

Revision ID: 64ffa9a7eb11
Revises: 
Create Date: 2025-03-26 15:59:26.759316

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64ffa9a7eb11'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('customer_id', name=op.f('pk_customer')),
    sa.UniqueConstraint('email', name=op.f('uq_customer_email')),
    schema='public'
    )
    op.create_table('product',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('product_id', name=op.f('pk_product')),
    schema='public'
    )
    op.create_table('order',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['public.customer.customer_id'], name=op.f('fk_order_customer_id_customer')),
    sa.PrimaryKeyConstraint('order_id', name=op.f('pk_order')),
    schema='public'
    )
    op.create_table('order_item',
    sa.Column('order_item_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('subtotal', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['public.order.order_id'], name=op.f('fk_order_item_order_id_order')),
    sa.ForeignKeyConstraint(['product_id'], ['public.product.product_id'], name=op.f('fk_order_item_product_id_product')),
    sa.PrimaryKeyConstraint('order_item_id', name=op.f('pk_order_item')),
    schema='public'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_item', schema='public')
    op.drop_table('order', schema='public')
    op.drop_table('product', schema='public')
    op.drop_table('customer', schema='public')
    # ### end Alembic commands ###
