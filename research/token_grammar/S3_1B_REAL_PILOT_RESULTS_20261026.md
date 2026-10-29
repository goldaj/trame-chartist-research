# S3.1B — pilote appris vs numérique, 36 vrais fits BTC
**26 octobre 2026. [GitHub Actions #40305840861](https://github.com/goldaj/trame-chartist-research/actions/runs/40305840861) : trois jobs réussis sur trois.**

## Expérience réellement effectuée
- Bitstamp BTC/USD SPOT, D1 2012+ / H1 / M1, sources publiques vérifiées SHA.
- D1 **3608 train**, H1/M1 **4096 train**, **1024 dev par horizon** sur 2022–2025 ; 2026 non utilisé.
- Trois horizons × deux grammaires **G1 bins fixes / G2 quantiles train-only** × trois bras **decoded / embedding_ordered / embedding_random** × deux objectifs **regression/joint** = **36 fits réels**.
- Modèle width16, profondeur 1, 40 mises à jour, **UNE graine 20261026** ; bases communes et embeddings ordonnés/random même taille. **+11 paramètres entraînables** pour les modèles learned vs référence numeric ; le contrefactuel réellement équilibré à paramètres égaux est ordered vs random.
- Aucun ordre réel/Hyperliquid, aucun PnL composé ni frais, aucune validation indépendante.

## Précision simultanée du sens et du montant (valeurs représentatives)
**BA** : balanced accuracy directionnelle. **MAE** prix en bps. **Amplitude** : erreur de l'amplitude absolue (bps).

| Horizon | Loss | Grammaire | Bras | BA % | MAE bps | Amplitude bps | UP prédit % |
|---|---|---|---|---:|---:|---:|---:|
| D1 | Joint | G1 | decoded | 52,83 | 181,478 | 176,297 | 66,8 |
| D1 | Joint | G1 | embedding_ordered | **53,02** | **181,460** | 176,409 | 67,8 |
| D1 | Joint | G1 | embedding_random | 50,00 | 181,797 | 175,497 | **100,0** |
| D1 | Regression | G2 | decoded | 49,37 | 181,635 | 180,121 | 56,4 |
| D1 | Regression | G2 | embedding_ordered | 50,65 | 181,621 | 179,984 | 69,1 |
| D1 | Regression | G2 | embedding_random | 49,90 | 181,853 | 178,365 | **0,1** |
| H1 | Joint | G2 | decoded | 49,18 | 34,209 | 30,245 | 95,5 |
| H1 | Joint | G2 | embedding_ordered | 49,18 | 34,210 | 30,242 | 95,5 |
| H1 | Joint | G2 | embedding_random | 50,00 | 35,230 | 27,114 | **100,0** |
| M1 | Regression | G1 | decoded | 52,81 | 5,839 | 4,112 | 16,8 |
| M1 | Regression | G1 | embedding_ordered | 52,81 | 5,830 | 4,118 | 16,8 |
| M1 | Regression | G1 | embedding_random | 50,00 | 5,829 | 4,116 | **0,0** |
| M1 | Joint | G2 | decoded | 51,10 | 6,137 | 4,042 | 34,5 |
| M1 | Joint | G2 | embedding_ordered | **51,32** | 6,112 | 4,047 | 32,6 |
| M1 | Joint | G2 | embedding_random | 48,17 | **5,776** | 4,139 | 14,7 |

**Observations** : l'initialisation ordonnée facilite parfois une petite hausse de BA vs centre fixe, mais l'effet est faible et pas toujours accompagné d'un progrès de l'erreur d'amplitude. L'initialisation aléatoire peut réduire artificiellement la MAE en retournant presque toujours un signe unique ; H1 reste largement bloqué sur UP. **Aucun gagnant et aucun edge validé** à ce stade.

## Preuves détaillées, toutes les 36 lignes dans artefacts Actions
[Run #40305840861](https://github.com/goldaj/trame-chartist-research/actions/runs/40305840861) :
- **D1** : `D1_s3_1B_real_pilot.json`, SHA256 `d6198a9f35b1d62f966b04f954769b3b320e335eddcbaf0b81ea32e3ea32e3e6`.
- **H1** : `H1_s3_1B_real_pilot.json`, SHA256 `983785662d94c7c4d31716bab76d09eb5456fbc61841c9aab6fd2332eeb76782`.
- **M1** : `M1_s3_1B_real_pilot.json`, SHA256 `3d7f443f3892a8804d6b826bf397e0f143f7d354e2fe94dabc5510a1ea55b082`.
- Code exécuté : `ec24205eb5ab2a1563f0d6ddc5c83382ff47e339`, rangé dans la branche publique PR #25.

## Étape suivante
[GitHub Actions 432 fits](https://github.com/goldaj/trame-chartist-research/actions/runs/40306642813) sur D1/H1/M1, 3 seeds et 200 mises à jour, **144 fits/horizon**.
Vérifier les **trois jobs et l'agrégateur**, ne pas annoncer le résultat à partir du pilote. Conserver les 36+432 rapports dans documentation/historique et les conclusions honnêtes sur l'effondrement directionnel.

Le test indépendant 2026 demeure gelé. La qualité du sens et l'erreur des **montants USD/bps** restent deux critères majeurs simultanés ; ne pas optimiser l'un en sacrifiant l'autre sans le signaler.
