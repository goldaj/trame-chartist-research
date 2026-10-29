# A7.5 — résultats réels H1 par année et par volatilité ex ante

**Calcul le 25 octobre 2026 ; clôture documentaire le 26 octobre 2026.**

> **Développement exploratoire seulement.** Les lignes de cours sont restées
> privées ; le test indépendant et les labels 2026 ne sont **pas** ouverts.
> Aucun résultat ici n'établit un avantage financier ni n'autorise le trading.

## Traçabilité reproductible

- Données : BTC/USD H1, release privée
  `goldaj/btc-historical-data`,
  tag `btcusd-bitstamp-2010-2026-reference-v1`.
  Respecter la décision utilisateur de **ne pas refaire l'audit de provenance**
  des fichiers fournis.
- Code exécuté : TRAME
  `2087d72e37e1dfcb549e2803b1c1fa0182ac41e8`,
  `research/btc_h1_m1/regime_analysis.py`, `statistical_baselines.py`,
  `stream.py` ; tests de garde-fous synthétiques verts,
  [CI TRAME A7 #40224053252](https://github.com/goldaj/trame-chartist-research/actions/runs/40224053252).
- Workflow d'exécution **dans le dépôt privé**, branche
  `chatgpt/trame-private-h1-regimes-20261025`, commit
  `0e5606e7aac7d19fcac52036337cecd7a3b7b8e6`.
- [Exécution privée réussie #40224149619](https://github.com/goldaj/btc-historical-data/actions/runs/40224149619) ;
  artefact privé `trame-real-h1-regimes-exploratory-private`,
  contenant uniquement `btc_h1_real_regime_development.json`.
- SHA-256 **des octets du JSON** :
  `95be1bc04dd44aa6534ef298916f7ecb9802c27f0280199d92ca32783dfb9236`.
  L'empreinte identifie ce rapport, elle ne certifie pas une
  indépendance statistique ni l'authenticité des cours en amont.
- 78 225 candidats d'origine entraînement parcourus ;
  34 953 candidats développement parcourus.
  **4 096 train / 1 024 développement** conservés par
  échantillonnage fixe, comme pour les témoins H1 A7.4.
- Entraînement : cibles avant 2022 ;
  développement : **2022–2025** ; pas de label 2026.

## Tableau 1 : décomposition par année

**Persistance**, horizon prochain H1. Erreur bps =
`mean(abs(prediction - cible) / cible) * 10000`, pas la
moyenne naïve d'un unique taux de changement.

| Année | n | MAE USD | Erreur relative bps | Couverture 80 % |
| --- | ---: | ---: | ---: | ---: |
| 2022 | 257 | 118,53953 | 43,30011 | 92,996 % |
| 2023 | 284 | 72,72535 | 25,11462 | 98,239 % |
| 2024 | 228 | 248,17105 | 37,29195 | 94,298 % |
| 2025 | 255 | 314,59216 | 31,25129 | 95,294 % |
| **Total développement** | **1 024** | **183,51822** | **33,91828** | **95,313 %** |

Ridge entraîné avant 2022 sur les mêmes cibles :
MAE 2022 **119,41784**, 2023 **72,82235**, 2024
**249,76117**, 2025 **312,99026** USD.
Il fait marginalement mieux en 2025 et moins bien les trois
autres années. Son MAE global est **183,72070 USD**.
Aucun écart n'est évalué comme statistiquement significatif.

**Important** : une MAE en dollars croît avec le prix nominal
du Bitcoin. Le niveau de 2025 ne prouve donc pas à lui seul
que le marché est intrinsèquement plus difficile que celui de 2022.
L'erreur relative des deux années va même dans le sens inverse.

## Tableau 2 : volatilité passée, connue à l'origine

Regroupement basé **uniquement sur les 20 codes de rendements passés**,
sans utiliser la volatilité future pour former les groupes.
Les deux seuils en écart-type de rendements log,
fixés sur **train avant 2022**, sont
`0,0041303752856` et `0,0074086098561`.
Ce sont des seuils issus du jeu échantillonné, pas des
définitions universelles de régimes.

| Volatilité passée | n | MAE persistance USD | Erreur bps | Couverture 80 % |
| --- | ---: | ---: | ---: | ---: |
| Faible | 541 | 124,31085 | 21,92929 | 99,261 % |
| Moyenne | 361 | 212,68299 | 39,08796 | 93,352 % |
| Forte | 122 | 359,76992 | 71,78546 | 83,607 % |
| **Total** | **1 024** | **183,51822** | **33,91828** | **95,313 %** |

Le groupe haute volatilité a une erreur relative
environ **3,27 fois supérieure** à celle du groupe faible
volatilité, dans cet échantillon. C'est une différence
descriptive, **pas** un ratio de risque généralisable
sans échantillonnage représentatif ni intervalle de confiance.

Ridge : MAE faible **123,97676**, moyenne **211,58396**,
forte **366,20290 USD**.
Les écarts restent faibles en régime calme/moyen et Ridge
est moins bon en régime agité dans ce pilote.
Ne pas sélectionner automatiquement une architecture
en fonction de ce résultat.

La couverture nominale est 80 %, alors que les observations
montrent **99,26 % en faible volatilité** et **83,61 % en forte**.
La distribution d'incertitude est excessivement conservatrice
sur la partie calme de cet échantillon ; sa calibration ne
se transfère pas nécessairement aux changements de régime.

## Contrôles de cohérence effectués à la clôture

- Somme par années : `257 + 284 + 228 + 255 = 1 024`.
- Somme par groupes de volatilité : `541 + 361 + 122 = 1 024`.
- Les **moyennes pondérées par n** des MAE et couvertures
  pour ces deux découpages reproduisent chacune :
  persistance **MAE 183,51822265625 USD**,
  couverture **0,953125** ;
  Ridge **MAE 183,72069709370587 USD**,
  couverture **0,955078125**.
  Elles sont cohérentes avec le rapport H1 A7.4.
- Drapeaux du JSON d'origine :
  `baseline_fit_train_only=true`,
  `regime_thresholds_derived_train_only=true`,
  `2026_test_opened=false`,
  `is_confirmatory=false`,
  `not_hyperliquid_fills=true`.
- Les erreurs relatives pondérées reconstituent
  **33,91828 bps** pour persistance et **34,02015 bps** pour Ridge.
- **Aucune ligne brute de cours et aucun actif de la release
  privée ne sont recopiés** dans ce dépôt public.

## Conclusion scientifique et Go / No-Go

**GO, observation descriptive A7.5-H1** : la qualité
prévisionnelle de la persistance et la couverture des intervalles
changent fortement entre les régimes. La MAE seule ne permet
pas de comparer des années de prix BTC différents ; il faut
conserver au minimum bps/erreurs relatives et calendrier.

**NO-GO, comparaison confirmatoire** : cette analyse ne couvre
que les témoins H1, pas les trois modèles neuronaux par régime,
ni les M1/D1, ni la capacité d'exécution à prix effectivement
tradables. Il manque des intervalles d'incertitude sur les
différences appariées, une étude de représentativité par période,
des scénarios extrêmes mieux définis, une vraie égalisation
compute/tuning et un test temporel jamais utilisé pour la
sélection. **A7.5 globale reste PARTIELLE.**

**NO-GO, économie/produit** : ce sont des bougies BTC/USD
spot et non des exécutions perpétuelles Hyperliquid ;
pas de frais, funding, carnet, fills ou preuve de rentabilité.

## Passation exacte à Codex

1. Repartir de la [PR #14](https://github.com/goldaj/trame-chartist-research/pull/14)
   et de ce fichier, de `A7_H1_REAL_RESULTS_20261025.md`
   et `A7_M1_REAL_RESULTS_20261025.md`.
2. Pour réévaluer les régimes avec les prix réels, utiliser
   la branche **privée** et le commit du workflow référencés ;
   ne pas stocker le fichier de cours dans TRAME.
3. A7.5 reste à poursuivre sur **M1, modèles neuronaux,
   stress tests et intervalles**. A7.6 et A7.7
   sont toujours bloqués / non effectués.
4. La suite scientifique P1/P2/P3/P4 est **NO-GO**
   tant qu'il manque sélection et validation indépendantes.
5. Ne pas demander un nouveau contrôle de provenance des
   historiques acceptés par l'utilisateur ; continuer à
   vérifier causalité, types et temps d'observation.
