"""Tests for Supabase PostgreSQL compatibility and migration safety."""
import os
import pytest
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql
from app.database import Base, get_active_database_type
import app.models
from scripts.migrate_to_supabase import migrate


def test_active_db_type():
    db_type = get_active_database_type()
    assert db_type in ["sqlite", "postgresql"]


def test_all_models_compile_to_postgresql_ddl():
    dialect = postgresql.dialect()
    for table in Base.metadata.sorted_tables:
        ddl = str(CreateTable(table).compile(dialect=dialect))
        assert len(ddl) > 0, f"Failed to generate PostgreSQL DDL for {table.name}"


def test_migration_dry_run():
    # Dry run should succeed against local database
    res = migrate("entrepreneur_mitra.db", "sqlite:///./temp_test.db", dry_run=True)
    assert res is True
