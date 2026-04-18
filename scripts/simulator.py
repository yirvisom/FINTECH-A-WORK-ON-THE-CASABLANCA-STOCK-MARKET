#!/usr/bin/env python3

import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import os

def run_simulation():
    # 1. Connexion à la base de données (Chemin vers votre Vault)
    db_path = 'data_secure/market_data.db'
    if not os.path.exists(db_path):
        print(f"❌ Erreur : La base de données est introuvable à l'adresse : {db_path}")
        print("Assurez-vous que votre vault est ouvert (make vault_open).")
        return

    engine = create_engine(f'sqlite:///{db_path}')
    
    # 2. Fonction interne de chargement (Bien indentée)
    def load_clean_data(table):
        # On récupère les données
        df = pd.read_sql(f"SELECT date, price FROM {table}", engine)
        
        # Conversion de la date
        df['date'] = pd.to_datetime(df['date'])
        
        # Nettoyage du prix : suppression des virgules et conversion en float
        df['price'] = (
            df['price']
            .astype(str)
            .str.replace(',', '', regex=False)
            .astype(float)
        )
        return df.sort_values('date')

    # Chargement des deux tables
    try:
        df_akdital = load_clean_data('akdital_data')
        df_attijari = load_clean_data('attijari_data')
    except Exception as e:
        print(f"❌ Erreur lors de la lecture des tables : {e}")
        return

    # 3. Synchronisation et calculs
    # On fusionne pour n'avoir que les dates où les deux actions sont cotées
    df = pd.merge(df_akdital, df_attijari, on='date', suffixes=('_akd', '_att'))
    
    # Paramètres de l'investissement
    cap_attijari = 525000
    cap_akdital = 175000
    cap_bdt = 300000
    taux_bdt_annuel = 0.035  # 3.5%

    # Prix au premier jour de la simulation
    price_start_akd = df['price_akd'].iloc[0]
    price_start_att = df['price_att'].iloc[0]
    
    # Nombre d'unités détenues
    nb_actions_akd = cap_akdital / price_start_akd
    nb_actions_att = cap_attijari / price_start_att

    # 4. Évolution du portefeuille
    df['val_akdital'] = df['price_akd'] * nb_actions_akd
    df['val_attijari'] = df['price_att'] * nb_actions_att
    
    # Calcul des Bons du Trésor (temps linéarisé)
    days_elapsed = (df['date'] - df['date'].iloc[0]).dt.days
    df['val_bdt'] = cap_bdt * (1 + taux_bdt_annuel)**(days_elapsed / 365)
    
    # Valeur Totale
    df['total_portfolio'] = df['val_akdital'] + df['val_attijari'] + df['val_bdt']

    # 5. Affichage des résultats
    final_val = df['total_portfolio'].iloc[-1]
    total_investi = cap_akdital + cap_attijari + cap_bdt
    profit_total = final_val - total_investi
    roi = (profit_total / total_investi) * 100

    print(f"\n--- Résumé de la Simulation ({df['date'].iloc[0].date()} au {df['date'].iloc[-1].date()}) ---")
    print(f"Valeur Finale Attijari : {df['val_attijari'].iloc[-1]:,.2f} MAD")
    print(f"Valeur Finale Akdital  : {df['val_akdital'].iloc[-1]:,.2f} MAD")
    print(f"Valeur Finale Bons Trésor : {df['val_bdt'].iloc[-1]:,.2f} MAD")
    print("-" * 50)
    print(f"VALEUR TOTALE DU PORTEFEUILLE : {final_val:,.2f} MAD")
    print(f"Performance Globale : {roi:+.2f}% ({profit_total:,.2f} MAD)")

    # 6. Génération du graphique
    plt.figure(figsize=(12, 7))
    plt.plot(df['date'], df['total_portfolio'], label='Total Portefeuille', color='black', linewidth=1.5)
    plt.stackplot(df['date'], df['val_attijari'], df['val_akdital'], df['val_bdt'], 
                  labels=['Attijariwafa Bank', 'Akdital', 'Bons du Trésor'], 
                  colors=['#1f77b4', '#ff7f0e', '#2ca02c'], alpha=0.6)
    
    plt.title('Simulation d\'Investissement : Akdital / Attijari / BdT', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Valeur du Portefeuille (MAD)')
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    output_graph = "evolution_portefeuille.png"
    plt.savefig(output_graph)
    print(f"\n📈 Graphique enregistré : {output_graph}")

if __name__ == "__main__":
    run_simulation()
