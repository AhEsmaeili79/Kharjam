"""Alembic environment configuration for database migrations."""

import sys
from pathlib import Path
from logging.config import fileConfig
from typing import Optional

from sqlalchemy import create_engine, pool, Engine, event, text
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import ENUM as PostgresEnum
from alembic import context
from alembic.operations import ops
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext

# ============================================================================
# Path Configuration
# ============================================================================

# Add project root to Python path (current file is in app/db/alembic/)
# Go up 4 levels: app/db/alembic -> app/db -> app -> . (project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ============================================================================
# Settings & Configuration
# ============================================================================

from app.config import database_config
from app.db.database import Base

# Import all models to register them with SQLAlchemy
import app.apps.auth.models
import app.apps.users.models
# Alembic config object
config = context.config

# Configure logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate
target_metadata = Base.metadata

# ============================================================================
# Database URL Configuration
# ============================================================================

def _normalize_db_url_for_sqlalchemy(url: str) -> str:
    """Convert asyncpg URL to psycopg2 URL for SQLAlchemy synchronous engine."""
    if url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)
    return url


def get_database_url() -> str:
    """
    Get database URL from settings or config file.
    
    Returns:
        Database URL string (normalized for synchronous SQLAlchemy)
    """
    url = None
    if database_config.database_url:
        url = database_config.database_url
    else:
        url = config.get_main_option("sqlalchemy.url", "")
    
    if url:
        return _normalize_db_url_for_sqlalchemy(url)
    return ""


def is_postgresql(url: str) -> bool:
    """Check if database is PostgreSQL."""
    return url.startswith("postgresql")


# Update config with settings if available
if database_config.database_url:
    # Normalize URL for synchronous SQLAlchemy and escape % for ConfigParser
    normalized_url = _normalize_db_url_for_sqlalchemy(database_config.database_url)
    escaped_url = normalized_url.replace('%', '%%')
    config.set_main_option("sqlalchemy.url", escaped_url)

# ============================================================================
# PostgreSQL Enum Type Handling
# ============================================================================

def extract_enum_from_column(column) -> Optional[tuple[str, tuple]]:
    """
    Extract enum type name and values from a column.
    
    Args:
        column: SQLAlchemy column object
        
    Returns:
        Tuple of (enum_name, enum_values) or None
    """
    if not hasattr(column, 'type'):
        return None
    
    if isinstance(column.type, SQLEnum) and column.type.name:
        return (column.type.name, tuple(column.type.enums))
    
    return None


def collect_enum_types(operation, enum_registry: dict) -> None:
    """
    Recursively collect enum types from Alembic operations.
    
    Args:
        operation: Alembic operation object
        enum_registry: Dictionary to store found enums
    """
    if isinstance(operation, ops.CreateTableOp):
        for column in operation.columns:
            enum_data = extract_enum_from_column(column)
            if enum_data:
                enum_registry[enum_data[0]] = enum_data[1]
    
    elif isinstance(operation, ops.AddColumnOp):
        if hasattr(operation, 'column'):
            enum_data = extract_enum_from_column(operation.column)
            if enum_data:
                enum_registry[enum_data[0]] = enum_data[1]
    
    elif isinstance(operation, ops.AlterColumnOp):
        if hasattr(operation, 'modify_type') and isinstance(operation.modify_type, SQLEnum):
            if operation.modify_type.name:
                enum_registry[operation.modify_type.name] = tuple(operation.modify_type.enums)
    
    # Recursively process nested operations
    if hasattr(operation, "ops"):
        for nested_op in operation.ops:
            collect_enum_types(nested_op, enum_registry)


def get_next_numeric_rev_id(script_directory: ScriptDirectory) -> str:
    """
    Generate the next numeric revision id based on existing migration files.
    """
    versions_path = Path(script_directory.versions)
    if not versions_path.exists():
        return "1"

    max_number = 0
    for file_path in versions_path.glob("*.py"):
        prefix = file_path.name.split("_", 1)[0]
        if prefix.isdigit():
            max_number = max(max_number, int(prefix))

    return str(max_number + 1 if max_number else 1)


def create_enum_type_sql(enum_name: str, enum_values: tuple) -> str:
    """
    Generate SQL to create PostgreSQL enum type if it doesn't exist.
    
    Args:
        enum_name: Name of the enum type
        enum_values: Tuple of enum values
        
    Returns:
        SQL string to create the enum type
    """
    values_str = ", ".join(f"'{value}'" for value in enum_values)
    
    # PostgreSQL doesn't support CREATE TYPE IF NOT EXISTS directly
    # Use DO block for idempotent enum creation
    return f"""
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = '{enum_name}') THEN
        CREATE TYPE {enum_name} AS ENUM ({values_str});
    END IF;
END $$;
    """.strip()


def process_revision_directives(context, revision, directives):
    """
    Process migration directives to ensure enum types are created before use
    and enforce numeric, ordered revision ids.
    """
    if not directives:
        return

    script = directives[0]

    # Enforce sequential numeric revision ids to align filenames like "1_message_YYYYMMDD.py"
    if hasattr(script, "rev_id"):
        script_directory = ScriptDirectory.from_config(context.config)
        script.rev_id = get_next_numeric_rev_id(script_directory)

    if not hasattr(script, "upgrade_ops") or not script.upgrade_ops:
        return

    # Only process for PostgreSQL
    db_url = get_database_url()
    if not is_postgresql(db_url):
        return

    # Collect all enum types used in this migration
    enum_registry = {}
    for operation in script.upgrade_ops.ops:
        collect_enum_types(operation, enum_registry)

    # Prepend enum creation operations if any were found
    if enum_registry:
        enum_creation_ops = [
            ops.ExecuteSQLOp(create_enum_type_sql(name, values))
            for name, values in enum_registry.items()
        ]
        script.upgrade_ops.ops = enum_creation_ops + list(script.upgrade_ops.ops)

# ============================================================================
# Migration Execution
# ============================================================================

def get_migration_config() -> dict:
    """
    Get common configuration for migrations.
    
    Returns:
        Dictionary of configuration options
    """
    return {
        "target_metadata": target_metadata,
        "compare_type": True,
        "compare_server_default": False,
        "process_revision_directives": process_revision_directives,
    }


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    
    This configures the context with just a URL and not an Engine.
    Calls to context.execute() emit SQL to the script output.
    """
    url = get_database_url()
    
    context.configure(
        url=url,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        **get_migration_config(),
    )

    with context.begin_transaction():
        context.run_migrations()


def create_connectable() -> Engine:
    """
    Create database engine for online migrations.
    
    Returns:
        SQLAlchemy Engine instance
    """
    db_url = get_database_url()
    if not db_url:
        raise ValueError("Database URL not configured")
    
    return create_engine(
        db_url,
        poolclass=pool.NullPool,
    )


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    
    Creates an Engine and associates a connection with the context.
    """
    connectable = create_connectable()

    # Patch PostgreSQL Enum creation to be idempotent
    original_create = PostgresEnum.create
    
    def patched_enum_create(self, bind=None, checkfirst=True):
        """Patch enum creation to check if it exists first."""
        if not isinstance(self, PostgresEnum) or not self.name:
            return original_create(self, bind=bind, checkfirst=checkfirst)
        
        # Check if enum already exists
        if bind is not None:
            result = bind.execute(
                text("SELECT 1 FROM pg_type WHERE typname = :name"),
                {"name": self.name}
            ).scalar()
            
            if result:
                # Enum already exists, skip creation
                return
        
        # Enum doesn't exist or bind is None, use original create method
        return original_create(self, bind=bind, checkfirst=checkfirst)
    
    # Monkey-patch the Enum's create method for this migration session
    PostgresEnum.create = patched_enum_create

    try:
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                **get_migration_config(),
            )

            with context.begin_transaction():
                context.run_migrations()
    finally:
        # Restore original create method
        PostgresEnum.create = original_create

# ============================================================================
# Entry Point
# ============================================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()