"""Create history table

Revision ID: d0b371e769d6
Revises:
Create Date: 2023-04-16 14:06:35.034242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d0b371e769d6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "conversation",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "created_at",
            sa.DateTime,
            nullable=False,
            server_default=sa.sql.expression.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_table(
        "history",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("value", sa.String, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime,
            nullable=False,
            server_default=sa.sql.expression.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "conversation_id",
            sa.Integer,
            sa.ForeignKey("conversation.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("history")
    op.drop_table("conversation")
