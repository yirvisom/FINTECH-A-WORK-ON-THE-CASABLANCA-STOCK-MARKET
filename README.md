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
git clone https://github.com/yirvisom/Finance_Project.git
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
make run          # Lance Jupyter Lab
```

Une fois le travail terminé, sécurise tout :

```bash
make vault_close  # Démonte le volume et ferme le tunnel chiffré
```

## 📂 Structure du Projet

  * `core/` : Logique métier (calculs financiers, scripts Python).
  * `notebooks/` : Analyses interactives et visualisations.
  * `data_secure/` : **[COFFRE-FORT]** Accessible uniquement quand le vault est monté.
  * `Makefile` : Le centre de pilotage du projet.

## APRÈS SIMULATION... 

<img width="1046" height="665" alt="image" src="https://github.com/user-attachments/assets/73d8e9dc-7245-476d-9e7a-93144767b2b4" />

## Conclusion Décisionnelle
Grâce à cette simulation, nous observons une VaR 95% à 869 660 MAD. Cela signifie qu'il n'y a que 5% de chances que notre capital tombe en dessous de ce seuil à un an.

## Recommandation : Cette stratégie "Prudente" est idéale pour un investisseur souhaitant s'exposer au marché boursier marocain tout en préservant son capital initial contre une perte supérieure à 13%.
-----

**Auteur :** [Yirviel Somé](https://github.com/yirvisom) – Finance Student & Linux Passionate.
