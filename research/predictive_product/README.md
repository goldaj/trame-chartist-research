# TRAME Predictive v1 : laboratoire produit, non déployable

**25 octobre 2026 : statut NO-GO de livraison.**
Cette branche est un jalon d'ingénierie pour préparer une
application financière future, **pas** une version de
prévision de marchés fonctionnelle. Ni l'interface de
prédiction définitive, ni les checkpoints entraînés et
validés sur BTC, ni les backtests économiques réels
n'existent ici.

## Sous-tâches produit et états

| Sous-tâche | Livré maintenant | Non livré |
| --- | --- | --- |
| P4.1 frontière sans transactions | `release_preflight.py` contrôle et interdit tout feu vert automatique | audit de sécurité indépendant |
| P4.2 interface | critères d'étiquetage et Research Lab HTML synthétique | UI de prévision de marchés avec vrai checkpoint |
| P4.3 versions | contrat de manifeste et empreinte, SHA-256 des rapports A8 | artefacts modèles certifiés issus d'essais réels |
| P4.4 installation | CLI autonome utilisant stdlib pour les gardes | installateur multiplateforme validé, packaging GPU |
| P4.5 qualité | tests adversariaux automatisés de cette branche | test navigateur/lecteur d'écran, revue UX |
| P4.6 publication | blocage automatique maintenu | **NO-GO**, revue indépendante et validation BTC absentes |

## Exécuter les outils sûrs hors ligne

Depuis la racine du clone :

```powershell
python -m research.predictive_product.release_preflight
python -m research.predictive_product.transaction_sandbox > p3_artificial_costs.json
python -m unittest research.predictive_product.test_safety -v
```

Aucun paquet externe requis pour ces seuls scripts ; les tests
n'accèdent pas à un exchange, une clé, un modèle préentraîné
ni aux archives BTC privées.

`release_preflight` renvoie `BLOCKED` et
`ready_for_launch: false` par défaut ; un fichier de
déclarations auto-attestées complet peut seulement conduire
à `EXTERNAL_REVIEW_REQUIRED`, **jamais** à un feu vert
automatique. Ce programme n'authentifie pas les preuves.

`transaction_sandbox` exécute un chemin de prix
**entièrement artificiel**, avec coût de transaction
exprimé en points de base, hypothèse de funding par période,
drawdown et exposition plafonnée. Ce n'est ni un
simulateur de carnet, ni une reconstruction réaliste des
spreads/frais/funding de perpétuels historiques.

## Besoins avant une version livrable

1. Campagne réelle sur historique BTC privé D1/H1/M1,
   avec scores natifs et baselines non triviales,
   sans toucher aux labels 2026 réservés avant gel.
2. Vérification de l'équité en calcul et des modèles
   réellement exécutés (Mamba sur CUDA si candidat),
   risques de poids non commerciaux et de contamination.
3. Sélection/entraînement reproductibles et checkpoints
   de modèles avec manifeste et empreinte.
4. Validation indépendante/calibration et robustesse
   hors échantillon ; résultats négatifs conservés.
5. Simulation économique *réaliste* et revue des hypothèses.
6. Interface locale fonctionnelle, installation Windows
   et Linux, tests navigateur, documentation, sécurité,
   conformité du packaging et arbitrage humain final.

Voir [RELEASE_GATES_20261025.md](RELEASE_GATES_20261025.md),
et le tableau de bord central
`docs/CODEX_EXECUTION_BOARD_20261025.md` sur la branche #10.

**Statut exact : les contrats P1/P2/P4 et la sandbox
numérique P3 sont des livrables d'ingénierie, la
validation scientifique financière et TRAME Predictive v1
restent non terminées.**
