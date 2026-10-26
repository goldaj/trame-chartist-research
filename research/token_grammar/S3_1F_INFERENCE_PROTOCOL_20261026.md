# TRAME S3.1F — protocole préenregistré : isoler la règle d'inférence
Date 26/10/2026. **Écrit avant toute mesure BTC réelle S3.1F**.

## Motivation vérifiée
S3.1D 45 fits [#40313075915](https://github.com/goldaj/trame-chartist-research/actions/runs/40313075915)
et S3.1E 27 fits [#40318969005](https://github.com/goldaj/trame-chartist-research/actions/runs/40318969005)
terminés, bilans dans `S3_1D_REAL_135_RESULTS_20261026.md`
et `S3_1E_REAL_81_RESULTS_20261026.md`.
S3.1E n'améliore pas de façon conjointe
BA direction / MAE du prix réellement servi
/ erreur amplitude. La tête `mu` et la
tête `logit` prédisent parfois des
signes contradictoires : sur S3.1E legacy,
7,9% D1, 19,0% H1, 26,7% M1.

**Question :** nos prédictions faibles proviennent-elles
en partie de la **règle finale de post-traitement**
plutôt que des poids entraînés ?

## Règles préenregistrées : même réseau, mêmes poids
Pour chaque modèle historique legacy de S3.1E,
`mu` retour normalisé et `logit`
log-odds de hausse :
1. `joint_hard` (actuelle sortie produit) :
   `r=+abs(mu)` si logit>=0, sinon
   `r=-abs(mu)`.
2. `signed_direct_mu` : `r=mu`
   **sans consulter le logit** ;
   direction = signe de la régression.
3. `joint_soft_tanh` : `r=tanh(logit/2)*abs(mu)`,
   évaluation d'un soft utilisé
   à **inférence**, PAS le hard.
   À distinguer de l'epsilon=1e-6
   du surrogate de training S3.1E.

Dans chaque cas,
`price=anchor*exp(r*train_scale_bps/10000)`
sur les mêmes cas. **AUCUN modèle différent
par méthode de prix, AUCUN nouvel entraînement
par règle de prix.** Réutiliser les trois
sorties sur chaque checkpoint des mêmes
poids du modèle legacy ; le Brier de la
tête directionnelle est diagnostiqué
mais n'est pas la probabilité du
signe d'un bras `signed_direct_mu`.

Les checkpoints S3.1E n'ont pas stocké
les poids ; reproduire exactement
les modèles legacy à mêmes graines,
mêmes hyperparamètres et corpus
que S3.1E. Un contrôle compare
`joint_hard` pour chaque seed/horizon/step
aux scores numériques S3.1E
`legacy` archivés ; toute divergence
de reproductibilité doit être
documentée, pas masquer une différence.

## Calendrier et effectifs EXACTS
Seulement train labels connus avant
2020-01-01 UTC, monitor labels
2020–21, BTC spot public Bitstamp
SHA vérifié. Ancien DEV externe
2022–25 **ne doit pas être lu**,
2026 HOLDOUT **gelé**.
Quantiles G2 signés, normaliseur,
prior P(up), seuils d'amplitude
dérivés du seul TRAIN. Mêmes
réservoirs et graines que S3.1C/D/E.

**9 entraînements distincts** =
3 horizons D1/H1/M1 ×3 seeds
20261025, 20261026, 20261027.
Une seule loss fixée historique
`Huber(mu,y)+0.5 BCE(logit,y>0)`,
backbone width16/depth1/JOINT 2418
params, contexte 20, AdamW lr0.003,
weight decay .001, clipping5.
Chaque modèle est entraîné une fois
jusqu'à 2000 updates, avec checkpoint
200/800/2000 = **27 jeux de poids**.
Chaque checkpoint évalué avec
3 règles **⇒ 81 évaluations**, mais
uniquement **9 modèles entraînés**
et **27 checkpoints** ; aucune
pseudo-réplication indépendante.

**Contrôles et critères :**
BA direction et accuracy brute,
nombre de prédictions UP/DOWN/FLAT,
monoclasse ≥99%, MAE prix USD/bps,
erreur amplitude bps, biais signé,
Brier du head joint + prior train,
désaccord `sign(mu) != sign(logit)`,
gain/perte de chacune des règles
versus `joint_hard` à seed/horizon/
checkpoint identiques. Baselines
persistance et toujours UP/DOWN.
Comparer les 3 règles sur le même
prix anchor, actual, fenêtres,
aucun algorithme optimisé sur monitor.
Les résultats SOFT ne doivent
jamais être qualifiés de prix servi
dans l'ancien produit.
Le nouveau bras direct est une
simulation exploratoire d'un
changement de produit, PAS une
stratégie valide en production.

## Hypothèses et critères NO-GO
H1 : la règle HARD peut introduire
des erreurs de direction/montant
non nécessaires quand les têtes
sont contradictoires ; `direct_mu`
pourrait réduire MAE prix mais
avoir une BA inférieure. `soft_tanh`
pourrait réduire MAE en se
rapprochant de la persistance
et ne pas apporter de sens utile.
H0 : aucune règle ne surpasse
durablement la baseline persistance
en MAE prix **ET** la règle hard
en BA et amplitude sur D1/H1/M1.

**Pas d'ouverture 2026**, pas de
sélection confirmatoire sur
MONITOR 2020–21 (déjà étudié).
Ne pas confondre meilleur MAE
avec gain de trading ; frais
ignorés comme demandé mais
aucune simulation PnL.
Aucun ordre, wallet, clé API
ou interaction Hyperliquid.

## Sous-étapes
- S3.1F.1 protocole (ce document).
- S3.1F.2 module d'inférence
  multiple à poids identiques,
  tests exacts sur règles hard
  et protection temporelle.
- S3.1F.3 runner identique S3.1E
  legacy + 3 règles au même checkpoint,
  panel strict contre pseudo-fits.
- S3.1F.4 CI fixtures et smoke
  BTC réel (3 horizons ×1 seed,
  10/20/40 uniquement).
- S3.1F.5 étude 9 modèles réels,
  81 scores appariés, comparaison
  avec témoins S3.1E et baseline.
- S3.1F.6 publication/critique
  et passation Codex, issue, histoire.
Pas de merge automatique, PR DRAFT
enfant de PR #28.
