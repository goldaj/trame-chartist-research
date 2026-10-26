# TRAME S3.1E — protocole préenregistré : aligner la perte sur les deux sorties
**Date 26 octobre 2026. Enregistré avant TOUT résultat BTC S3.1E.**

## Problème vérifié dans S3.1D
[45 modèles /135 checkpoints BTC réels](https://github.com/goldaj/trame-chartist-research/actions/runs/40313075915)
montrent qu'augmenter la perte d'amplitude diminue
l'erreur sur la magnitude, mais **détériore le prix
final et la direction** (rapport
`research/token_grammar/S3_1D_REAL_135_RESULTS_20261026.md`).
La prévision de prix réellement exposée par
`ContinuousDirectionModel.forecast_prices` en JOINT
est : `price_hat = anchor*exp( hard_sign(logit)*abs(mu)*train_scale_bps/10000 )`.
Or la loss historique applique la Huber à `mu`,
pas directement au **retour signé réconcilié**.
Le logit peut demander DOWN alors que `mu` a un
signe UP. Les têtes pourraient optimiser des buts
incompatibles. C'est une hypothèse, pas une preuve.

## Trois bras comparables préenregistrés
**Même architecture, même 2418 paramètres** :
`ContinuousDirectionModel(width=16,depth=1,
context=20,mode=joint)` sur les mêmes 20
rendements passés encodés G2 SIGNED et décodés
en scalaire bps, quantiles G2 fit TRAIN seulement.
Identiques seeds, mini-batches, AdamW lr0.003,
weight decay0.001, clip norm5, initialisation SHA.
Les seuls paramètres variables sont les
coefficients de loss. Pas d'embeddings trainables
ni de changement des règles de pricing live.

En retour normalisé, définissons :
- `P = SmoothL1(mu,y,beta=1)` ;
- `B = BCEWithLogits(logit,1[y>0])` pour y non nul ;
- `r_soft = tanh(logit/2) * sqrt(mu²+epsilon²)`
  avec `epsilon=1e-6`, approximation
  **différentiable** du retour réconcilié signé ;
- `R = SmoothL1(r_soft,y,beta=1)`.

Les bras :
1. `legacy` : **P + 0.50B** (identique S3.1D référence).
2. `reconciled_025` : P + 0.50B + **0.25R**.
3. `reconciled_100` : P + 0.50B + **1.00R**.

**Limite explicite** : `tanh(logit/2)` vaut une
certitude douce de direction comprise entre
-1 et +1 et **N'EST PAS** le `hard_sign`
non différentiable utilisé à l'inférence.
L'expérience teste si entraîner un surrogate
cohérent aide la **sortie dure effectivement
évaluée**. Ne jamais déclarer la sortie soft
égale au prix réellement produit. Les deux
sorties (hard et soft) seront scorées
séparément sans choisir de seuil sur monitor.

## Diagnostics définis AVANT résultats
En plus des résultats **HARD SIGN** :
- BA direction, accuracy brute, UP %, modèles
  monoclasse ≥99%, MAE prix **USD et bps**,
  MAE amplitude bps, Brier skill vs prior TRAIN.
- `sign_disagreement_fraction` entre `mu>0`
  et `logit>=0` ; zéros consignés.
- MAE soft price USD/bps et `hard_soft_gap_bps`,
  comparaison descriptive sans exploitation
  pour le pricing ni sélection du seuil.
- train et monitor perte **legacy commune**
  pour toutes les variantes ; monitor loss arm
  séparée, gradients avant clipping, temps,
  seed, SHA de poids initiaux/ordre de batches.
- baselines persistance et toujours UP/DOWN
  sur les mêmes cas monitor.
- Les 3 sorties deviennent pré-calibrées
  seulement si le Brier skill positif et
  reproductible ; sinon pas d'edge.

**Hypothèses :** L'alignement `R` pourrait
améliorer simultanément direction et prix final ;
il pourrait aussi réduire systématiquement
les amplitudes via `tanh` et détériorer la
reconstruction hard ou favoriser le monoclasse.
H0 : pas de différence conjointe crédible
sur les trois horizons/seeds/temps.

## Cohortes et calendrier strictement S3.1C/D
Spot BTC/USD Bitstamp public avec identité
Git SHA, D1/H1/M1. **Train** : labels
disponibles avant 2020-01-01 UTC ;
**monitor interne** : labels 2020–2021.
Ne jamais ouvrir l'ancien DEV 2022–2025
déjà surexploité, ni le holdout 2026.
Le lecteur avec `stop_labels_before=2022-01-01`
arrête les bougies elles-mêmes. Tout fit
des quantiles/prior/normalisation TRAIN only.
Même réservoirs et RNG que S3.1D.

Matrice complète :
3 horizons × 3 bras × 3 graines =
**27 trajectoires** (each 2000 updates,
même optimiseur aux checkpoints
**200, 800, 2000**) = **81 mesures**
NON indépendantes. Runner CI pilote
3 horizons ×3 bras ×1 graine ×
10/20/40 updates = **9 trajectoires**
ingénierie, pas résultat scientifique.
Ne pas faire d'analyse de profit cumulée,
pas de frais selon instruction utilisateur,
aucune transaction ni appel Hyperliquid.

## Sous-étapes chercheurs × ingénieurs
- S3.1E.1 : protocole fixé (présent document).
- S3.1E.2 : implémentation `soft_reconcile`,
  loss 3 bras, tests dérivées non nulles
  et parité exact legacy/S3.1D.
- S3.1E.3 : runner, mesures hard/soft et
  panel apparié strict, contrôles 2022–26.
- S3.1E.4 : CI synthétique puis pilote
  9 trajectoires BTC réelles sans
  sélection scientifique.
- S3.1E.5 : campagne 27 trajectoires,
  81 checkpoints, archive SHA et
  analyse direction/MAE prix/amplitude.
- S3.1E.6 : Codex AGENTS/historique/issue,
  conclusions et hypothèse suivante.
Pas de fusion automatique dans main ;
PR DRAFT empilée sur S3.1D PR #27.

## Précautions épistémiques
MONITOR 2020–21 a déjà été utilisé en
S3.1C/D ; c'est encore une expérience
**exploratoire**, pas une validation
indépendante. Les cibles historiques
se chevauchent, 3 seeds ne sont pas
des échantillons financiers indépendants.
Ne pas ouvrir 2026 sans gel de
la famille de modèles complet et
une stratégie confirmatoire séparée.
