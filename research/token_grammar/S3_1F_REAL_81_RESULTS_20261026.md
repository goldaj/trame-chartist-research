# TRAME S3.1F — prix BTC sur mêmes poids : 9 entraînements, 81 évaluations
**26/10/2026, expérience TERMINÉE.**
[GitHub Actions #40326818917](https://github.com/goldaj/trame-chartist-research/actions/runs/40326818917) : **4/4 jobs réussis**, D1/H1/M1 + panel. Git SHA de l'EXÉCUTION scientifique : `58bc0f1e9425975a037ad2bf135943890a5b474b`.

## Protocole figé avant résultats BTC
`research/token_grammar/S3_1F_INFERENCE_PROTOCOL_20261026.md`.
BTC/USD spot public Bitstamp, données originales vérifiées Git SHA.
D1 train **2876**, monitor **731** ; H1/M1 train **4096**,
monitor **1024** par horizon. TRAIN labels connus avant
2020-01-01 UTC ; MONITOR interne 2020–2021 seulement ;
**ancien DEV externe 2022–25 et holdout 2026 non consultés**.
G2 signed quantiles et normalisation fittées TRAIN uniquement.

**NEUF modèles réellement entraînés** = trois horizons ×trois
graines (20261025, 20261026, 20261027), tous à 2000 updates.
Même modèle `ContinuousDirectionModel` (width16,
depth1, 2418 paramètres, Joint, contexte 20),
même loss **legacy** S3.1E, mêmes batch indices, mêmes
optimiseurs et init qu'en S3.1E. Checkpoints
200, 800, 2000 : **27 états de poids** ;
à chaque état 3 règles prix : **81 mesures dépendantes**,
pas 81 modèles ni 81 observations financières indépendantes.

Trois méthodes sur LES MÊMES poids :
1. `joint_hard` = logit>=0 ? +|mu| : -|mu|, règle historique ;
2. `signed_direct_mu` = retour de la tête mu ;
3. `joint_soft_tanh` = (2 sigmoid(logit)-1)|mu|, règle de sortie
   **alternative**, pas l'ancien produit live.

Tous les prix sont reconstruits par
`anchor*exp(return_bps/10000)` et scorés avec la même
vérité cible. Le code vérifie **égalité numérique
exacte de joint_hard avec forecast_prices historique**
et teste la parité des scores historiques S3.1E legacy
sur les mêmes exemples/graine/checkpoint, avant analyses.
La BA de SOFT est **identique à HARD par construction**
car tanh ne change pas le signe du logit sauf
égalité exacte au seuil ; aucun nouveau pouvoir
directionnel ne peut en être déduit.

## Résultats au checkpoint 2000, moyenne descriptive de trois graines
BA % = balanced accuracy du SENS ;
MAE prix bps = erreur du prix USD reconstruit en bps
de l'ancre (plus bas est mieux) ;
AMP bps = erreur de l'amplitude absolue du mouvement.
USD estimations dans le panel complet.

| Horizon | Règle | BA sens % | MAE prix USD | MAE prix bps | AMP erreur bps | UP prédit % | MONO /3 |
|---|---|---:|---:|---:|---:|---:|---:|
| D1 | HARD actuel | **52,24** | 865,84 | 282,704 | **248,938** | 69,3 | 0 |
| D1 | mu DIRECT | 51,24 | 866,51 | 282,897 | **248,938** | 64,6 | 0 |
| D1 | tanh SOFT | **52,24** | **854,98** | **280,707** | 273,477 | 69,3 | 0 |
| H1 | HARD actuel | **51,93** | **167,79** | 54,611 | **48,955** | 61,6 | 0 |
| H1 | mu DIRECT | 51,26 | 168,08 | 54,642 | **48,955** | 55,2 | 1 |
| H1 | tanh SOFT | **51,93** | 167,97 | **54,511** | 53,856 | 61,6 | 0 |
| M1 | HARD actuel | **53,02** | 25,76 | 8,368 | **7,319** | 49,7 | 0 |
| M1 | mu DIRECT | 52,40 | 25,77 | 8,377 | **7,319** | 43,2 | 0 |
| M1 | tanh SOFT | **53,02** | **25,58** | **8,337** | 8,215 | 49,7 | 0 |

## Comparaison à persistance (prix inchangé), chiffres S3.1F
| Horizon | Persistance prix MAE bps | SOFT MAE bps | Différence SOFT − persistance | Graînes sous le témoin |
|---|---:|---:|---:|---:|
| D1 | 281,03674 | 280,70711 | **−0,32963 bps (−0,117%)** | 3/3 |
| H1 | 54,53529 | 54,51124 | **−0,02405 bps (−0,044%)** | 3/3 |
| M1 | 8,34657 | 8,33700 | **−0,00957 bps (−0,115%)** | 3/3 |

Les trois graines partagent les MÊMES cas historiques, donc
3/3 n'est PAS trois validations indépendantes.
Les améliorations minimes peuvent simplement refléter
le fait que la règle soft rapproche les prix de l'ancre
comme un modèle **shrinké vers la persistance**.

## Conclusion critique chercheur × ingénieur
1. **SOFT améliore le MAE prix vs HARD** :
   D1 −1,997 bps ; H1 −0,100 bps ; M1 −0,0309 bps.
   Sa justesse directionnelle est **mathématiquement
   la même** que HARD, donc ne pas parler de prédiction
   directionnelle nouvellement apprise.
2. **SOFT détériore l'erreur d'amplitude** :
   D1 **+24,539 bps (+9,86%)**,
   H1 **+4,901 (+10,01%)**,
   M1 **+0,896 (+12,24%)**.
   L'ampleur devient moins fidèle quand on réduit
   les prédictions vers zéro.
3. **Direct mu ne gagne pas** :
   MAE prix légèrement plus élevé sur les trois
   horizons, baisse de BA de ~1,00 /0,67 /0,62 points.
   L'erreur d'amplitude reste la même car HARD
   et DIRECT utilisent tous deux `abs(mu)`.
4. **Persistance compétitive** : malgré les améliorations
   SOFT contre persistance de ~0,04–0,12% en MAE prix,
   la marge est très faible et les mêmes séries 2020–21
   ont déjà servi aux choix des études S3.1C/D/E.
5. Le taux de désaccord signes des deux têtes à 2000 :
   D1 7,9%, H1 19,0%, M1 26,7%.
   Ce diagnostic explique que le direct soit différent
   du hard, pas que le sens vrai soit plus accessible.
   Le Brier score reste celui de la tête `logit` et
   **ne calibre PAS la direction de direct_mu**.
6. **NO-GO pour déclarer un edge financier, un trader
   autonome ou une supériorité robuste des IA**.
   Ni les 3 graines ni les 27 checkpoints ne sont
   des périodes indépendantes. 2026 gelé,
   aucun PnL cumulé, aucune simulation de frais
   conformément à la demande.

## Suite recommandée : S3.1G, audit d'utilité sélective
L'utilisateur a expliqué que **la direction ET
la précision de l'amplitude** doivent permettre
à un trader de décider QUAND agir, sans modéliser
les frais. Avant de grossir les IA :
- Sur des poids figés et data causalement isolées,
  définir **uniquement avec TRAIN** des seuils
  de magnitude prédite et évaluer le sens
  et l'erreur d'amplitude conditionnellement
  aux prédictions réellement assez grandes.
- Rapporter **couverture**, nombre de cas,
  BA vs accuracy brute, MAE prix USD/bps,
  erreur relative et absolue d'amplitude,
  biais de classe, comparaison persistance
  **sur le même sous-échantillon**.
- Préenregistrer le protocole, partitions et
  seuils sans sélectionner après avoir
  consulté les chiffres 2020–21 ;
  aucune extrapolation PnL.
- Ne pas confondre « modèle sans frais »
  et « trader profitable ». **Maintenir 2026 scellé**.
Ne pas encore modifier simultanément architecture,
grammaire, profondeur ou modèle.

## Provenance / SHA256 des rapports complets
- D1 27 scores : `cedce2429cba23fabaffd2f64cbf8c1b9bfd392d2f46fb5ea2fe4a3817cbb570`.
- H1 27 scores : `46554230716de979d8988303bf2ca879ec9dd322647ddedb7e85a3488ca48180`.
- M1 27 scores : `13a9899a077c1a7734384559777e18430d0a5181811efa706618874e1968be6b`.
- Panel 9/27/81 JSON : `48c796e4977975e76e18cb78a54f82c3dbd8a31beb1affefb23300d3319d966a`.
- Panel Markdown : `5bca07cae8ab3916c3b9f2f7a59277a928be4c1fd366fbf67a11c8e3d7e61250`.
- Code source exécuté `58bc0f1e9425975a037ad2bf135943890a5b474b`.
- Rapport Actions [#40326818917](https://github.com/goldaj/trame-chartist-research/actions/runs/40326818917)
  **4/4 jobs SUCCESS**, artifacts 30 jours.
- Archive des cinq fichiers + MANIFEST vérifié :
  `trame_s3_1f_9_models_81_evaluations.zip` dans la conversation.
