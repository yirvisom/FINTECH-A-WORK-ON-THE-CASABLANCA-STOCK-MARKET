#!/bin/bash

# 1) Let's create a 10GB "container" file in our home directory
truncate -s 10G ~/finance_vault.img

# 4) Let's encrypt it with cryptsetup
sudo cryptsetup luksFormat ~/finance_vault.img

# 5) We then open the encrypted volume
sudo cryptsetup open ~/finance_vault.img DecryptedWork

# 6) We now format it for red hat systems (most used in finance companies)
sudo mkfs.xfs /dev/mapper/DecryptedWork

# 7) Now we mount it
sudo mkdir -p ~/secure_project
sudo mount /dev/mapper/DecryptedWork ~/secure_project
sudo chown yirviel:yirviel ~/secure_project

