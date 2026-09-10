"""
Entrepreneur Mitra (SIH26092) - Supabase PostgreSQL Migration Script.
Safely migrates schema and data from local SQLite to Supabase PostgreSQL without Prisma or third-party ORMs.
Adheres strictly to SQLAlchemy 2.0.
"""
import sys
import os
import argparse
from typing import Dict, Any, List
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Base
import app.models  # Ensures all 10 models are loaded into Base.metadata
from app.models.user import User
from app.models.profile import EntrepreneurProfile, ProfileAttribute
from app.models.scheme import Scheme, SchemeRule, SchemeBenefit, DocumentRequirement, SchemeSource
from app.models.partner import PartnerLocation
from app.models.document import UserDocument
from app.models.application import Application
from app.models.saved_scheme import SavedScheme
from app.models.alert import Alert
from app.models.audit import AuditLog, EligibilityEvaluation


MODEL_TRANSFER_ORDER = [
    ("users", User),
    ("entrepreneur_profiles", EntrepreneurProfile),
    ("profile_attributes", ProfileAttribute),
    ("schemes", Scheme),
    ("scheme_rules", SchemeRule),
    ("scheme_benefits", SchemeBenefit),
    ("document_requirements", DocumentRequirement),
    ("scheme_sources", SchemeSource),
    ("partner_locations", PartnerLocation),
    ("user_documents", UserDocument),
    ("applications", Application),
    ("saved_schemes", SavedScheme),
    ("alerts", Alert),
    ("audit_logs", AuditLog),
    ("eligibility_evaluations", EligibilityEvaluation),
]


def migrate(sqlite_path: str, supabase_url: str, dry_run: bool = False):
    print("=" * 70)
    print("Entrepreneur Mitra — SQLite -> Supabase PostgreSQL Safe Migration")
    print("=" * 70)
    
    if not os.path.exists(sqlite_path):
        print(f"[-] Error: Source SQLite database not found at '{sqlite_path}'")
        return False

    # Normalize Supabase URL
    norm_url = supabase_url.strip()
    if norm_url.startswith("postgres://"):
        norm_url = norm_url.replace("postgres://", "postgresql://", 1)

    print(f"[*] Source SQLite: {sqlite_path}")
    print(f"[*] Target Supabase: {norm_url.split('@')[-1] if '@' in norm_url else norm_url}")
    print(f"[*] Dry Run: {'YES' if dry_run else 'NO'}")

    src_engine = create_engine(f"sqlite:///{sqlite_path}", connect_args={"check_same_thread": False})
    SrcSession = sessionmaker(bind=src_engine)
    src_session = SrcSession()

    try:
        tgt_engine = create_engine(
            norm_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            echo=False
        )
        # Test connection
        with tgt_engine.connect() as conn:
            res = conn.execute(text("SELECT 1")).scalar()
            print("[+] Successfully connected to Supabase PostgreSQL!")
    except Exception as e:
        print(f"[-] Connection failed to Supabase PostgreSQL: {e}")
        print("    Please check your network and SUPABASE_DATABASE_URL credentials.")
        return False

    if dry_run:
        print("[*] Dry run enabled. Counting source records:")
        for table_name, model in MODEL_TRANSFER_ORDER:
            try:
                cnt = src_session.query(model).count()
                print(f"    - {table_name:25s}: {cnt:4d} records ready to migrate")
            except Exception as e:
                print(f"    - {table_name:25s}: (Table not populated: {e})")
        src_session.close()
        return True

    # 1. Create Target Tables
    print("[*] Creating target schema in Supabase PostgreSQL via SQLAlchemy 2.0...")
    Base.metadata.create_all(bind=tgt_engine)
    print("[+] All tables verified / created successfully.")

    TgtSession = sessionmaker(bind=tgt_engine)
    tgt_session = TgtSession()

    # 2. Transfer Data in Topological Dependency Order
    stats: Dict[str, Dict[str, int]] = {}
    print("\n[*] Transferring records...")
    
    for table_name, model in MODEL_TRANSFER_ORDER:
        try:
            records = src_session.query(model).all()
            src_count = len(records)
            inserted_count = 0

            # Get primary key column names
            mapper = inspect(model)
            pk_names = [col.name for col in mapper.primary_key]

            for rec in records:
                # Build dict of columns
                row_data = {col.name: getattr(rec, col.name) for col in mapper.columns}
                
                # Check if record already exists in target
                filter_kwargs = {pk: row_data[pk] for pk in pk_names}
                exists = tgt_session.query(model).filter_by(**filter_kwargs).first()
                if not exists:
                    new_rec = model(**row_data)
                    tgt_session.add(new_rec)
                    inserted_count += 1

            tgt_session.commit()
            tgt_count = tgt_session.query(model).count()
            stats[table_name] = {
                "source": src_count,
                "inserted": inserted_count,
                "target_total": tgt_count
            }
            print(f"    [OK] {table_name:25s}: Source={src_count} | New Inserted={inserted_count} | Target Total={tgt_count}")
        except Exception as e:
            tgt_session.rollback()
            print(f"    [ERR] {table_name:25s}: Migration error: {e}")

    src_session.close()
    tgt_session.close()

    print("\n" + "=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)
    for tbl, s in stats.items():
        print(f"  {tbl:25s} -> SQLite: {s['source']:3d} | Supabase: {s['target_total']:3d}")
    print("[+] Supabase migration process complete.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate Entrepreneur Mitra SQLite to Supabase PostgreSQL")
    parser.add_argument("--sqlite", default="entrepreneur_mitra.db", help="Path to SQLite database file")
    parser.add_argument("--url", default=os.getenv("SUPABASE_DATABASE_URL", os.getenv("DATABASE_URL", "")), help="Supabase PostgreSQL URL")
    parser.add_argument("--dry-run", action="store_true", help="Perform validation without writing to Supabase")

    args = parser.parse_args()

    if not args.url or args.url.startswith("sqlite"):
        print("[!] No Supabase PostgreSQL URL supplied.")
        print("    Usage: python scripts/migrate_to_supabase.py --url 'postgresql://postgres.xxx:pass@aws-0-region.pooler.supabase.com:6543/postgres'")
        print("    Or set SUPABASE_DATABASE_URL in .env.")
        print("    Testing source SQLite database records in dry-run mode:\n")
        migrate(args.sqlite, "sqlite:///./temp.db", dry_run=True)
    else:
        migrate(args.sqlite, args.url, dry_run=args.dry_run)
