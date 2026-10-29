# S3.1F TERMINÉE : 9 vrais modèles BTC, 27 checkpoints, 81 prédictions appariées (26/10/2026)

**Run COMPLET** [Actions #40326818917](https://github.com/goldaj/trame-chartist-research/actions/runs/40326818917)
**4/4 jobs SUCCESS** D1/H1/M1 + panel.
Source Git SHA exécuté
`58bc0f1e9425975a037ad2bf135943890a5b474b`.

**Résultats scientifiques complets et SHA des 5 fichiers** :
`research/token_grammar/S3_1F_REAL_81_RESULTS_20261026.md`.
5 fichiers JSON/MD réels + MANIFEST archivés
dans la conversation au nom
`trame_s3_1f_9_models_81_evaluations.zip`.
Le job final a vérifié 9 FITS distincts,
27 checkpoints de poids, **81 scores
dépendants**. Contrainte de parité
`joint_hard` vs S3.1E legacy sur
mêmes seeds/cas prouvée en tests ;
sur BTC réel, les scores historiques
à 2000 sont identiques aux bilans S3.1E.

**Résultat à 2000 updates (3 seeds,
moyennes monitor 2020–21)** :
- D1 HARD BA52,24%, MAE prix282,704bps,
  AMP248,938 ; DIRECT BA51,24%/282,897/
  248,938 ; SOFT BA52,24%/280,707/273,477.
- H1 HARD BA51,93%/54,611/48,955 ;
  DIRECT 51,26%/54,642/48,955 ;
  SOFT 51,93%/54,511/53,856.
- M1 HARD BA53,02%/8,368/7,319 ;
  DIRECT 52,40%/8,377/7,319 ;
  SOFT 53,02%/8,337/8,215.

**SOFT meilleure erreur prix** vs HARD
de −1,997bps D1, −0,100bps H1,
−0,031bps M1 mais **amplitude
pire** +9,86%, +10,01%, +12,24%.
BA SOFT = HARD **PAR CONSTRUCTION**,
même signe logit, pas nouveau signal.
Persistance MAE D1 281,037bps,
H1 54,535, M1 8,347 ; SOFT bat
très légèrement la persistance par
0,118%/0,044%/0,115% de MAE,
mais les 3 seeds PARTAGENT le même
monitor, déjà surexploré en S3.1C/D/E.
AUCUN EDGE confirmé.

**Prochaine priorité S3.1G** : audit
de prédiction sélective à magnitude
prédite, conformément au besoin
utilisateur « sens et montant pour
décider s'il faut agir, frais ignorés ».
Établir **seuils de magnitude
ENTIÈREMENT sur TRAIN**, évaluer
couverture/BA sens et erreur montant
conditionnellement à prédiction
mouvement significatif, comparer
persistance sur LE MÊME sous-échantillon.
Définir préalablement les contrôles
pour éviter que la sélection du seuil
sur monitor 2020–21 (déjà étudié)
fabrique un edge. 2022–25 non
recyclé en validation indépendante,
2026 toujours réservé. Pas
d'ordre, PnL cumulé ou portefeuille.

---

# Codex — S3.1F, isoler trois règles de prévision sur les MÊMES poids
26 octobre 2026. Branche `chatgpt/trame-s3-postprocess-ablation-20261026`,
[PR #29 DRAFT](https://github.com/goldaj/trame-chartist-research/pull/29),
basée sur PR #28 S3.1E, pas de merge auto.

## Historique des preuves déjà acquises
S3.1D 45 vraies trajectoires BTC /135 checkpoints,
[Actions #40313075915](https://github.com/goldaj/trame-chartist-research/actions/runs/40313075915)
4/4 jobs verts ; rapport
`research/token_grammar/S3_1D_REAL_135_RESULTS_20261026.md`.
Augmenter la pénalité de magnitude diminue erreur magnitude mais
augmente erreur du prix HARD vraiment prédit.
S3.1E 27 vraies trajectoires /81 mesures,
[Actions #40318969005](https://github.com/goldaj/trame-chartist-research/actions/runs/40318969005)
4/4 jobs verts ; rapport
`research/token_grammar/S3_1E_REAL_81_RESULTS_20261026.md`.
Une loss différentiable SOFT de réconciliation
n'a pas amélioré simultanément BA et MAE prix HARD.
Désaccord signe `mu` vs `logit`
legacy D1 7,9%, H1 19,0%, M1 26,7%,
mais aucun edge profitable identifié.

## Protocole SCIENTIFIQUE S3.1F préenregistré
`research/token_grammar/S3_1F_INFERENCE_PROTOCOL_20261026.md`
établi AVANT tout résultat BTC réel de cette expérience.

Pas de nouvelle taille ni de nouvel objectif :
réentraîner **une seule fois par horizon/graine**
le modèle `legacy` EXACT S3.1E :
`ContinuousDirectionModel` 2418 params,
width16/depth1/JOINT, G2 quantiles TRAIN
décodée en bps, contexte 20, loss
Huber(`mu`)+0,5 BCE(`logit`),
AdamW0,003, weight decay0,001,
clip5, mêmes données et mini-batches.
Pour le MÊME modèle et MÊME checkpoint :
1. `joint_hard` = signe `logit` × abs(`mu`)
   (règle originelle effectivement servie).
2. `signed_direct_mu` = `mu` (règle alternative).
3. `joint_soft_tanh` = tanh(`logit/2`) × abs(`mu`)
   (autre règle alternative, pas le legacy live).
Les trois prix sont reconstruits en USD
de la même ancre BTC et évalués sur les
mêmes vraies cibles, **aucun modèle
supplémentaire par règle de prix**.

**Matrice : 9 vrais entraînements** = D1/H1/M1
×3 seeds (20261025,26,27) ;
checkpoints continus 200/800/2000 =
27 états de poids ; 3 règles par
état = **81 évaluations DÉPENDANTES**.
Ne pas prétendre 81 nouveaux modèles.
TRAIN cible connue avant 2020,
MONITOR 2020–21 ; dev externe
2022–25 et holdout 2026 jamais
ouverts pour sélection.
Source public BTC/USD Bitstamp SHA vérifiée,
aucun secret/ordre Hyperliquid, pas
de portefeuille simulé ; frais ignorés.

## Code, garde-fous et état
- `research/token_grammar/inference_ablation.py` :
  `inference_rule_prices` et `run_cases`,
  sortie joint HARD évaluée bit-à-bit
  contre la fonction `forecast_prices`
  historique. La loss est la même
  que S3.1E legacy, pas une autre.
- `research/token_grammar/test_inference_ablation.py` :
  parité des vrais scores du legacy S3.1E
  sous même seed/step sur données artificielles ;
  cohérence BA/MAE, refus dev externe
  2022+ et invalidité des entrées.
- `research/token_grammar/inference_panel.py`
  et `test_inference_panel.py` :
  lignes à poids partagés, regroupement
  **9 fits/27 états/81 scores**,
  comparaisons appariées, contrôles
  de chrono et paramètres.
- CI fixtures [#40326446195](https://github.com/goldaj/trame-chartist-research/actions/runs/40326446195)
  initiée, à vérifier.
- Pilote BTC réel (D1/H1/M1, un modèle
  par horizon, 10/20/40 updates)
  [#40326446278](https://github.com/goldaj/trame-chartist-research/actions/runs/40326446278)
  initié, vérifier 3/3 jobs avant
  campagne finale.
- `.github/workflows/trame-s3-1f-inference-fixtures.yml`
  et `trame-s3-1f-real-canary.yml`.
- Campagne full **pas encore confirmée** :
  créer sur cette branche le workflow
  3 horizons ×3 seeds /2000 steps,
  avec agrégation 9/27/81 et preuve
  numérique legacy S3.1E.
  N'annoncer résultat qu'après 4/4
  jobs et vérification artifacts SHA.

## Après vraie campagne (recherche puis ingénierie)
1. Vérifier le pilote, coder et exécuter
   campagne full si nécessaire ;
   certifier parité S3.1E legacy.
2. Calculer par horizon et chaque seed
   BA sens, MAE prix USD/bps, erreur
   magnitude bps, %UP, monoclasse,
   persistance; ne pas agréger D1/M1
   sans le dire.
3. Vérifier taux de désaccord des têtes
   et s'il explique précisément les
   erreurs supplémentaires de la règle
   HARD ; éviter causalité abusive.
4. Puis consigner scientifiques
   `S3_1F_REAL_81_RESULTS_20261026.md`,
   SHA sources et Brier de tête qui
   **n'est pas une calibration de
   la règle direct_mu**.
5. Codex AGENTS.md/historique, issue
   scientifique #20 et PR #29.
6. NO-GO live trading, aucun PnL
   financier inventé ; envisager
   protocole confirmatoire seulement
   après gel complet de la famille.
