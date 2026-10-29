# TRAME S3.1D — PRÉENREGISTREMENT : ablation de fonction de perte
26 octobre 2026. **Enregistré AVANT tout résultat S3.1D sur BTC réel**.

## Résultat scientifique qui motive l'expérience
S3.1C est **déjà terminée** [GitHub Actions #40309653884](https://github.com/goldaj/trame-chartist-research/actions/runs/40309653884),
27 trajectoires véritables et 81 checkpoints, avant
2022. Résultats :
`research/token_grammar/S3_1C_REAL_81_RESULTS_20261026.md`.
Allonger 200→2000 updates améliore H1 et M1 parfois,
dégrade D1, et ne garantit jamais une erreur d'amplitude
meilleure. La dynamique d'optimisation seule ne suffit
pas à expliquer le biais monoclasse.

**Question isolée S3.1D** : si nous gardons le modèle,
les données, l'entrée, la durée et les prédictions
**strictement identiques**, que change le **poids de la
fonction de perte directionnelle et d'amplitude** ?

## Bras et objectifs, FIXÉS avant les données
Tout bras utilise exactement le même réseau
`ContinuousDirectionModel(width=16,depth=1,
mode="joint",context=20)`, les 20 rendements
passés quantifiés G2 puis **décodés en scalaire bps**,
la même normalisation TRAIN pré-2020 et la même
règle de prévision finale S2b :
`direction = sign(sigmoid(logit)-0.5)` multipliée
par `abs(mu)`. Aucun entraînement d'embeddings :
nous isolons ici les pertes, pas la grammaire.

Pour chaque mini-lot de cibles normalisées `y` :
- `Lprice = SmoothL1(mu,y,beta=1)`.
- `Ldirection = BCEWithLogits(logit,1[y>0])`
  sur les seuls rendements futurs non nuls.
- `Lamplitude = SmoothL1(abs(mu),abs(y),beta=1)`.

Les **5 bras préenregistrés** ont tous la même
architecture, le même nombre de paramètres et la même
interprétation du cours futur :
1. `reference` = Lprice + **0,50**×Ldirection.
2. `direction_025` = Lprice + **0,25**×Ldirection.
3. `direction_100` = Lprice + **1,00**×Ldirection.
4. `magnitude_025` = Lprice +0,50×Ldirection
   + **0,25**×Lamplitude.
5. `magnitude_100` = Lprice +0,50×Ldirection
   + **1,00**×Lamplitude.

Toutes les cibles, seuil de direction (0,5),
scale et architecture sont COMMUNS. On garde
un BCE non nul dans tous les bras pour éviter
un bras avec tête de direction non entraînée :
les comparaisons sont donc réellement
**des variations de loss**, pas de
post-traitement de sortie.

## Données et contrôle anti-fuite
Cohortes publiques BTC SPOT Bitstamp D1/H1/M1,
le même `collect_internal` de S3.1C désormais
durci : aucune bougie externe lue après 2021.
TRAIN seulement sur cibles connues **strictement
avant 2020-01-01** ; MONITOR **2020–2021**.
Quantiles G2, normalisation, prior directionnel
et baselines depuis TRAIN exclusivement.
Aucune réutilisation de DEV 2022–2025 ;
2026 holdout gelé.

`width=16, depth=1`, trois seeds
(20261025, 20261026, 20261027),
mêmes mini-batches à chaque seed,
même SHA init, AdamW LR0.003 et weight decay0.001,
gradient clip=5. Ne jamais sélectionner un
seuil de probabilité par monitor.
Même modèle et même optimiseur continué :
200, 800, 2000 mises à jour.

## Matrice et statistiques
**45 entraînements** =
3 horizons ×5 losses ×3 seeds.
Chacun observé aux 3 checkpoints
200/800/2000 = **135 mesures** ; ces checkpoints
ne sont PAS 135 modèles indépendants.

Pour chaque checkpoint : BA direction, accuracy brute,
taux UP prédit, monoclasse ≥99 %, MAE prix **USD et bps**,
erreur d'amplitude **bps**, Brier skill vs prior TRAIN,
NLL/BCE et Huber sur monitor, décalage train/monitor
à loss de base commune (référence, non biaisée par
les poids spécifiques), gradients pré-clipping,
temps CPU/paramètres, cohorte et hashes.
Paires **par seed/horizon/step** : différence en BA,
MAE USD, MAE bps et amplitude vs reference.
Ne pas mélanger D1/H1/M1 comme un seul échantillon.

Hypothèses : renforcer BCE pourrait diminuer
sorties monoclasse mais augmenter erreur prix ;
renforcer Lamplitude pourrait améliorer le montant
mais non le signe. **H0** : aucun bras ne surpasse
la référence de façon conjointe, récurrente et
prévisible sur les trois horizons.

## Sous-étapes
- **S3.1D.1** présent protocole avant résultats.
- **S3.1D.2** loss personnalisée seule,
  constructeur de modèle inchangé,
  tests de parité exacte `reference` vs
  loss Joint de S3.1C et validation 2026.
- **S3.1D.3** runner et panneau apparié,
  tests synthétiques gradients/train-only.
- **S3.1D.4** pilote d'ingénierie D1/H1/M1
  puis matrice complète 45 trajectoires /
  135 observations sur BTC SPOT réel.
- **S3.1D.5** analyse contradictoire :
  pouvoir prédictif du sens ET précision
  montant, stabilité, biais monoclasse,
  aucune inférence de rendement trading.
- **S3.1D.6** passation Codex, AGENTS.md,
  historique conversation et issue #20,
  PR brouillon sans merge automatique.

Aucun frais simulé selon utilisateur,
aucun PnL portefeuille ni compte Hyperliquid.
Contrôle 2020–21 interne, **pas un test
indépendant** ni edge de trading.
