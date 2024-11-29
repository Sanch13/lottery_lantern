"""Initial migration

Revision ID: 3b8a909bef56
Revises: 
Create Date: 2024-11-25 11:03:54.396389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b8a909bef56'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lotteries',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('create', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_lotteries_id'), 'lotteries', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('telegram_id', sa.BigInteger(), nullable=True),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('full_name_from_tg', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_telegram_id'), 'users', ['telegram_id'], unique=True)
    op.create_table('tickets',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('ticket_number', sa.Integer(), nullable=False),
    sa.Column('create', sa.DateTime(), nullable=True),
    sa.Column('lottery_id', sa.BigInteger(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['lottery_id'], ['lotteries.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'lottery_id', name='unique_ticket_per_lottery')
    )
    op.create_index(op.f('ix_tickets_id'), 'tickets', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tickets_id'), table_name='tickets')
    op.drop_table('tickets')
    op.drop_index(op.f('ix_users_telegram_id'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_lotteries_id'), table_name='lotteries')
    op.drop_table('lotteries')
    # ### end Alembic commands ###
