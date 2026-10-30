# Audit de branches GitHub — passation 30 octobre 2026

**Périmètre vérifié :** branches et PR ouvertes. **Périmètre restant :** diff complet de chaque branche, exécution des tests, CI et validation fonctionnelle. Ne pas assimiler inventaire et certification.

- Dépôt : `goldaj/trame-chartist-research` ; branche par défaut : `main`.
- PR ouvertes : aucune.

## Branches (33)
- `chatgpt/btc-h1-m1-20261025`
- `chatgpt/btc-history-bridge-20261025`
- `chatgpt/mini-transformer-synthetic-20261025`
- `chatgpt/p1b0-numerical-lab-20261025`
- `chatgpt/p1b0-stage1-validation-20261025`
- `chatgpt/paired-benchmark-sandbox-20261025`
- `chatgpt/point-in-time-data-contract-20261025`
- `chatgpt/review-20261024`
- `chatgpt/trame-btc-stat-baselines-20261025`
- `chatgpt/trame-compute-fair-20261025`
- `chatgpt/trame-continuous-direction-20261026`
- `chatgpt/trame-d1-parity-20261026`
- `chatgpt/trame-forecast-foundations-20261025`
- `chatgpt/trame-grammar-audit-20261026`
- `chatgpt/trame-hybrid-controls-20261025`
- `chatgpt/trame-lab-hardening-20261025`
- `chatgpt/trame-mamba-ssm-20261025`
- `chatgpt/trame-multi-architecture-20261025`
- `chatgpt/trame-predictive-delivery-gates-20261025`
- `chatgpt/trame-public-btc-data-import-20261026`
- `chatgpt/trame-representation-ablation-20261026`
- `chatgpt/trame-research-lab-evidence-20261025`
- `chatgpt/trame-research-lab-v01-20261025`
- `chatgpt/trame-s3-learned-embeddings-20261026`
- `chatgpt/trame-s3-objective-ablation-20261026`
- `chatgpt/trame-s3-postprocess-ablation-20261026`
- `chatgpt/trame-s3-predictive-grammars-20261026`
- `chatgpt/trame-s3-reconciliation-loss-20261026`
- `chatgpt/trame-s3-selective-forecast-20261026`
- `chatgpt/trame-s3-training-dynamics-20261026`
- `chatgpt/trame-s3-true-token-embeddings-20261026`
- `chatgpt/trame-scaling-depth-direction-20261026`
- `main` (défaut)

## Défis / décisions pour l'agent suivant
- Les 28 PR historiques clôturées sans fusion explicite ont été comparées à `main` et sont ancêtres de la branche de consolidation au moment de l'audit. Trois fusions documentaires/recherche additionnelles ont été effectuées le 30 octobre.
- Contrôler les protocoles point-in-time, droits des jeux de données, leakage, ablations et validation hors échantillon. Ne pas assimiler résultats synthétiques à des performances de trading.
- Comparer chaque branche à sa cible (SHA, ahead/behind, fichiers et PR) avant de supprimer quoi que ce soit.
- Préserver la production et les releases. Exécuter tests et build avant intégration.

**Statut :** inventaire réalisé, audit complet du code et des tests non terminé.
