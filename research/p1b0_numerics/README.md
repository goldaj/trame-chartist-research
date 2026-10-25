# Laboratoire numérique P1-B0, expérience 2026-10-25

**Statut : prototype scientifique exécutable, non entraîné sur les marchés.**
Ce dossier est **nouveau et non gelé**, indépendant des protocoles et rapports
figés du 14 au 16 octobre 2026. La spécification source de vérité reste
[le candidat théorique P1-B0 0.2](../trame_research_plan/20261016/p1b0_candidate.json).

## Question de recherche

Le générateur de codes proposé par TRAME possède-t-il une distribution
**numériquement normalisée, finie et différentiable sur les corrections
centrales**, même aux extrêmes, de façon à pouvoir commencer la conception
d'un apprentissage sans perdre silencieusement les événements rares ?

Une question distincte reste **totalement ouverte** : un modèle entraîné
sur des séries de marché serait-il meilleur qu'une référence simple sur
un futur vraiment indépendant ?

### Hypothèses falsifiables (expériences techniques)

- HN1 : pour les configurations proposées, la masse totale vaut 1 à
  1e-12 près en double précision.
- HN2 : la vraisemblance logarithmique des codes rares dans les queues
  reste finie lorsque la soustraction naïve de CDF renvoie zéro.
- HN3 : les gradients analytiques des corrections centrales coïncident
  avec des différences finies pertinentes ; une vérification d'une NLL
  gigantesque par soustraction brute est **elle-même** numériquement mal
  conditionnée.
- HN4 : pour des mêmes logits numériques, FLAT et HIER sont identiques ;
  l'écriture hiérarchique reconstruit correctement les entiers négatifs.
- HN5 : un mélange **entièrement artificiel** de deux distributions normales
  arrondies est plus facile à représenter avec une correction apprise
  qu'avec la BASE imposée, à paramètres mu/sigma fixes.
- HN6 (limitation falsificatrice) : la capacité à calculer une log-probabilité
  de queue ne suffit **pas** à pouvoir tirer numériquement un événement
  de probabilité plus petite que le sous-flux de float64.

## Définition implémentée

- Support : tous les entiers k. Coeur I=[-2048, 2047].
- q(k) = Phi((k+.5-mu)/sigma) - Phi((k-.5-mu)/sigma).
- a_k = 4*tanh(g_k/4) dans I, zéro hors I.
- Z = q(hors I) + somme_{k dans I} q(k)*exp(a_k).
- p(k)=q(k)*exp(a_k)/Z dans I, q(k)/Z ailleurs.
- Conditions de l'expérience : |mu|<=256, sigma de 0.25 à S
  avec S dans {64, 256}, aucune réduction du dictionnaire.
- HIER : q=floor(k/8), reste modulo 8 pour construire
  le score brut depuis 512 composantes grossières et 3 paires binaires.
- Le gradient calculé est **uniquement** celui des 4096 corrections brutes :
  (p(j)-1_{j=cible})*(1-tanh²(g_j/4)), y compris lorsque la cible est
  hors I. Le gradient de mu, sigma et du réseau complet reste à développer.

Les masses des cellules sont calculées en espace logarithmique avec
SciPy **log_ndtr** et une différence logarithmique stable utilisant
**expm1**. Les deux catégories de queues contribuent au normalisateur.
Les tirages de queue, lorsqu'ils sont représentables, utilisent la
loi normale tronquée avant arrondi, **sans clip au dictionnaire**.

La tête est isolée du backbone : elle calcule les probabilités
d'un **seul état conditionnel fourni**, sans attention, sans données,
sans oracle de prix futurs et sans optimisation d'un GPT.

## Reproduction

Python 3.12, NumPy 2.3.5, SciPy 1.17.0, environnement isolé :

~~~bash
python -m pip install 'numpy==2.3.5' 'scipy==1.17.0'
python -m unittest discover -s research/p1b0_numerics -p 'test_*.py' -v
python research/p1b0_numerics/preflight.py > preflight.json
python research/p1b0_numerics/synthetic_fit.py > synthetic-fit.json
python research/p1b0_numerics/rollout_study.py > toy-rollout.json
~~~

La CI crée automatiquement ces rapports **synthétiques** en artefacts
du job GitHub Actions ; aucune clé API, donnée de marché, modèle
existant, compte ou appel réseau métier n'est utilisé.

### Expérience A : 15 cas de stress numérique

Cinq configurations (mu,sigma,S) :
(0,8,64), (256,64,64), (-256,64,64), (256,256,256),
(0,0.25,64), chacune déclinée en BASE, FLAT à corrections
artificiellement saturées, et HIER à composantes prédéfinies.
Validation de la masse totale à 1e-12, des log-probabilités
k=+-4000 et de la borne des corrections. Les fixtures indépendantes
incluent quadrature numérique de quatre intervalles, gradients par
différences finies et générateur aléatoire à graine fixe.

**Résultat d'exécution locale** (Python 3.12, NumPy 2.3.5,
SciPy 1.17.0, expérience construite le 25/10/2026) :

- 15/15 cas normalisés ; erreur absolue maximale sur masse totale :
  **3.33e-16**.
- A mu=256,sigma=64,S=64, la probabilité de sortie du dictionnaire
  en BASE vaut environ **1.01e-172**.
- A mu=256,sigma=256,S=256, elle vaut environ **1.30e-12**.
- A mu=0,sigma=8,S=64, les deux queues sont mathématiquement
  non nulles, mais la conversion en double donne **0** :
  le sampler **ne peut pas** produire ces événements en pratique.
- k=+-4000 possède une log-probabilité finie même quand la masse
  arrondie en float64 serait égale à zéro.
- Quatorze tests synthétiques passent localement. Les tests ne
  constituent **aucune** mesure de prédiction boursière.

**Résultat négatif important :** support infini *mathématique*
n'implique pas support infini *effectivement simulable* en float64.
Le chemin de tirage des événements sous-flués devra être qualifié
avant toute affirmation sur le risque de crise, même si leur
contribution aux moyennes courantes est négligeable.

### Expérience B : correction de loi sur mélange synthétique

Échantillon artificiel connu de 2000 codes d'apprentissage et
1000 codes synthétiques séparés, graine 20261025 :
moitié N(-8,2), moitié N(+8,2), puis arrondi entier.
Leurs états n'utilisent **aucun prix réel**.

BASE fixe (mu=0,sigma=8) ; HIER et FLAT partent des mêmes corrections
nulles. Seuls les paramètres de correction sont modifiés par
100 passes de descente du gradient sur vraisemblance moyenne,
pas d'ajustement de mu/sigma ni de backbone.

| Bras | NLL train | NLL test synthétique |
| --- | ---: | ---: |
| BASE fixe | 3.52297 | 3.53002 |
| HIER corrigé | 3.34998 | 3.34758 |
| FLAT corrigé | 2.86391 | 2.85375 |

Les deux mécanismes de correction réduisent donc la NLL de cette
distribution **fabriquée pour être multimodale**. FLAT possède plus de
paramètres que HIER ; l'expérience n'égalise ni paramètres ni FLOPs
ni recherche d'hyperparamètres. Aucun classement scientifique des
têtes de TRAME ni généralisation au marché n'en découle.
La réutilisation de cette fixture comme « test indépendant » serait
incorrecte après ces observations.

### Expérience C : simulation causale à 20 pas et CRPS en prix fictifs

Le nouveau module `rollout.py` prend seulement le numéro de pas et
le cumul des codes **déjà générés**. La loi qui fournit la tête n'a
aucune interface permettant de recevoir des prix futurs ; le même
contrat permet un calcul de log-vraisemblance en teacher forcing, où
la cible n'est intégrée à l'état qu'**après** sa notation.

`empirical_crps` calcule le CRPS d'une distribution empirique
sur les **prix natifs**, avec une formule O(n log n) vérifiée contre
le double calcul par paires. Il s'agit du score de l'**ensemble fini**
et non d'un estimateur sans biais de la loi sous-jacente.

Smoke test construit : origine fictive 100, échelle 0.02, 20 pas,
512 trajectoires BASE indépendantes (graine 20261025), puis une
trajectoire synthétique séparée servant de pseudo-observation.

| Grandeur purement fictive | Résultat |
| --- | ---: |
| Médiane de l'ensemble à 20 pas | 99.875 |
| Quantile empirique 10 % | 88.692 |
| Quantile empirique 90 % | 111.907 |
| Pseudo-prix réalisé (artificiel) | 117.058 |
| CRPS de l'ensemble (unité de prix fictive) | 12.1823 |
| Erreur absolue de persistance (même cas) | 17.0581 |

Ce seul tirage n'est **pas** une preuve de supériorité de la tête sur
la persistance. Tous les nombres sont construits, dans les mêmes
conditions par le même simulateur ; aucune valeur de marché n'y entre.
Les tests comptent désormais 14 cas.

## Limites et portes de sortie

1. Le sampler se sert de probabilités float64 ; ses queues sous-fluées
   sont inaccessibles. Tester un algorithme de queue en log-espace
   avant d'en faire un simulateur de crise ; conserver le refus si non.
2. Les gradients mu/sigma et la stabilité en rétropropagation
   PyTorch/JAX ne sont pas validés. Pas encore de démonstration d'un
   entraînement bout-à-bout.
3. Les bornes de log-prix sont contrôlées par
   decode_lattice_price ; exp() peut échouer sur des trajectoires
   longues et doit être surveillé, sans suppression d'échantillons.
4. Le coût des **4096** contributions par pas subsiste même avec
   HIER : cette démonstration n'est pas un benchmark GPU.
5. Le nombre de présentations des historiques BCE réutilisées
   **n'est pas** le nombre d'observations indépendantes. Aucune
   partition future protégée n'a été ouverte.
6. Ne pas chercher de « meilleur marché » avec ce code :
   l'étape prédictive nécessite encore corpus admissible,
   décisions de gel, contrôles de fuite point-in-time,
   entraînement des témoins et scores natifs.

## Plan suivant, conditionnel

- Vérifier les dérivées par rapport à mu/sigma et le log-normalisateur
  via un backend autodiff sur une matrice de stress.
- Définir le sampler à support log-probabiliste effectif et ses limites,
  ou accepter une politique de refus des extrêmes en l'annonçant.
- Construire un générateur 20 pas sur **séries entièrement synthétiques**
  avec assertions de causalité, état entier n et indices futurs masqués.
- Mesurer le coût CPU/GPU/énergie par bras (normalisateur inclus)
  et qualifier le gradient quand q(k) est sous-flué.
- En parallèle, clore le contrat du corpus réel et les témoins
  quantile/numerical fortes **avant** tout run de marché.
- Seulement après : entraînement miniature Q/BASE/HIER/FLAT sur
  une séparation temporelle exclusivement *développement*,
  puis évaluation hors échantillon selon protocole préenregistré.

## Références

- [SciPy log_ndtr](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.log_ndtr.html)
  pour l'évitement des erreurs de la CDF ordinaire dans les queues.
- [Scipy truncnorm](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.truncnorm.html)
  pour le tirage conditionnel de la normale tronquée.
- [Gneiting et Raftery, proper scoring](https://stat.uw.edu/research/tech-reports/strictly-proper-scoring-rules-prediction-and-estimation-revised),
  pertinent pour la future évaluation de lois sur prix,
  **pas** une validation de TRAME.
