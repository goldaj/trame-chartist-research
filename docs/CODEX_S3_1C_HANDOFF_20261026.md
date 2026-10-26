# Codex TRAME S3.1C — dynamique de convergence et prédictions monoclasse
26 octobre 2026. **PR #26 en brouillon**, branche
`chatgpt/trame-s3-training-dynamics-20261026`
parent de #25 S3.1B (puis #24, #23).
Pas de merge automatique. Demande utilisateur
« t'as crash, continue », après récupération
S3.1B et ses **432 fits BTC réels**.

## Motivation et hypothèses
[S3.1B run #40306642813](https://github.com/goldaj/trame-chartist-research/actions/runs/40306642813)
**4/4 jobs réussis**, 432 modèles.
Rapport et empreintes :
`research/token_grammar/S3_1B_REAL_432_RESULTS_20261026.md`.
Les embeddings **nn.Embedding(11,1)** à
initialisation ordonnée ne surpassent pas
les centres numériques de façon nette.
L'initialisation random entraîne
souvent un comportement monoclasse,
ex. H1 G2 Joint 11/12 random vs 0/12
ordered et decoded. Direction BA~50%,
pas de gain net conjoint direction/amplitude.

**Question nouvelle S3.1C** : 200 updates
de S3.1B suffisent-ils pour conclure,
ou est-ce du sous-entraînement / des
gradients instables qui provoquent
le collapse ? Protocole préenregistré
avant résultats :
`research/token_grammar/S3_1C_CONVERGENCE_PROTOCOL_20261026.md`.

## Distinction de cohortes CRITIQUE
NE PAS réutiliser le DEV EXTERNE 2022–2025
pour choisir le budget des updates. Il a
déjà été consulté par les travaux précédents.
NE PAS ouvrir le HOLDOUT 2026.
L'étude S3.1C utilise seulement les cas
**historiques TRAIN avant 2022**, par
`iter_cases(..., train_only=True)`,
sans construire d'exemples dev externes.
Deux réservoirs séparés, deux RNG :
- **TRAIN_INTERNAL** avec label connu
  `label_available_time < 2020-01-01 UTC`.
  **SEULE** source de gradients, normaliseur,
  quantiles G2, prior P(up), baseline.
- **MONITOR_INTERNAL** avec cible disponible
  `2020-01-01 <= time < 2022-01-01 UTC`.
  Aucun gradient, quantile, seuil ni
  sélection de normalisation depuis lui.
  Les seuls usages sont perte de suivi,
  direction BA/monoclasse, MAE prix
  USD/bps et amplitude et Brier.
- Le cas dont le label est disponible
  **exactement à 2022-01-01** est
  explicitement *exclu* même si l'ancien
  `iter_cases` le classait TRAIN.

## Sous-étapes réellement implémentées
- `research/token_grammar/convergence.py`
  - `collect_internal` réserve au plus 4096
    TRAIN +1024 MONITOR avec RNG et
    sampling indépendants, M1 stride60.
  - `split_internal_pre2022` fail-closed
    pour chaque label hors plage et 2026.
  - G2 11 tokens, mêmes modèles
    decoded/ordered/random que S3.1B,
    loss Joint et backbone width16 depth1.
  - `torch.manual_seed(seed)` et
    séquence mini-batches identiques pour
    les bras au même seed.
  - **27 trajectoires** = trois horizons
    ×3 bras×3 seeds, **chacune réellement
    2000 mises à jour sur le même optimiseur**.
    Checkpoints **200, 800, 2000** =
    81 observations internes, pas
    81 fits séparés.
  - Gradient global AVANT clip, fraction
    clipping, `last_minibatch_loss`,
    `train_monitor_loss`,
    `internal_validation_monitor_loss`,
    scores direction/amplitude et Brier,
    train-only prior et baselines,
    empreintes SHA cohortes/code.
- `research/token_grammar/convergence_panel.py`
  agrège strictement 3 bras/checkpoint,
  vérifie SHA backbone/params +11,
  temporel pré-2022, tableau multi-horizon
  27 trajectoires /81 checkpoints et
  18 contrastes, données ouvertes uniquement
  pour validation interne.
- Tests `test_convergence.py` et
  `test_convergence_panel.py` sur
  chiffres inventés (validation interne
  distincte, aucune 2022–25/2026,
  stops et empreintes de modèles).
- CI `.github/workflows/trame-s3-convergence-fixtures.yml`
  **verte** sur fixtures artificielles.
- Vraie exécution
  `.github/workflows/trame-s3-convergence-real.yml`,
  [Actions #40309653884](https://github.com/goldaj/trame-chartist-research/actions/runs/40309653884).
  **VÉRIFIER la conclusion réelle**, les trois
  jobs D1/H1/M1 + l'agrégateur
  avant d'annoncer tout résultat.

## Critères de décision
Une simple réduction de loss n'est pas
un gain de trading ; la question est
d'améliorer **simultanément le sens (BA,
%UP, collapse) ET le montant (MAE
USD/bps, erreur amplitude bps)** sur
MONITOR interne 2020–21.
Présenter les diagnostics grad clipping,
loss train/validation et Brier vs prior
calculé **sur TRAIN INTERNAL**,
avec dispersion des trois seeds.
Scores internes ne sont pas confirmation
généralisable ; ni 2022–25, ni 2026
ne sont à reconsulter par ce protocole.

## Après le run
1. Si 4/4 jobs réussis, télécharger les
   3 JSON de cohortes et le panel MD/JSON ;
   vérifier SHA256, conserver et documenter
   sous `research/token_grammar/S3_1C_...`.
2. Conclure si le collapse persiste
   avec plus de steps ou si train/monitor
   divergent ; expliquer limites.
3. Faire suivre l'issue #20,
   `AGENTS.md`,
   `docs/CHATGPT_PROJECT_HISTORY.md`
   et PR #26, sans prétendre
   à un modèle trading/Hyperliquid.
4. Prioriser le prochain choix scientifique :
   si overfit -> régularisation/context length ;
   si underfit -> budget d'entraînement
   et loss directionnelle ;
   si monoclasse malgré convergence ->
   choix de cible/head/calibration.
5. Seulement ensuite nouvel embedding
   vectoriel ou gros réseau S4 avec
   paramètres/FLOPs honnêtes.

Frais ignorés selon demande utilisateur,
aucune transaction, aucun PnL capitalisé.
La source BTC spot est publique/licenciée
et vérifiée par SHA. Aucun secret/wallet
ou données de compte dans TRAME.
