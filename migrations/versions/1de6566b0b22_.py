"""empty message

Revision ID: 1de6566b0b22
Revises: None
Create Date: 2015-06-18 17:06:48.075821

"""

# revision identifiers, used by Alembic.
revision = '1de6566b0b22'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('addresses',
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('address1', sa.String(length=50), nullable=False),
    sa.Column('address2', sa.String(length=50), nullable=True),
    sa.Column('city', sa.String(length=25), nullable=False),
    sa.Column('state', sa.String(length=25), nullable=False),
    sa.Column('country', sa.String(length=50), nullable=False),
    sa.Column('zip', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('address_id')
    )
    op.create_table('images',
    sa.Column('img_id', sa.Integer(), nullable=False),
    sa.Column('img_name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('img_id')
    )
    op.create_table('galleries',
    sa.Column('gallery_id', sa.Integer(), nullable=False),
    sa.Column('image_1', sa.Integer(), nullable=False),
    sa.Column('image_2', sa.Integer(), nullable=False),
    sa.Column('image_3', sa.Integer(), nullable=False),
    sa.Column('image_4', sa.Integer(), nullable=False),
    sa.Column('image_5', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['image_1'], ['images.img_id'], ),
    sa.ForeignKeyConstraint(['image_2'], ['images.img_id'], ),
    sa.ForeignKeyConstraint(['image_3'], ['images.img_id'], ),
    sa.ForeignKeyConstraint(['image_4'], ['images.img_id'], ),
    sa.ForeignKeyConstraint(['image_5'], ['images.img_id'], ),
    sa.PrimaryKeyConstraint('gallery_id')
    )
    op.create_table('users',
    sa.Column('username', sa.String(length=15), nullable=False),
    sa.Column('img_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('pass_hash', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['img_id'], ['images.img_id'], ),
    sa.PrimaryKeyConstraint('username')
    )
    op.create_table('cards',
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=15), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('gallery_id', sa.Integer(), nullable=True),
    sa.Column('logo_id', sa.Integer(), nullable=True),
    sa.Column('position', sa.String(length=50), nullable=False),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('phone_num', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['addresses.address_id'], ),
    sa.ForeignKeyConstraint(['gallery_id'], ['galleries.gallery_id'], ),
    sa.ForeignKeyConstraint(['logo_id'], ['images.img_id'], ),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ),
    sa.PrimaryKeyConstraint('card_id')
    )
    op.create_table('companies',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('logo_id', sa.Integer(), nullable=True),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('gallery_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('phone_num', sa.String(length=30), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['addresses.address_id'], ),
    sa.ForeignKeyConstraint(['gallery_id'], ['galleries.gallery_id'], ),
    sa.ForeignKeyConstraint(['logo_id'], ['images.img_id'], ),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('userdir',
    sa.Column('userdir_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=15), nullable=False),
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('notes', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['addresses.address_id'], ),
    sa.ForeignKeyConstraint(['card_id'], ['cards.card_id'], ),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ),
    sa.PrimaryKeyConstraint('userdir_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userdir')
    op.drop_table('companies')
    op.drop_table('cards')
    op.drop_table('users')
    op.drop_table('galleries')
    op.drop_table('images')
    op.drop_table('addresses')
    ### end Alembic commands ###