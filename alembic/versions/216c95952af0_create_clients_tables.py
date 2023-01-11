"""Create clients tables

Revision ID: 216c95952af0
Revises: 0d86bbb0d929
Create Date: 2022-12-27 17:58:35.028182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '216c95952af0'
down_revision = '0d86bbb0d929'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nickname', sa.String(length=64), nullable=False, comment='Ник клиента'),
    sa.Column('comment', sa.Text(), nullable=True, comment='Комментарий'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clients_id'), 'clients', ['id'], unique=False)
    op.create_index(op.f('ix_clients_nickname'), 'clients', ['nickname'], unique=True)
    op.create_table('clients_nicknames',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nickname', sa.String(length=64), nullable=False, comment='Ник клиента'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clients_nicknames_id'), 'clients_nicknames', ['id'], unique=False)
    op.create_index(op.f('ix_clients_nicknames_nickname'), 'clients_nicknames', ['nickname'], unique=True)
    op.create_table('clients_urls',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False, comment='Ссылка на страницу клиента'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_index(op.f('ix_clients_urls_id'), 'clients_urls', ['id'], unique=False)
    op.create_table('client_client_urls',
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('url_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['url_id'], ['clients_urls.id'], ),
    sa.PrimaryKeyConstraint('client_id', 'url_id')
    )
    op.create_table('clients_clients_nicknames',
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('nickname_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['nickname_id'], ['clients_nicknames.id'], ),
    sa.PrimaryKeyConstraint('client_id', 'nickname_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clients_clients_nicknames')
    op.drop_table('client_client_urls')
    op.drop_index(op.f('ix_clients_urls_id'), table_name='clients_urls')
    op.drop_table('clients_urls')
    op.drop_index(op.f('ix_clients_nicknames_nickname'), table_name='clients_nicknames')
    op.drop_index(op.f('ix_clients_nicknames_id'), table_name='clients_nicknames')
    op.drop_table('clients_nicknames')
    op.drop_index(op.f('ix_clients_nickname'), table_name='clients')
    op.drop_index(op.f('ix_clients_id'), table_name='clients')
    op.drop_table('clients')
    # ### end Alembic commands ###