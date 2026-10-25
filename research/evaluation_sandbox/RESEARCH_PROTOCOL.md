# TRAME : protocole de score comparatif prospectif (candidat, non gelé)

**Statut au 25 octobre 2026 : document de recherche et banc de test synthétique,
sans prévision de marché ni nouveau test indépendant.**
Ne modifie aucun des protocoles gelés de 2026-10-14 à 2026-10-16,
n'autorise aucun téléchargement d'une partition protégée et ne change
aucune architecture P1-D/P1-B0.

## Question testable

Un modèle génératif TRAME produit-il, **à information disponible égale**,
des prévisions sur les **prix natifs** qui dépassent systématiquement la
baseline de persistance `P(t+h) = P(t)`, avant de comparer les représentations
P1-D et les têtes BASE/HIER/FLAT ?

H0 : une fois le protocole figé, les différences de pertes de TRAME et
persistance ne sont pas suffisamment robustes pour rejeter une équivalence
pratique. H1 : avantage sur des prix nouveaux, répétable et non limité à une
seule série ou un seul régime. Un gain local isolé ne prouve pas un
« langage universel du marché ».

## Frontières des preuves

1. **Déjà consulté** : BCE 1999–2009 (ajustement et audit des cibles),
   cohortes CHF 2010–2014 (développement exploratoire), crypto 2021
   (calibration/développement). Ces archives peuvent servir à
   *concevoir ou développer*, **jamais** être rebaptisées « test intact ».
2. **Futur test indépendant** : désigner *avant accès aux valeurs* les
   instruments, sources, dates et statuts point-in-time pertinents.
   Aucun test n'est désigné ni ouvert par cette note.
3. **Unité de preuve** : la cotation future observée est distincte d'une
   « présentation » réutilisée dans vingt fenêtres de contexte. Les fenêtres
   qui se recouvrent ne multiplient pas les observations indépendantes.
4. **Source temporelle** : calendrier de publication et révisions à tracer ;
   les cours BCE révisés ne prouvent pas leur disponibilité originale à t.
   Le modèle ne voit ni valeur future, ni statut de publication futur connu
   seulement rétrospectivement.

## Matrice minimale à déclarer avant toute expérience prédictive

| Axe | Valeurs candidates et risque |
| --- | --- |
| Marché | Forex BCE, crypto spot, indices/actions, taux, matières premières ; *plusieurs sources indépendantes*, attribution et type de prix |
| Temps | au moins un régime calme et un régime de rupture par famille disponible ; sélection ex ante |
| Résolution | dates réellement observées ; pas de bougies imaginées par interpolation |
| Horizon | 1, 5, 20 observations publiées ; analyser séparément |
| Contrôles | persistance (obligatoire), témoin numérique fort à budget égal (à figer), modèles TRAME successifs |
| Partitions | fit/calibration, développement, véritable futur holdout ; pas de sélection sur holdout |
| Réplicats | même calendrier, budget, graines et arrêts par bras ; publier échecs |
| Validité externe | nouveau temps, puis nouvel instrument, puis famille nouvelle ; trois questions distinctes |

Un embargo égal ou supérieur au maximum des fenêtres d'entrées/étiquettes
peut prévenir le chevauchement aux frontières. Le calcul exact doit tenir
compte des 256 valeurs de contexte et des 20 horizons ; **un embargo seul
n'empêche pas** les transformations apprises globalement (normaliseur,
tokenizer, sélection de candidats, métadonnées révisées) de fuir le futur.
Contrôler les dates de *disponibilité* des valeurs, pas seulement les dates
inscrites sur les bougies.

## Mesures et règles avant d'entraîner

- **Primaire candidate** : amélioration appariée de l'erreur absolue
  `|P_pred-P_vrai|` relativement à la persistance, par couple
  actif/horizon, en unités de prix de l'actif ; **aucune somme en dollars entre
  actifs ou devises**.
- **Secondaire** : RMSE en prix natifs, MAE des log-prix, biais signé ;
  intervalles de prédiction et couverture 80 % *si* une loi de prix
  (incluant le choix intra-cellule) a été explicitement spécifiée et testée.
- **Scores probabilistes** : une NLL de codes calculée avec deux quantizers
  distincts ne constitue pas automatiquement une comparaison de densités en
  prix. Pour un score propre comparable, annoncer à l'avance une distribution
  commune en prix et la manière de la calculer. Monte-Carlo : convergence,
  graine, intervalle d'erreur d'échantillonnage et prix extrêmes, y compris
  cas non finis, doivent être rapportés séparément.
- **Incertitude** : intervalles construits en respectant dépendances
  calendaires, de série et d'horizons. Ne pas appliquer un test iid aux
  centaines de milliers de présentations recouvrantes ; prévoir bootstrap
  par blocs d'origines ou autre méthode justifiée. Séparer exploration
  de confirmation, corriger la multiplicité des essais rapportés.
- **Critère d'arrêt** : fuite détectée → score non interprétable ;
  non-finitude ou simulation instable → protocole incomplet ;
  TRAME ne dépasse pas la persistance → résultat négatif publié,
  pas de publication sélective des actifs favorables.
- **Critère de promotion à entraînement** : partitions choisies, tests de
  causalité, métriques et témoins définis ; calcul d'essai budgété et
  protocole de conformité reproductible.

## Outil livré : contrôle de score (aucune donnée réelle)

`score_points.py` attend un JSONL d'**observations préparées en amont**
où chaque ligne comporte exactement :

```json
{"asset":"DEMO","origin_index":10,"target_index":11,"horizon":1,"anchor":100.0,"actual":110.0,"forecast":109.0}
```

L'index est celui des **observations disponibles** dans la série de cet
actif, pas celui de jours calendaires. Pour l'horizon 1, target = origin + 1.
Le script refuse doublons, valeurs non positives, indices incohérents et
colonnes inattendues ; il compare prévision et persistance pour les mêmes
origines et **ne fusionne jamais les horizons ni les actifs**. Il compte
les observations futures distinctes ; il ne prétend pas assurer l'absence
de fuite entre le modèle qui a produit les données et ses cibles.

```bash
python -m unittest discover -s research/evaluation_sandbox -p 'test_*.py' -v
python research/evaluation_sandbox/score_points.py predictions.jsonl
```

Le dernier appel ne doit être fait que sur un fichier explicitement choisi ;
aucune archive TRAME n'est touchée automatiquement. La fixture ci-dessus
est construite à la main et ne représente aucun prix réel. **Aucune
performance TRAME n'a été produite par cet outil.**

## Sources méthodologiques (principes, pas preuves TRAME)

- Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*, évaluation
  sur nouvelles données et rolling origin :
  https://otexts.com/fpp3/accuracy.html
- Evaluation forecasts, pièges et pratiques :
  https://doi.org/10.1007/s10618-022-00894-5
- Diebold & Mariano, comparaison des erreurs de prévision dépendantes :
  https://doi.org/10.1080/07350015.1995.10524599

## Point de vigilance

Les résultats TRAME actuels démontrent que des encodages ont été
**reconstruits**, pas qu'une seule prévision soit correcte. Ce protocole
proposé est **non gelé** et doit être revu avant toute expérience facturée ou
accès à de nouvelles données tenues à part.
