"""Change username to fio in clients

Revision ID: e106f2e976b0
Revises: ea44ca41c1a2
Create Date: 2023-01-11 11:33:15.374185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e106f2e976b0'
down_revision = 'ea44ca41c1a2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clients', sa.Column('fio', sa.String(length=64), server_default='', nullable=False, comment='ФИО клиента'))
    op.drop_index('ix_clients_nickname', table_name='clients')
    op.drop_column('clients', 'nickname')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clients', sa.Column('nickname', sa.VARCHAR(length=64), autoincrement=False, nullable=False, comment='Ник клиента'))
    op.create_index('ix_clients_nickname', 'clients', ['nickname'], unique=False)
    op.drop_column('clients', 'fio')
    # ### end Alembic commands ###
