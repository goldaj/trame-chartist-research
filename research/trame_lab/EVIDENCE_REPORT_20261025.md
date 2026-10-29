# A8 — consolidation de preuves hors ligne dans TRAME Research Lab

Date : 25 octobre 2026. La présente voie transforme des artefacts
d'expériences **réellement exécutées** en un rapport HTML/JSON
**sans inventer** de résultat financier ni ajuster de modèle.

## Décomposition des sous-tâches

- [x] **A8.1 — Schéma des preuves et politique de comparaison.**
  Entrées initialement autorisées : artefacts JSON A3c
  (`trame_a3c_proxy_budget_synthetic_pilot_v0.1`) et A5
  (`a5_attention_gru_control_paired_synthetic_v0.1`).
  Chaque panneau conserve son protocole, statut
  `ARTIFICIAL_ONLY` / `ARTIFICIAL_TRAIN_AND_DEVELOPMENT`,
  seeds, paramètres et ses avertissements ; il n'y a jamais de
  classement inter-protocoles.
- [x] **A8.2 — Adaptation contrôlée** : validation stricte de
  provenance, schéma, JSON fini, résultats non dupliqués,
  garde-fous contre revendications `compute_matched`
  ou `reserved_synthetic_test_opened`.
- [x] **A8.3 — Présentation autonome** : HTML sémantique et
  JSON companion avec titre, corps de preuve, tableau lisible,
  liens de reproduction, limites, aucune donnée du portefeuille
  ni interprétation commerciale.
- [x] **A8.4 — Tests et CI** : fixtures JSON *fabriquées*,
  injection HTML hostile, source mal formée, duplicate seed,
  double-output, overwrite, état de preuve trompeur ; test CLI.
- [x] **A8.5 — Livraison/documentation** : commandes,
  renvois vers PR/Actions, critères d'admissibilité, bilan.
  Ne pas présenter une comparaison compute-fair complète.

## Frontières et risques

A3c compare trois architectures et des nombres de pas ajustés
sur une **fraction seulement** des opérations PyTorch comptées.
A5 compare quatre architectures avec le même nombre de pas
mais **sans** égaliser les paramètres ou les FLOPs.
Les moyennes NLL de ces deux expériences ne sont **pas**
interchangeables ; chaque table doit conserver sa provenance.

Les traces stockées dans la CI restent la source de vérité.
Un fichier JSON qui a les bonnes clés mais aucune signature
n'est pas une preuve indépendante : afficher l'identifiant de
l'artefact, son SHA si fourni et signaler qu'aucune vérification
cryptographique n'est effectuée par cette v0.1.

Les anciens rapports v0.1 `research/trame_lab/cli.py` ne sont
pas réécrits ; ce générateur est un *module complémentaire*.
Il fonctionne hors ligne sans GPU ni BTC privé.

## Utilisation des résultats `A3c` et `A5`

Extraire **les véritables fichiers JSON** des artéfacts GitHub Actions
à partir des runs dont le commit a été conservé :

- [A3c run #40219261965](https://github.com/goldaj/trame-chartist-research/actions/runs/40219261965) :
  `synthetic_a3c_proxy_budget.json`, pilote apparié à budgets
  d'opérations *partiellement comptées*.
- [A5 run #40220598879](https://github.com/goldaj/trame-chartist-research/actions/runs/40220598879) :
  `a5_synthetic_hybrid.json`, comparaison à même nombre de pas.

Après extraction des JSON dans un même répertoire local,
exécuter depuis la racine du projet (Python 3.12 uniquement ;
aucun paquet supplémentaire n'est requis) :

```powershell
python -m research.trame_lab.evidence_report --input synthetic_a3c_proxy_budget.json --input a5_synthetic_hybrid.json --output trame_evidence.html
```

Le programme écrit `trame_evidence.html` et
`trame_evidence.json` sans écraser un fichier préexistant ;
ouvrir le HTML directement dans un navigateur. Un SHA-256 est
**calculé sur les octets du JSON d'entrée** pour reproduire le rapport,
mais **il ne prouve pas l'authenticité de sa provenance**.
La création des deux sorties n'est pas une transaction atomique
en cas d'arrêt brutal entre les écritures.

Pour lancer seulement les tests :

```powershell
python -m unittest research.trame_lab.test_evidence_report -v
```

CI GitHub Actions : `.github/workflows/trame-a8-evidence.yml`,
[run vert #40222019571](https://github.com/goldaj/trame-chartist-research/actions/runs/40222019571).

## Statut

**A8.1 à A8.5 livrées pour un rapport de preuves synthétiques
exploratoires**. L'importation de métriques financières,
le contrôle navigateur/lecteur d'écran, la validation
cryptographique des sources, l'intégration dans un produit
complet et une évaluation utilisateurs **restent ouverts**.

Ce module ne classe jamais entre eux des modèles exécutés
sous les différents protocoles A3c et A5. Il complète le
Research Lab existant, sans prétendre être la version P4.
