# --- Variables ---
PYTHON      = python3
VENV        = venv
BIN         = $(VENV)/bin
JUPYTER     = $(BIN)/jupyter-lab
SCRIPTS     = ./scripts

# Variables Vault
VAULT_IMG   = finance.img
VAULT_NAME  = finance_vault
MOUNT_POINT = ./data_secure
SIZE        = 500M

# Couleurs pour le terminal
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
RED    := $(shell tput -Txterm setaf 1)
RESET  := $(shell tput -Txterm sgr0)

.PHONY: help setup vault_setup vault_open vault_close run clean data_clean check_mount

help:
	@echo "$(GREEN)Usage: make [cible]$(RESET)"
	@echo ""
	@echo "  $(YELLOW)make setup$(RESET)        : Crée le venv et installe les dépendances"
	@echo "  $(YELLOW)make vault_setup$(RESET)  : Crée et formate l'image chiffrée"
	@echo "  $(YELLOW)make vault_open$(RESET)   : Ouvre et monte le coffre-fort"
	@echo "  $(YELLOW)make data_clean$(RESET)   : Nettoie et injecte directement dans le vault"
	@echo "  $(YELLOW)make run$(RESET)          : Lance Jupyter Lab (vérifie le vault)"
	@echo "  $(YELLOW)make vault_close$(RESET)  : Démonte et ferme le coffre-fort"

# --- Vérification du montage ---
check_mount:
	@mountpoint -q $(MOUNT_POINT) || (echo "$(RED)❌ Erreur: Le vault n'est pas monté dans $(MOUNT_POINT)$(RESET)"; exit 1)

# --- Installation ---
setup:
	@echo "$(GREEN)--- Configuration de l'environnement ---$(RESET)"
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements.txt
	@echo "$(GREEN)Environnement prêt.$(RESET)"

# --- Sécurité (LUKS + XFS) ---
vault_setup:
	@echo "$(GREEN)--- Création du container chiffré ---$(RESET)"
	truncate -s $(SIZE) $(VAULT_IMG)
	sudo cryptsetup luksFormat $(VAULT_IMG)
	sudo cryptsetup open $(VAULT_IMG) $(VAULT_NAME)
	sudo mkfs.xfs /dev/mapper/$(VAULT_NAME)
	sudo cryptsetup close $(VAULT_NAME)
	@mkdir -p $(MOUNT_POINT)
	@echo "$(GREEN)Coffre-fort créé avec succès.$(RESET)"

vault_open:
	@mkdir -p $(MOUNT_POINT)
	@if [ ! -L /dev/mapper/$(VAULT_NAME) ]; then \
		sudo cryptsetup open $(VAULT_IMG) $(VAULT_NAME); \
	fi
	@if ! mountpoint -q $(MOUNT_POINT); then \
		sudo mount /dev/mapper/$(VAULT_NAME) $(MOUNT_POINT); \
		sudo chown $(USER):$(USER) $(MOUNT_POINT); \
	fi
	@echo "$(GREEN)✅ Vault ouvert et monté dans $(MOUNT_POINT).$(RESET)"

# --- Nettoyage et Importation Sécurisée ---
# On force l'utilisation de l'argument --output pour être 100% sûr du chemin
data_clean: check_mount
	@echo "$(GREEN)🧹 Nettoyage et injection directe dans le vault...$(RESET)"
	$(BIN)/python $(SCRIPTS)/data_cleaning.py --output $(MOUNT_POINT)/market_data.db
	@echo "$(GREEN)🚀 $(MOUNT_POINT)/market_data.db mis à jour.$(RESET)"

# --- Exécution ---
run: vault_open
	@echo "$(GREEN)Starting Jupyter Lab...$(RESET)"
	$(JUPYTER) notebooks/presentation.ipynb

vault_close:
	@echo "$(YELLOW)Fermeture sécurisée...$(RESET)"
	@if mountpoint -q $(MOUNT_POINT); then sudo umount $(MOUNT_POINT); fi
	@if [ -L /dev/mapper/$(VAULT_NAME) ]; then sudo cryptsetup close $(VAULT_NAME); fi
	@echo "$(GREEN)✅ Vault fermé et verrouillé.$(RESET)"

clean:
	rm -rf __pycache__ .ipynb_checkpoints
	@echo "Nettoyage des fichiers temporaires terminé."
