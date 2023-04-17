"""Create message table

Revision ID: ae60bb5bb235
Revises: d0b371e769d6
Create Date: 2023-04-17 23:03:08.910388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ae60bb5bb235"
down_revision = "d0b371e769d6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "message",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "created_at",
            sa.DateTime,
            nullable=False,
            server_default=sa.sql.expression.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("role", sa.String(20), nullable=False),
        sa.CheckConstraint(
            "role IN ('user', 'system', 'assistant')", name="message_role_check"
        ),
        sa.Column("name", sa.String(100), nullable=True),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column(
            "conversation_id",
            sa.Integer,
            sa.ForeignKey("conversation.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("message")
