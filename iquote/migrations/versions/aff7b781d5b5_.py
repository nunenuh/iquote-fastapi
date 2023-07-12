"""empty message

Revision ID: aff7b781d5b5
Revises: 22589fee036f
Create Date: 2023-07-11 07:06:23.742872

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "aff7b781d5b5"
down_revision = "22589fee036f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_like_quote",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("quote_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["quote_id"],
            ["quote.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "quote_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_like_quote")
    # ### end Alembic commands ###
