# 📊 Casablanca Quant Framework (BVC)

### *Financial Engineering meets Linux Systems Security*

Ce dépôt contient un environnement de recherche quantitative dédié au marché boursier marocain (**Bourse de Casablanca**). Il intègre des outils d'analyse de portefeuille, des simulations de Monte-Carlo et une architecture de stockage sécurisée.

## 🛡️ La Sécurité au Service de la Finance

Contrairement aux projets standards, celui-ci repose sur un **Trusted Storage Design**. Les données financières sensibles (exports BVC, bases de données SQLite) ne sont jamais stockées "en clair" sur le disque dur.

  * **Chiffrement LUKS :** Les données résident dans une image disque chiffrée de 500 Mo.
  * **Système de fichiers XFS :** Performance optimisée pour les volumes de données financiers.
  * **Isolation Git :** Le container chiffré (`finance.img`) est automatiquement ignoré par Git, garantissant zéro fuite de données vers le cloud.

## 🚀 Fonctionnalités

  * **Monte-Carlo Engine :** Simulation de trajectoires pour les actifs de la BVC (Akdital, TGCC, IAM, etc.).
  * **Portfolio Optimizer :** Calcul du ratio de Sharpe et de la frontière efficiente.
  * **Secure Workflow :** Gestion complète via `Makefile` pour un déploiement fluide sur Linux.

## 🛠️ Installation & Utilisation

Le projet est entièrement automatisé pour **Fedora/Red Hat**.

### 1\. Préparer l'environnement

Clonez d'abord le travail :

```bash
git clone (https://github.com/yirvisom/FINTECH-A-WORK-ON-THE-CASABLANCA-STOCK-MARKET.git)
```

Installe les dépendances Python dans un environnement virtuel isolé :

```bash
make setup
```

### 2\. Initialiser le coffre-fort (Vault)

Crée ton image chiffrée LUKS. *Tu devras choisir une phrase de passe forte.*

```bash
make vault_setup
```

### 3\. Workflow Quotidien

Pour commencer à travailler sur tes modèles :

```bash
make vault_open   # Déverrouille et monte le dossier data_secure/
make data_clean   # Nettoie les données et les met dans le vault sécurisé
make run          # Lance Jupyter Lab
```

Une fois le travail terminé, sécurise tout :

```bash
make vault_close  # Démonte le volume et ferme le tunnel chiffré
```

## 📂 Structure du Projet

  * `historical_data` : Data des variations de cours des deux actions (très importants pour les simulations).
  * `notebooks/` : Analyses interactives et visualisations.
  * `data_secure/` : **[COFFRE-FORT]** Accessible uniquement quand le vault est monté.
  * `Makefile` : Le centre de pilotage du projet.
  * `scripts` : La partie "code" contenant les fichiers à exécuter pour les différentes analyses.

## APRÈS SIMULATION... 

<img width="1270" height="680" alt="image" src="https://github.com/user-attachments/assets/4e98cd9a-dd96-4a1e-ae20-5d136577d49c" />


Analyse Prédictive : La Simulation de Monte-Carlo
La simulation de Monte-Carlo transforme les données historiques (le "tempérament" passé des actifs) en un modèle de probabilités futures. Nous avons simulé 1 000 scénarios possibles pour l'évolution de notre million de MAD sur l'année 2026-2027.

1. Pourquoi cette dispersion (les lignes grises) ?
Chaque ligne grise représente une trajectoire possible du marché.

L'écartement des lignes illustre la volatilité cumulée d'Akdital et d'Attijariwafa Bank. Plus l'éventail est large, plus le marché est incertain.
La ligne rouge (Moyenne) représente le scénario central. Si elle est ascendante, cela confirme que le portefeuille a un "biais haussier" basé sur ses performances historiques.
2. Gestion du Risque : La Value at Risk (VaR 95%)
La VaR est l'indicateur de référence en gestion de fonds. Elle répond à la question : "Dans le pire des cas (hors catastrophe majeure), combien puis-je perdre ?"

Interprétation : Une VaR 95% signifie que dans 950 scénarios sur 1000, votre capital restera au-dessus de ce montant.
Décisionnel : C'est ce chiffre qui permet de rassurer les investisseurs en fixant une "limite de perte probable". Si la VaR est de 920 000 MAD, on sait que le risque de perdre plus de 8% du capital est statistiquement très faible (5%).
3. Conclusion pour la Stratégie d'Avril 2026
Cette simulation nous permet de passer d'une intuition à une stratégie chiffrée :

Allocation : Si la dispersion est trop forte (lignes grises trop écartées), nous pourrions décider de réduire la part d'Akdital pour augmenter celle des Bons du Trésor.
Objectif : La tendance centrale nous donne un objectif de rendement réaliste pour notre rapport de gestion de fin d'année.
Note technique : Les simulations reposent sur l'hypothèse que les rendements suivent une loi normale et que la volatilité de 2025 restera similaire en 2026.
-----

**Auteur :** [Yirviel Somé](https://github.com/yirvisom) – Finance Student & Linux Passionate.
