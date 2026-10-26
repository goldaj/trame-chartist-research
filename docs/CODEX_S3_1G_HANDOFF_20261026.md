# Codex — TRAME S3.1G : fiabilité des signaux de mouvement prévu (26/10/2026)

## Résultats et obligations hérités
Projet TRAME `goldaj/trame-chartist-research`.
S3.1F [PR #29](https://github.com/goldaj/trame-chartist-research/pull/29)
**COMPLÈTEMENT FINIE**, [run #40326818917](https://github.com/goldaj/trame-chartist-research/actions/runs/40326818917)
4/4 jobs réussis, 9 vrais entraînements
D1/H1/M1 et 81 scores de 3 règles à
poids identiques. Bilan :
`research/token_grammar/S3_1F_REAL_81_RESULTS_20261026.md`
et archive ZIP avec SHA. SOFT améliore
légèrement le MAE prix mais détériore
l'erreur d'amplitude de 10–12%.
Justesse direction SOFT == HARD
PAR CONSTRUCTION. AUCUN EDGE.

L'utilisateur souhaite particulièrement une
IA exacte à la fois sur SENS et MONTANT ;
ignore les frais et suppose qu'un humain
filtre les opportunités économiquement
intéressantes. Il faut **tester la qualité
conditionnelle** des grands signaux, pas
inventer un portefeuille profit.

## S3.1G protocole AVANT essais BTC
[PR #30 DRAFT](https://github.com/goldaj/trame-chartist-research/pull/30)
`chatgpt/trame-s3-selective-forecast-20261026`
enfant de #29 (pas de merge auto).
`research/token_grammar/S3_1G_SELECTIVE_PROTOCOL_20261026.md`.
9 modèles legacy S3.1F à 2000 updates
(D1/H1/M1 ×3 seeds), architecture/loss/
RNG/quantiles/G2 identiques. Sur chaque
modèle faire des prédictions sur TRAIN
avant 2020, en dériver **UNIQUEMENT**
les 4 seuils magnitude absolue
HARD all=0, q50, q75, q90.
Les appliquer au MONITOR 2020–2021,
puis scorer les TROIS règles S3.1F
HARD/DIRECT/SOFT sur les MÊMES
bougies. L'ancien dev externe
2022–25 et le holdout 2026
restent fermés.

**108 cellules de métriques dépendantes** =
9 modèles ×4 seuils ×3 règles.
PAS 108 entraînements. Couverture et
N cas conservés obligatoire ;
si <30 cas ou manque classe
réelle hausse/baisse, BA = null
et aucune interprétation. Comparer
sur les MÊMES cas la persistance.
Mesurer BA direction, accuracy,
MAE prix USD/bps, erreur
amplitude bps, biais classe,
quantité magnitude prévue vs réalisée.
La tête Brier n'est PAS un
score probabiliste de la direction
du bras DIRECT.

La distribution de magnitudes
TRAIN est **in-sample** car
modèle entraîné dessus ;
seuils non sélectionnés sur MONITOR
mais ce n'est ni out-of-fold
ni validation indépendante.
MONITOR 2020–21 a été exploré
à plusieurs reprises en S3.1C-F,
donc ne déclarer aucun edge.

## État technique au moment du handoff
- `selective_forecast.py` runner, seuils
  train-only, modèles legacy, capture
  cas et scores S3.1F ; `selective_panel.py`.
- `test_selective_forecast.py`,
  `test_selective_panel.py` :
  parité all-case exacte S3.1F (même
  modèle, graines et mini-batches),
  interdiction fuite MONITOR→seuils,
  impossibilité de fabriquer BA
  d'une classe absente, SHA
  de sélection identiques entre
  les trois règles.
- [CI artificielle #40329278603](https://github.com/goldaj/trame-chartist-research/actions/runs/40329278603)
  **SUCCESS**.
- Pilote trois horizons 40 updates,
  une graine
  [Actions #40329375986](https://github.com/goldaj/trame-chartist-research/actions/runs/40329375986),
  vérifier conclusion **3/3**.
- Workflow étude complète **à créer**,
  3 horizons ×3 vrais fits chacun,
  36 cellules par horizon ; agrégateur
  strict 9 fits/108 scores.
  Vérifier les 4 jobs et les JSON/MD
  + SHA256 avant bilan.
- `docs/CHATGPT_PROJECT_HISTORY.md`
  doit conserver cette suite pour Codex ;
  `AGENTS.md` doit référencer le
  présent document, PR #30 et
  issue #20.

## Interprétation à éviter
- Coverage q90 != forcément 10% MONITOR.
- « BA forte mais 8 cas » n'est
  pas une preuve de justesse.
- Comparer Soft/HARD/DIRECT sur
  **le même masque sélection HARD**.
- MAE SOFT plus faible peut être
  juste un shrink vers le dernier prix.
- AUCUNE recette de trading prouvée
  ni PnL cumulé, aucune transaction
  Hyperliquid. Frais ignorés selon
  consigne propriétaire.
- Pas de nouvelle architecture ni
  grammaire avant ce diagnostic.
- **Après S3.1G : geler les révisions
  successives sur monitor 2020–21**,
  proposer une validation séparée
  confirmatoire sur période encore
  isolée, sans ouvrir 2026 trop tôt.
