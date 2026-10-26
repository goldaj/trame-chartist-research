# TRAME — premiers résultats BTC publics réels, D1/H1/M1
Date : 26 octobre 2026. Source **originale authentique** des
BTC/USD Bitstamp spot ; résultat **EXPLORATOIRE**
sur le développement 2022–2025, **pas un test indépendant**.

## Provenance et exécution
- **D1** : historique 2012-01-01 → 2026-06-30 dans TRAME,
  [run public #40295846917](https://github.com/goldaj/trame-chartist-research/actions/runs/40295846917),
  3608 train / 1024 dev. L'ancienne cohorte D1 privée
  incluait quelques exemples Bitstamp 2011H2 :
  les anciens scores D1 NE doivent PAS être
  interprétés comme une réplication à cohorte égale.
- **H1 et M1** : originaux gzip de la source publique
  `alessiostomeo/btc-cycle-data` épinglée au commit
  `b57f460fab1afb82705eb813cee2ef4afb1f6848`,
  vérifiés par longueurs et Git blob SHA1, puis
  [run public #40296158821](https://github.com/goldaj/trame-chartist-research/actions/runs/40296158821)
  **2 jobs réussis**. H1 1 fichier gzip de
  2 727 050 octets ; M1 15 fichiers gzip de
  **110 005 289 octets** ; 4096 train et 1024 dev
  pour chacun. Aucune API privée ou secret.
- Tous les bras S2b du pilote : width=16, depth=1,
  40 mises à jour, **une graine 20261026**.
  Comparaison codage `continuous_bps` vs
  `legacy_quantized_bps`, loss Huber `regression`
  ou Huber + BCE `joint`, mêmes poids
  initiaux/indices de mini-lots/cibles continues,
  **mêmes scales d'entrée et de cible train-only**.
- Le fichier peut contenir des valeurs spot datées
  2026, mais `stream.iter_cases` exclut les
  **cibles 2026** avant toute génération d'exemple.
  Le score de développement concerne 2022–2025 ;
  **2026 n'est pas ouvert pour sélection/validation**.
- Aucun coût de transaction, aucun ordre,
  aucun PnL de portefeuille ou exécution
  Hyperliquid ; il s'agit de précision de prévision
  **spot**, pas de simulation d'un trader.

## S2b : justesse directionnelle et amplitude
Balanced accuracy (BA) : moyenne des rappels
hausse et baisse, **50% = absence de discrimination**
pour un classifieur monoclasse sur les mouvements
non plats. Les scores « accuracy » bruts et
les proportions de hausses prédites restent
obligatoires pour les tableaux finaux.

| Horizon | Mode | Entrée | Acc. sens % | BA % | MAE USD | MAE bps | Erreur amplitude bps | Hausses / 1024 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| D1 | Huber | continu | 52,83 | 53,41 | 973,82 | 181,43 | 175,24 | 147 |
| D1 | Huber | arrondi | 52,83 | 53,40 | 973,81 | 181,42 | 175,23 | 149 |
| D1 | Huber+BCE | continu | 51,66 | 51,14 | 974,35 | 181,72 | 173,84 | 914 |
| D1 | Huber+BCE | arrondi | 51,56 | 51,04 | 974,29 | 181,75 | 173,82 | 911 |
| H1 | Huber | continu | 49,51 | 50,10 | 186,13 | 34,46 | 28,94 | 1023 |
| H1 | Huber | arrondi | 49,61 | 50,19 | 186,04 | 34,44 | 28,97 | 1022 |
| H1 | Huber+BCE | continu | 49,41 | 50,00 | 185,89 | 34,42 | 29,14 | 1024 |
| H1 | Huber+BCE | arrondi | 49,41 | 50,00 | 185,86 | 34,42 | 29,13 | 1024 |
| M1 | Huber | continu | 47,46 | 51,53 | 33,36 | 5,88 | 4,13 | 115 |
| M1 | Huber | arrondi | 49,02 | 52,81 | 33,09 | 5,84 | 4,08 | 172 |
| M1 | Huber+BCE | continu | 48,63 | 50,31 | 35,28 | 6,10 | 4,16 | 527 |
| M1 | Huber+BCE | arrondi | 49,71 | 49,51 | 34,24 | 5,97 | 4,15 | 854 |

**Attention** : M1/H1 beaucoup de prédictions
monoclasse. Aucun gagnant déclaré avec une
seule graine et 40 updates. S2b reste
**insuffisamment entraîné** et pas validé
indépendamment. Les modèles M1 de ce pilote
n'ont pas réussi le pari « le continu vaut mieux
parce qu'il garde plus d'information » :
il ne faut pas chercher à rationaliser ce
résultat en décrétant un résultat définitif.

## S3 : diagnostic de reconstruction, PAS de prédiction
Chaque valeur correspond à la reconstruction de
**rendements PASSÉS** d'une fenêtre, aucun modèle
de cours futurs n'est entraîné dans ce diagnostic.
Les contextes de 20 bougies se chevauchent et
ne constituent pas des observations indépendantes.

| Résolution | Signes non nuls perdus par G0a | Erreur G0a amplitude bps | Erreur G1 signée fixe bps | Erreur G2 quantiles train-only bps |
|---|---:|---:|---:|---:|
| D1 | 2,86% | 2,51 | 95,07 | 310,73 |
| H1 | 13,74% | 2,50 | 14,77 | 141,97 |
| M1 | **64,26%** | 2,23 | 2,85 | 24,53 |

G0b continu : zéro perte de signe et zéro erreur
de reconstruction par construction. G1/G2 signées
conservent le signe des retours non nuls dans ce
codec, mais déforment parfois massivement
l'amplitude. Il serait erroné de conclure
que leur encodage est meilleur pour un trader
du seul fait de conserver le signe.

## Preuves d'identité des rapports agrégés
SHA256 des rapports JSON des runs publics :
- D1 S2b `802bd147fce0efd9a0f91048012c4c10e675e4da8a8ea435f9eee269b69bc71e`
- D1 grammaire `c88b23abc23cf14b6dd117a5eddbfd154da12872cbb6b0bbf0104a9a20b77158`
- H1 S2b `d566fa43207b24ef1c60031ccb22a67c55289b86bc0d9a69dc86ac9e053ae26a`
- H1 grammaire `acb22eafb9600fb66d1c65a180d8cd2517597d93fdd6d6aeebb845eaef6b6305`
- M1 S2b `f64603149e2332fce6a33f8bd8c9ecb8c0c8016ef6b29327125145e4f9a65e71`
- M1 grammaire `63a2dc34502005da7adf19f5eb80bc59b420dc6c604bd9114a9ed024dae02f47`

Les premiers rapports complets sont
**des artefacts GitHub Actions publics**, avec
la rétention définie par GitHub. Leurs SHA
permettent de constater si un fichier de
rapport a été modifié, mais pas de prouver
indépendamment la véracité de toutes les
observations source. Les données originales
sont identifiées par manifest + SHA Git blob.

## Nouvelle campagne importante
[Workflow public 3-seed / 200 steps #40296933559](https://github.com/goldaj/trame-chartist-research/actions/runs/40296933559)
lancé pour **144 fits** (48 par horizon),
même source/pub, 2 codecs ×2 losses
×2 widths ×2 depths ×3 seeds ×3 horizons.
**Son statut DOIT être vérifié avant d'en
parler comme d'un résultat.** Aucun score
de cette campagne ne peut être inféré
des pilotes ci-dessus.

## Priorités pour Codex
1. Vérifier réussite effective de chaque
   job 144-fit, conserver provenance et
   hashes, puis exploiter
   `research/representation_ablation/panel.py`
   pour comparer **par horizon**, en deltas
   `continu - arrondi` à graines appariées.
2. Mesurer dispersion inter-graines ;
   vérifier l'effondrement en une classe
   du bras `joint` et calibrer Brier skill
   vs a priori train-only.
3. Étendre ensuite les grammaires G1/G2
   en modèles prédictifs contrôlés **après**
   S2b et avant le prochain scaling massif
   des capacités neuronales.
4. Les secteurs D1 2010–11 indicatif
   (close seulement) et Bitstamp 2011H2
   ne sont **pas** publiés dans TRAME,
   faute de droits de redistribution
   suffisamment établis. Ce sont des
   cohortes historiques séparées, sans
   effet sur les comparaisons 2012+.
