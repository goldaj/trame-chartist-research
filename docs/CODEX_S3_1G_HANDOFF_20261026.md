# POINT D'ARRÊT OFFICIEL — S3.1G TERMINÉE (26/10/2026)

**Le propriétaire demande de finir proprement, documenter GitHub et LISTER LA SUITE ; il ne demande PAS de lancer un nouveau cycle de recherche maintenant. ARRÊT VOLONTAIRE APRÈS CETTE PASSATION.**

**Vérification GitHub :** [run #40329836255](https://github.com/goldaj/trame-chartist-research/actions/runs/40329836255) **4/4 jobs SUCCESS**, SHA scientifique `d2db41a6cce09067e168ab4082c4c713b2d1d153`. Trois horizons D1/H1/M1, trois graines, **9 entraînements réels** et **108 cellules dépendantes** = 9×4 seuils×3 règles, avec tableau agrégé validé (36 lignes, 24 familles de deltas). Aucun nouveau modèle n'a été exécuté pour cette clôture. S3.1F était **déjà terminée** [run #40326818917](https://github.com/goldaj/trame-chartist-research/actions/runs/40326818917), 9 modèles/27 checkpoints/81 mesures et PR #29 DRAFT. Ne PAS revenir à S3.1F.

**Source de vérité résultats S3.1G :** `research/token_grammar/S3_1G_REAL_108_RESULTS_20261026.md` (chiffres détaillés, témoins mêmes cas, SHA source, limites, roadmap, artefacts). Observations : BA HARD q90 **50,00% D1**, **50,39% H1**, **52,50% M1** contre BA all **52,24/51,93/53,02%** ; couverture q90 MONITOR **7,3/11,2/4,3%**, n moyen **53/115/44** ; aucun gain directionnel et montant convaincant. Plusieurs MAE prix supérieurs à persistance sur le **même masque**. SOFT contracte prix mais détériore erreur amplitude. Aucune rentabilité, validation indépendante ou edge démontrés.

**Causalité :** train labels <2020 ; monitor interne 2020–2021 déjà sur-utilisé ; ancien dev externe 2022–2025 et holdout 2026 NON OUVERTS, aucune réoptimisation des seuils sur monitor. Frais exclus à la demande propriétaire ; absence de frais ne prouve pas profit. Aucun ordre Hyperliquid, wallet, clé ou donnée de compte.

**Backlog ordonné au point d'arrêt :**
1. S3.1H : préenregistrer AUDIT de calibration et robustesse par magnitude et régimes, tester décalage train/monitor, dépendance des bougies, baselines comparables sans ouvrir test.
2. Contrôler mécanique sampling M1 (stride60), cohortes temporelles et sortie signée/amplitude ; prioriser signaux non monoclasse.
3. Gel de configuration confirmatoire et critères Go/No-Go AVANT tout holdout indépendant ; aucune affirmation à partir du monitor réutilisé.
4. S3.2 : grammaires alternatives (patches 4/8/16, embeddings vectoriels, signe/magnitude), **une variable changée à la fois**, coûts et horizon contrôlés.
5. S4 : scaling taille × profondeur (ex. 1/2/4 couches) seulement après diagnostic, contrôler params/compute, rapporter BA ET MAE du prix USD/bps ET erreur amplitude.
6. Livrable seulement après validation indépendante et conformité/sécurité ; pas de trade live.

**Gestion GitHub :** conserver PR #30 DRAFT (fille de #29), autres PRs empilées en brouillon ; NE PAS merger ni lancer de CI/entraînement additionnel automatiquement. Une prochaine séance part de **ce fichier, AGENTS.md, l'issue #20 et le rapport S3.1G**.

---

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
