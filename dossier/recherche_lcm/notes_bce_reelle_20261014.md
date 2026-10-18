# Corpus réel BCE : six séries de change quotidiennes, 1999–2020

**Audit du 14 octobre 2026 — Source : ECB statistics.** Une acquisition réelle a réussi depuis l'API officielle BCE, sans compte ni achat. Elle apporte un domaine de prix distinct de la cryptomonnaie et une profondeur historique de vingt-deux années. Aucun modèle n'a été ajusté et aucune performance prédictive n'a été mesurée.

## Nature exacte des données

Les séries sont `EXR.D.{USD,JPY,GBP,CHF,CAD,AUD}.EUR.SP00.A`. Chaque valeur représente le nombre d'unités de la devise pour **1 EUR**. Ce sont des cours de référence quotidiens : aucune ouverture, aucun plus haut/bas, aucun volume, spread ou chemin intrajournalier n'est fourni. Il serait incorrect de fabriquer ces champs ou de présenter la valeur comme une clôture de séance négociable. La BCE destine ces références à l'information et déconseille leur usage transactionnel. [Présentation officielle](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html).

L'[API officielle bornée](https://data-api.ecb.europa.eu/service/data/EXR/D.USD+JPY+GBP+CHF+CAD+AUD.EUR.SP00.A?startPeriod=1999-01-01&endPeriod=2020-12-31&format=csvdata) a renvoyé HTTP 200. Les paramètres demandaient exclusivement le 1er janvier 1999 au 31 décembre 2020. Le contrôle des lignes confirme qu'**aucun cours postérieur à 2020 n'a été acquis** dans ce fichier. Les données crypto réservées de novembre–décembre 2021 n'ont pas été consultées.

## Provenance et conservation

La réponse originale CSV contient **7 346 039 octets**, avec ses 32 colonnes de données et métadonnées. Elle a été reçue le **14 octobre 2026 à 09:43:22 UTC**, soit **11:43:22 à Paris**. Le fichier brut a été conservé sans transformation, sous un nom incluant date et empreinte ; sa réouverture pour l'audit a vérifié la même empreinte SHA-256 :

`b8a684b6331d3cf0310a1838efdce806495906ead99d672671642c3bf24130de`

L'[archive brute](</C:/Users/golda/Documents/ChatGPT/bot trading hyperliquid/research/trame_poc0/ecb_exploratory/raw/ecb_exr_daily_six_1999_2020_20261014T094250Z_b8a684b6331d.csv>) est accompagnée d'un manifeste contenant URL demandée et résolue, dates UTC, statut HTTP, en-têtes, taille et empreinte. Il s'agit d'une conservation avec contrôle d'intégrité, pas d'un stockage matériel WORM. Les résultats sont séparés dans l'[audit JSON](</C:/Users/golda/Documents/ChatGPT/bot trading hyperliquid/research/trame_poc0/ecb_exploratory/audit.json>) et les [comptes annuels](</C:/Users/golda/Documents/ChatGPT/bot trading hyperliquid/research/trame_poc0/ecb_exploratory/counts_by_year.csv>).

## Résultats de l'audit

| Série, devise par EUR | Lignes brutes | Valeurs numériques | Valeurs vides, statut H | Première / dernière observation numérique |
|---|---:|---:|---:|---|
| USD | 5 694 | 5 632 | 62 | 04/01/1999 – 31/12/2020 |
| JPY | 5 694 | 5 632 | 62 | 04/01/1999 – 31/12/2020 |
| GBP | 5 694 | 5 632 | 62 | 04/01/1999 – 31/12/2020 |
| CHF | 5 694 | 5 632 | 62 | 04/01/1999 – 31/12/2020 |
| CAD | 5 694 | 5 632 | 62 | 04/01/1999 – 31/12/2020 |
| AUD | 5 694 | 5 632 | 62 | 04/01/1999 – 31/12/2020 |
| **Total** | **34 164** | **33 792** | **372** | |

Les six séries partagent exactement les **5 632 mêmes dates numériques**. Aucun doublon de clé série/date, valeur numérique non finie ou non positive, observation de week-end, devise inattendue ou date hors période n'a été détecté. Les valeurs numériques portent toutes `OBS_STATUS=A`.

Les 372 cellules vides portent `OBS_STATUS=H`. La [liste officielle des statuts BCE](https://data-api.ecb.europa.eu/service/codelist/ECB/CL_OBS_STATUS/1.0), également conservée avec empreinte dans le dossier brut, définit A comme valeur normale et H comme absence liée à un jour férié ou un week-end. **Ces H ne sont pas des erreurs de téléchargement ni des valeurs nulles.** Ils n'ont pas été remplacés ou interpolés.

Sur les 5 740 dates du lundi au vendredi de la période demandée, 108 ne comportent aucune valeur numérique : 62 sont représentées explicitement par H et 46 n'ont aucune ligne. Les H présents s'arrêtent en 2012 ; les années suivantes omettent des dates sans créer de cellules H. Cette différence de représentation ne démontre pas un changement économique. Les 46 absences de ligne ne sont pas toutes individuellement certifiées par un calendrier historique TARGET dans cet audit. Leur liste est conservée pour vérification ultérieure. L'écart maximal entre deux observations numériques est de cinq jours calendaires.

## Disponibilité historique : limite à conserver

Le champ `TIME_PERIOD` est une **date de référence**, pas un horodatage certifié de première publication. Le titre complet des séries mentionne 14:15 CET, ce qui ne donne pas leur heure de disponibilité pour un utilisateur. Le communiqué officiel de décembre 2015 annonce un changement de publication d'environ **14:30 CET à 16:00 CET à compter du 1er juillet 2016**. Appliquer 16:00 rétrospectivement comme fait observé pour toute la période serait erroné. [Communiqué BCE](https://www.ecb.europa.eu/press/pr/date/2015/html/pr151207.en.html).

Le fichier représente la version de l'historique disponible en octobre 2026. Il ne prouve ni l'absence de révisions ni la valeur exactement visible à chaque date ancienne. Une étude quotidienne peut prévoir la prochaine référence après disponibilité de la précédente, en conservant cette réserve. Une synchronisation intrajournalière entre places nécessiterait des preuves supplémentaires. Un décalage prudent d'une publication est une convention expérimentale possible, à annoncer ; il ne reconstitue pas les versions historiques manquantes.

## Apport à la recherche de prévision

Ce corpus permet d'étudier une représentation de **prix seuls** : niveau de référence, variations logarithmiques entre publications, durée calendaire entre observations et identité de série. Il faut conserver les jours sans publication comme absences, sans créer des rendements artificiels nuls le week-end.

La diversité provient surtout des vingt-deux années et de ce nouveau domaine. Les six devises partagent un dénominateur EUR et des facteurs communs : 33 792 valeurs ne sont pas autant d'exemples indépendants. Les séparations temporelles devront être communes aux séries ; normalisations et représentations apprises devront utiliser seulement l'entraînement. L'audit de qualité effectué ici ne constitue pas un test final resté scellé ni une preuve qu'un modèle généralisera à d'autres classes d'actifs.

## Attribution et réutilisation

La [politique officielle de réutilisation](https://www.ecb.europa.eu/stats/ecb_statistics/governance_and_quality_framework/html/usage_policy.en.html) autorise la réutilisation gratuite des statistiques publiques sous conditions d'attribution et de préservation des statistiques et métadonnées. Le brut est conservé intact ; les comptes et commentaires sont des analyses distinctes, attribuables à cette recherche. Toute transformation future devra être identifiée comme calcul de l'auteur à partir des statistiques BCE, sans être présentée comme une publication de la BCE. La politique prévoit des révisions et ne garantit pas la continuité de toutes les séries.
