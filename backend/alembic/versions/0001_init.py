"""initial schema

Revision ID: 0001_init
Revises: 
Create Date: 2025-12-12
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="nurse"),
        sa.Column("totp_secret", sa.String(length=64), nullable=False),
        sa.Column("backup_codes", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "evaluations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("evaluator_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("evaluatee_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("status", sa.String(length=50), server_default="draft"),
        sa.Column("scores", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("total_score", sa.String(length=10), nullable=True),
        sa.Column("classification", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("evaluations")
    op.drop_table("users")
