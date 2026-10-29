# S1 — premier scaling réel D1/H1/M1, 5 tailles × 3 profondeurs
26 octobre 2026. **Exécution exploratoire** [workflow privé
#40281223578](https://github.com/goldaj/btc-historical-data/actions/runs/40281223578),
six jobs privés **réussis**. Code public **`b3db15999c0dd2f15f27163a973ababd93b0347e`**,
workflow privé `4693f73a6f2f4e309a4c80749fa41269cb8ad429`.
Aucune lecture des cibles 2026, aucune action de trading.

## Ce qui a vraiment tourné
- 3 résolutions D1/H1/M1 × 3 familles Transformer/GPT-mini/GRU
  × 3 profondeurs **1/2/4** × 5 tailles visées :
  **135 entraînements (une seed par configuration)**.
- Largeurs choisies pour approcher le compte de paramètres ciblé,
  mais certaines variantes du palier 2 400 diffèrent de >10 % :
  **1 762 à 2 858 paramètres réels**. Les tailles réelles
  des plus grands bras vont de **2 336 042 à 2 385 986**.
  Ne pas revendiquer égalité du nombre de paramètres au palier 2,4 k.
- Palier 2 400 / 37 000 / 148 000 : **40 updates**, seed `20261026`.
  Paliers 592 000 / 2 360 000 : **8 updates**, même seed.
  Leurs scores NE SONT PAS un vrai comparatif des tailles.
- 3 622 train/1 024 dev D1, 4 096 train/1 024 dev H1/M1 ;
  2010–2011 indicatif exclu, source spot privée.
- Le CPU a exécuté les modèles jusqu'à 2,39 M de paramètres ;
  ceci **ne démontre pas** la convergence ni la capacité à faire tourner
  les 405 expériences de comparaison à budgets équivalents.

## Balanced direction accuracy (%) moyenne descriptive des 9 configurations
de chaque couple taille/horizon (3 familles × 3 profondeurs,
**1 graine chacune**, pas une incertitude statistique) :

| Taille cible | Updates | D1 | H1 | M1 |
|---|---:|---:|---:|---:|
| 2 400 | 40 | 48,72 | 50,00 | 50,00 |
| 37 000 | 40 | 49,82 | 50,63 | 49,88 |
| 148 000 | 40 | 50,00 | 49,30 | 49,84 |
| 592 000 | 8 | 49,83 | 49,70 | 49,72 |
| 2 360 000 | 8 | 49,67 | 50,02 | 50,00 |

**NO-GO scientifique** : ce tableau ne démontre **aucune progression
directionnelle** avec la taille ni la profondeur. La grande majorité
des réseaux restent dans un régime de prédiction
quasi-monoclasse (toujours hausse/baisse) et leur balanced accuracy
approche 50 %. La variance inter-graines n'est pas connue ici.

## Erreur d'amplitude bps (même regroupement, plus faible = mieux)
| Taille cible | Updates | D1 | H1 | M1 |
|---|---:|---:|---:|---:|
| 2 400 | 40 | 180,88 | 33,06 | 4,76 |
| 37 000 | 40 | 174,72 | 32,20 | 4,17 |
| 148 000 | 40 | 162,44 | 31,66 | 4,27 |
| 592 000 | 8 | 158,55 | 28,14 | 4,45 |
| 2 360 000 | 8 | 155,51 | 26,66 | **17,61** |

Une meilleure amplitude D1/H1 peut provenir de biais d'échelle de sortie,
non d'une connaissance prédictive. À l'inverse, le grand M1 (2,36 M)
se dégrade fortement. Avec **8 steps** et une seule seed, il serait
scientifiquement aberrant d'en déduire une loi d'échelle générale.
Ne pas comparer bruts D1/H1/M1 : horizons distincts.

## SHA256 des six JSON agrégés privés
- D1 small : `c52ff65e3231f3cf9afdbe45b5eb793b5fa8e14d3856dc1c443f622b45600583`
- D1 large : `962cecc503e00779e5775dadd686440e657671bf8718d32f9774167a06b36ec6`
- H1 small : `dd2e433f36d7df1eb81adca11b39b62785dd1a6100fc409e962a5c5aff386127`
- H1 large : `ef012c71e42515b249a7767708d7dc1f2ab52302742fe9b255031d27817893e7`
- M1 small : `1bbd4acf26a5734c740e864231999aa311a35d495063ba437bf3b204ea64d499`
- M1 large : `50e785e919e498ea7b3b41f2b189062e05f3a3dfc3a62a2cd50c32ee3e24d74a`

## Suivants
1. Trois graines, davantage de pas pour tailles 2.4k/37k/148k sur
   **tous horizons et toutes profondeurs** ; comparer à 40 updates.
   Workflows privés séparés pour budget/identité des sorties.
2. Définir un « effet profondeur » par delta apparié à paramètres proches,
   et un effet « taille » à profondeur fixée. La comptabilité FLOPs
   reste partielle ; ne pas écrire « compute-matched ».
3. Étudier séparément la représentation des rendements continus
   et les sorties direction+amplitude. M1 subit l'arrondi du codec
   `log_return×1000` qui écrase des mouvements réels.
4. Aucune ouverture 2026 ni sélection de modèle pour Hyperliquid.
