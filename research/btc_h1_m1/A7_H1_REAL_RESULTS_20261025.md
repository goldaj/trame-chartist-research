# A7.4 — première campagne H1 sur véritables bougies BTC/USD

**25 octobre 2026. Étude de développement exploratoire, PAS test indépendant.**

Cette campagne a **réellement exécuté** les codes TRAME sur le gzip
H1 original de la release privée `goldaj/btc-historical-data`,
**sans placer l'archive de cours dans TRAME public**.

## Traçabilité exacte

- Référentiel BTC privé :
  `btcusd-bitstamp-2010-2026-reference-v1`.
- Fichier retenu : `BTCUSD_bitstamp_hourly_2012-2026.csv.gz`,
  taille attendue et constatée **2 727 050 octets**.
- Code TRAME utilisé : commit
  `fdf50911022e9a869c8551bcc8e3944f75a33588`,
  branche `chatgpt/trame-btc-stat-baselines-20261025` (PR #14).
- Workflow privé de recherche : branche
  `chatgpt/trame-private-h1-evaluation-20261025`
  dans le dépôt des données, commit
  `27036f36bb47335efb8ec7f1a8937a6e706d5a1c`.
- [Exécution réussie #40223399371](https://github.com/goldaj/btc-historical-data/actions/runs/40223399371)
  et artefact **privé** `trame-real-btc-h1-exploratory-private`
  (rétention du workflow : 30 jours). Il ne contient que
  deux rapports JSON de recherche, jamais des prix bruts.
- SHA-256 du JSON architectures : 
  `7de2956bd4cc26597016490757692779a7b97c9da8982922e371df7c6f2bc232`.
- SHA-256 du JSON témoins :
  `409edf5217bb84c91187749b44a911ece1533115ef079a497ebe0f1c29798b4a`.
  Ces empreintes identifient des sorties particulières, sans
  attester de la validité causale ou de la représentativité du prix.

## Échantillon réellement utilisé

- 78 225 origines **train candidates scannées**, dont
  4 096 retenues par échantillonnage par réservoir.
- 34 953 origines **développement candidates scannées**,
  dont 1 024 retenues.
- Train : labels antérieurs à **2022-01-01 UTC**.
- Développement : labels **2022–2025**.
- Labels de **2026 non ouverts** ; `independent_test_used=False`.
- Bougies à volume nul ou contexte temporel interrompu exclus.
- Modèles neuronaux : trois seeds
  20261025, 20261026, 20261027, **40 pas chacun**,
  CPU `torch 2.10.0+cpu`, Python 3.12.
- Les budgets de compute et de recherche d'hyperparamètres
  **ne sont pas strictement égalisés**.
  H1 prédit la prochaine heure, pas la prochaine journée/minute.

## Mesures observées sur développement H1

**MAE native USD ; plus petit = moins d'erreur sur cet échantillon
uniquement.** Les modèles neuronaux sont moyennés sur trois seeds.

| Bras | MAE USD | NLL dev, moyenne si applicable |
| --- | ---: | ---: |
| Persistance (prix précédent) | **183,51822** | N/A |
| Ridge (trois features historiques) | 183,72070 | N/A |
| Transformer original | **183,49213** | 3,31817 |
| GPT-style mini moderne | 183,55011 | 3,32611 |
| GRU témoin | 183,68577 | 3,38889 |

Autres mesures des deux témoins :
persistance RMSE **334,98809 USD**, couverture 80 % nominale
observée **95,31 %** ; Ridge RMSE **337,13628 USD**,
couverture 80 % observée **95,51 %**.

**Lecture scientifique :** le Transformer est à peine meilleur
que la persistance sur la moyenne observée, d'environ
**0,026 USD** pour une MAE de ~183,5 USD. Le signe de ce très
faible écart n'est ni significatif ni stable démontré.
La NLL et la MAE ne constituent pas le même objectif,
et l'intervalle fourni par les témoins paraît
**conservateur** sur cet échantillon (surcouverture).

Les résultats par seed, conservés dans le JSON privé,
diffèrent ; ne pas sélectionner le « gagnant » sur une moyenne
de trois graines avant intervalles appariés, découpes de régimes
et véritable gel du protocole. Un score exprimé en dollars
sur dix ans de BTC nécessite une analyse normalisée
et des statistiques par régime.

## Verdict Go / No-Go

- **GO** : le connecteur de release, les lecteurs, les contrats
  temporels, la tête gaussienne, les témoins et les trois modèles
  s'exécutent réellement sur H1. La voie privée GitHub Actions
  lève le blocage d'absence de `gh auth login` sur la machine locale.
- **NO-GO** : annoncer un avantage prédictif ou sélectionner un
  modèle final. Ne pas toucher à 2026 pour les ajustements.
- **NO-GO économique** : Bitstamp spot n'est pas le carnet
  Hyperliquid perp et les données ne comprennent pas les
  fills, frais, funding, impact ni capacités.
- **À poursuivre** : répétition par régimes, latence, budgets
  compute-fair, comparaison plus longue M1 et D1, erreurs
  normalisées, mesures appariées/dispersion, tests de
  résistance aux trous, nouveaux modèles et protocole de
  holdout non déjà exploré.
- **M1** : workflow privé distinct lancé ; **aucun score
  M1 n'est présumé** avant fin et lecture du rapport.

## Instructions de reproduction pour Codex

1. Lire `AGENTS.md` et `docs/CODEX_EXECUTION_BOARD_20261025.md`.
2. Ne jamais publier les gzip/csv de prix ni le jeton temporaire.
3. Sur une machine autorisée, `gh auth login` et suivre
   `research/btc_h1_m1/README.md`, ou utiliser le workflow
   de la branche **privée** dédiée ci-dessus. Le token Actions
   n'est exposé **qu'à l'étape shell de téléchargement**,
   jamais aux commandes Python d'entraînement.
4. Préserver les SHA, les origines et le statut exploratoire.
5. Ne jamais utiliser les scores de développement comme
   résultat d'un test financier indépendant.

Cette note documente un **premier succès d'ingénierie sur prix réels**,
pas une validation scientifique définitive.
