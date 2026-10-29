# TRAME S3.1C — PRÉENREGISTREMENT DIAGNOSTIC DE CONVERGENCE
Date 26/10/2026, **écrit avant tout résultat réel S3.1C**.

## Point de départ
S3.1B [432 fits BTC réels](https://github.com/goldaj/trame-chartist-research/actions/runs/40306642813)
a confirmé que les embeddings scalaires trainables ne
surpassent pas les centres numériques en direction et
précision de montant. Les embeddings random produisent
beaucoup de prédictions monoclasse. Voir
`research/token_grammar/S3_1B_REAL_432_RESULTS_20261026.md`.

L'ancienne dev 2022–2025 a été **réutilisée de nombreuses
fois** lors des études S1 à S3.1B ; elle n'est pas un
jeu confirmatoire indépendant. Pour la première
fois, S3.1C n'utilisera **QUE des cibles historiques
avant 2022** et ne montrera aucun score 2022–2025
au moteur d'optimisation. 2026 reste strictement gelé.

## Hypothèses H0/H1
H1a : les modèles monoclasse sont en partie
**sous-entraînés** : 200 updates sont trop courts ;
200→800→2000 devrait réduire le collapse sans
détériorer la précision de montant sur validation
temporelle 2020–2021.
H1b : une représentation initialisée selon les
centres historiques est plus stable qu'une
initialisation de tokens aléatoire sur un long
entraînement, à capacité exactement égale.
H0 : ni prolonger l'entraînement ni l'initialisation
ordonnée ne fait mieux qu'un prior directionnel
train-only lorsque l'on tient compte de l'amplitude.

## Nouvelles cohortes, sans répétition du dev externe
Pour D1/H1/M1, charger les mêmes archives Bitstamp
publiques SHA vérifiées, mais demander au flux
uniquement ses **exemples TRAIN <=2021**, puis
échantillonner au maximum **4096** cas par
réservoir déterministe (graine 20261025,
strides D1/H1=1, M1=60).
Partition interne stricte à l'instant où le
label est connu, via `label_available_time` :
- **TRAIN_INTERNE** : disponibilité de cible
  **strictement avant 2020-01-01 00:00 UTC**.
  Seuls ces exemples contribuent aux gradients,
  quantiles du tokenizer G2, standardisation,
  prior P(up), baselines et choix d'optimiseur.
- **MONITOR_INTERNE** : cible disponible
  **2020-01-01 inclus à 2022-01-01 exclus**,
  **jamais** utilisée pour training,
  quantiles/échelle ni gradients.
- **DEV EXTERNE 2022–2025** : pas interrogé
  ni évalué dans S3.1C ; ne jamais appeler
  le calcul S3.1B standard basé sur dev.
- **HOLDOUT 2026** : jamais ouvert.

**Attention aux fenêtres temporelles** :
chaque cas reçoit 20 retours passés terminés
et même si les premières 20 bougies de 2020
peuvent provenir de décembre 2019, aucune
cible du monitor ne peut alimenter TRAIN.
Les 2020–21 ne deviennent jamais gradients,
ni paramètres de quantiles ni normaliseur.
Pas de chevauchement des cibles train/monitor.

## Modèles choisis AVANT résultats
Un seul backbone **width16, depth1, loss JOINT
Huber + 0,5 BCE** et contexte 20, pour éviter
d'explorer rétroactivement 40 architectures.
Une seule grammaire **G2 signée quantiles
train-only** (meilleure réduction monoclasse
du S3.1B sur H1).
Trois bras `decoded`, `embedding_ordered`,
`embedding_random` à mêmes cibles et
batch indices, init backbone identique :
learned **+11 paramètres** vs decoded,
ordered-v-random même nombre exact.
Graines 20261025, 20261026, 20261027.
**27 trajectoires** = 3 horizons×3 bras×3 seeds.
Chaque trajectoire est entraînée **une fois**
jusqu'à 2000 mises à jour, avec checkpoints
préfixés **200 / 800 / 2000** :
**81 évaluations internes** sans réinitialiser
l'optimiseur ni repartir de zéro.
Il ne faut pas qualifier les 81 checkpoints
de 81 entraînements indépendants.

## Observables enregistrés à chaque checkpoint
- `train_monitor_loss` et `validation_monitor_loss`
  calculées sans gradients sur sous-échantillons
  fixes (échantillon de 256/512 cas TRAIN et
  ensemble complet monitor), même loss joint ;
  aucune adaptation au monitor.
- Tendance du gradient global **avant clipping**,
  fréquence gradient non fini, perte dernier
  mini-lot, temps CPU depuis l'origine.
- Score MONITOR 2020–2021 :
  **balanced accuracy** direction et accuracy
  brute, %UP/DOWN, taux de sorties monoclasse
  ≥99%, MAE prix **USD et bps** et erreur
  absolue d'amplitude en bps.
- Brier/CE/Skill vs prior P(up) calculé
  **exclusivement sur TRAIN_INTERNE**.
  Ne pas recalibrer le seuil décisionnel
  d'après le monitor. Conserver 0,5 fixe.
- Nombre de paramètres, SHA backbone initial,
  tailles des deux cohortes, empreinte des
  dates d'origine de chacune, quantiles et
  train-scale d'entrée sans label futur.
- Baselines toujours-UP/DOWN/persistance et
  prior TRAIN_INTERNE. Aucun PnL/portfolio.
- Protocole de décision préengagé :
  ne parler d'amélioration réelle que si
  plusieurs seeds et horizons montrent
  BA ET précision MAE prix + amplitude
  améliorées tout en réduisant les
  sorties monoclasse. Si BA reste proche
  de 50%, **NO-GO** pour scaling aveugle.

## Sous-étapes
- **S3.1C.1** ce protocole et contrôles
  anti-fuite préenregistrés.
- **S3.1C.2** implémenter chargement **train-only**
  et split de disponibilité TRAIN<2020/
  MONITOR2020–21 sans ouvrir 2022+.
- **S3.1C.3** instrumenter gradients/loss,
  checkpoints 200/800/2000 sur même
  optimiseur, modèle et mini-batches ; tests
  artificiels adversariaux.
- **S3.1C.4** valider en CI publique sur fixtures
  *sans données réelles ni 2022–2025*.
- **S3.1C.5** 27 vraies trajectoires BTC
  D1/H1/M1 ; rapport de convergence, tableau
  sens/montant/Brier avec SHA des artefacts.
- **S3.1C.6** conclusion chercheurs × ingénieurs,
  Codex/AGENTS/historique et issue #20.
- **S3.2** nouveaux embeddings vectoriels,
  patches et architecture non monoclasse
  seulement si ce diagnostic le justifie.

## Intégrité
Aucune clé, compte, portefeuille ou opération
Hyperliquid ; données BTC SPOT publiques
autorisées, attribution et SHA conservés.
Frais ignorés selon propriétaire. Les
cibles 2020–21 sont internes au TRAIN
historique global, aucune revendication
de validation générale. Le réservoir
initial doit être **indépendant des labels
des années 2022–2025** : utiliser
`iter_cases(...,train_only=True)` plutôt
que `collect` qui produit aussi des dev
externes. Test 2026 toujours réservé.
