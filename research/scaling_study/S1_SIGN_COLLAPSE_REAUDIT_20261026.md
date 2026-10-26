# S1 audit rétrospectif : effondrement en une seule classe
26 octobre 2026. Calcul descriptif additionnel à partir des **trois
artefacts privés originaux** de la campagne 200 updates :
[workflow GitHub Actions privé #40281657954](https://github.com/goldaj/btc-historical-data/actions/runs/40281657954).
Réutilise les résultats S1 existants, **aucun nouvel entraînement**,
aucun 2026, aucun frais ni ordre de trading.

## Méthode et valeur probante
Sur chaque résolution, les 81 lignes = 3 architectures × 3 tailles
cibles × 3 profondeurs × 3 graines. Chaque ligne évalue
**les mêmes 1 024 origines** de développement 2022–2025 ;
les 81 scores ne sont pas statistiquement indépendants.
Un bras est appelé `monoclasse_99pct` si son nombre de prédictions
en hausse ou en baisse représente **au moins 99 % des 1 024 cas**.
Le seuil est choisi *pour ce diagnostic après les premiers résultats*
et n'est PAS un critère confirmatoire préenregistré.

| Résolution | Bras monoclasse ≥99 % | Fraction |
|---|---:|---:|
| D1 | 72 / 81 | 88,89 % |
| H1 | 45 / 81 | 55,56 % |
| M1 | 34 / 81 | 41,98 % |

Sur le grand nombre de configurations D1, prédire hausse dans
presque tous les cas rend le taux d'accuracy de 50,7 % trivial
au regard du taux de vrais mouvements haussiers. Une
`balanced_direction_accuracy=50 %` ne prouve pas une
discrimination utile du sens.

## Meilleures configurations *descriptives* par balanced accuracy
Moyenne sur les **3 graines**, pas un meilleur seed isolé :
- D1 : Transformer classique, cible 37 000 paramètres / profondeur 4,
  balanced accuracy **50,15 %**, **98,6 %** de prévisions en hausse.
  MAE **182,44 bps** ; persistance **181,72 bps**.
- H1 : Transformer classique, cible 148 000 paramètres / profondeur 4,
  balanced accuracy **52,10 %**, **60,7 %** de prévisions en hausse.
  MAE **34,34 bps** ; persistance **33,84 bps**. Étendue
  inter-graines de balanced accuracy ≈ **4,0 points de %**.
  Cette configuration est sélectionnée post hoc sur développement,
  donc aucun test indépendant ni intervalle de confiance
  confirmatoire, et son MAE est moins bon que le témoin.
- M1 : Transformer classique, cible 2 400 paramètres / profondeur 2,
  balanced accuracy **51,10 %**, **45,6 %** de prévisions en hausse.
  MAE **5,28 bps**, proche mais supérieure à la persistance
  **5,27 bps**. Étendue inter-graines ≈ **3,0 points de %**.

### Pourquoi ce diagnostic importe
1. Le pourcentage de sens juste doit rester accompagné de
   balanced accuracy et de la répartition des signes prédits.
2. Une petite amélioration directionnelle *sur des données de
   développement utilisées pour sélectionner des architectures*
   est parfaitement compatible avec le bruit ou du surajustement.
3. L'erreur native USD ne suffit pas : rendre le montant comparé
   en bps à la persistance et documenter l'erreur **d'amplitude
   absolue** est obligatoire, en plus du signe.
4. Les architectures ne sont pas comparées à FLOPs égaux
   et 200 updates ne prouvent pas leur convergence.
5. Même les 243 prédictions agrégées par configs et seeds ne
   fournissent pas ici des **résidus individuellement appariés
   temporellement**, nécessaires à une vraie évaluation de
   significativité robuste aux dépendances temporelles.

## Hypothèse séparée S2
S2 compare des rendements continus avec/sans une tête explicite
de classification hausse/baisse, en conservant D1/H1/M1, le
freeze 2026 et des témoins qui n'ont aucun signal prédictif.
**Aucune campagne sur cours BTC S2 n'a encore été exécutée**.
La future évaluation doit préciser la couverture du signal, le
Brier skill face au prior train-only, l'accuracy équilibrée,
le score du sens brut, la vraie erreur d'amplitude bps et les
temps CPU par graine.

## Traçabilité des trois sources immuables
- D1 : `D1_scaling_3seeds_200updates.json`,
  SHA256 `c4bd1b321c1dcd017d26a65c440f651e30f77d97db44f16f076853b9db3d06c1`
- H1 : `H1_scaling_3seeds_200updates.json`,
  SHA256 `a6c891ff706260e072d2a1a95c57cf66161e78347c30ca7cc9f0c9bd8666e2ea`
- M1 : `M1_scaling_3seeds_200updates.json`,
  SHA256 `b7943ea979f66cd2c372bae9941f35323fa9f4a7588737b0e5bd0853825190aa`

L'analyse est reproductible en inspectant les champs
`n_predicted_up`, `n_predicted_down`, `forecast_rows`,
`balanced_direction_accuracy` et `mae_bps_anchor` de
ces JSON privés. Aucun fichier de prix, identifiant de
portefeuille ou ordonnance n'est présent ici.
