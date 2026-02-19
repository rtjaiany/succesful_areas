import pandas as pd
import geopandas as gpd
from pathlib import Path
import unicodedata
import re

def normalize_text(text):
    if pd.isna(text):
        return ""
    text = str(text).upper()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^A-Z0-9\s]', '', text)
    return text.strip()

def normalize_ibge_code(code):
    """Normalize IBGE code to 7-digit string without decimals."""
    if pd.isna(code):
        return None
    # Stringify and remove potential .0 from float conversion
    s = str(code).split('.')[0]
    # Zfill to 7 digits (some datasets might have 6 if they lost leading zero)
    return s.zfill(7)

def main():
    # Paths
    SHAPEFILE_PATH = Path("data/raw/shapefiles/BR_Municipios_2022/BR_Municipios_2022.shp")
    ROADS_PATH = Path("data/processed/road_predictors_muni_final.csv")
    INTEGRATED_CITIES_PATH = Path("data/processed/integrated_cities_data.csv")
    BUSINESS_PATH = Path("data/raw/business_data/business_status.csv")
    
    # Embeddings: find the most recent CSV
    EMBEDDINGS_DIR = Path("data/processed/")
    embedding_files = list(EMBEDDINGS_DIR.glob("municipality_embeddings_*.csv"))
    if embedding_files:
        EMBEDDINGS_PATH = sorted(embedding_files)[-1]
    else:
        EMBEDDINGS_PATH = None
        
    OUTPUT_PATH = Path("data/processed/final_integrated_dataset.csv")

    print("Step 1: Loading Master Shapefile (IBGE 5570 municipalities)...")
    master_gdf = gpd.read_file(SHAPEFILE_PATH)
    master_gdf['CD_MUN'] = master_gdf['CD_MUN'].apply(normalize_ibge_code)
    master_gdf['norm_name'] = master_gdf['NM_MUN'].apply(normalize_text)
    master_gdf['SIGLA_UF'] = master_gdf['SIGLA_UF'].astype(str).str.upper()

    print("Step 2: Merging Road Predictors...")
    if ROADS_PATH.exists():
        roads_df = pd.read_csv(ROADS_PATH)
        # Check column for code
        code_col = 'CD_MUN' if 'CD_MUN' in roads_df.columns else (roads_df.columns[0] if 'Unnamed' not in roads_df.columns[0] else roads_df.columns[1])
        roads_df[code_col] = roads_df[code_col].apply(normalize_ibge_code)
        
        # Merge on Code
        master_gdf = master_gdf.merge(roads_df, left_on='CD_MUN', right_on=code_col, how='left', suffixes=('', '_road'))
        if code_col != 'CD_MUN':
            master_gdf.drop(columns=[code_col], inplace=True)
    else:
        print(f"Warning: {ROADS_PATH} not found.")

    print("Step 3: Merging Integrated Cities Data...")
    if INTEGRATED_CITIES_PATH.exists():
        cities_df = pd.read_csv(INTEGRATED_CITIES_PATH)
        cities_df['cod_ibge'] = cities_df['cod_ibge'].apply(normalize_ibge_code)
        
        # Merge on Code
        master_gdf = master_gdf.merge(cities_df, left_on='CD_MUN', right_on='cod_ibge', how='left', suffixes=('', '_integrated'))
        master_gdf.drop(columns=['cod_ibge'], inplace=True, errors='ignore')
    else:
        print(f"Warning: {INTEGRATED_CITIES_PATH} not found.")

    print("Step 4: Merging Business Status...")
    if BUSINESS_PATH.exists():
        # Business data often uses semicolon
        try:
            business_df = pd.read_csv(BUSINESS_PATH, sep=';')
            if len(business_df.columns) < 2:
                business_df = pd.read_csv(BUSINESS_PATH, sep=',')
        except:
            business_df = pd.read_csv(BUSINESS_PATH)
            
        id_cols = ['cod_cidade', 'CD_MUN', 'CD_IBGE', 'code', 'cod_ibge']
        found_id_col = next((c for c in id_cols if c in business_df.columns), None)
        
        if found_id_col:
            business_df[found_id_col] = business_df[found_id_col].apply(normalize_ibge_code)
            master_gdf = master_gdf.merge(business_df, left_on='CD_MUN', right_on=found_id_col, how='left', suffixes=('', '_business'))
            if found_id_col != 'CD_MUN':
                master_gdf.drop(columns=[found_id_col], inplace=True)
        else:
            print("Warning: No ID column found for Business Status. Skipping.")

    print("Step 5: Merging Municipality Embeddings...")
    if EMBEDDINGS_PATH:
        embed_df = pd.read_csv(EMBEDDINGS_PATH)
        
        # State mapping for name-based matching
        STATE_MAP = {
            'RONDONIA': 'RO', 'ACRE': 'AC', 'AMAZONAS': 'AM', 'RORAIMA': 'RR', 'PARA': 'PA', 'AMAPA': 'AP', 'TOCANTINS': 'TO',
            'MARANHAO': 'MA', 'PIAUI': 'PI', 'CEARA': 'CE', 'RIO GRANDE DO NORTE': 'RN', 'PARAIBA': 'PB', 'PERNAMBUCO': 'PE', 
            'ALAGOAS': 'AL', 'SERGIPE': 'SE', 'BAHIA': 'BA', 'MINAS GERAIS': 'MG', 'ESPIRITO SANTO': 'ES', 'RIO DE JANEIRO': 'RJ', 
            'SAO PAULO': 'SP', 'PARANA': 'PR', 'SANTA CATARINA': 'SC', 'RIO GRANDE DO SUL': 'RS', 'MATO GROSSO DO SUL': 'MS', 
            'MATO GROSSO': 'MT', 'GOIAS': 'GO', 'DISTRITO FEDERAL': 'DF'
        }
        
        # Try name matching with state fallback
        name_col = next((c for c in ['municipality_name', 'NM_MUN', 'name'] if c in embed_df.columns), None)
        state_col = next((c for c in ['state_name', 'SIGLA_UF', 'state'] if c in embed_df.columns), None)
        
        if name_col:
            embed_df['norm_name_embed'] = embed_df[name_col].apply(normalize_text)
            if state_col:
                embed_df['norm_state'] = embed_df[state_col].apply(normalize_text)
                embed_df['SIGLA_UF_match'] = embed_df['norm_state'].map(STATE_MAP)
                # Fill missing if it was already a SIGLA_UF (2 letters)
                mask = (embed_df['SIGLA_UF_match'].isna()) & (embed_df['norm_state'].str.len() == 2)
                embed_df.loc[mask, 'SIGLA_UF_match'] = embed_df.loc[mask, 'norm_state']
                
                print(f"  Embeddings mapping sample: \n{embed_df[[name_col, state_col, 'SIGLA_UF_match']].head()}")
                
                master_gdf = master_gdf.merge(embed_df, left_on=['norm_name', 'SIGLA_UF'], right_on=['norm_name_embed', 'SIGLA_UF_match'], how='left', suffixes=('', '_embed'))
                master_gdf.drop(columns=['SIGLA_UF_match', 'norm_state', 'norm_name_embed'], inplace=True, errors='ignore')
            else:
                master_gdf = master_gdf.merge(embed_df, left_on='norm_name', right_on='norm_name_embed', how='left', suffixes=('', '_embed'))
                master_gdf.drop(columns=['norm_name_embed'], inplace=True, errors='ignore')

    print("Step 6: Cleaning up and saving result...")
    # Remove temporary columns
    temp_cols = [c for c in master_gdf.columns if 'norm_name' in c or 'SIGLA_UF_match' in c]
    master_gdf.drop(columns=temp_cols, inplace=True, errors='ignore')
    
    # Save as CSV
    master_gdf.to_csv(OUTPUT_PATH, index=False)
    
    print(f"\nFinal dataset created: {OUTPUT_PATH}")
    print(f"Total municipalities: {len(master_gdf)}")
    
    # Coverage Report
    print("\nMerge Coverage Report (Non-null counts):")
    # Columns we hope to see
    report_cols = ['CD_MUN', 'NM_MUN', 'total_road_km', 'avrg_monthly_salary', 'active', 'red', 'blue', 'embedding_0']
    available_cols = [c for c in report_cols if c in master_gdf.columns]
    print(master_gdf[available_cols].count())

if __name__ == "__main__":
    main()
