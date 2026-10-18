# Faisabilité des données, du calcul et d'une trajectoire opérationnelle LCM

Note de recherche — 13 octobre 2026. Travail documentaire uniquement : aucun modèle entraîné, aucune collecte payante lancée, aucune infrastructure créée, aucun ordre envoyé.

## 1. Conclusion et périmètre

Construire un modèle autoregressif de trajectoires de marché est techniquement faisable. Démontrer qu'il possède une information prédictive exploitable après coûts reste une expérience à mener. La profondeur de l'historique, la qualité temporelle des données et la méthode de validation sont probablement des facteurs plus limitants que la possibilité de louer un GPU.

Le projet Hyperliquid et son serveur OVH constituent un terrain d'application et un point de départ. Ils ne bornent pas la recherche : le corpus peut être multi-actifs, multi-places et multi-fréquences, et l'entraînement comme l'inférence peuvent migrer vers une infrastructure adaptée. Deux trajectoires sont proposées : une preuve de concept sobre pour falsifier rapidement les mauvaises hypothèses, puis un programme de modèle de fondation si les premiers résultats justifient son coût.

L'objectif initial doit distinguer trois preuves : apprendre une distribution des futurs plausible ; améliorer la prévision hors échantillon par rapport à des références ; créer une décision économiquement utile. La première ne démontre pas les deux autres. Un résultat négatif sur le trading directionnel pourrait conduire à un résultat utile sur les probabilités de forte volatilité, la sélection des moments où s'abstenir ou la mesure de risques, sans prétendre que ce pivot prouve l'hypothèse initiale.

## 2. État du terrain Hyperliquid : faits vérifiés

### OHLCV, profondeur temporelle et métadonnées

L'API `candleSnapshot` ne donne accès qu'aux **5 000 bougies les plus récentes**. Ce n'est pas simplement une taille maximale de réponse contournable en paginant vers un passé illimité. Les intervalles comprennent 1m, 5m et 1h. La réponse fournit ouverture, haut, bas, clôture, volume, nombre de trades et bornes temporelles. L'endpoint REST `l2Book` retourne au plus 20 niveaux par côté. `userFees` permet de consulter les frais associés à une adresse. Les identifiants spot, perps et HIP-3 diffèrent ; les noms affichés dans une interface peuvent être remappés. [Documentation officielle de l'endpoint Info](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint).

Calculs de portée théorique de 5 000 bougies, hors âge de cotation, trous ou interruption :

| Intervalle | Calcul | Profondeur maximale correspondante |
|---|---:|---:|
| 1 minute | 5 000 / 1 440 | 3,47 jours |
| 5 minutes | 25 000 / 1 440 | 17,36 jours |
| 1 heure | 5 000 / 24 | 208,33 jours |

`meta` expose notamment l'univers et les contraintes de contrats ; `metaAndAssetCtxs` expose le financement courant, l'intérêt ouvert, le mark, l'oracle et d'autres contextes. `fundingHistory` fournit des taux historiques horodatés. La documentation ne transforme pas ces contextes courants en un historique exhaustif de tous les champs. L'exemple de métadonnées inclut un indicateur de radiation. [API officielle Perpetuals](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals).

**Conséquence de conception.** Constituer un registre des instruments valable à chaque date : place, marché, identifiant, sous-jacent, collatéral, précision, changements de règles, dates de présence et provenance. Ne pas reconstruire l'univers d'hier à partir des seuls actifs disponibles aujourd'hui. Une réponse `metaAndAssetCtxs` obtenue aujourd'hui ne peut pas remplir les caractéristiques d'un exemple ancien. Les jointures doivent utiliser la dernière information effectivement disponible avant la décision.

### Archives officielles : ce qui existe, et ce qui reste à vérifier

La documentation annonce des snapshots L2 dans `hyperliquid-archive/market_data` et des contextes dans `asset_ctxs`, avec mise à jour approximativement mensuelle, sans garantie de ponctualité ni de complétude. Elle ne fournit pas dans ce bucket de bougies ni de données spot. Le demandeur paie les transferts. Un autre bucket, `hl-mainnet-node-data`, contient notamment `node_fills_by_block`, des formats anciens distincts de fills/trades, des blocs/transactions, et `misc_events_by_block` pour des événements dont le financement. [Historique officiel Hyperliquid](https://hyperliquid.gitbook.io/hyperliquid-docs/historical-data).

**Conséquence de conception.** La reconstruction d'OHLCV depuis les transactions est une piste concrète, pas une preuve que le corpus est déjà disponible, complet ou gratuit. Avant de budgéter un préentraînement, réaliser ultérieurement un inventaire des objets et un échantillonnage de couverture : dates réellement présentes, actifs, taille transférée, formats, trous, doublons, règles de comptage des fills et cohérence contre une fenêtre récente de référence. Une transaction économique peut apparaître dans des enregistrements correspondant aux deux côtés ; agréger sans contrôle peut doubler le volume. Ne pas assimiler les PnL d'utilisateurs à des prix de marché, ni supposer identiques les formats anciens et récents.

### Snapshots du carnet et livre reconstructible : distinction essentielle

Le flux WebSocket `l2Book` est décrit comme un flux de snapshots ; le mode rapide expose 5 niveaux et le mode lent 20. `trades` expose les transactions ; la documentation conseille la clé composée `(block_time, coin, tid)` pour une identité globale de transaction. Les mises à jour BBO sont liées aux changements du meilleur bid/ask. [Abonnements WebSocket officiels](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket/subscriptions).

Un snapshot décrit l'état visible à un instant. Deux snapshots ne révèlent pas toutes les créations, annulations et exécutions survenues entre eux. Ils ne donnent donc pas, à eux seuls, la position exacte d'un ordre dans une file, ni la certitude d'une exécution maker. Le modèle peut apprendre sur ces observations, mais le simulateur doit conserver cette limite.

La documentation du nœud décrit un snapshot L4 issu d'un état ABCI, puis l'application du flux des statuts d'ordres pour maintenir un livre complet. Elle avertit également d'un ordre de grandeur d'environ 100 Go de logs quotidiens avec les réglages par défaut ; ce chiffre n'est pas une mesure de notre collecte ni une garantie de charge future. [Schémas L1 officiels](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/nodes/l1-data-schemas).

Le logiciel officiel de nœud expose notamment les sorties `--write-order-statuses`, `--write-raw-book-diffs`, `--write-fills` et une option de regroupement par bloc avec métadonnées temporelles. [Dépôt officiel hyperliquid-dex/node](https://github.com/hyperliquid-dex/node).

Une collecte prospective reconstructible nécessite donc un état initial compatible, les événements nécessaires dans leur ordre exact, l'identification des blocs, la détection des pertes, des points de contrôle et une procédure de resynchronisation. La présence d'archives de snapshots ou de transactions ne prouve pas que ces conditions sont réunies pour tout le passé. Sans cela, limiter les revendications aux quantités réellement observables : spread, profondeur aux niveaux capturés, déséquilibre et transactions disponibles. Le terme « carnet complet reconstruit » est une conclusion à valider, pas un nom de fichier.

### Limites et maintien d'une collecte

Les limites publiées comprennent un poids REST agrégé de 1 200 par minute par IP, des poids propres aux requêtes et aux quantités retournées, 10 connexions WebSocket et 1 000 abonnements. Les limites par adresse concernent les actions, pas les requêtes `info`. [Limites officielles](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits). Le serveur peut fermer une connexion sans message émis vers elle depuis 60 secondes ; le protocole prévoit ping/pong. [Timeouts et heartbeats](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket/timeouts-and-heartbeats).

La conception future doit prévoir un régulateur de débit partagé, des reprises progressives, des compteurs de trous et d'âge des données, et une séparation des budgets de recherche et d'exploitation. Une connexion active n'est pas une preuve de complétude du flux. Les données manquantes ne doivent pas être transformées silencieusement en absence de transaction.

### HIP-3 et HIP-4 : extension du corpus, avec sémantique explicite

HIP-3 délègue au créateur de marché des aspects tels que l'oracle, les spécifications, certains paramètres et l'arrêt/règlement d'un actif. Une même étiquette peut être réutilisée après règlement : un historique doit distinguer les épisodes économiques. [HIP-3 officiel](https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-3-builder-deployed-perpetuals).

HIP-4 désigne des contrats entièrement collatéralisés, à règlement borné et daté ; leur comportement ne correspond pas à celui d'un perpétuel crypto ordinaire. [HIP-4 officiel](https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-4-outcome-markets).

Recommandation de recherche : les exclure du premier corpus homogène, puis les ajouter comme domaines identifiés si l'hypothèse de transfert le justifie. « Plus d'instruments » ne signifie pas automatiquement « plus d'exemples interchangeables ». À une phase ultérieure, des horloges de séance, échéances, oracles et règles de collatéral deviennent des variables indispensables.

## 3. Choisir la fréquence par l'hypothèse, pas par le nombre de lignes

| Représentation | Intérêt scientifique | Limite principale | Expérience adaptée |
|---|---|---|---|
| H1 | Régimes, contexte de plusieurs jours, faible coût d'inférence | Peu d'observations uniques ; perte de la trajectoire intrahoraire | POC de distributions de rendements et volatilité à 1/4/24 h |
| 5 minutes | Compromis entre dynamique intrajournalière et taille du corpus | Frictions plus importantes relativement au signal ; dépendance des exemples | Extension multihorizon, à comparer à H1 sur mêmes périodes |
| 1 minute | Structure fine, plus de transitions observées | 5 000 bougies couvrent très peu de temps ; dépendance et bruit élevés | Corpus reconstruit ou acquis, objectifs sensibles à l'exécution |
| Transactions / événements de carnet | Intensité, flux, temps entre événements, dynamique de liquidité | Collecte et replay coûteux ; continuité et simulation de file difficiles | Programme microstructure distinct, après preuve de qualité des données |
| Hiérarchie H1 + 5m + événements | Séparer contexte lent et dynamique rapide | Plus de paramètres, jointures temporelles complexes | Architecture ambitieuse testée par ablations |

H1 reste un point de départ possible parce qu'il correspond au terrain déjà observé, et non parce qu'il serait universellement optimal. L'horizon de prédiction doit être choisi avant l'expérience économique. Une précision supérieure à une minute peut être inutilisable si l'exécution et la rotation absorbent l'espérance de gain. Inversement, les modèles d'événements peuvent viser le spread, le risque de mauvais remplissage ou la volatilité plutôt que la direction.

## 4. Dimensionnement du corpus : unités et dépendances

Calculs théoriques pour des marchés ouverts 24 h/24, une année de 365 jours, sans trous. Une « ligne » est ici une bougie d'un actif, pas un événement indépendant. Les années bissextiles, lancements et radiations sont volontairement ignorés dans ces scénarios.

| Fréquence | Bougies / actif / an | 10 actifs × 3 ans | Stockage numérique à 80 octets / ligne |
|---|---:|---:|---:|
| H1 | 8 760 | 262 800 | 21,0 Mo |
| 5m | 105 120 | 3 153 600 | 252,3 Mo |
| 1m | 525 600 | 15 768 000 | 1,26 Go |

Les 80 octets représentent une hypothèse de représentation compacte, pas une mesure des fichiers du projet. Ajouter 32 caractéristiques float32 ajoute 128 octets par ligne : environ 33,6 Mo, 403,7 Mo et 2,02 Go respectivement. À cela s'ajoutent l'historique brut, les métadonnées, les index, contrôles qualité, versions de jeux de données et checkpoints. CSV, JSON et objets Python peuvent occuper bien davantage ; un fichier columnar compressé peut occuper moins. Le stockage réel se mesure sur un échantillon, et le cache de travail n'est pas égal à la taille compressée.

Pour une cible ambitieuse, 1 000 séries × 5 années × 525 600 bougies par an représentent 2,628 milliards de bougies à la minute, avant correction de couverture. C'est un ordre de grandeur arithmétique, **pas l'affirmation que ces historiques sont accessibles ni homogènes**. À 80 octets par ligne : 210,24 Go compacts avant caractéristiques et réplicas. Des données événementielles peuvent changer cette échelle de plusieurs ordres de grandeur ; il faut les dimensionner depuis le débit observé par marché et par régime, notamment les journées de crise.

Trois comptes doivent rester séparés : nombre de bougies uniques ; nombre de tokens effectivement passés à l'entraînement ; quantité d'information indépendante. Le découpage en fenêtres se chevauchant multiplie le deuxième, sans multiplier le premier. Le regroupement en patches réduit la longueur des séquences sans créer d'information. Plusieurs places cotant BTC ajoutent un signal microstructurel possible, mais ne constituent pas autant d'histoires macroéconomiques indépendantes. Les données synthétiques sont utiles pour tester les contraintes et préentraîner certaines invariances ; elles ne prouvent pas l'existence d'un avantage de marché.

## 5. Calcul, mémoire et trois tailles possibles

Pour un modèle dense, les poids bf16 occupent approximativement 2 octets par paramètre. À l'entraînement, poids, gradients, états d'optimiseur, activations et buffers s'ajoutent. Une configuration classique de précision mixte et Adam peut atteindre environ 18 octets par paramètre avant activations ; d'autres implémentations diffèrent. [Documentation Hugging Face sur la mémoire GPU](https://huggingface.co/docs/transformers/main/en/model_memory_anatomy).

Calculs dérivés, en unités décimales, avec 18 octets par paramètre pour la colonne d'entraînement :

| Paramètres | Poids seuls bf16 | États persistants d'entraînement, hors activations | Usage de recherche envisagé |
|---|---:|---:|---|
| 10 M | 20 Mo | 180 Mo | Premier modèle spécialisé |
| 30 M | 60 Mo | 540 Mo | POC plus expressif, nombreuses ablations |
| 100 M | 200 Mo | 1,8 Go | Transfert entre actifs/domaines |
| 500 M | 1 Go | 9 Go | Préentraînement ambitieux et corpus étendu |
| 1 B | 2 Go | 18 Go | Modèle de fondation à justifier empiriquement |
| 7 B | 14 Go | 126 Go | Recherche distribuée ; aucune nécessité établie ici |

Ce tableau ne permet pas de choisir une carte graphique en lisant seulement la troisième colonne. Activations, longueur de contexte, batch, vocabulaire, stratégie d'attention et temporaires peuvent dominer. Une première enveloppe à tester serait une carte de 16–24 Go pour 10–30 M paramètres ; 24–80 Go pour 100–500 M selon le contexte et le batch ; puis 80 Go ou distribution pour 1 B et au-delà selon la configuration. Ce sont des **hypothèses de planification**, pas des garanties que tous les réglages tiennent.

L'attention dense devient coûteuse avec le carré de la longueur de séquence. Mettre chaque attribut OHLCV dans un token distinct peut multiplier cette longueur. Un vecteur de bougie projeté, un token de bougie quantifié ou des patches causaux réduisent ce coût. Une architecture hiérarchique avec contexte lent et contexte rapide séparés peut être plus utile que l'augmentation brute du nombre de paramètres.

L'approximation classique du calcul d'entraînement dense est de l'ordre de `6 × N × D` opérations, avec `N` paramètres et `D` tokens traités. Elle ne comprend pas tous les coûts d'une architecture concrète et ne convertit pas directement le calcul en durée de cloud. [Kaplan et al., Scaling Laws for Neural Language Models, section 2](https://arxiv.org/pdf/2001.08361).

Pour budgéter réellement : effectuer ultérieurement un microbenchmark complet de quelques centaines de pas sur les formes de tenseurs prévues ; mesurer tokens/seconde, mémoire au pic, temps d'entrée/sortie et overhead de checkpoint ; extrapoler à la campagne incluant réplications et ablations. Le nombre d'époques, les fenêtres répétées et les essais rejetés doivent être comptés. Les lois d'échelle du langage ne garantissent aucune loi d'échelle de la rentabilité.

### Budget de scénarios, sans devis ni dépense

Les tarifs unitaires ci-dessous sont **des hypothèses rondes**, volontairement sans fournisseur, région ou modèle GPU associé. Ils servent uniquement à montrer la multiplication et ne représentent pas un prix contractuel. La campagne comprend les essais, pas seulement le modèle gagnant.

| Scénario | Hypothèse d'heures GPU cumulées | Hypothèse €/heure GPU | Calcul seul |
|---|---:|---:|---:|
| POC 10–30 M | 30–150 h | 1 € | 30–150 € |
| Programme 100–500 M | 300–2 000 h | 3 € | 900–6 000 € |
| Programme 1 B+ | 3 000–20 000 h | 5 € | 15 000–100 000 € |

Ces enveloppes ne prédisent ni le temps nécessaire, ni les performances atteignables. Pour une exécution sur 8 GPU pendant 100 h, le compte est de 800 GPU-heures avant éventuels surcoûts de nœud. Les essais interrompus, recherches d'hyperparamètres, cinq réplications d'une comparaison, stockage, acquisition/licence de données, transferts S3, sauvegardes, CPU de préparation, inférence et temps humain s'ajoutent. Une grande partie du travail initial restera l'ingénierie et l'examen des données.

Les prix et disponibilités devront être relevés dans la région choisie juste avant toute décision ; la page française officielle sépare calcul, stockage et registre de conteneurs pour ses offres AI. [Tarifs officiels OVHcloud France](https://www.ovhcloud.com/fr/public-cloud/prices/). Un achat de matériel permanent ne se justifie pas avant d'avoir mesuré les besoins et la fréquence réelle des campagnes.

## 6. Infrastructure existante : point d'appui, pas plafond

Constat provenant de l'audit en lecture seule réalisé par l'agent principal du projet le 13 octobre 2026 à 18:05:30 UTC, soit 20:05:30 à Paris : 2 vCPU ; mémoire totale 3 819 Mio, disponible 1 610 Mio ; swap utilisée 413 Mio sur 2 047 Mio ; disque 38 Gio dont environ 27 Gio libres ; aucun accélérateur de calcul exposé dans l'inventaire inspecté. Le bot en cours utilise environ 107 Mio au moment du relevé et son groupe de ressources a une limite mémoire de 1 Gio et un quota CPU correspondant à un cœur. Il s'agit d'un état ponctuel, pas d'un benchmark ni d'une garantie de marge durable.

L'audit transmis mentionne une cadence H1, des captures contenant 169 bougies closes, 5 niveaux de carnet et des timestamps de demande/réception, ainsi qu'une cotation postérieure environ une minute après capture. Ce contenu ne représente pas 169 périodes indépendantes à chaque capture : les fenêtres successives se recouvrent. La cotation postérieure peut servir à une cible ou à mesurer l'exécution différée, jamais à une caractéristique prétendument connue à l'instant initial.

Pour le POC, ce serveur peut rester le collecteur léger ou le point de comparaison avec le bot existant. L'entraînement, les extractions volumineuses et les modèles supplémentaires doivent être conçus sur une machine distincte. Une future prédiction peut être publiée sous forme d'artefact ou de réponse de service avec date limite, version et indicateur de validité ; le bot n'a besoin de consommer qu'un contrat simple. Cette séparation évite qu'un modèle ou une recherche perturbe le processus qui gère déjà les positions.

Pour la cible ambitieuse, une architecture nouvelle peut comprendre stockage objet brut immuable, catalogue de données, calcul CPU pour normalisation, entraînement GPU éphémère, registre de modèles et service d'inférence indépendant. Une file d'événements et des nœuds spécialisés ne sont justifiés que si l'objectif nécessite réellement la microstructure. Le choix d'une pile et d'un fournisseur doit suivre les volumes mesurés et le niveau de service demandé, sans obligation de conserver OVH ni de le remplacer.

## 7. Frictions : exemple pédagogique de seuil économique

Le tarif public de base des perpétuels, niveau 0, indique 0,045 % taker et 0,015 % maker par exécution. Les taux réels dépendent du compte, des réductions et du type de marché ; certains mécanismes HIP-3 modifient les frais. [Barème officiel Hyperliquid](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees). Le financement est payé chaque heure ; la documentation calcule son paiement à partir de la taille de position, du prix oracle et du taux. [Financement officiel](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/funding).

Exemple inventé : une position de 10 000 unités de notionnel entre et sort en taker, avec notionnel supposé constant. À 4,5 points de base par côté, les frais valent environ 4,5 + 4,5 = **9 points de base aller-retour**, soit 9 unités monétaires. Supposons ensuite un coût total de spread et slippage de 3 points de base aller-retour, plus un financement net payé de 1 point de base : le seuil de friction atteint 13 points de base, soit 13 unités. Une prévision de hausse moyenne de 8 points de base resterait négative de 5 points de base avant marge d'incertitude. Ces 3 et 1 points de base sont des hypothèses, pas des observations de BTC ni une promesse de taux.

Si le rendement est calculé du mid au mid, intégrer le coût de franchissement du spread. Si les prix d'entrée/sortie simulés sont déjà bid/ask exécutables et incluent le slippage, ne pas rajouter une deuxième fois le même spread. Comptabiliser le funding aux instants et sur les expositions réellement concernés. Le « financement actuel » donné au modèle ne doit pas être remplacé rétroactivement par le taux finalement réalisé.

Un ordre maker payé moins cher peut ne pas être exécuté, être partiellement exécuté ou être exécuté précisément quand le marché évolue défavorablement. Le simple contact du plus bas/plus haut d'une bougie avec la limite ne démontre pas son exécution. Si l'on ne dispose que de bougies, les cas intrabougie où stop et objectif sont tous deux touchés doivent être traités de façon prudente et explicite, ou exclus de la comparaison d'exécution.

## 8. Trajectoire POC : isoler les inconnues dans le bon ordre

1. **Définir l'hypothèse falsifiable.** Exemple : la représentation tokenisée de bougies améliore le score probabiliste des rendements et de la volatilité futurs sur BTC H1, puis cette amélioration permet une décision après coûts. Fixer horizons, baseline principale et test final avant de regarder les résultats.
2. **Vérifier le corpus.** Dédupliquer les bougies des captures, établir la couverture réelle, horodater la disponibilité des caractéristiques, figer un dictionnaire des champs. Si H1 est retenu, comparer au moins un historique suffisant pour différents régimes ; 169 bougies dans un contexte n'équivalent pas à un corpus d'apprentissage.
3. **Séparer prévision et trading.** D'abord battre une distribution empirique/conditionnelle simple et des modèles tabulaires. Comparer une architecture continue et une architecture tokenisée à information, budget et découpage comparables. Le tokenizer doit être appris exclusivement sur la partie entraînement.
4. **Limiter le premier modèle.** 10–30 M paramètres est une expérience possible ; plus petit reste recevable. Tester le signal et les contraintes de génération avant toute course à la taille. Le terme « large » est une direction du programme, pas un critère de succès du POC.
5. **Valider chronologiquement.** Tous les actifs partagent les mêmes frontières temporelles. Purger les cibles qui traversent une frontière et garder une zone de séparation adaptée à l'horizon ; réserver une période finale intouchée. Les transformations, règles de sélection et calibrations sont ajustées sans consulter cette période.
6. **Mesurer le gain économique séparément.** Stratégie simple préenregistrée, frais propres aux marchés, spread/slippage, financement, rotation, incertitude et capacité. Publier les résultats des références, même si elles battent le modèle.
7. **Passer en observation prospective.** Prédictions enregistrées avant leurs cibles, aucune position nouvelle confiée au modèle. Mesurer fraîcheur, disponibilité, calibration, dérive et différence simulation/conditions observées. Une période prospective ne se remplace pas par plus de backtests.

Critère de réussite raisonnable du POC : un protocole reproductible et un verdict fiable sur l'hypothèse précise. Une inférence qui produit des bougies plausibles mais n'améliore pas les scores hors échantillon est une réussite de génération, pas une validation de trading.

## 9. Trajectoire ambitieuse : devenir un modèle de fondation de marché

Le passage à 100–500 M, puis à 1 B+, doit être conditionné à une courbe empirique : gain hors échantillon en fonction du nombre de paramètres, du corpus unique et du calcul, avec coût total et intervalles d'incertitude. Augmenter séparément ces axes ; si tous changent simultanément, la cause du gain devient difficile à identifier.

Le corpus étendu peut réunir plusieurs classes d'actifs et plusieurs places avec identifiants de domaine et masques de disponibilité. Prévoir une évaluation sur marchés ou actifs jamais vus, et des périodes entièrement postérieures aux données du modèle. Les jours de marché fermés, les ajustements d'actions, les changements de contrat et les historiques révisés nécessitent un traitement propre à chaque domaine. Il faut un droit d'usage permettant l'entraînement et la redistribution éventuelle ; la visibilité publique d'un graphique ne suffit pas à établir ce droit.

Une architecture candidate ambitieuse serait un backbone causal partagé, une représentation numérique des bougies, des tokens de domaine, un contexte de régime lent et une branche de microstructure lorsque les données le permettent. Les sorties restent des distributions de trajectoires cohérentes et des mesures d'incertitude. Le module de décision et de limites reste séparé, avec possibilité d'abstention. Comparer cette architecture à un préentraînement simple avant de multiplier les composants.

En exploitation, chaque prédiction doit porter version de modèle, version de représentation, horizon, temps de validité, empreinte du contexte et contrôles de qualité. Un timeout, une donnée périmée, une distribution incohérente ou une dérive détectée doit produire une abstention définie. Le déploiement par observation, simulation puis exposition limitée est une séquence de preuves ; il ne garantit pas que les performances persistent. Retour arrière, réconciliation des positions, limites d'exposition et capacité de coupure restent nécessaires même si le modèle semble bien calibré.

## 10. Doutes, blocages et éléments surprenants

| Point | État de connaissance | Moyen de le résoudre ou conséquence |
|---|---|---|
| Profondeur des bougies API | Limite officielle établie | Archives de transactions, fournisseur licencié ou collecte prospective ; pas une simple pagination |
| Complétude du passé Hyperliquid | Non établie pour le corpus ciblé | Inventaire et vérification d'échantillons avant engagement de calcul |
| Nombre de captures réellement utiles | Les fenêtres peuvent se recouvrir | Compter les timestamps uniques et périodes disjointes |
| Carnet exploitable pour une simulation maker | Snapshots insuffisants pour une file exacte | Capturer/rejouer les événements ou accepter un modèle d'exécution conservateur |
| Avantage de la tokenisation | Hypothèse | Ablation continue vs discrète, à mêmes données et budgets |
| Bénéfice de la taille | Hypothèse | Courbes d'échelle propres au corpus et au score visé |
| Préentraînement multi-place | Plus de diversité, dépendance possible | Déduplication conceptuelle, tests par place et domaine |
| Profit après coûts | Non démontré | Test net chronologique, stress et observation prospective |
| Capacité OVH historique | Suffisante pour un rôle léger, pas un entraînement ambitieux | Infrastructure distincte ou migration libre selon les besoins |
| Corpus LLM/TSFM tiers | Risque de dates inconnues et contamination | Documenter périodes d'entraînement et tester prospectivement si doute |
| Coût réel | Non mesuré | Microbenchmark et budget complet ; pas de conversion directe paramètres→prix |

Deux surprises utiles ressortent. D'une part, la quantité de bougies numériques occupe relativement peu de disque à petite ou moyenne échelle : c'est leur indépendance, leur fidélité et leur provenance qui sont rares. D'autre part, le système peut gagner surtout en apprenant **quand l'incertitude est trop élevée pour décider**, même si sa trajectoire moyenne est peu différente d'une référence naïve. Cette seconde possibilité est une hypothèse testable, pas une explication a posteriori à utiliser pour sauver tous les résultats.

Une démarche tenace consiste à continuer à tester des représentations, des horizons et des objectifs utiles tout en autorisant une conclusion négative pour une hypothèse donnée. Elle ne permet pas d'affirmer qu'un gain de trading durable existe nécessairement dans les seules courbes disponibles. Le projet restera scientifiquement solide si chaque itération réduit une incertitude mesurable et si les résultats négatifs sont conservés.
