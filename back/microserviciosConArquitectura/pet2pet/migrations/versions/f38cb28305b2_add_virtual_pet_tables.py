"""Add virtual pet tables

Revision ID: f38cb28305b2
Revises: dde9051aea46
Create Date: 2024-10-28 13:22:46.067688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f38cb28305b2'
down_revision: Union[str, None] = 'dde9051aea46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('virtual_pets',
    sa.Column('virtual_pet_id', sa.Integer(), nullable=False),
    sa.Column('pet_id', sa.Integer(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('experience_points', sa.Integer(), nullable=True),
    sa.Column('happiness', sa.Float(), nullable=True),
    sa.Column('energy', sa.Float(), nullable=True),
    sa.Column('last_interaction', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('attributes', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['pet_id'], ['pets.pet_id'], name=op.f('fk_virtual_pets_pet_id_pets'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('virtual_pet_id', name=op.f('pk_virtual_pets'))
    )
    op.create_table('virtual_pet_achievements',
    sa.Column('achievement_id', sa.Integer(), nullable=False),
    sa.Column('virtual_pet_id', sa.Integer(), nullable=True),
    sa.Column('achievement_type', sa.String(length=50), nullable=True),
    sa.Column('unlocked_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('rewards', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['virtual_pet_id'], ['virtual_pets.virtual_pet_id'], name=op.f('fk_virtual_pet_achievements_virtual_pet_id_virtual_pets'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('achievement_id', name=op.f('pk_virtual_pet_achievements'))
    )
    op.create_table('virtual_pet_activities',
    sa.Column('activity_id', sa.Integer(), nullable=False),
    sa.Column('virtual_pet_id', sa.Integer(), nullable=True),
    sa.Column('activity_type', sa.String(length=50), nullable=True),
    sa.Column('points_earned', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('details', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['virtual_pet_id'], ['virtual_pets.virtual_pet_id'], name=op.f('fk_virtual_pet_activities_virtual_pet_id_virtual_pets'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('activity_id', name=op.f('pk_virtual_pet_activities'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('virtual_pet_activities')
    op.drop_table('virtual_pet_achievements')
    op.drop_table('virtual_pets')
    # ### end Alembic commands ###