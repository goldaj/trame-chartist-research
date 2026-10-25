# TRAME Predictive v1 — critères scientifiques, ingénierie et décisions

**25 octobre 2026. Contrat de travail, pas une validation du produit.**

L'état cible est une **application locale** de prévision
probabiliste, avec distributions/calibration mesurées sur
historiques financiers indépendants, export et documentation,
**sans connexion à un compte ni capacité d'envoyer des ordres**.
Aucun résultat synthétique du projet ne prouve l'utilité de
TRAME pour un marché.

## P1 : sélection et entraînement vérifiables

- [x] **P1.1 : critères ex ante** : MAE/RMSE native par actif et
  horizon, CRPS/pinball/couverture, robustesse par régime,
  coûts CPU/GPU, mémoire, latence et coût du tuning ;
  baseline persistance et témoins AR/Ridge. Aucun classement
  multihorizon avec NLL des tokens incompatibles.
- [x] **P1.2 : fiche entraînement** : `source_release`,
  `source_resolution`, `split_version`, `origin_policy`,
  `architecture`, `representation`, `objective`,
  `seed`, `hardware`, `environment`, `train_budget`,
  `search_budget`, `code_commit`, `train_only_transforms`,
  `artifact_sha256`, `license`.
- [x] **P1.3 : checkpoints** : format explicite non exécutable
  si possible (ex. safetensors), empreinte SHA-256,
  paramètres et version de code, droits des poids,
  aucune clé, pas de pickle arbitraire depuis des sources
  inconnues, provenance matérielle des checkpoints.
- [x] **P1.4 : sélection contrôlée** : même jeu et mêmes
  origines éligibles, seeds, tests appariés par blocs,
  dispersion, correction de comparaisons multiples,
  budget de tuning. Si un modèle n'est pas mesurable
  avec les mêmes données : statut `excluded`, jamais 0.
- [ ] **P1.5 : figer le(s) modèle(s) candidat(s)** seulement
  après des runs sur prix réels et une revue des limitations.
  Aucun modèle final sélectionné à ce jour.

## P2 : robustesse et validité hors échantillon

- [x] **P2.1 : protocole** : isoler développement et
  holdout, aucune ouverture du test avant le gel des modèles,
  règles de `available_at`, gestion des trous et révisions.
- [x] **P2.2 : catalogue de stress à implémenter** :
  ruptures de tendance, sauts, faible liquidité, volatilité
  extrême, trous calendaires et volumes nuls, changement
  d'actif/résolution, décalage temporel.
- [x] **P2.3 : calibration exigée** :
  courbes de fiabilité, couverture des intervalles,
  pinball/CRPS et incertitude sur les différences de scores.
- [x] **P2.4 : dérive et refus de prédiction** :
  règles de détection hors domaine définies avant
  évaluation et règles d'abstention hors zone validée.
- [ ] **P2.5 : audit indépendant/gel** : évaluer le modèle
  retenu une fois sur un vrai jeu test jamais utilisé
  lors du tuning, publier résultats bruts y compris négatifs.
  Jamais remplacé par la CI synthétique.

## P3 : valeur économique, exclusivement hors ligne

- [x] **P3.1 : protocole de simulation** : signaux formés
  seulement avec observations réellement connues à
  l'origine, décision et horodatage enregistrés, résolution
  et objectif économique séparés du score statistique.
- [x] **P3.2 : coûts imposés** : spread, frais,
  slippage, funding (perp), latence et indisponibilité ;
  déclarer les frais en bps et faire varier plusieurs
  hypothèses pessimistes. Bitstamp spot n'est pas
  historique d'exécution Hyperliquid.
- [x] **P3.3 : témoins économiques** :
  cash/no position, buy-and-hold spot à risque comparable,
  stratégies de seuil triviales et tests d'ablation
  sans indicateurs futurs.
- [x] **P3.4 : risques économiques** :
  drawdown, rendement total/net, turnover, exposition,
  dispersion par bloc, capacité, queues défavorables
  et sensibilité aux hypothèses de coûts.
- [ ] **P3.5 : validation économique financière** :
  seulement avec prix/volumes d'exécution admissibles,
  vraies périodes indépendantes et modèle gelé ;
  la présence d'un simulateur synthétique ne débloque
  pas les ordres ni ne garantit de rentabilité.

## P4 : produit livrable local

- [x] **P4.1 : frontière architecturale** :
  interface/API offline, aucun portefeuille, aucune clé
  privée ni endpoint d'ordre de bourse, aucune
  recommandation ou mise en production automatique.
- [x] **P4.2 : interface exigée** :
  origine UTC, actif, intervalle, horizon, modèle et
  version, intervalles probabilistes, signalement
  "hors domaine", niveau de preuve et avertissements.
- [x] **P4.3 : versions/artefacts** :
  checkpoints et manifests signés/empreintés, politique
  anti-écrasement, journal de génération, logs
  sans informations sensibles.
- [x] **P4.4 : installation exigée** :
  Python/Windows/PyCharm et Linux, CPU fallback
  explicite, dépendances figées, GPU opt-in, tests
  d'installation et mise à jour documentée.
- [x] **P4.5 : critères d'utilisabilité** :
  tests navigateur/accessibilité, export autonome,
  répétabilité inter-machines et cas d'erreur lisibles.
- [ ] **P4.6 : publication Predictive v1** :
  impossible tant que P1.5/P2.5/P3.5 ne sont pas
  validés et que l'outil n'est pas installé/testé
  sur les environnements ciblés.

## NO-GO consolidé à cette date

- Benchmarks A3c : FLOPs seulement partiels, budget de
  tuning non égalisé.
- Mamba A4 : vrai GPU officiel non exécuté ; gardes CPU verts.
- Hybrides A5 : contrôle attention+GRU synthétique,
  aucun hybride Mamba réel évalué.
- Fondations A6 : aucun modèle préentraîné chargé ;
  contamination inconnue. TimesFM-3/Moirai-2 poids
  non commerciaux exclus du produit.
- Données A7 : release BTC privée épinglée, mais aucun
  benchmark financier effectif dans cette session,
  holdout 2026 préservé et multi-actifs non qualifiés.
- Research Lab A8 : outil autonome de rapports
  synthétiques existant, non un produit prédictif.

## Principes de livraison

Le verdict automatique `ready_for_launch` doit rester
**faux** en l'absence de preuves réelles indépendantes
et de revue humaine explicite. Un manifeste utilisateur
auto-déclaré ne prouve pas à lui seul la véracité des runs
ou l'absence de contamination. Aucune connexion au bot
Hyperliquid sans décision distincte de l'utilisateur.

Docs Codex de référence :
`docs/CODEX_EXECUTION_BOARD_20261025.md`,
`research/architecture_comparison/A3C_RESULTS_20261025.md`,
`research/btc_h1_m1/A7_STATUS_20261025.md`
sur leurs branches respectives.

## Implémentations complémentaires de la reprise

Le contrôle P1.2–P1.4 de l'identité technique est dans
`checkpoint_contract.py`, sans ouverture de modèles sérialisés
arbitraires et sans prétendre certifier la qualité d'entraînement.
Les diagnostics P2 de causalité, abstention et calibration descriptive
de développement sont dans `development_diagnostics.py`, avec tests
adversariaux pour 2026, horizons mélangés et signaux disponibles trop tard.

P3 impose la chronologie et la continuité des marques de prix ;
trois niveaux hypothétiques de coûts sont comparés aux témoins cash
et buy-and-hold. La simulation reste fondée sur des prix **inventés**
et n'est pas une reconstruction de transactions Hyperliquid.

Les jeux de tests P1/P2 ont passé Linux et Windows ;
la CI de P3/P4 a passé Ubuntu. Ces validations **n'altèrent pas**
les états P1.5, P2.5, P3.5, P4.6 tous ouverts et **NO-GO**.
