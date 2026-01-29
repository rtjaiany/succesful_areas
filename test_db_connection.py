"""
Test PostgreSQL Database Connection

Quick script to verify database connectivity and configuration.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Load environment variables
load_dotenv()


def test_connection():
    """Test database connection and display configuration."""

    print("=" * 70)
    print("PostgreSQL Connection Test")
    print("=" * 70)

    # Display configuration (without password)
    print("\n📋 Configuration:")
    print(f"  Host: {os.getenv('DB_HOST', 'Not set')}")
    print(f"  Port: {os.getenv('DB_PORT', 'Not set')}")
    print(f"  Database: {os.getenv('DB_NAME', 'Not set')}")
    print(f"  User: {os.getenv('DB_USER', 'Not set')}")
    print(f"  Password: {'***' if os.getenv('DB_PASSWORD') else 'Not set'}")

    # Check if all required variables are set
    required_vars = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print("\n❌ Missing environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\n💡 Please set these variables in your .env file")
        return False

    # Try to import and connect
    print("\n🔌 Testing connection...")

    try:
        from src.preprocessing.database_integration import DatabaseManager

        db = DatabaseManager()

        if db.engine is None:
            print("❌ Failed to create database engine")
            print("   Check your credentials and ensure PostgreSQL is running")
            return False

        # Test connection
        with db.engine.connect() as conn:
            result = conn.execute("SELECT version();")
            version = result.fetchone()[0]
            print(f"✅ Connection successful!")
            print(f"\n📊 PostgreSQL Version:")
            print(f"  {version}")

        # Get database stats
        print("\n📈 Database Statistics:")
        stats = db.get_summary_stats()

        if stats:
            print(f"  Total records: {stats.get('total_records', 0)}")
            print(f"  Unique municipalities: {stats.get('unique_municipalities', 0)}")
            print(f"  Unique states: {stats.get('unique_states', 0)}")

            if stats.get("earliest_extraction"):
                print(f"  Earliest extraction: {stats.get('earliest_extraction')}")
            if stats.get("latest_extraction"):
                print(f"  Latest extraction: {stats.get('latest_extraction')}")
        else:
            print("  No data in database yet")

        # Check if table exists
        print("\n🗄️  Table Status:")
        with db.engine.connect() as conn:
            result = conn.execute(
                """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                  AND table_name = 'satellite_embeddings'
            """
            )

            if result.fetchone():
                print("  ✅ satellite_embeddings table exists")

                # Count records
                result = conn.execute("SELECT COUNT(*) FROM satellite_embeddings")
                count = result.fetchone()[0]
                print(f"  📊 Records in table: {count}")
            else:
                print("  ⚠️  satellite_embeddings table does not exist")
                print(
                    "  💡 Run: python src/preprocessing/database_integration.py --create-tables"
                )

        print("\n" + "=" * 70)
        print("✅ All tests passed!")
        print("=" * 70)

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you've installed all dependencies:")
        print("   pip install -r requirements.txt")
        return False

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("  1. Check if PostgreSQL is running")
        print("  2. Verify credentials in .env file")
        print("  3. Ensure database 'iguide_db' exists")
        print("  4. Check firewall settings")
        return False


def main():
    """Main execution."""
    success = test_connection()

    if success:
        print("\n🚀 Next steps:")
        print("  1. Extract data: python src/gee/extract_embeddings.py")
        print(
            "  2. Preprocess: python src/preprocessing/process_satellite_data.py <file.csv>"
        )
        print(
            "  3. Ingest: python src/preprocessing/database_integration.py --ingest <file.csv>"
        )
    else:
        print("\n⚠️  Please fix the issues above and try again")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
