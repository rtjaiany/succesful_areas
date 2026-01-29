"""
Database Integration for Satellite Embeddings

Handles database table creation and data ingestion.
"""

import os
import pandas as pd
from pathlib import Path
from sqlalchemy import (
    create_engine,
    text,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ARRAY,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from loguru import logger
from dotenv import load_dotenv
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.logger_config import setup_logger

# Load environment variables
load_dotenv()

Base = declarative_base()


class SatelliteEmbedding(Base):
    """SQLAlchemy model for satellite embeddings table."""

    __tablename__ = "satellite_embeddings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    municipality_id = Column(String(7), nullable=False)
    municipality_name = Column(String(255), nullable=False)
    state_code = Column(String(2))
    state_name = Column(String(100))

    # Embedding columns (0-63)
    embedding_0 = Column(Float)
    embedding_1 = Column(Float)
    embedding_2 = Column(Float)
    embedding_3 = Column(Float)
    embedding_4 = Column(Float)
    embedding_5 = Column(Float)
    embedding_6 = Column(Float)
    embedding_7 = Column(Float)
    embedding_8 = Column(Float)
    embedding_9 = Column(Float)
    embedding_10 = Column(Float)
    embedding_11 = Column(Float)
    embedding_12 = Column(Float)
    embedding_13 = Column(Float)
    embedding_14 = Column(Float)
    embedding_15 = Column(Float)
    embedding_16 = Column(Float)
    embedding_17 = Column(Float)
    embedding_18 = Column(Float)
    embedding_19 = Column(Float)
    embedding_20 = Column(Float)
    embedding_21 = Column(Float)
    embedding_22 = Column(Float)
    embedding_23 = Column(Float)
    embedding_24 = Column(Float)
    embedding_25 = Column(Float)
    embedding_26 = Column(Float)
    embedding_27 = Column(Float)
    embedding_28 = Column(Float)
    embedding_29 = Column(Float)
    embedding_30 = Column(Float)
    embedding_31 = Column(Float)
    embedding_32 = Column(Float)
    embedding_33 = Column(Float)
    embedding_34 = Column(Float)
    embedding_35 = Column(Float)
    embedding_36 = Column(Float)
    embedding_37 = Column(Float)
    embedding_38 = Column(Float)
    embedding_39 = Column(Float)
    embedding_40 = Column(Float)
    embedding_41 = Column(Float)
    embedding_42 = Column(Float)
    embedding_43 = Column(Float)
    embedding_44 = Column(Float)
    embedding_45 = Column(Float)
    embedding_46 = Column(Float)
    embedding_47 = Column(Float)
    embedding_48 = Column(Float)
    embedding_49 = Column(Float)
    embedding_50 = Column(Float)
    embedding_51 = Column(Float)
    embedding_52 = Column(Float)
    embedding_53 = Column(Float)
    embedding_54 = Column(Float)
    embedding_55 = Column(Float)
    embedding_56 = Column(Float)
    embedding_57 = Column(Float)
    embedding_58 = Column(Float)
    embedding_59 = Column(Float)
    embedding_60 = Column(Float)
    embedding_61 = Column(Float)
    embedding_62 = Column(Float)
    embedding_63 = Column(Float)

    extraction_date = Column(DateTime, default=datetime.utcnow)
    data_source = Column(String(100), default="Google Satellite Embedding V1")


class DatabaseManager:
    """Manage database operations for satellite embeddings."""

    def __init__(self):
        """Initialize database connection."""
        setup_logger()

        # Build connection string
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "iguide_db")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")

        if not db_user or not db_password:
            logger.warning("Database credentials not found in environment variables")
            self.engine = None
            return

        connection_string = (
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )

        try:
            self.engine = create_engine(connection_string)
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            self.engine = None

    def create_tables(self):
        """Create database tables if they don't exist."""
        if not self.engine:
            logger.error("No database connection available")
            return False

        try:
            Base.metadata.create_all(self.engine)
            logger.success("Database tables created successfully")

            # Create indexes
            self.create_indexes()

            return True
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            return False

    def create_indexes(self):
        """Create indexes for efficient querying."""
        if not self.engine:
            return

        try:
            with self.engine.connect() as conn:
                # Index on municipality_id
                conn.execute(
                    text(
                        "CREATE INDEX IF NOT EXISTS idx_municipality_id "
                        "ON satellite_embeddings(municipality_id)"
                    )
                )

                # Index on state_code
                conn.execute(
                    text(
                        "CREATE INDEX IF NOT EXISTS idx_state_code "
                        "ON satellite_embeddings(state_code)"
                    )
                )

                # Index on extraction_date
                conn.execute(
                    text(
                        "CREATE INDEX IF NOT EXISTS idx_extraction_date "
                        "ON satellite_embeddings(extraction_date)"
                    )
                )

                conn.commit()
                logger.info("Database indexes created successfully")
        except Exception as e:
            logger.error(f"Failed to create indexes: {e}")

    def ingest_csv(self, csv_path: str, batch_size: int = 1000):
        """
        Ingest CSV data into database.

        Args:
            csv_path: Path to CSV file
            batch_size: Number of records to insert per batch
        """
        if not self.engine:
            logger.error("No database connection available")
            return False

        try:
            logger.info(f"Loading data from {csv_path}")
            df = pd.read_csv(csv_path)

            logger.info(f"Ingesting {len(df)} records into database")

            # Insert data in batches
            df.to_sql(
                "satellite_embeddings",
                self.engine,
                if_exists="append",
                index=False,
                chunksize=batch_size,
            )

            logger.success(f"Successfully ingested {len(df)} records")
            return True

        except Exception as e:
            logger.error(f"Failed to ingest data: {e}")
            return False

    def query_by_municipality(self, municipality_id: str):
        """
        Query embeddings for a specific municipality.

        Args:
            municipality_id: Municipality ID to query

        Returns:
            pd.DataFrame: Query results
        """
        if not self.engine:
            logger.error("No database connection available")
            return None

        query = f"""
        SELECT * FROM satellite_embeddings 
        WHERE municipality_id = '{municipality_id}'
        ORDER BY extraction_date DESC
        """

        try:
            df = pd.read_sql(query, self.engine)
            logger.info(
                f"Retrieved {len(df)} records for municipality {municipality_id}"
            )
            return df
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return None

    def query_by_state(self, state_code: str):
        """
        Query embeddings for all municipalities in a state.

        Args:
            state_code: State code to query

        Returns:
            pd.DataFrame: Query results
        """
        if not self.engine:
            logger.error("No database connection available")
            return None

        query = f"""
        SELECT * FROM satellite_embeddings 
        WHERE state_code = '{state_code}'
        ORDER BY municipality_name
        """

        try:
            df = pd.read_sql(query, self.engine)
            logger.info(f"Retrieved {len(df)} records for state {state_code}")
            return df
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return None

    def get_summary_stats(self):
        """Get summary statistics from the database."""
        if not self.engine:
            logger.error("No database connection available")
            return None

        query = """
        SELECT 
            COUNT(*) as total_records,
            COUNT(DISTINCT municipality_id) as unique_municipalities,
            COUNT(DISTINCT state_code) as unique_states,
            MIN(extraction_date) as earliest_extraction,
            MAX(extraction_date) as latest_extraction
        FROM satellite_embeddings
        """

        try:
            df = pd.read_sql(query, self.engine)
            logger.info("Retrieved summary statistics")
            return df.to_dict("records")[0]
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return None


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Database operations for satellite embeddings"
    )
    parser.add_argument(
        "--create-tables", action="store_true", help="Create database tables"
    )
    parser.add_argument("--ingest", type=str, help="Path to CSV file to ingest")
    parser.add_argument("--stats", action="store_true", help="Show database statistics")

    args = parser.parse_args()

    db_manager = DatabaseManager()

    if args.create_tables:
        logger.info("Creating database tables...")
        db_manager.create_tables()

    if args.ingest:
        logger.info(f"Ingesting data from {args.ingest}...")
        db_manager.ingest_csv(args.ingest)

    if args.stats:
        logger.info("Retrieving database statistics...")
        stats = db_manager.get_summary_stats()
        if stats:
            print("\nDatabase Statistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
