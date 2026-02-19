"""
Preprocess and Integrate Cities Data

This script takes multiple Excel files from data/raw/cities_data,
standardizes the IBGE municipality ID, filters columns based on a dictionary,
renames them, and merges everything into a single processed CSV.
"""

import os
import unicodedata
import pandas as pd
from pathlib import Path
from loguru import logger


class CitiesPreprocessor:
    """
    Preprocessor for cities data from various external sources.
    """

    # Possible names for IBGE code columns in raw files
    ID_COL_MAPPINGS = [
        "codigo_ibge_municipio",
        "cd_mun",
        "CD_MUN",
        "MUNIC_CODE7",
        "Código [-]",
        "tcode",
    ]

    TARGET_ID_COL = "cod_ibge"

    def __init__(
        self,
        raw_dir: str = "data/raw/cities_data",
        processed_dir: str = "data/processed",
    ):
        self.raw_dir = Path(raw_dir)
        self.processed_dir = Path(processed_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.dictionary_path = self.raw_dir / "dictionary_city.xlsx"

        # Load dictionary mapping
        logger.info("Loading mapping dictionary...")
        self.mapping_df = pd.read_excel(self.dictionary_path)
        # Create a mapping dict: Name -> Label
        self.mapping_dict = dict(zip(self.mapping_df["Name"], self.mapping_df["Label"]))
        logger.info(f"Loaded {len(self.mapping_dict)} mappings from dictionary.")

    def preprocess_all(self):
        """
        Iterates through all Excel files and merges them.
        """
        integrated_df = None

        # List files in raw directory
        files = [
            f for f in self.raw_dir.glob("*.xlsx") if f.name != "dictionary_city.xlsx"
        ]
        logger.info(f"Found {len(files)} data files to process.")

        for file_path in files:
            try:
                logger.info(f"Processing file: {file_path.name}")
                df = pd.read_excel(file_path)

                # 1. Identify and rename the IBGE code column
                id_col = None
                for col in df.columns:
                    if col in self.ID_COL_MAPPINGS:
                        id_col = col
                        break

                if id_col is None:
                    logger.warning(f"No ID column found in {file_path.name}. Skipping.")
                    continue

                df = df.rename(columns={id_col: self.TARGET_ID_COL})

                # Standardize ID to 7-digit string
                df[self.TARGET_ID_COL] = (
                    df[self.TARGET_ID_COL]
                    .astype(str)
                    .str.split(".")
                    .str[0]
                    .str.zfill(7)
                )

                # 2. Filter columns based on dictionary 'Name'
                present_targets = [
                    col for col in df.columns if col in self.mapping_dict
                ]
                if not present_targets:
                    logger.warning(
                        f"No mapped columns found in {file_path.name}. Keeping only ID."
                    )

                # Select only ID and mapped columns
                cols_to_keep = [self.TARGET_ID_COL] + present_targets
                df_filtered = df[cols_to_keep].copy()

                # 3. Rename columns using 'Label'
                df_filtered = df_filtered.rename(columns=self.mapping_dict)

                # 4. Integrate (Merge)
                if integrated_df is None:
                    integrated_df = df_filtered
                else:
                    # Merge on cod_ibge
                    integrated_df = pd.merge(
                        integrated_df, df_filtered, on=self.TARGET_ID_COL, how="outer"
                    )

                logger.success(f"Successfully processed and merged {file_path.name}")

            except Exception as e:
                logger.error(f"Failed to process {file_path.name}: {e}")

        if integrated_df is not None:
            # 5. Add Municipality Name and State Name
            integrated_df = self._add_municipality_info(integrated_df)

            # Ensure cod_ibge is the first column, followed by name and state
            fixed_cols = [self.TARGET_ID_COL, "municipality_name", "state_name"]
            other_cols = [c for c in integrated_df.columns if c not in fixed_cols]
            integrated_df = integrated_df[fixed_cols + other_cols]

            output_path = self.processed_dir / "integrated_cities_data.csv"
            integrated_df.to_csv(output_path, index=False)
            logger.info("=" * 50)
            logger.success(
                f"PREPROCESSING COMPLETE! Final file saved to: {output_path}"
            )
            logger.info(f"Total municipalities: {len(integrated_df)}")
            logger.info(
                f"Total features: {len(integrated_df.columns) - 3}"
            )  # Subtracting id, name, state
            logger.info("=" * 50)
        else:
            logger.error(
                "No data was integrated. Check your source files and dictionary."
            )

    def _clean_text(self, text):
        """
        Normalizes text: removes accents, converts to title case, and strips whitespace.
        Also handles potential encoding artifacts/symbols.
        """
        if pd.isna(text) or not isinstance(text, str):
            return text

        # Remove accents
        text = "".join(
            c
            for c in unicodedata.normalize("NFD", text)
            if unicodedata.category(c) != "Mn"
        )

        # Strip and clean artifacts
        text = text.strip().title()

        return text

    def _add_municipality_info(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds municipality and state names based on cod_ibge.
        Uses GeoSES_BR.xlsx for state and Cidades IBGE.xlsx for city name.
        """
        logger.info("Enriching data with municipality and state names...")

        try:
            # Load State info from GeoSES
            geoses_path = self.raw_dir / "GeoSES_BR.xlsx"
            states_df = pd.read_excel(geoses_path)[["MUNIC_CODE7", "FU_NAME"]]
            states_df["MUNIC_CODE7"] = states_df["MUNIC_CODE7"].astype(str).str.zfill(7)
            state_mapping = dict(zip(states_df["MUNIC_CODE7"], states_df["FU_NAME"]))

            # Load City info from Cidades IBGE
            cidades_path = self.raw_dir / "Cidades IBGE.xlsx"
            cities_df = pd.read_excel(cidades_path)[["CD_MUN", "MUNICIPIO"]]
            cities_df["CD_MUN"] = (
                cities_df["CD_MUN"].astype(str).str.split(".").str[0].str.zfill(7)
            )
            city_mapping = dict(zip(cities_df["CD_MUN"], cities_df["MUNICIPIO"]))

            # Map values
            df["municipality_name"] = df[self.TARGET_ID_COL].map(city_mapping)
            df["state_name"] = df[self.TARGET_ID_COL].map(state_mapping)

            # Clean names (remove accents and symbols)
            df["municipality_name"] = df["municipality_name"].apply(self._clean_text)
            df["state_name"] = df["state_name"].apply(self._clean_text)

            return df

        except Exception as e:
            logger.warning(f"Failed to add municipality/state names: {e}")
            df["municipality_name"] = "Unknown"
            df["state_name"] = "Unknown"
            return df


def main():
    preprocessor = CitiesPreprocessor()
    preprocessor.preprocess_all()


if __name__ == "__main__":
    main()
