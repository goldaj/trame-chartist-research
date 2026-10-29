# TRAME S3.1G — Préenregistrement : fiabilité selon magnitude prédite
**26/10/2026. Écrit AVANT toute évaluation BTC réelle S3.1G.**

## Motivation
S3.1F a terminé [9 modèles BTC réels /81 évaluations](https://github.com/goldaj/trame-chartist-research/actions/runs/40326818917).
Résultats: `research/token_grammar/S3_1F_REAL_81_RESULTS_20261026.md`.
Le SOFT améliore légèrement le MAE prix (proche de persistance)
mais détériore l'erreur de magnitude de 10 à 12%.
La BA SOFT est égale à HARD **par construction**.
L'utilisateur privilégie une bonne prédiction du SENS
et du MONTANT, pour décider **QUAND une opportunité
mérite l'attention d'un trader** (frais exclus).
La vraie question n'est plus le score moyen toutes bougies :
est-ce que les prédictions de mouvements forts
sont *plus exactes* et quantifiables ?

## Méthode sélection, seuils sans fraude
Un modèle historique **S3.1F legacy** par
horizon/graines, exactement mêmes poids,
architectures, loss, seeds 20261025/26/27,
2000 mises à jour, G2 quantiles TRAIN-only,
contexte20, width16/depth1, 2418 paramètres,
optimizer AdamW. **Ne changer aucun paramètre
ou règle de prix en S3.1G.**

Sur les cas TRAIN (labels connus avant 2020)
calculer, sans gradient après fitting du modèle,
la distribution des **amplitudes ABSOLUES des
prévisions HARD en bps** ; dériver quatre
seuils fixes par modèle :
- `all` : seuil 0 bps ;
- `q50` : médiane (50e centile) train ;
- `q75` : 75e centile train ;
- `q90` : 90e centile train.

Sélectionner les seuls cas MONITOR 2020–21
où **la prédiction HARD** en amplitude bps
>= seuil TRAIN. La **même sélection
de cas** sert à comparer `joint_hard`,
`signed_direct_mu`, `joint_soft_tanh`
sur exactement les MÊMES poids.
Pas de sélection sur magnitude réalisée
hindsight, pas de seuil recalibré
sur la distribution monitor, aucun
choix d'un quantile « gagnant » post-hoc.
Le seuil q0 ne doit pas exclure les
prédictions plates. Garder les
couvertures observées (qui ne sont
pas forcément 50/25/10% hors TRAIN).

**Limite statistique** : le modèle a
été entraîné sur les exemples TRAIN,
donc les seuils de |prédiction|
TRAIN sont **in sample**, bien que
sans accès aux cibles MONITOR.
Ce n'est pas une calibration out-of-fold
ni une validation indépendante.

## Mesures sur chaque même sous-ensemble
Pour chaque horizon/graines/quantile,
trois règles S3.1F au MÊME checkpoint
2000 updates :
- `coverage` % du MONITOR,
  nombre de cas conservés,
  `n_true_up/n_true_down/n_true_flat`,
  `n_pred_up/down`, biais monoclasse.
- Sens : **accuracy brute** et
  **balanced accuracy** ; si l'une
  des deux classes réelles manque,
  BA = null et le sous-groupe
  est **non interprétable**, ne jamais
  lui affecter artificiellement 50%.
- Prix final : MAE **USD et bps**
  sur les cas sélectionnés.
- Magnitude : MAE `abs(prédiction)`
  vs `abs(réalisé)` en bps et
  ratio moyenne magnitudes prédites
  / observées ; signaler éventuel
  shrikage sans gain direction.
- Score de `p_up` si joint hard/soft :
  Brier et skill vs prior TRAIN,
  **ne pas attribuer ce Brier à la
  direction de direct_mu**.
- Toujours comparer sur les mêmes cas
  `persistence_flat`, avec MAE USD/bps
  ET couverture identique ; autres
  baselines optionnelles si distinctes
  mais pas mélanger les exemples.
- Dispersion entre les trois seeds
  de modèles ; les mêmes bougies
  sont partagées, donc ces graines
  NE SONT PAS des séries indépendantes.
  Pas de p-value naïve.

Les 4 seuils sont des tests
EXPLORATOIRES pré-définis :
si une sous-population contient <30
cas ou manque une classe, afficher
`insufficient_coverage` avec le
nombre réel et **aucune revendication
directionnelle**. Comparer BA,
MAE prix et erreur amplitude
ENSEMBLE. Pas de nombre $ de
croissance sans trajectoire d'ordres.

## Causalité / données
BTC spot Bitstamp D1/H1/M1 public,
SHA vérifiés. Le loader S3.1F
`collect_internal` lit uniquement
labels connus avant 2022 via
`stop_labels_before`.
TRAIN avant 2020, MONITOR interne
2020–2021, jamais grad ni quantile
sur monitor. L'ancien développement
2022–2025 a été surexploré et
**n'est pas consulté**.
Holdout 2026 gelé.
Aucun compte, ordre ou stratégie
Hyperliquid, frais non simulés
selon demande utilisateur.

## Matrice exacte et critères d'intégrité
**9 véritables entraînements** =
D1/H1/M1 × 3 seeds, 2000 updates,
comme S3.1F. Contrairement au
S3.1F, un seul checkpoint final.
**9 ×4 seuils ×3 règles =
108 cellules de résultats** ;
ces cellules ne sont pas 108
nouveaux modèles ou observations
indépendantes. D1/H1/M1 séparés.
Comparer les scores `all` au
S3.1F 2000 updates par seed pour
vérifier qu'aucune différence de
code/labels/model drift n'est
passée inaperçue. Toute différence
>1e-8 signalée/échoue en CI.

## Sous-étapes
1. S3.1G.1 préenregistrement (ici).
2. S3.1G.2 runner seuil TRAIN, 3
   règles mêmes poids, observation
   true sign/amplitude et prix,
   parité cas all S3.1F.
3. S3.1G.3 tests artificiels adversariaux
   anti-fuite et seuils train-only ;
   CI sur fixtures.
4. S3.1G.4 canary réel BTC D1/H1/M1
   une seed et 40 updates, puis
   campagne 9 vrais fits ×2000.
5. S3.1G.5 panel 108 cellules,
   couverture, direction, montant,
   baseline persistance, limites
   statistiques.
6. S3.1G.6 compte rendu chercheur et
   ingénieur, Codex/AGENTS,
   CHATGPT_PROJECT_HISTORY, issue #20
   et PR DRAFT.
Puis **stop aux réglages successifs sur
2020–21** et pré-enregistrer un vrai
plan de validation indépendante
à ouvrir une fois le modèle et
l'usage figés ; ne pas ouvrir
2026 prématurément.
