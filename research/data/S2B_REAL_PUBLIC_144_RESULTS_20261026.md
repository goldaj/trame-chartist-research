# TRAME S2b — 144 entraînements réels publics sur les 3 horizons
26 octobre 2026, suite au consentement explicite du propriétaire
à utiliser les données historiques BTC en public.

## Traçabilité et validation
- [GitHub Actions #40296933559](https://github.com/goldaj/trame-chartist-research/actions/runs/40296933559),
  3/3 jobs **réussis**, un par horizon D1/H1/M1.
- **SHA du code modèle** (identique sur les 3 rapports) :
  `2c9a3bab9d274852564abe6c70042a1145e6193c`.
- Release de provenance : original public
  `alessiostomeo/btc-cycle-data` au commit
  `b57f460fab1afb82705eb813cee2ef4afb1f6848`,
  SHA-1 et taille de chaque source vérifiés par le
  downloader `research/data/public_data.py`.
  D1 2012–2026H1 est aussi committé en CSV dans TRAME.
- **144 fits réels** =
  3 horizons × 2 entrées (log-return continu / code
  historique arrondi) × 2 objectifs
  (Huber / Huber + 0.5 BCE) × 2 largeurs
  (16/32) × 2 profondeurs (1/2) × **3 graines**
  (`20261025`, `20261026`, `20261027`).
  **200 optimizer updates** pour chaque fit, CPU.
- **D1** 3 608 train / 1 024 dev (Bitstamp OHLCV
  2012+, pas de 2011H2 pour cause d'attribution) ;
  **H1 et M1** 4 096 train / 1 024 dev.
- Entre le bras continu et le bras quantifié :
  même modèle, même seed, même hash de poids initiaux,
  **même échelle d'entrée et de cible sur train
  continu**, même séquence de mini-lots,
  mêmes labels de prix réels. Le panel apparié
  compare seulement des bras partageant ces invariants.
- L'année 2026 demeure **hors train/dev**.
  Il s'agit d'un test sur le **développement 2022–2025**,
  **pas** d'une validation indépendante.

## Moyennes descriptives par famille de perte
Chaque cellule est une moyenne sur **12 fits par
résolution et mode** : 2 widths × 2 depths × 3 seeds.
Ces fits sur les **mêmes 1 024 cibles par horizon**
ne sont pas 12 expériences statistiques indépendantes.

**BA = balanced accuracy hausse/baisse, en %** ;
**MAE bps = erreur absolue de prix relative à l'ancre,
en points de base** ; **err amplitude bps** =
erreur sur valeur absolue du mouvement attendu.
C'est le même protocole S2b, non un backtest
d'exécution de trades.

| Horizon | Loss | BA continu % | BA arrondi % | Δ BA cont−arrondi (pp) | MAE cont bps | MAE arr bps | Err amplitude cont bps | Err amplitude arr bps |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| D1 | Huber | 50,25 | 50,19 | +0,058 | 184,427 | 184,437 | 158,526 | 158,513 |
| D1 | Huber+BCE | 50,03 | 50,02 | +0,007 | 183,871 | 183,865 | 159,782 | 159,685 |
| H1 | Huber | 50,00 | 50,01 | −0,008 | 34,651 | 34,650 | 28,652 | 28,633 |
| H1 | Huber+BCE | 51,14 | 50,85 | +0,289 | 34,490 | 34,489 | 28,753 | 28,832 |
| M1 | Huber | 49,76 | 50,01 | −0,252 | 5,400 | 5,391 | 4,506 | 4,508 |
| M1 | Huber+BCE | 49,69 | 49,86 | −0,172 | 5,442 | 5,444 | 4,470 | 4,434 |

**Diagnostic scientifique** : il n'y a **aucune victoire
constante du continu** en balanced accuracy ou précision
du montant sur D1, H1 et M1. En H1 Huber+BCE,
la hausse moyenne +0.29 point de BA est minime,
mais ne garantit aucune amélioration hors développement.
Sur M1, les bras arrondis font légèrement mieux
en BA moyenne, malgré une forte destruction du
signe à la tokenisation. Cela peut refléter des
régularisations implicites, bruit sur les très petits
mouvements, sous-entraînement ou variance, sans
permettre d'en attribuer une cause unique.

## Échec récurrent : modèles quasi monoclasse
Un modèle est signalé `monoclasse_99pct` s'il
prédit hausse ou baisse sur au moins 99% des
1 024 origines de développement. Biais à
citer dans tous les tableaux :
- D1 Huber+BCE continu : **11/12** bras monoclasse ;
  arrondi : **10/12**.
- D1 Huber continu : 7/12, arrondi : 7/12.
- H1 Huber : **12/12 continu ET arrondi**,
  prédisant pratiquement tout en hausse
  (BA 50% sans discrimination).
- H1 Huber+BCE : 6/12 dans les deux.
- M1 Huber : 7/12 continu, 5/12 arrondi ;
  M1 Huber+BCE : 5/12 continu, 4/12 arrondi.

La proportion de hausses prédites en H1
Huber moyen est ~100% : la « justesse »
brute à 49% ne signifie pas compétence.

## Probabilités de direction du bras Huber+BCE
`brier_skill_vs_train_prior` :
- D1 continu **−0,00060**, arrondi **−0,00059**
  (moins bien que prior naïf, en moyenne).
- H1 continu **+0,00376**, arrondi **+0,00392**.
- M1 continu **+0,00172**, arrondi **+0,00232**.

Ce sont des valeurs très proches de zéro, sur un
ensemble de développement déjà sollicité pour
les choix de recherche ; pas une preuve
de calibration robuste ni d'edge utilisable.

## Référence au diagnostic pur de grammaire
Les audits publics antérieurs
[H1/M1](https://github.com/goldaj/trame-chartist-research/actions/runs/40296158821)
et [D1](https://github.com/goldaj/trame-chartist-research/actions/runs/40295846917)
constatent que `round(log-return×1000)` efface
le signe de :
- **D1 : 2,86 %** des retours non plats dans les
  fenêtres de contexte de développement.
- **H1 : 13,74 %**.
- **M1 : 64,26 %**.

Ces fréquences portent sur des fenêtres
**recouvrantes de 20 retours** et non sur
autant d'observations indépendantes.
Conserver le signe historique n'est PAS
équivalent à prédire le signe de la
bougie future.

## Empreintes SHA-256 des rapports 144-fit publics
- `D1_public_s2b_200steps_3seeds.json` :
  `84e27eb3d718fa867196305ffa5dd050990e03143b9d2fea25cb71cef0a4490f`
- `H1_public_s2b_200steps_3seeds.json` :
  `66d72fa6a3e4d53b51c9e13be4a45d921b399a702bfab49c1f1e3ca4d9942bc0`
- `M1_public_s2b_200steps_3seeds.json` :
  `4e0c4c58d20a434cac8792a43953913b69eba67e19485ccd9a9341b4fefbef34`

Les JSON complets et métriques par seed/width/depth
sont dans les **artefacts GitHub Actions** du run
#40296933559, rétention définie dans le workflow,
aucun prix brut publié dans les artefacts.

## GO / NO-GO et prochaine étape
- **GO technique** : accès réel BTC public
  D1/H1/M1, téléchargement H1/M1 intégral,
  144 fits sur vraies bougies,
  parité des modèles et des splits,
  tracabilité par commit et empreintes.
- **NO-GO scientifique** : « le continu
  prédit mieux que l'arrondi » n'est
  **pas démontré**. Les modèles sont
  sous-entraînés (200 updates) et
  fortement biaisés vers une direction.
  Aucune validation indépendante 2026,
  aucune mesure fiable de gain financier.
- **Précaution importante** : cette comparaison
  teste l'effet du **préprocessing d'entrée**
  à loss fixée, pas la supériorité
  d'une « grammaire complète » ;
  une décomposition explicite sens/amplitude,
  patches et vocabulaire appris peut modifier
  l'apprentissage autrement.
- **Suite logique S3.1** :
  issue [#20](https://github.com/goldaj/trame-chartist-research/issues/20)
  : prendre G0b (continu),
  G1 (signe et amplitude à seuils fixes),
  G2 (seuils train-only) puis patch tokens,
  à même architecture/cibles/loss/seeds.
  **Préenregistrer** les variantes avant
  d'observer leurs scores de développement.
  Stratifier par année et volatilité,
  conserver la fraction de sortie monoclasse,
  BA et erreur d'amplitude bps.
- Les frais de trading restent exclus selon
  l'utilisateur ; aucune action Hyperliquid,
  aucun PnL portefeuille cumulé validé.
