# A7.4 — première campagne M1 réelle, cours historiques BTC/USD

**25 octobre 2026. Développement exploratoire, jamais un test indépendant.**

## Reproductibilité

- Données : quinze archives minute 2012–2026 de la release
  **privée et épinglée** `btcusd-bitstamp-2010-2026-reference-v1`,
  dans `goldaj/btc-historical-data`. Aucun prix publié dans TRAME.
- TRAME commit : `fdf50911022e9a869c8551bcc8e3944f75a33588` ;
  même protocole H1/M1 en adaptant l'horizon et le stride.
- Exécution GitHub Actions privée
  [#40223842842](https://github.com/goldaj/btc-historical-data/actions/runs/40223842842),
  branche `chatgpt/trame-private-m1-evaluation-20261025`,
  workflow au commit `2c496cf8cbc20198e4023d6bcd9c03dd286645dc`.
- Artefact privé `trame-real-btc-m1-exploratory-private`
  (deux JSON, **aucune archive de cours**).
- SHA-256 JSON architectures :
  `2e9ab5be020743dcf6d73f962433d0c9f1ecee8e188c7642ad83ba8284aa4ade`.
- SHA-256 JSON témoins :
  `60daf727777af265d5f94fcd4f1883a21625fa24acf5f243f2b1bbd69dfc1521`.

## Données et expérience

- 32 693 origines train candidates scannées ; 22 175
  origines développement candidates scannées.
  Ces chiffres sont affectés par le **stride 60** de l'étude
  M1 et les conditions d'éligibilité.
- 4 096 train et 1 024 développement retenus
  par échantillonnage par réservoir.
- Train : labels avant **2022-01-01 UTC** ;
  développement : **2022–2025** ;
  **cibles 2026 non utilisées**.
- Trois seeds 20261025/26/27, 40 pas pour chaque
  architecture CPU float64, paramétrage exploratoire.
- Aucun égalisation complète des FLOPs/budgets de tuning,
  ni aucune simulation d'exécution perpétuelle.

## Résultats, prochaine minute

**MAE en dollars du développement M1** ;
modèles neuronaux moyennés sur trois seeds.

| Approche | MAE USD | NLL dev moyenne, si applicable |
| --- | ---: | ---: |
| **Persistance** | **29,49414** | N/A |
| Ridge trois features passées | 30,47323 | N/A |
| Transformer original | 30,27041 | 1,62229 |
| GPT-style mini | 30,03578 | 1,50131 |
| GRU témoin | 30,00138 | 1,58270 |

RMSE des témoins : persistance **48,40951 USD**,
Ridge **50,30240 USD**. La couverture empirique des
intervalles théoriques 80 % est **97,56 %** pour la
persistance et **97,46 %** pour Ridge : forte surcouverture
à ce stade de développement, non une bonne calibration.

**Conclusion de recherche (provisoire et limitée)** :
sur ces exemples minute, la **persistance est meilleure
en MAE native que les trois mini-modèles neuronaux**.
Les écarts entre réseaux varient selon les seeds ; NLL
et MAE sont des objectifs différents. Les hypothèses
de distribution et la prévision à une minute peuvent
favoriser la persistance, sans démontrer qu'une famille
d'architecture serait supérieure/inférieure en général.
Le modèle n'a pas été réglé ni entraîné pour converger
réellement sur M1.

Attention : la comparaison directe des NLL **H1 versus
M1 est scientifiquement irrecevable**, les horizons
étant différents. Les MAE en dollars sont elles aussi
sensibles au niveau BTC des époques retenues.

## Suites scientifiques minimales

1. **A7.5** : intervalles par année et par volatilité
   ex ante ; rendement/erreur relative normalisés, pas
   seulement dollars. Distinguer changements de régimes
   et volume nul.
2. Multiplier les budgets d'entraînement, seeds,
   contextes, ablations, stratégies de sampling et
   géométries de modèles ; mesurer le vrai compute.
3. Évaluer des horizons pertinents pour l'usage visé
   plutôt que de supposer que la prochaine minute ou heure
   est le meilleur produit à construire.
4. Ne pas ouvrir 2026 avant un gel explicite et une
   méthodologie vraiment confirmatoire. Aucun pseudo-test
   indépendant post hoc.
5. Évaluer l'intérêt économique dans un banc sans
   look-ahead et avec coûts, mais **aucune preuve de PnL
   profitable ni transfert Hyperliquid** actuellement.

**Verdict : GO sur l'exécution des recherches réelles M1 ;
NO-GO pour sélectionner un gagnant, valider la calibration
ou livrer TRAME Predictive v1.**
