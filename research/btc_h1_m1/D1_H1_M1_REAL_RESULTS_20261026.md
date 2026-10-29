# A7-D1 — premières preuves réelles et reprise tri-horizon
26 octobre 2026, **exploration de développement uniquement**.
Aucune validation 2026, aucun ordre, aucune performance financière prouvée.

## Origine, preuves et périmètre
- Release privée `goldaj/btc-historical-data`, tag
  `btcusd-bitstamp-2010-2026-reference-v1`.
- Branch publique de code `chatgpt/trame-d1-parity-20261026`,
  exécution initiale sur SHA **`3473ea322b7084f9e0ba343eb05accf1ddd31d28`**.
- Workflow privé [D1 A7 + S1 #40280347574](https://github.com/goldaj/btc-historical-data/actions/runs/40280347574),
  **réussi**. Branche privée `chatgpt/trame-private-d1-a7-scaling-20261026`,
  commit `29516ffa0113fe3e0e477fca56cc7e354999c200`.
- Workflow privé H1/M1 harmonisé
  [#40280464439](https://github.com/goldaj/btc-historical-data/actions/runs/40280464439),
  **réussi** (les deux jobs), code public même SHA.
- Échantillonnage D1 réel : **3 622** origines train candidates et
  retenues, **1 461** développement candidates, **1 024** retenues ;
  entraînement cibles antérieures à 2022, développement 2022–2025.
  2010–2011 indicatif reste **hors pipeline OHLCV**, les vrais
  Bitstamp 2011H2–2025 sont utilisés.
- H1/M1 : **4 096 train / 1 024 dev** chacun, comme A7 initial.
- Prototypes : 1 couche, ~2.4–2.6 k paramètres, 3 seeds
  `20261025/26/27`, **40 updates seulement**. Non convergés ;
  budget FLOPs, recherche d'hyperparamètres et temps non égalisés.
- Prix BTC/USD spot et non carnet Hyperliquid.
  Les frais sont volontairement ignorés sur instruction utilisateur.
  Le sens annoncé ne vaut pas une entrée de marché.

## Résultats réels sur développement (moyenne 3 seeds pour réseaux)
**MAE prix native en USD**, par horizon. Ne pas comparer les valeurs
USD de D1/H1/M1 entre elles sans normalisation/stratification.

| Bras | D1 MAE USD | H1 MAE USD | M1 MAE USD |
|---|---:|---:|---:|
| Persistance / dernier prix | 974,7802 | 183,5182 | 29,4941 |
| Ridge historique train-only | 979,0448 | 183,7207 | 30,4732 |
| Transformer masqué classique | 973,7139 | 183,4921 | 30,2704 |
| GPT-style GQA/RoPE mini | 974,6576 | 183,5501 | 30,0358 |
| GRU contrôle | 974,3426 | 183,6858 | 30,0014 |

**Direction juste sur tous les cas (%)** :
| Bras | D1 | H1 | M1 |
|---|---:|---:|---:|
| Ridge | 51,660 | 49,414 | 48,535 |
| Transformer | 50,163 | 49,447 | 47,266 |
| Mini GPT | 50,293 | 49,414 | 48,535 |
| GRU | 50,684 | 49,414 | 47,266 |

La **persistance prédit FLAT**, sans signal actif ; elle ne mérite
pas une précision de hausse/baisse inventée. D1 réels : 519 hausses,
504 baisses, 1 flat ; le GRU prédit **1 024 hausses sur 1 024**
pour chacune de ses trois seeds, d'où exactement 50,684 % et
**balanced directional accuracy = 50,00 %** : aucune discrimination.
H1 : les 3 seeds GPT et GRU prédisent **1 024 hausses** chacune.
M1 : plusieurs réseaux basculent presque intégralement du tout-haussier
au tout-baissier selon la graine. Le score brut 47–51 % ne démontre
aucun avantage sur les contrôles de classe majoritaire.

## Montant du mouvement prévu : sous-estimation massive
L'erreur d'amplitude est en points de base, entre valeurs absolues de
rendements prévus/réels et pas entre signes :

| Indicateur | D1 | H1 | M1 |
|---|---:|---:|---:|
| Taille absolue moyenne **réelle** du mouvement (bps) | 181,72 | 33,84 | 5,27 |
| Taille absolue prédite Transformer (bps ; moyenne seeds) | 6,00 | 1,85 | 0,81 |
| Taille absolue prédite mini GPT (bps) | 1,21 | 1,58 | 0,75 |
| Taille absolue prédite GRU (bps) | 3,95 | 2,28 | 0,63 |

**Lecture :** la prédiction se rapproche trop souvent de la
persistance ; elle peut présenter une MAE USD similaire sans capter
le signe et surtout le mouvement pertinent pour un trader.
Cela ne prouve pas que la taille de l'architecture n'aide pas.
Le codec `FIXED_SCALE=1000` quantifie le log-return en entiers ;
pour les petites variations M1/H1, la classe peut être perdue.
Un bras continu/hybride direction+amplitude doit être étudié
avec un protocole **distinct**, sans changer rétrospectivement
la représentation des anciennes expériences.

## D1 témoins par année, reproduits sur les prix réels
MAE USD persistance D1 :
- 2022 : n=250, 640,10 $ ;
- 2023 : n=263, 464,71 $ ;
- 2024 : n=260, 1 312,68 $ ;
- 2025 : n=251, 1 492,56 $.
Ce sont des MAE nominales influencées par le prix BTC, **pas**
une preuve que le modèle se dégrade structurellement.

## Empreintes SHA-256 des sorties agrégées (archives privées)
- `btc_d1_real_baselines_dev.json`: `9509d3cf17e6c77067a4d9cd47a3e298fcf75d57f74105f7d9ba1ac7547891c6`
- `btc_d1_real_architectures_dev.json`: `fbbf7683d38b5ac753adb4ef5bbef66df6159ea79a55cf59aa474e264a157765`
- `btc_d1_real_regimes_dev.json`: `0e18771ba8ae62cfab4e4d98c1faf220ce22a3a2d3de9302a645fa69d856a576`
- `btc_d1_real_direction_dev.json`: `21f46e67887db3841743c37d3d982b41d5208ac6627728059cf02fa018700382`
- `H1_real_direction.json`: `e910e4cc586d2443c4b109c5b6054b752d8fa7364ce629dd1b7e81749d467fcb`
- `M1_real_direction.json`: `770d2d563cdad4cc3859ea9e18f7134af8b8abfa23e55937e894a78d9084a644`

Ces SHA attestent l'identité des **rapports JSON**, pas une
validation d'indépendance ni la garantie de distribution BTC.
Archives Actions privées à rétention 30 jours ; aucun prix brut,
token ou JSON de prévisions individuelles n'a été publié.

## Verdict et priorités
- **GO** D1.1–D1.7 : ingestion journalière, tests synthétiques,
  baselines, modèles, décomposition des régimes, mesures directionnelles
  D1/H1/M1 exécutées et documentées. Les résultats sont exploratoires.
- **NO-GO** sélection d'un gagnant, avantage directionnel,
  NLL inter-horizons, portefeuille cumulatif, ouverture des cibles
  2026, mise en production.
- Suivant : correction des contrôles toujours-up/down, test de
  sensibilité *taille × profondeur* par horizon, budget de convergence
  réellement suffisant et représentation continue/hybride. Aucun
  classement « plus gros = mieux » avant une comparaison équitable.
