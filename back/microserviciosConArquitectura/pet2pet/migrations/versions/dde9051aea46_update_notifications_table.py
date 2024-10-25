"""Update notifications table

Revision ID: dde9051aea46
Revises: 0af52691dad3
Create Date: 2024-10-25 18:40:50.664762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dde9051aea46'
down_revision: Union[str, None] = '0af52691dad3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notifications', sa.Column('message', sa.String(length=500), nullable=False))
    op.add_column('notifications', sa.Column('additional_data', sa.JSON(), nullable=True))
    op.add_column('notifications', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.drop_constraint('notifications_user_id_fkey', 'notifications', type_='foreignkey')
    op.create_foreign_key(op.f('fk_notifications_user_id_users'), 'notifications', 'users', ['user_id'], ['user_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_notifications_user_id_users'), 'notifications', type_='foreignkey')
    op.create_foreign_key('notifications_user_id_fkey', 'notifications', 'users', ['user_id'], ['user_id'])
    op.drop_column('notifications', 'updated_at')
    op.drop_column('notifications', 'additional_data')
    op.drop_column('notifications', 'message')
    # ### end Alembic commands ###
