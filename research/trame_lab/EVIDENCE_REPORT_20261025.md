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
- [ ] **A8.2 — Adaptation contrôlée** : validation stricte de
  provenance, schéma, JSON fini, résultats non dupliqués,
  garde-fous contre revendications `compute_matched`
  ou `reserved_synthetic_test_opened`.
- [ ] **A8.3 — Présentation autonome** : HTML sémantique et
  JSON companion avec titre, corps de preuve, tableau lisible,
  liens de reproduction, limites, aucune donnée du portefeuille
  ni interprétation commerciale.
- [ ] **A8.4 — Tests et CI** : fixtures JSON *fabriquées*,
  injection HTML hostile, source mal formée, duplicate seed,
  double-output, overwrite, état de preuve trompeur ; test CLI.
- [ ] **A8.5 — Livraison/documentation** : commandes,
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
