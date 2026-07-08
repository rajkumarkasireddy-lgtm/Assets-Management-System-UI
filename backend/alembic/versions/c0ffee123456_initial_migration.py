"""initial_migration

Revision ID: c0ffee123456
Revises: 
Create Date: 2026-07-08 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c0ffee123456'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('display_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('department', sa.String(), nullable=True),
        sa.Column('designation', sa.String(), nullable=True),
        sa.Column('manager', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='Active'),
        sa.Column('avatar', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('join_date', sa.String(), nullable=True),
        sa.Column('must_change_password', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('allocation_date', sa.String(), nullable=True),
        sa.Column('allocation_time', sa.String(), nullable=True),
        sa.Column('allocation_status', sa.String(), nullable=True),
        sa.Column('required_asset_category', sa.String(), nullable=True),
        sa.Column('allocated_asset_details', sa.JSON(), nullable=True),
        sa.Column('allocation_history', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_display_id'), 'users', ['display_id'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # 2. Create assets table
    op.create_table(
        'assets',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('display_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('manufacturer', sa.String(), nullable=False),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('serial', sa.String(), nullable=False),
        sa.Column('purchase_date', sa.String(), nullable=False),
        sa.Column('warranty_expiry', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('assigned_to_id', sa.UUID(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('cost', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['assigned_to_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assets_display_id'), 'assets', ['display_id'], unique=True)
    op.create_index(op.f('ix_assets_serial'), 'assets', ['serial'], unique=True)

    # 3. Create tickets table
    op.create_table(
        'tickets',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('display_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('priority', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_by_id', sa.UUID(), nullable=False),
        sa.Column('assignee_id', sa.UUID(), nullable=True),
        sa.Column('asset_id', sa.UUID(), nullable=True),
        sa.Column('sla', sa.String(), nullable=False),
        sa.Column('support_resolution', sa.Text(), nullable=True),
        sa.Column('admin_remarks', sa.Text(), nullable=True),
        sa.Column('asset_action', sa.String(), nullable=True),
        sa.Column('asset_details', sa.Text(), nullable=True),
        sa.Column('asset_remarks', sa.Text(), nullable=True),
        sa.Column('asset_resolution', sa.Text(), nullable=True),
        sa.Column('assigned_role', sa.String(), nullable=True),
        sa.Column('timeline', sa.JSON(), nullable=True),
        sa.Column('audit_trail', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['assignee_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tickets_display_id'), 'tickets', ['display_id'], unique=True)

    # 4. Create ticket_comments table
    op.create_table(
        'ticket_comments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('ticket_id', sa.UUID(), nullable=False),
        sa.Column('author_name', sa.String(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 5. Create assignments table
    op.create_table(
        'assignments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('display_id', sa.String(), nullable=False),
        sa.Column('asset_id', sa.UUID(), nullable=False),
        sa.Column('employee_id', sa.UUID(), nullable=False),
        sa.Column('assigned_date', sa.String(), nullable=False),
        sa.Column('return_date', sa.String(), nullable=True),
        sa.Column('expected_return', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['employee_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assignments_display_id'), 'assignments', ['display_id'], unique=True)

    # 6. Create vendors table
    op.create_table(
        'vendors',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('display_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('contact', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('contract_end', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vendors_display_id'), 'vendors', ['display_id'], unique=True)

    # 7. Create maintenance table
    op.create_table(
        'maintenance',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('display_id', sa.String(), nullable=False),
        sa.Column('asset_id', sa.UUID(), nullable=False),
        sa.Column('engineer', sa.String(), nullable=False),
        sa.Column('date', sa.String(), nullable=False),
        sa.Column('resolution', sa.Text(), nullable=False),
        sa.Column('parts', sa.String(), nullable=False),
        sa.Column('cost', sa.Float(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_maintenance_display_id'), 'maintenance', ['display_id'], unique=True)

    # 8. Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('display_id', sa.String(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('user', sa.String(), nullable=False),
        sa.Column('target', sa.String(), nullable=False),
        sa.Column('timestamp', sa.String(), nullable=False),
        sa.Column('ip', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_display_id'), 'audit_logs', ['display_id'], unique=True)

    # 9. Create notifications table
    op.create_table(
        'notifications',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False, server_default='info'),
        sa.Column('time', sa.String(), nullable=False),
        sa.Column('unread', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 10. Create knowledge_base table
    op.create_table(
        'knowledge_base',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('display_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('views', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_base_display_id'), 'knowledge_base', ['display_id'], unique=True)


def downgrade() -> None:
    op.drop_table('knowledge_base')
    op.drop_table('notifications')
    op.drop_table('audit_logs')
    op.drop_table('maintenance')
    op.drop_table('vendors')
    op.drop_table('assignments')
    op.drop_table('ticket_comments')
    op.drop_table('tickets')
    op.drop_table('assets')
    op.drop_table('users')
