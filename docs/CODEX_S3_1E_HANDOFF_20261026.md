# Codex TRAME — S3.1E cohérence entre têtes et prix final, 26/10/2026

**PR #28 DRAFT**, branche
`chatgpt/trame-s3-reconciliation-loss-20261026`,
basée sur PR #27 S3.1D terminée (puis
#26 S3.1C, #25 S3.1B, #24 S3.1A...).
Ne pas fusionner automatiquement.

## Point de reprise, résultats précédents attestés
- S3.1D **45 trajectoires BTC réelles /135 checkpoints
  complètement terminées**, [run #40313075915](https://github.com/goldaj/trame-chartist-research/actions/runs/40313075915)
  4/4 jobs verts. SOURCE
  `research/token_grammar/S3_1D_REAL_135_RESULTS_20261026.md`
  et SHA256 des cinq artefacts.
- Loss magnitude ×1 baisse erreur amplitude
  16–21% par rapport à référence mais
  **aggrave MAE prix final** 6–10% et
  diminue BA 0,6 à 1,7 points (D1/H1/M1,
  2000 optimizer updates). Aucun edge
  confirmé. La persistance bat ou égale
  quasiment nos MAE prix en D1/H1/M1.
- L’utilisateur a demandé « t'as crash,
  continue ». L'historique exact et
  l'état final dans
  `docs/CHATGPT_PROJECT_HISTORY.md`.

## S3.1E : protocole préenregistré avant runs réels
`research/token_grammar/S3_1E_RECONCILIATION_PROTOCOL_20261026.md`.

Question : `ContinuousDirectionModel`
produit deux têtes distinctes :
`mu` retour signé et `logit` probabilité
de hausse. Le prix JOINT servi à
l'inférence est calculé :
`price=anchor*exp(hard_sign(logit)*abs(mu)*scale/10000)`,
tandis que Huber historique punit `mu`
mais pas la combinaison en sortie.
Cela peut provoquer une incohérence.

Trois bras **même backbone, param_count 2418,
init SHA, cohortes, batch order, optimizer,
20 rendements G2 signé décodés bps** :
- `legacy` = SmoothL1(mu,y) +0.5BCE(logit,y_up)
- `reconciled_025` = legacy +
  0.25 SmoothL1(tanh(logit/2)*sqrt(mu²+1e-12),y)
- `reconciled_100` = legacy +
  1.0 fois la même loss différentiable.

**CRUCIAL** : la version soft est un
SURROGATE pour les gradients, **jamais
équivalente** à la règle hard-sign de
l'inférence. On score obligatoirement
les prix HARD via `forecast_prices`
existante, et en plus le SOFT pour
diagnostiquer leur gap et fréquence
`sign(mu)!=sign(logit)`.
Critères majeurs **BA direction ET
MAE prix USD/bps ET erreur amplitude
bps**, UP %, monoclasse, Brier skill vs
prior TRAIN, temps/pertes/gradients.

## Chronologie et budget
BTC Bitstamp SPOT public SHA vérifié :
- TRAIN cibles connues avant 2020 ;
- MONITOR 2020–21 uniquement ;
- **ne PAS charger ou sélectionner
  sur l'ancien dev externe 2022–25,
  ni le holdout 2026**.
- G2 quantile/normaliseur/prior appris
  uniquement depuis TRAIN.

27 trajectoires distinctes =
3 horizons D1/H1/M1 ×3 losses×3 seeds,
chaque entraînement continu jusqu'à
2000 updates, observé aux checkpoints
200/800/2000 = 81 scores CORRÉLÉS.
Trois graines ne sont pas trois
histoires financières indépendantes.
Comparaison interprétable seulement
à splits, architecture et capacité identiques.

## Code, tests et exécutions
- `research/token_grammar/reconciliation_loss.py`
  et `reconciliation_panel.py`.
  `test_reconciliation_loss.py`,
  `test_reconciliation_panel.py`.
- CI synthétique
  [#40318703540](https://github.com/goldaj/trame-chartist-research/actions/runs/40318703540)
  réussie, parité exacte loss legacy,
  flux gradients, S3.1D inchangée,
  refus cibles 2022–25/2026.
- Ingénierie smoke sur 9 trajectoires
  vraies (10/20/40 updates, 1 seed)
  [#40318703968](https://github.com/goldaj/trame-chartist-research/actions/runs/40318703968)
  **3/3 jobs verts** ; PAS des résultats
  statistiques.
- Campagne scientifique réelle
  [#40318969005](https://github.com/goldaj/trame-chartist-research/actions/runs/40318969005)
  **EN COURS** lors de la rédaction.
  **NE PAS** l'annoncer réussie avant
  vérification **4/4 jobs** dont panel
  final, et SHA des cinq artefacts.
- `.github/workflows/trame-s3-1e-27-full.yml`
  vérifie 27 fits, 81 observations,
  hard-price réellement servi,
  dev externe et test gelés.

## Suite immédiate (automatique selon utilisateur)
1. Vérifier run #40318969005, échec
   éventuel et ses logs, corriger
   honnêtement sans mélanger run raté
   avec mesures scientifiques.
2. Récupérer D1/H1/M1 JSON et panel
   JSON/MD, SHA256 et construire
   une archive de reproductibilité.
3. Faire bilan chercheur + ingénieur :
   BA / MAE prix $ / bps / amplitude,
   désaccord entre têtes, Brier, UP,
   coût CPU, comparaison persistance,
   dispersion par graine/horizon.
   Pas de « gagnant » sans supériorité
   **conjointe** et stable.
4. Publier `S3_1E_REAL_81_RESULTS_20261026.md`,
   mettre à jour AGENTS, ce handoff,
   historique, PR #28 et issue #20.
5. Après seulement, décider question
   suivante. Ne pas gonfler aveuglément
   les paramètres ou tester 2026.

**Aucun ordre, clé API, compte ou portefeuille
Hyperliquid**. Frais ignorés comme demandé,
aucun rendement cumulatif inventé. Les chiffres
ne constituent pas une validation indépendante
ou un conseil de trading.
