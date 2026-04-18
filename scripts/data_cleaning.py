#!/usr/bin/env python3
import pandas as pd
from sqlalchemy import create_engine
import argparse
import os

def import_market_data(target_db):
    files_to_import = {
        "./historical_data/Akdital Stock Price History.csv": "akdital_data",
        "./historical_data/Attijariwafa Bank Stock Price History.csv": "attijari_data"
    }
    
    engine = create_engine(f"sqlite:///{target_db}")
    
    for file, table in files_to_import.items():
        try:
            df = pd.read_csv(file)
            df.columns = [c.strip().replace(' ', '_').lower() for c in df.columns]
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            
            df.to_sql(table, engine, if_exists='replace', index=False)
            print(f"✅ {os.path.basename(file)} -> {target_db} (Table: '{table}')")
            
        except Exception as e:
            print(f"❌ Erreur sur {file} : {e}")

if __name__ == "__main__":
    # 1. On définit les chemins possibles
    VAULT_PATH = "./data_secure/market_data.db"
    DEFAULT_PATH = "market_data.db"

    # 2. Logique d'auto-détection du Vault
    # Si le dossier data_secure existe et est monté, on l'utilise par défaut
    if os.path.exists("./data_secure") and os.path.ismount("./data_secure"):
        final_destination = VAULT_PATH
        print("🔒 Vault détecté et monté. Utilisation du stockage sécurisé.")
    elif os.path.exists("./data_secure"):
        # Le dossier existe mais n'est peut-être pas monté (coffre fermé)
        final_destination = VAULT_PATH
        print("⚠️ Dossier data_secure trouvé, écriture à l'intérieur.")
    else:
        final_destination = DEFAULT_PATH
        print("ℹ️ Vault non trouvé. Écriture à la racine.")

    # 3. On permet quand même de forcer un chemin via argument (optionnel)
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="Forcer une destination spécifique", default=final_destination)
    args = parser.parse_args()

    # 4. Exécution
    import_market_data(args.output)
