# Sources réelles du premier POC TRAME — vérification du 14 octobre 2026

Périmètre : préparation d’un banc local de recherche personnelle hors production. Vérifications web primaires et requêtes HTTP HEAD sur des archives ; aucun nouveau téléchargement de prix, compte créé, achat, contact fournisseur ou accès au serveur. Le document 06 et le manifeste de l’illustration existante ont été repérés en lecture seule. Cette note propose les décisions de provenance ; elle n’atteste ni la continuité de l’intégralité du corpus ni une autorisation de trading réel.

## Décision proposée

Commencer par **huit paires spot Binance, bougies UTC de 1 heure, sur 2021–2022** : BTCUSDT, ETHUSDT, BNBUSDT, ADAUSDT, XRPUSDT, LTCUSDT, EOSUSDT, TRXUSDT. La même liste possède des points d’accès en janvier 2019 : une extension 2019–2020 est donc plausible et utile pour varier les régimes, après vérification de tous les mois. Ce premier corpus reste une expérience crypto sur une place et une devise de cotation communes ; il ne démontre pas encore le transfert multi-marchés.

Pour la diversité ultérieure gratuite avec des droits documentés, retenir **les taux de change de référence quotidiens BCE** comme première branche complémentaire. Ils conviennent à une série quotidienne ou à du contexte publié, pas à un remplacement des bougies horaires. Pour le FX intrajournalier, **Dukascopy** est une piste documentée de recherche personnelle à qualifier séparément. Aucune source d’actions en OHLCV horaire, gratuite, sans compte et avec tous les droits utiles établis n’est validée par cette vérification ciblée. Ce constat ne signifie pas qu’une telle source est impossible à trouver.

## Binance Vision : droits et réalité technique

Le [dépôt officiel](https://github.com/binance/binance-public-data) décrit des archives journalières et mensuelles, les champs des klines et un fichier CHECKSUM par archive. Il avertit que des archives peuvent être corrigées ultérieurement. Les timestamps spot passent en microsecondes à partir de janvier 2025 : les périodes 2019–2022 nécessitent la branche millisecondes, tout en vérifiant cette unité sur les valeurs lors de l’ingestion. Le volume spot de base et le volume en devise de cotation doivent conserver leurs noms et unités distincts.

Les [conditions datasets actuelles](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md), version 1.0, sont datées du **26 août 2026**. Elles confirment accès gratuit sous CC-BY-NC-SA-4.0 et recherche/backtest personnels hors production ; l’usage commercial et l’exécution réelle ont des restrictions spécifiques. Les données et modèles dérivés sont dans leur périmètre. La mention MIT du README concerne un autre objet que ces datasets. Décision : corpus admis pour ce POC personnel isolé, avec attribution et conditions conservées ; aucun droit de production ou de commercialisation des poids n’est présumé. Les droits lors d’acquisitions antérieures ne se déduisent pas de ce téléchargement futur.

Un contrôle **HEAD sans corps de réponse** a été exécuté sur 24 URL : huit actifs × janvier 2019, janvier 2021, décembre 2022. Les 24 ont répondu HTTP 200. Il s’agit d’une preuve de disponibilité de ces fichiers, pas d’une inspection des cours ni d’une validation des mois intermédiaires.

| Paire | Octets annoncés, 2019-01 | Octets annoncés, 2021-01 | Octets annoncés, 2022-12 |
|---|---:|---:|---:|
| BTCUSDT | 41 901 | 45 988 | 44 019 |
| ETHUSDT | 39 432 | 43 823 | 40 023 |
| BNBUSDT | 36 927 | 41 325 | 33 928 |
| ADAUSDT | 35 591 | 39 876 | 34 181 |
| XRPUSDT | 36 899 | 40 051 | 33 734 |
| LTCUSDT | 37 156 | 41 429 | 35 691 |
| EOSUSDT | 36 772 | 38 800 | 30 457 |
| TRXUSDT | 36 778 | 37 765 | 35 827 |

Patron d’URL vérifié : `https://data.binance.vision/data/spot/monthly/klines/{SYMBOL}/1h/{SYMBOL}-1h-{YYYY-MM}.zip`, accompagné de `.CHECKSUM`. Exemples : [BTC janvier 2019](https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1h/BTCUSDT-1h-2019-01.zip), [EOS décembre 2022](https://data.binance.vision/data/spot/monthly/klines/EOSUSDT/1h/EOSUSDT-1h-2022-12.zip). Ces liens sont des archives, pas des pages de documentation.

2021–2022 représente **192 archives et au maximum 140 160 créneaux horaires** sur huit actifs, avant interruptions, doublons et trous. Il s’agit d’un plafond calendaire calculé : 8 × 730 × 24. L’extension 2019–2022 représenterait 384 archives et 280 512 créneaux. Ce volume modeste est adapté à un diagnostic de tokenizer ; il ne constitue pas un corpus de modèle fondation.

La liste est fixée avant toute comparaison de performance. Elle donne accès à des historiques anciens et inclut des actifs dont la trajectoire diffère de celle de BTC ; elle reste sélectionnée rétrospectivement et ne permet pas une affirmation d’absence de biais de survivance. Ne pas la reconstruire à partir de la liste des paires actuellement négociables. Les changements de nom, migrations ou retraits ultérieurs ne doivent pas faire disparaître les instruments historiques du manifeste.

## Complément recommandé : BCE, FX quotidien réel

La [page primaire des taux](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html) donne accès aux historiques CSV/XML, sans clé de compte, et décrit une publication quotidienne autour de 16 h CET lors des jours ouvrés concernés. Les taux sont des références informatives ; ils ne sont pas des transactions exécutables. Proposition : USD, JPY, GBP, CHF, CAD et AUD contre EUR, avec date, taux, unité et état de disponibilité. Ne créer ni haut, bas, ouverture, ni volume fictifs pour les faire entrer artificiellement dans OHLCV.

La [politique de réutilisation des statistiques du SEBC](https://www.ecb.europa.eu/stats/ecb_statistics/governance_and_quality_framework/html/usage_policy.en.html) établit gratuité et réutilisation commerciale ou non commerciale, sous conditions de citation, fidélité des statistiques/métadonnées et exception pour les données de tiers. Les [conditions générales de copyright BCE](https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html) demandent aussi de signaler les transformations. Conserver les données sources intactes ; présenter les rendements et caractéristiques calculés comme nos transformations, avec attribution.

L’[API documentée](https://data.ecb.europa.eu/help/api/data) définit le flux EXR et la clé `D.USD.EUR.SP00.A`, ainsi que dates de début/fin et format CSV. Son option `detail=nodata` permet de contrôler les métadonnées sans recevoir d’observations. Exemple à préparer pour l’acquisition future : `https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?startPeriod=2021-01-01&endPeriod=2022-12-31&format=csvdata`. Cette requête de valeurs n’a pas été exécutée dans cette note.

L’intégration dans une séquence horaire doit utiliser seulement le dernier taux déjà publié, avec âge de l’information et masque de modalité. Reproduire la valeur du jour dès 00 h serait une fuite temporelle. En l’absence d’archive de l’heure historique exacte, déclarer l’hypothèse et adopter un décalage conservateur, ou garder la série dans une branche quotidienne indépendante.

## Alternatives examinées, sans les déclarer acquises

| Source | Ce que la source primaire établit | Décision pour la suite |
|---|---|---|
| [Dukascopy Historical Data Export](https://www.dukascopy.com/swiss/english/marketwatch/historical/) | Export gratuit de prix dans plusieurs temporalités et usage pour des modèles prédictifs décrits. Les [conditions du site](https://www.dukascopy.com/swiss/english/legal-pages/terms-of-use/) limitent le téléchargement à l’usage personnel non commercial. | Candidat pour un second petit corpus FX. Le parcours réel d’export sans compte, la profondeur 2021–2022 et les conditions de chaque flux restent à tester ; ne pas les déduire d’un client GitHub tiers. |
| [FAQ Dukascopy](https://www.dukascopy.com/swiss/english/about/faq/?toEng=1) | Le volume de bougie résulte de l’agrégation de volumes des meilleurs bid ou ask ; l’historique complet L2 n’est pas conservé selon cette FAQ. | Ne pas traiter ce volume comme un volume de transactions comparable au spot Binance. Prévoir une sémantique de volume séparée. |
| [HistData FAQ](https://www.histdata.com/f-a-q/) | CSV, champs OHLC et timestamps en EST fixe sans ajustement saisonnier. | Piste technique utile ; provenance fine et droits d’exploitation/diffusion des dérivés insuffisamment établis dans les pages consultées. Non sélectionné automatiquement. |
| [Stooq, téléchargements](https://stooq.com/db/h/) | La page primaire a renvoyé une vérification JavaScript ; son texte de conditions n’a pas pu être inspecté dans cette passe. | Aucun statut de licence affirmé. Ni un article secondaire ni la licence d’une bibliothèque de téléchargement ne peuvent combler cette preuve manquante. |

## Relecture du document 06 : corrections et distinctions utiles

Les assertions du document 06 sur Binance, ses conditions, les unités de timestamps et les contrôles d’archives concordent avec les sources reconsultées. Ne pas remplacer « archives disponibles » par « corpus complet contrôlé ». Son exemple BTC mars 2020, déjà acquis dans une étape antérieure, mentionne une heure absente ; c’est un contre-exemple concret à une hypothèse de grille toujours complète.

La partie 06 décrit correctement un état documentaire antérieur sans entraînement. Lorsque le POC démarre, conserver cet historique daté et ajouter un état nouveau au lieu de laisser croire que les phrases « aucun entraînement lancé » décrivent éternellement tout le projet. De même, distinguer 192 archives prévues, 24 entêtes contrôlés ici et le seul exemple de prix déjà présent avant cette sous-tâche.

Aucun fichier séparé nommé « sourcehypothes » n’a été retrouvé par la recherche de noms ; les hypothèses de sources sont donc consignées ici explicitement : disponibilité des mois non sondés, continuité horaire, heure de publication historique, droits selon l’usage et distinction des unités de volume. Toutes devront passer de « hypothèse » à « mesure » ou « décision documentée » au moment de l’ingestion.

Le manifeste du POC doit au minimum conserver : URL exacte, acquisition UTC, SHA-256 du ZIP et CHECKSUM correspondant, instrument historique, marché spot, granularité, unités, premier/dernier instant, nombre de lignes, doublons/trous, référence datée des conditions, transformations et rôle train/validation/test. Le codebook, les normalisations et les seuils se fixent sur l’entraînement ; aucune statistique du test n’est nécessaire pour choisir ces paramètres.
