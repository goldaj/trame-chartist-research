# TRAME : corpus réel, langage typé et protocole de prévision

Complément scientifique 2.1, 15 octobre 2026. Ce document précise et, sur les points indiqués, amende les documents 02 à 08. Il distingue acquisition réalisée, résultat mathématique et expérience proposée. Aucun réseau prédictif n'a été développé ou entraîné.

## À lire d'abord : ce qui change

**Le langage doit décrire comment un prix a été observé, en plus de sa forme.** Une moyenne mensuelle, une clôture, un fixing et une transaction ne sont pas interchangeables. Nous proposons d'ajouter au langage des types d'observation, des unités, des périodes et des instants de disponibilité. Les actifs peuvent partager une grammaire tout en gardant ces différences de sens.

Un nouveau fichier réel a été acquis auprès de la Banque mondiale. Six séries - or, argent, cuivre, Brent, maïs et blé - contiennent chacune 732 valeurs mensuelles entre janvier 1960 et décembre 2020. Cela apporte des périodes historiques très différentes. Cela ne fournit pas leurs trajectoires à la seconde. La définition de l'or change en juin 2025 dans la description du fichier : un symbole constant n'implique pas un instrument de mesure constant.

**Une régularité peut venir de la mesure.** Le moyennage d'un prix dont les variations sont indépendantes peut produire des variations de moyennes autocorrélées. Ce phénomène classique oblige à comparer un futur modèle à un témoin qui connaît le mode d'observation. Une bonne prévision des moyennes demeure utile scientifiquement, mais ne suffit pas à démontrer une prédictibilité nouvelle du prix instantané.

Pour transformer les courbes en langage, nous précisons un vocabulaire à précision progressive : partie entière, détails successifs, puis éventuellement résidu. Le même prix peut être lu grossièrement ou finement. Une voie spéciale doit conserver les grandes amplitudes. Cette construction est une proposition à tester ; la hiérarchie grossier/fin existe déjà dans des travaux comme Kronos.

Le prochain protocole sépare trois questions : quelle représentation aide le modèle, ce qu'apporte le partage entre actifs, et ce qu'apporte l'observation des autres actifs. Le prix cible, les dates et les informations disponibles restent identiques dans chaque comparaison. Le GPT reste central. Les petites expériences servent à comprendre les conditions de réussite et d'échec, sans condamner une famille entière.

La limite actuelle est précise : nous avons des données réelles et un plan d'expérience plus discriminant, mais aucun résultat de prévision. La constitution d'un corpus de transactions et cotations multi-marchés à haute fréquence reste à réaliser.

<!-- pagebreak -->

## 1. Une observation n'est pas seulement un nombre

Notons `P_a(s)` une trajectoire conceptuelle associée à l'instrument a. Une observation s'écrit `Y_j = O_j[P_a] + e_j`, où `O_j` désigne son opérateur de mesure. Cette écriture est un modèle conceptuel : un prix efficient unique sous-jacent n'est pas supposé directement accessible, et les différentes places peuvent porter des prix distincts.

Un opérateur peut être la dernière transaction admissible avant une heure, un milieu de fourchette à un instant, un fixing, une moyenne de fixings, le maximum des transactions d'une période ou une formule d'indice. Les modalités de sélection des transactions, les corrections et les conventions de calendrier font partie de cet opérateur. Elles peuvent évoluer.

Le dossier v2 représentait déjà les temps de disponibilité et les valeurs manquantes. L'amendement est d'en faire une **syntaxe obligatoire de la langue**, avec un rôle expérimental mesurable, plutôt qu'un simple nettoyage préalable.

| Champ du contrat d'observation | Rôle scientifique |
|---|---|
| instrument, place, contrat, échéance | Désigner ce qui est observé ; identifier les changements de contrat |
| unité, devise de cotation, tick | Permettre le décodage physique ; distinguer échelle et précision |
| opérateur et version | Séparer moyenne, fixing, transaction, clôture, règlement et indice |
| début et fin de support temporel | Dire quelle période contribue au nombre |
| horodatage de l'événement et de disponibilité | Exclure une valeur publiée après l'origine de prévision |
| source, version reçue, correction | Distinguer un historique révisé des observations disponibles à l'époque |
| état de présence et âge | Distinguer observation nouvelle, valeur ancienne, absence de transaction, fermeture et lacune inconnue |
| relations structurelles | Signaler les composites, contrats successifs, composantes d'indice et changements de numéraire |

Les champs constants peuvent être encodés une fois par séquence, puis modifiés seulement lorsqu'ils changent. Ils ne justifient pas une répétition coûteuse de longs identifiants sur chaque seconde. Une version inconnue est un état explicite ; elle n'est pas devinée à partir d'un résultat futur.

Deux courbes du même actif, issues de fixings et de transactions, peuvent être deux observations différentes d'un phénomène lié. Deux actifs distincts libellés en dollars peuvent partager une fluctuation du numéraire. Le « Marché unique » doit donc être étudié avec des variables communes, des variables propres et des opérateurs de mesure. Une représentation latente qui ignore le dernier terme peut confondre convention de publication et mécanisme économique.

## 2. Nouvelle acquisition réelle : ce que le fichier prouve

Le classeur mensuel a été téléchargé depuis le [site officiel de la Banque mondiale](https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/world-bank-commodities-price-data-the-pink-sheet) le 15 octobre 2026 à 07:09:25 UTC. Taille : 586 099 octets. La mise à jour indiquée est le 2 octobre 2026. Le manifeste conserve l'URL, les en-têtes et l'empreinte SHA-256 :

`ea1c350827878ea3bbe30e3cda16a13fd3bd5b409b8458940dc94a36b5a33154`

L'audit en lecture seule porte sur les cellules sources. La feuille Monthly Prices comporte 801 mois consécutifs, de janvier 1960 à septembre 2026, et 71 colonnes de séries nommées. Elle contient 50 451 valeurs numériques, 6 416 absences et quatre erreurs Excel. Ces nombres sont des mesures de ce fichier, pas une déclaration générale de qualité de la source.

| Série sélectionnée | Unité du fichier | Valeurs 1960-2020 | Plage source |
|---|---|---:|---|
| Gold | USD / once troy | 732 | BR7:BR738 |
| Silver | USD / once troy | 732 | BT7:BT738 |
| Copper | USD / tonne métrique | 732 | BM7:BM738 |
| Crude oil, Brent | USD / baril | 732 | C7:C738 |
| Maize | USD / tonne métrique | 732 | AE7:AE738 |
| Wheat, US HRW | USD / tonne métrique | 732 | AL7:AL738 |

Ces 4 392 cellules sont numériques, positives et sans absence. Nous les avons choisies pour leur diversité économique et leur profondeur, sans chercher un résultat prédictif favorable. La présence d'une valeur sous un nom actuel en 1960 ne certifie pas que l'instrument actuel existait alors sous cette définition. Les prolongements historiques et les changements de fournisseur restent à qualifier avant une interprétation causale des ruptures.

Les erreurs `#VALUE!` concernent Rice, Thai 25%, en août 1988, juin 1989, juin 1990 et février 2008, aux cellules AH350, AH360, AH372 et AH584. Elles sont conservées comme erreurs. Les absences sont 6 332 ellipses Unicode et 84 séquences de trois points. Le premier passage du parseur s'est arrêté ; après inspection des caractères et des types Excel, les marqueurs d'absence ont été explicités. Aucun nombre n'a été inventé. La feuille Mismatch Details comporte 152 lignes de comparaison interne : elle n'a pas été interprétée comme une instruction de corriger les observations.

La cellule Description!B103 décrit pour l'or une moyenne de cours spot à partir de juin 2025, précédée d'une moyenne des fixings de l'après-midi de Londres. Ce changement rend nécessaire un indicateur de définition. Il ne démontre ni rupture économique ni erreur de prix. Le [bulletin d'octobre 2026](https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Pink-Sheet-October-2026.pdf) décrit aussi des révisions et remplacements de séries : un historique reçu aujourd'hui n'est pas une archive de chaque publication d'origine.

Le [catalogue Banque mondiale](https://datacatalog.worldbank.org/search/dataset/0038238/commodity-prices-history-and-projections) déclare cet ensemble public sous CC BY 4.0 et une mise à jour des prix le deuxième jour ouvré du mois. Ce calendrier général ne fournit pas les heures de disponibilité de chaque observation historique. Le catalogue contient aussi des projections : elles ne doivent jamais devenir des prix observés. Ici seule la feuille historique mensuelle a été auditée.

Le classeur entier a été reçu et sa couverture examinée. Il est exploratoire. Aucune partie ne sera présentée comme un test final jamais inspecté. Les 732 mois par série jusqu'à 2020 représentent 732 dates communes, et non 4 392 épisodes macroéconomiques indépendants.

## 3. Matrice des sources et des questions admissibles

| Source et cible concrète | Profondeur et résolution qualifiées | Usage possible et limite |
|---|---|---|
| Banque mondiale : six matières premières ci-dessus | Fichier réel 1960-2026 ; sélection documentaire 1960-2020 mensuelle | Histoire longue et conventions ; pas de chemin intrajournalier ni de volume |
| BCE : USD, JPY, GBP, CHF, CAD, AUD contre EUR | Acquisition antérieure 1999-2020, quotidienne | 33 792 valeurs de référence ; numéraire partagé ; disponibilité historique à qualifier |
| FRED : série SP500 | Catalogue : clôture quotidienne, dix années glissantes | Source récente de niveau d'indice ; ne couvre pas 2000/2008 aujourd'hui ; pas acquise ici |
| NYSE Daily TAQ : actions et fonds cotés américains admissibles | Catalogue depuis 1993 ; transactions et cotations | Peut couvrir 2000/2008 ; accès sous licence, échantillon et conventions non audités ici |
| Databento GLBX.MDP3 : contrats GC et ES à identifier | Catalogue futures depuis juin 2010 ; schémas transactions/cotations et OHLCV 1 s | Candidats or et indice à haute fréquence ; ne couvre pas 2000/2008 dans ce catalogue ; pas acquis |

Les trois dernières lignes sont des qualifications documentaires, pas des fichiers déjà disponibles pour entraîner TRAME. Aucun achat ni compte n'a été engagé. Le prix d'un futur GC est une cible différente d'un fixing de l'or. ES est un contrat à terme lié au S&P 500 ; il n'est ni l'indice lui-même ni une série de ses actions. « S&P 500 » est ici une hypothèse de lecture du « SP550 » cité par le porteur.

La [fiche FRED SP500](https://fred.stlouisfed.org/series/SP500) précise la clôture quotidienne, l'absence de dividendes dans cet indice de prix et la fenêtre de dix ans ; elle impose aussi des restrictions de reproduction. Une vue publique n'établit pas le droit de redistribuer un corpus. La [fiche NYSE Daily TAQ](https://www.nyse.com/data-products/catalog/daily-taq) donne 1993 comme début d'historique. Le [manuel v4.3](https://www.nyse.com/publicdocs/nyse/data/Daily_TAQ_Client_Spec_v4.3.pdf), section 1.5.5, précise que les horodatages historiques ont évolué de la seconde vers la milliseconde, puis la microseconde et la nanoseconde. Il serait faux de supposer une précision homogène sur trente ans.

Le [catalogue Databento](https://databento.com/docs/venues-and-datasets) annonce la couverture futures CME à partir de juin 2010. La [définition OHLCV](https://databento.com/docs/schemas-and-data-formats/ohlcv) précise des intervalles de 1 seconde à 1 jour, des barres horodatées au début, l'absence de ligne lorsqu'il n'y a pas de transaction et une journée UTC. La construction utilise les temps de réception des transactions ; le règlement officiel est un objet distinct. Ces conventions devront être enregistrées, pas seulement déduites du suffixe « 1s ».

La [documentation des contrats continus](https://databento.com/docs/examples/symbology/continuous) conserve les prix non ajustés des contrats successifs. Un saut au changement de contrat n'est donc pas automatiquement un mouvement du même actif. Notre cible proposée reste le contrat explicitement identifié, avec des horizons qui ne franchissent pas son changement d'identité ; l'étude des raccordements sera une expérience distincte.

Les familles d'actions devront inclure des titres sortis de cote et des identités historiques, selon une règle d'univers définie au moment considéré. Choisir aujourd'hui les seules grandes valeurs survivantes sélectionnerait le passé avec une information future. Les composites ne seront pas répartis au hasard entre apprentissage et test si leurs composantes y dévoilent déjà presque la même cible.

## 4. Un contre-exemple analytique à intégrer au raisonnement

L'effet de l'agrégation temporelle est connu depuis Working (1960) ; [Crawley (2019)](https://www.federalreserve.gov/econres/feds/in-search-of-lost-time-aggregation.htm) en expose à nouveau les conséquences. Le rapprochement avec notre corpus est essentiel : une régularité de la série mesurée peut venir de la méthode de mesure. Il ne s'agit pas d'une découverte empirique de TRAME.

Voici une dérivation autonome pour clarifier la cible. Supposons, à titre de contre-exemple mathématique et non comme description de l'or, `P(s) = P(0) + sigma W(s)` avec W brownien standard. Pour des périodes de durée Delta, définissons `A_k = (1/Delta) intégrale P(s) ds` sur la période k, et `D_k = A_k - A_(k-1)`.

Par échange des intégrales, D_k reçoit deux contributions d'incréments indépendants : ceux de la période précédente avec un poids croissant de 0 à 1 et ceux de la période courante avec un poids décroissant de 1 à 0. On obtient :

`Var(D_k) = sigma² Delta (1/3 + 1/3) = 2 sigma² Delta / 3`.

`Cov(D_k, D_(k+1)) = sigma² Delta intégrale_0^1 u(1-u) du = sigma² Delta / 6`.

Donc `Corr(D_k, D_(k+1)) = 1/4`. Les variations entre deux prix de fin de période demeurent indépendantes dans ce contre-exemple. Comme les D sont gaussiens, la prévision utilisant seulement D_k satisfait `E[D_(k+1) | D_k] = D_k/4`. Ce n'est pas la formule du meilleur prédicteur utilisant tout le passé.

On peut ainsi prévoir une partie de la prochaine variation de moyenne sans avoir découvert de dépendance entre les prochains incréments instantanés. Ce résultat analytique n'est ni une simulation ajoutée au corpus ni une mesure sur les données Banque mondiale. La valeur 1/4 dépend des hypothèses ; elle ne sera pas imposée aux vraies données comme une constante universelle.

Conséquence expérimentale : chaque résultat sera attribué à son objet. Prévoir une moyenne mensuelle et prévoir une clôture mensuelle sont deux tâches. Un témoin avec le bon opérateur d'observation devra accompagner les témoins de persistance et de dynamique simple. Un gain résiduel ne prouve pas immédiatement un motif économique inconnu ; il peut aussi refléter un témoin encore mal spécifié.

## 5. Une grammaire progressive, décodable et conditionnelle

### 5.1 Alphabet commun et information auxiliaire

L'objet de départ X est un passé réellement observable. Le code est `Z = f(X, S)` ; S contient les informations communes nécessaires au décodage : ancre, échelle passée, unité, temps et métadonnées autorisées. Ces informations ne sont ni gratuites ni optionnelles dans une comparaison. L'hypothèse de recherche est qu'une représentation peut rendre un même contenu plus facile à apprendre sous calcul limité, pas qu'un changement de notation crée de l'information.

Pour une même cible future Y et une même mesure de densité, l'identité du document 01 devient :

`E[-log q(Y | Z,S)] = H(Y | X,S) + I(Y;X | Z,S)`

`                     + E_(Z,S) KL[p(Y | Z,S) || q(Y | Z,S)]`.

Cette écriture suppose Z déterministe et les quantités définies. Le deuxième terme mesure l'information prédictive perdue dans le code. Le troisième inclut l'écart du modèle et de son apprentissage. Une reconstruction presque parfaite de X ne garantit pas une petite erreur d'apprentissage. À l'inverse, jeter des détails peut aider un modèle fini en régularisant, sans améliorer l'information théorique disponible.

### 5.2 Construction pédagogique à niveaux emboîtés

Pour un nombre x normalisé causalement, posons `q0 = floor(x)` et `r0 = x - q0`. Pour j de 1 à J : `b_j = floor(2 r_(j-1))`, puis `r_j = 2 r_(j-1) - b_j`. Les détails b_j sont binaires. L'intervalle décodé a pour borne basse `q0 + somme_j b_j 2^(-j)` et pour largeur `2^(-J)`. Son milieu reconstruit x avec une erreur au plus `2^(-J-1)`.

Exemple purement pédagogique : x = 2,70 donne q0 = 2 puis les quatre bits 1, 0, 1, 1. Le milieu de l'intervalle est 2,71875. Si le prix physique est `P = 100 + 10 x`, la valeur est 127 et la reconstruction 127,1875, avec une borne d'erreur de 0,3125. Ces valeurs sont inventées pour expliquer le code ; elles ne sont pas des observations de marché.

La partie entière ne doit pas être écrêtée silencieusement à un vocabulaire fini. Un code entier de longueur variable ou un symbole ESC suivi d'une amplitude conserve les grandes valeurs. Pour x négatif, la même définition par floor reste valide ; le code entier doit porter son signe. Pour les géométries OHLC du document 02, les amplitudes de mèches doivent rester non négatives au décodage. Pour les prix nuls ou négatifs, la transformation affine ou asinh remplace le logarithme.

Cette construction ne définit pas encore le meilleur tokenizer. C'est un témoin interprétable à comparer aux cellules fixes, aux vocabulaires appris et aux entrées continues. Les échelles passées sont strictement causales ; leur précision et leur transmission sont comptées. Le nombre J devient une variable contrôlée. Si l'on choisit J après avoir vu l'amplitude d'une observation passée, sa longueur fait elle-même partie de l'information transmise. Pour une observation future, on ne peut pas choisir J avec sa vraie valeur avant de la prédire.

### 5.3 Prédire les mots et prédire le prix

Deux expériences complémentaires sont nécessaires. Dans P1-A, les différentes langues décrivent seulement le passé, puis le même type de tête continue prédit le même prix physique. On isole mieux l'effet de la représentation d'entrée. Dans P1-B, le GPT prédit réellement les composantes du prochain code, puis ses raffinements et éventuellement un résidu : on teste la factorisation générative complète recherchée par le projet.

La loi P1-B se factorise par exemple en `p(q0_future | passé) × produit_j p(b_j_future | passé, q0_future, b_<j_future)`. Pendant la génération, les composantes déjà produites peuvent conditionner les suivantes ; leurs vraies valeurs futures ne sont pas fournies. Un entraînement avec conditionnement sur les composantes cibles précédentes peut représenter une factorisation valide de vraisemblance, mais son évaluation doit ensuite reproduire la génération réelle.

Une distribution de tokens ne donne pas automatiquement une densité de prix comparable. Il faut expliciter la loi à l'intérieur de chaque cellule, les queues, les résidus et le changement d'unité. Une perplexité inférieure avec moins de détails peut simplement récompenser une cible plus facile. Le jugement final porte sur la même variable physique. Les bornes de reconstruction présentées plus haut ne sont jamais des bornes d'erreur de prévision.

L'antériorité est explicite : [Kronos](https://arxiv.org/html/2508.02739v1) utilise déjà une hiérarchie de sous-tokens grossiers et fins pour des données financières et un modèle autorégressif. Le caractère à étudier ici est la combinaison d'une sémantique d'observation explicite, d'une précision contrôlée, de résidus et de comparaisons à information commune. La nouveauté scientifique de cette combinaison n'est pas établie par notre recherche actuelle.

### 5.4 Mesurer le coût sans confondre les unités

Un rapport devra distinguer bits sérialisés, tokens présentés au GPT, nombre de prix observés, durée historique couverte, paramètres et opérations. Un champ float32 n'est pas un nombre réel de précision infinie. Plusieurs détails binaires peuvent être regroupés en un token ; un token rare à grande amplitude peut au contraire demander plusieurs mots. Les identités et ancres constantes s'amortissent sur la séquence, mais leur coût ne disparaît pas.

On ne peut généralement égaliser tous les axes à la fois. Deux fronts de comparaison sont proposés : même contenu observable et même capacité approximative ; puis même budget de calcul pour une tâche physique donnée. Un budget de tokens identique qui raccourcit fortement le passé pour une langue ne permet pas d'attribuer le résultat au seul vocabulaire. Le rapport exposera ces deux compromis plutôt qu'un classement unique.

## 6. Protocole P1 proposé, non gelé et non exécuté

### 6.1 Trois tâches séparées

**P1-M :** prévoir la prochaine moyenne mensuelle publiée, puis les horizons 3 et 12 mois, en unités natives. Les séries Banque mondiale servent à concevoir ce protocole, avec des versions disponibles à la date d'origine si elles sont retrouvées. Sans ces versions, l'expérience sera désignée « rétrospective sur historique révisé », et sa portée sera limitée en conséquence. Une hypothèse de délai de publication ne corrige pas les révisions futures du passé.

**P1-D :** prévoir la prochaine référence quotidienne BCE, puis 5 et 20 publications. Un horizon en nombre de publications n'est pas un nombre fixe de jours civils ; les deux durées sont consignées. Six références contre EUR offrent un premier test de transfert et de numéraire, sans prétendre représenter tous les marchés.

**P1-S :** après acquisition qualifiée, prévoir à 1, 10 et 60 secondes un prix précisément défini pour GC, ES et un univers historique d'actions. Le dernier prix observé à la frontière, le milieu de fourchette et le prochain prix de transaction seront des cibles distinctes. Une seconde sans transaction ne produit pas une transaction fictive. Pour la dernière transaction connue, son âge fait partie de l'état, et les résultats sont séparés selon qu'un nouvel événement intervient ou non dans l'horizon.

Ces tâches partagent des principes et éventuellement des paramètres, pas une cible statistique artificiellement identique. Le résultat primaire ne sera pas une moyenne de dollars, de points d'indice et de taux de change. Les erreurs en unités natives restent disponibles ; les agrégations utilisent des poids d'actifs fixés et des échelles calculées avant le test. Un score relatif au témoin est calculé à l'intérieur de chaque série avant agrégation, avec traitement explicite des dénominateurs nuls.

### 6.2 Comparaisons qui identifient une question

Pour un actif cible a, notons `L_a` un GPT entraîné seulement sur son histoire, `G_a` un GPT aux paramètres partagés entre actifs mais n'observant que l'histoire de a à l'inférence, et `M_a` un GPT partagé observant aussi les autres actifs disponibles. Les trois emploient la même cible et le même contrat d'observation.

| Contraste | Interprétation autorisée | Contrôle nécessaire |
|---|---|---|
| G_a contre L_a | Bénéfice du partage et du corpus d'apprentissage élargi | Rapporter exposition de la cible, budget total et nombre de paramètres ; ce contraste seul ne sépare pas tous ces facteurs |
| M_a contre G_a | Utilité conditionnelle du contexte d'autres actifs | Même architecture M entraînée avec masque des autres actifs comme témoin ; mêmes dates et mêmes origines |
| M_a contre contexte ancien | Valeur des observations croisées récentes | Retards fixés à l'avance ; historique marginal conservé ; interprétation d'ablation, sans p-value de permutation automatique |
| Même GPT, plusieurs encodages du même X | Effet de la représentation sous contraintes déclarées | Tête de sortie, fenêtre temporelle et information auxiliaire communes dans P1-A |
| Même langue, capacité croissante | Effet d'échelle dans la région étudiée | Quantité et diversité contrôlées ; diagnostic de convergence et plusieurs initialisations |

Le témoin masqué doit être entraîné dans cette condition : masquer seulement au test un modèle habitué à tous les actifs créerait un décalage artificiel. Le partage H1 sera également étudié sous budget total égal et sous exposition cible égale ; ces comparaisons répondent à des questions différentes. Un expert local reçoit, si nécessaire, davantage de répétitions de sa propre histoire, sans les compter comme de nouvelles observations.

Une permutation aléatoire des secondes détruirait la dynamique. Des décalages de séries peuvent changer saisonnalités et régimes ; ils ne constituent donc pas automatiquement une randomisation valide. Le témoin prioritaire est un contexte absent ou vieilli, entraîné dans les mêmes conditions. Les décalages éventuels restent des stress tests explicitement imparfaits.

### 6.3 Découpage temporel et dépendances

Pour la mise au point historique mensuelle, une proposition est 1960-1999 pour l'ajustement initial, 2000-2009 pour le développement et 2010-2020 comme pseudo-test rétrospectif, avec origines successives et apprentissage uniquement dans leur passé. Ces périodes ont des significations différentes et ne donnent pas à elles seules une preuve de stabilité. Elles font déjà partie du fichier reçu ; elles ne sont pas un futur test scellé.

Le test final devra être séparé avant la sélection des langues : nouvelle tranche temporelle ou famille non utilisée pour choisir les variantes, avec inventaire des modèles préentraînés et de leurs corpus. Si une famille est réservée pour tester son transfert, ses prix futurs ne peuvent pas être réintroduits comme contexte croisé d'un autre échantillon. Les composantes, composites, dérivés et conversions de devise sont regroupés pour vérifier ce point.

Toutes les séries utilisent la même coupure en temps de disponibilité. Les fenêtres d'apprentissage dont la cible franchit la coupure sont retirées. Un contexte historique antérieur peut légitimement être lu à une origine de test ; interdire arbitrairement tout contexte partagé n'est pas requis par la causalité. Les prévisions à horizons chevauchants et les actifs contemporains restent dépendants.

Les statistiques d'incertitude sont calculées sur des différences de pertes appariées, en rééchantillonnant des blocs temporels communs à tous les actifs. La longueur des blocs doit couvrir au moins l'horizon de chevauchement et faire l'objet d'une sensibilité. La stabilité selon les actifs, les décennies et les conventions est montrée séparément. Plusieurs fenêtres d'un même choc ne sont pas plusieurs crises indépendantes.

### 6.4 Scores, échelle et droit de ne pas conclure

P1-A pourra utiliser une grille de quantiles commune, évaluée par pertes quantiles, couverture et largeur d'intervalles, avec médiane évaluée en erreur absolue native. La grille et les règles de monotonie seront fixées avant comparaison. Ces sorties marginales ne prétendent pas représenter une loi jointe de trajectoires ; P1-B devra l'évaluer séparément, avec des scénarios complets et leurs propriétés temporelles.

Le premier tour compare un petit nombre d'encodages interprétables sur une capacité diagnostique, puis conserve une branche continue de référence et une branche progressive pour plusieurs capacités. Une variante peu performante à petite taille demeure dans le registre ; elle peut être retestée à une capacité supérieure selon un critère annoncé. Les réglages, essais infructueux et changements de protocole sont comptés, pas seulement les modèles finaux.

Une amélioration sera déclarée localement pour les tâches, périodes, budgets et familles testés. Son absence avec un intervalle large est un manque de précision. Son absence avec un intervalle étroit borne l'effet dans cette configuration. Aucun de ces deux résultats ne réfute toutes les langues, toutes les tailles et toutes les informations possibles. À l'inverse, l'espoir d'une émergence à grande échelle ne remplace pas une hypothèse testable sur la direction et les conditions du progrès.

## 7. Nouveau cycle du panel critique simulé

Ce cycle est une confrontation raisonnée entre rôles fictifs. Les trois tâches parallèles d'agents tentées pour cette itération ont échoué sur une limite de service et n'ont produit aucune relecture exploitable. Les conclusions ci-dessous ont été élaborées et vérifiées par l'agent principal ; aucune validation indépendante n'est revendiquée.

| Rôle fictif | Objection | Modification retenue |
|---|---|---|
| Spécialiste de la mesure | Un motif peut venir d'une moyenne ou d'un changement de fournisseur | Opérateur typé et version dans le langage ; témoin avec agrégation |
| Chercheur GPT | P1-A ne teste pas encore la génération du prochain token | Ajouter P1-B autorégressif, tout en isolant d'abord la représentation d'entrée |
| Théoricien de l'information | Les ancres et résidus peuvent cacher presque tout le signal | Inclure S dans les équations et publier le coût total |
| Économètre | Plus d'actifs ne signifie pas plus de chocs indépendants | Blocs temporels communs et contrôles de numéraire/composites |
| Ingénieure de données | « 1 seconde » ne signifie pas la même chose selon le fournisseur et l'époque | Vérifier précision, convention de barres, absence de transaction et disponibilité |
| Porteur du projet | Un protocole trop petit risque d'écarter la bonne langue | Garder un programme d'échelle et limiter chaque conclusion à sa configuration |

L'objection la plus forte à notre propre proposition reste le coût de la richesse : multiplier types, résidus et vues peut rendre la langue difficile à apprendre et favoriser la mémorisation des sources. Il faut donc une ablation « avec/sans types connus », un test sur un fournisseur différent et un test sur une version de mesure différente. Les types n'ont pas vocation à identifier secrètement l'année ou le résultat futur ; seuls les changements connus à l'origine sont admissibles.

## 8. Étapes suivantes et statut de preuve

L'acquisition Banque mondiale et son audit sont achevés. Les scripts de reconstruction POC0, leurs résultats et leur gel n'ont pas été modifiés. Les mois crypto réservés de novembre et décembre 2021 n'ont pas été ouverts. Le résultat sur l'agrégation est analytique et antérieur dans la littérature. Le code progressif et le protocole P1 sont des conceptions, sans entraînement ni comparaison prédictive exécutée.

La prochaine étape documentaire est de transformer P1 en fiche préenregistrable : choisir une première tâche précise, compléter les conventions historiques et la disponibilité, fixer les horizons, les variantes, les budgets de comparaison, les métriques et les règles d'amendement. Une tâche BCE quotidienne est plus proche d'un premier protocole réalisable avec les fichiers actuels ; l'or mensuel apporte un test complémentaire du type d'observation. Le corpus fin GC/ES/actions reste une acquisition future à qualifier par échantillon et conditions d'accès.

Le programme continue à rechercher une grammaire transférable et un modèle GPT capable d'apprendre des dépendances inédites. La nouvelle exigence est de pouvoir attribuer une amélioration à l'information du passé, à sa représentation, à la capacité du modèle ou à la mesure elle-même. Cette attribution donnera un sens scientifique à un futur succès.
