"""Asociamos los prestamos con los pagos

Revision ID: 6b3e19a9a317
Revises: 8575c3328b35
Create Date: 2024-11-29 09:50:38.465566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b3e19a9a317'
down_revision = '8575c3328b35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pago_deduccion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pago_id', sa.Integer(), nullable=False),
    sa.Column('deduccion_id', sa.Integer(), nullable=False),
    sa.Column('monto_pagado', sa.Float(), nullable=False),
    sa.Column('cuotas_restantes', sa.Integer(), nullable=False),
    sa.Column('fecha_pago', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['deduccion_id'], ['deducible.id'], ),
    sa.ForeignKeyConstraint(['pago_id'], ['ganancia.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pago_deduccion')
    # ### end Alembic commands ###
