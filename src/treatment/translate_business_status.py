"""
Translate and enrich Business Status data.

This script adds an English description column to business_status.csv
and ensures proper text normalization.
"""

import pandas as pd
import unicodedata
from pathlib import Path
from loguru import logger


class BusinessStatusTranslator:
    TRANSLATION_MAP = {
        "Agricultura, pecuaria, producao florestal, pesca e aquicultura": "Agriculture, livestock, forestry, fishing and aquaculture",
        "Industrias extrativas": "Extractive industries",
        "Industrias de transformacao": "Manufacturing industries",
        "Eletricidade e gas": "Electricity and gas",
        "Agua, esgoto, atividades de gestao de residuos e descontaminacao": "Water, sewage, waste management and decontamination",
        "Construcao": "Construction",
        "Comercio; reparacao de veiculos automotores e motocicletas": "Trade; repair of motor vehicles and motorcycles",
        "Transporte, armazenagem e correio": "Transportation, storage and mail",
        "Alojamento e alimentacao": "Accommodation and food",
        "Informacao e comunicacao": "Information and communication",
        "Atividades financeiras, de seguros e servicos relacionados": "Financial, insurance and related services",
        "Atividades imobiliarias": "Real estate activities",
        "Atividades profissionais, cientificas e tecnicas": "Professional, scientific and technical activities",
        "Atividades administrativas e serviços complementares": "Administrative and support services",
        "Administracao publica, defesa e seguridade social": "Public administration, defense and social security",
        "Educacao": "Education",
        "Saude humana e servicos sociais": "Human health and social services",
        "Artes, cultura, esporte e recreacao": "Arts, culture, sport and recreation",
        "Outras atividades de servicos": "Other service activities",
        "Servicos domesticos": "Domestic services",
        "Organismos internacionais e outras instituicoes extraterritoriais": "International organizations and extraterritorial institutions",
        "Outras": "Others",
    }

    def __init__(self, file_path: str = "data/raw/business_data/business_status.csv"):
        self.file_path = Path(file_path)

    def _normalize_text(self, text):
        """Standardizes text to match keys even with minor encoding differences."""
        if pd.isna(text) or not isinstance(text, str):
            return text
        # Remove accents and special symbols, convert to simple ascii-like
        normalized = "".join(
            c
            for c in unicodedata.normalize("NFD", text)
            if unicodedata.category(c) != "Mn"
        )
        return normalized.strip().lower()

    def translate(self):
        if not self.file_path.exists():
            logger.error(f"File not found: {self.file_path}")
            return

        logger.info(f"Loading {self.file_path}...")
        df = pd.read_csv(self.file_path)

        # Create a normalized version of our map for robust matching
        norm_map = {self._normalize_text(k): v for k, v in self.TRANSLATION_MAP.items()}

        def get_translation(row_text):
            norm_text = self._normalize_text(row_text)
            return norm_map.get(
                norm_text, row_text
            )  # Fallback to original if not found

        logger.info("Adding English description column...")
        df["description"] = df["desc_secao"].apply(get_translation)

        # Reorder columns to put 'description' next to 'secao_cnae' or 'desc_secao'
        cols = list(df.columns)
        if "desc_secao" in cols:
            idx = cols.index("desc_secao")
            cols.insert(idx + 1, cols.pop(cols.index("description")))
            df = df[cols]

        logger.info("Cleaning up special symbols in Portuguese descriptions...")

        # Since the user complained about symbols, let's normalize the Portuguese column too
        # to remove things like
        def deep_clean(text):
            if pd.isna(text):
                return text
            # Replace common encoding errors if found
            return text.replace("", " ").strip()

        df["desc_secao"] = df["desc_secao"].apply(deep_clean)

        logger.success(f"Saving updated CSV to {self.file_path}...")
        df.to_csv(self.file_path, index=False)
        logger.info("Translation complete!")


if __name__ == "__main__":
    translator = BusinessStatusTranslator()
    translator.translate()
