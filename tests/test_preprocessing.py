"""
Unit tests for satellite data preprocessing
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.preprocessing.process_satellite_data import SatelliteDataPreprocessor


@pytest.fixture
def sample_data():
    """Create sample satellite embedding data for testing."""
    data = {
        "municipality_id": ["3550308", "3304557", "2927408"],
        "municipality_name": ["São Paulo", "Rio de Janeiro", "Salvador"],
        "state_name": ["São Paulo", "Rio de Janeiro", "Bahia"],
    }

    # Add 64 embedding dimensions
    for i in range(64):
        data[f"embedding_{i}"] = np.random.randn(3)

    data["extraction_date"] = ["2026-01-28"] * 3

    return pd.DataFrame(data)


@pytest.fixture
def sample_csv(tmp_path, sample_data):
    """Create a temporary CSV file with sample data."""
    csv_path = tmp_path / "test_embeddings.csv"
    sample_data.to_csv(csv_path, index=False)
    return csv_path


def test_load_data(sample_csv):
    """Test data loading functionality."""
    preprocessor = SatelliteDataPreprocessor(sample_csv)
    df = preprocessor.load_data()

    assert df is not None
    assert len(df) == 3
    assert "municipality_id" in df.columns


def test_validate_data(sample_csv):
    """Test data validation."""
    preprocessor = SatelliteDataPreprocessor(sample_csv)
    preprocessor.load_data()
    issues = preprocessor.validate_data()

    # Should have no issues with clean data
    assert "invalid_dimensions" not in issues


def test_clean_data_with_duplicates(tmp_path):
    """Test cleaning data with duplicates."""
    # Create data with duplicates
    data = {
        "municipality_id": ["3550308", "3550308", "3304557"],
        "municipality_name": ["São Paulo", "São Paulo", "Rio de Janeiro"],
        "state_name": ["São Paulo", "São Paulo", "Rio de Janeiro"],
    }

    for i in range(64):
        data[f"embedding_{i}"] = [1.0, 1.0, 2.0]

    df = pd.DataFrame(data)
    csv_path = tmp_path / "test_duplicates.csv"
    df.to_csv(csv_path, index=False)

    preprocessor = SatelliteDataPreprocessor(csv_path)
    preprocessor.load_data()
    cleaned_df = preprocessor.clean_data()

    # Should remove duplicates
    assert len(cleaned_df) == 2


def test_add_metadata(sample_csv):
    """Test metadata addition."""
    preprocessor = SatelliteDataPreprocessor(sample_csv)
    preprocessor.load_data()
    df = preprocessor.add_metadata()

    assert "processed_date" in df.columns
    assert "data_source" in df.columns


def test_generate_summary_stats(sample_csv):
    """Test summary statistics generation."""
    preprocessor = SatelliteDataPreprocessor(sample_csv)
    preprocessor.load_data()
    stats = preprocessor.generate_summary_stats()

    assert stats["total_municipalities"] == 3
    assert stats["embedding_dimensions"] == 64
    assert "embedding_stats" in stats


def test_full_pipeline(sample_csv, tmp_path):
    """Test full preprocessing pipeline."""
    preprocessor = SatelliteDataPreprocessor(sample_csv)
    output_path = tmp_path / "processed_output.csv"

    df, stats, saved_path = preprocessor.process()

    assert df is not None
    assert stats is not None
    assert Path(saved_path).exists()
    assert len(df) == 3
