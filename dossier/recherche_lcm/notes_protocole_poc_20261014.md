# TRAME — Protocole proposé pour POC0

**14 octobre 2026. Version de conception après contradiction.** Ce fichier définit une expérience future ; il ne rapporte aucun développement, téléchargement supplémentaire, entraînement ou résultat de comparaison effectué par son auteur. Le périmètre convenu est désormais **audit de données réelles et reconstruction de représentations sur CPU**, sans prévision, sans AUC, sans simulation de trading et sans revendication d'alpha.

## 1. Recommandation centrale

POC0 doit répondre à une question étroite : **que conserve chaque langue, à quel coût et avec quelles erreurs, lorsqu'elle décrit exactement les mêmes observations de marché ?** Il prépare le concours prédictif ultérieur ; il ne peut pas désigner la langue qui prédit le mieux.

Le choix pragmatique est de conserver janvier–août 2021 pour ajuster les transformations, septembre–octobre pour leur audit extérieur et novembre–décembre comme période réservée **non téléchargée**. La reconstruction continue quasiment exacte constitue un contrôle de calcul. Les représentations avec perte s'évaluent par leur compromis entre erreur et coût de représentation, et par la préservation des propriétés utiles aux futures tâches.

« À information égale » signifie ici **même source admissible, mêmes dates, mêmes unités et même disponibilité**. Les langues ne retiennent pas la même quantité d'information : c'est précisément l'objet de l'expérience. Il serait contradictoire de présenter une simple suite de signes comme strictement aussi informative que les prix réels.

## 2. Périmètre et décisions à geler avant acquisition

| Élément | Proposition arrêtée pour POC0 |
|---|---|
| Place et marché | Archives officielles Binance Vision, spot, cotation USDT |
| Instruments | BTCUSDT, ETHUSDT, BNBUSDT, ADAUSDT, XRPUSDT, LTCUSDT, EOSUSDT, TRXUSDT |
| Granularité source | 1 heure, UTC |
| Période à acquérir | Janvier à octobre 2021 inclus, soit au plus 80 archives mensuelles plus leurs CHECKSUM |
| Période réservée | Novembre–décembre 2021 ; aucune acquisition, lecture, statistique ou graphique maintenant |
| Extension éventuelle | Année 2022 : nouvelle période extérieure réservée à une étape ultérieure |
| Fréquence dérivée | 4 heures, agrégation depuis les seules bougies H1 complètes |
| Codecs principaux | Continu, bins fixes, quantiles, signes/présence, bins en volatilité passée |
| Diagnostic distinct | Paliers sur clôtures horaires, sans inventer de chemin intrabougie |
| Calcul | CPU local, traitement par actif et fréquence ; aucune dépendance à un GPU |
| Statut des données | Recherche personnelle hors production, avec attribution et registre des droits |
| Réutilisation du bot | Aucune consommation des campagnes 002/007 ni de leurs holdouts |

Les huit actifs forment un **univers de convenance explicitement choisi**, pas une preuve d'absence de biais de survivance ni un échantillon représentatif de toute la crypto. EOS et TRX ajoutent de la diversité au panier initial, mais huit cryptomonnaies d'une même place et d'une seule année ne démontrent ni transfert entre marchés ni robustesse à tous les régimes. Les noms historiques de 2021 doivent être conservés ; aucune substitution par un ticker actuel sans historique documenté.

La documentation officielle décrit les bougies, leurs champs et les fichiers CHECKSUM ; elle indique que des archives peuvent être corrigées ultérieurement. Le manifeste doit donc conserver l'empreinte du fichier effectivement reçu, pas uniquement son URL. Les conditions consultées en octobre 2026 distinguent recherche personnelle hors production et usages commerciaux ou d'exécution réelle. Le futur modèle de production requerra une qualification distincte de ses droits. [Documentation Binance Public Data](https://github.com/binance/binance-public-data), [conditions officielles](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md).

## 3. Découpage, frontières et volumes théoriques

Définir chaque bougie par un intervalle semi-ouvert `[open_time, end_time)`. Pour H1, `end_time = open_time + 1 heure` ; le champ de clôture de l'archive, souvent inférieur d'une unité d'horodatage à cette frontière, reste conservé comme champ source. Les dates de split portent sur `open_time`, avec l'exigence que la bougie entière appartienne au bloc.

| Rôle | Intervalles d'ouverture UTC | Heures théoriques par actif | Rôle permis |
|---|---|---:|---|
| Ajustement des codecs | 2021-01-01 00:00 inclus à 2021-09-01 00:00 exclu | 5 832 | Références de volume, quantiles, prototypes de signes et seuils de diagnostic |
| Audit extérieur de développement | 2021-09-01 00:00 inclus à 2021-11-01 00:00 exclu | 1 464 | Mesurer les erreurs et constater les limites des codecs figés |
| Réserve non acquise | 2021-11-01 00:00 inclus à 2022-01-01 00:00 exclu | 1 464 | Aucun usage pendant POC0 |

Avant trous et amorçage, les dix mois représentent **7 296 lignes par actif**, soit **58 368 lignes pour huit actifs**. Les effectifs théoriques sont de 46 656 lignes d'ajustement et 11 712 lignes de développement. Les agrégats H4 comptent au plus 1 824 observations par actif, dont 1 458 d'ajustement et 366 de développement. Ces nombres sont des attentes calendaires, pas un constat sur les fichiers.

Une bougie ouvrant le 31 août à 23 h termine exactement à la frontière du 1er septembre : elle appartient à l'ajustement, et toutes ses valeurs sont disponibles au moment où le codec est gelé. Une bougie ouvrant le 1er septembre à 00 h appartient au développement. Les mêmes frontières sont appliquées aux huit actifs et à H4.

Comme POC0 ne prédit aucun futur, **il n'existe pas encore de labels à purger à 1, 4 ou 24 heures**. Les horizons futurs sont réservés à POC1. Confondre la reconstruction H4 avec une prévision à quatre heures serait une erreur de protocole. Le contexte passé du 31 août peut servir à calculer les caractéristiques du 1er septembre, car il est déjà connu.

## 4. Protection du futur et registre d'amendements

Le meilleur contrôle est matériel : **ne pas télécharger les mois réservés**. Le téléchargeur futur doit recevoir une liste autorisée de dates janvier–octobre, plutôt qu'une année entière filtrée après lecture. Une recherche récursive, un graphique de couverture ou une normalisation globale ne doivent pas ouvrir d'autres fichiers du projet.

Le manifeste du POC doit préciser que novembre–décembre sont réservés par protocole, mais qu'aucun snapshot local de cette réserve n'est encore authentifié. Une archive distante pourra changer entre aujourd'hui et son acquisition future ; l'empreinte sera alors enregistrée. La période n'est donc pas un fichier « scellé » déjà possédé.

Toute modification après lecture des résultats de développement devient un amendement daté : motif, paramètres changés, anciennes et nouvelles métriques, nombre de variantes supplémentaires. Les résultats antérieurs restent visibles. Le développement reste du développement même si l'on préfère ensuite un autre codec. Aucun amendement ne transforme rétroactivement septembre–octobre en test final indépendant.

L'expérience sur 2022 ne doit pas être annoncée comme une preuve prospective : elle reste une période historique extérieure, connue dans ses grandes lignes par le chercheur. La vraie validation prospective viendra après gel du modèle et du protocole.

## 5. Audit des données et construction H4

### 5.1 Contrôles avant toute représentation

Enregistrer URL, date de réception, taille, CHECKSUM publié, empreinte calculée, schéma et plage temporelle. Contrôler doublons de timestamp, ordre, unités, format d'horodatage, OHLC, volume et nombre de transactions. Une vérification de checksum atteste l'identité du fichier reçu ; elle n'atteste pas sa complétude ni une latence historique de publication.

Pour les prix positifs de ce corpus spot, exiger `L <= min(O,C) <= max(O,C) <= H`, des prix strictement positifs et des volumes non négatifs. Distinguer les données absentes, les valeurs réellement nulles et les lignes invalides. Ne pas déduire le format d'horodatage d'un réglage actuel de l'API : valider celui des fichiers de 2021.

Après un trou, la ligne suivante ne reçoit pas comme ancre la précédente ligne du tableau si celle-ci n'est pas la bougie attendue. La première différence serait sinon calculée sur une durée plus longue tout en étant étiquetée H1. Marquer la rupture et redémarrer les états qui exigent une continuité.

### 5.2 Agrégation stricte

Les blocs H4 sont ancrés à 00, 04, 08, 12, 16 et 20 h UTC. Pour quatre bougies H1 contiguës : ouverture de la première, haut maximal, bas minimal, clôture de la dernière, somme des volumes et, si utilisé, somme des transactions. Conserver la liste des quatre identifiants sources.

Si une des quatre bougies est absente ou invalide, l'agrégat H4 est absent. Ni remplissage par zéro, ni bougie plate imputée, ni mélange avec un fichier H4 officiel différent. L'agrégat devient disponible à la fin du bloc ; ses valeurs finales n'existent pas aux trois heures intermédiaires.

Les résultats H1 et H4 portent sur des vues dépendantes du même marché. Ils doivent apparaître dans des panneaux séparés et ne se cumulent pas pour fabriquer un plus grand échantillon statistique.

### 5.3 Cohortes communes

Publier d'abord la couverture brute. Pour la comparaison principale des cinq codecs, utiliser leur **intersection de lignes admissibles**, y compris l'amorçage nécessaire à sigma64. Publier aussi les pertes de couverture par cause et des diagnostics élargis par codec, sans mélanger leurs dénominateurs avec le classement principal.

Ne pas exiger qu'une ligne soit présente simultanément sur les huit actifs si les comparaisons sont par actif : cela supprimerait inutilement des observations valides. Les moyennes macro entre actifs utilisent les mêmes huit poids et affichent l'effectif de chaque actif.

## 6. Coordonnées communes et références

Pour une bougie t, A est la clôture de la bougie précédente **contiguë**, et :

`g = ln(O/A)` ; `b = ln(C/O)` ; `u = ln(H/max(O,C))` ; `d = ln(min(O,C)/L)` ; `v = ln(1 + V/V_ref)`.

Ces cinq coordonnées sont les seules entrées à encoder pour les codecs principaux. La reconstruction suit le document 02. Le niveau A et la référence de volume font partie de l'état nécessaire au décodage ; leur coût ne doit pas disparaître du bilan de représentation.

**V_ref proposé :** médiane des volumes strictement positifs de janvier–août, par actif et par fréquence. Elle est figée au 1er septembre et conserve son unité d'actif de base. Si aucun volume positif n'existe, le champ doit être déclaré non calibrable, sans référence arbitraire cachée. Le même V_ref est utilisé par les cinq codecs. Cette référence apprise sur toute la période d'ajustement est un paramètre du codec gelé : ses scores sur janvier–août sont des diagnostics internes, pas un test historique de modèle qui aurait été connu dès janvier.

**Sigma64 proposé :** écart-type population des 64 rendements close-to-close **strictement antérieurs** à la bougie t, c'est-à-dire `r[t-64], …, r[t-1]`. Il exclut `r[t]`. Chaque rendement doit provenir de deux clôtures consécutives, donc 65 clôtures passées sont nécessaires. Après un trou, attendre à nouveau cette continuité. Le plancher est fixé à `1e-6` en unités de log-rendement et son activation est comptée. Aucune substitution avec des valeurs futures.

H1 utilise 64 rendements horaires ; H4 utilise 64 rendements de quatre heures. Cela représente des durées différentes et doit figurer dans les résultats. Le choix vise un nombre fixe d'observations de volatilité pour chaque fréquence ; il ne constitue pas une comparaison à durée de contexte égale entre H1 et H4. Ne pas annualiser sigma pour cette quantification.

## 7. Cinq codecs entièrement spécifiés

### C0 — Continu, contrôle d'identité

Conserver g,b,u,d,v en précision float64, puis appliquer l'inverse avec A et V_ref. Ce contrôle vérifie schéma, unités et implémentation. Il doit reconstruire les prix à l'erreur numérique près. Il n'est pas un concurrent susceptible d'être battu sur l'erreur de reconstruction par un codec avec perte.

### C1 — Bins fixes

Pas fixe `delta = 0.001` pour g,b,u,d, soit **10 points de base logarithmiques**. Arrondi au plus proche, les demi-pas s'éloignant de zéro ; décodage par multiplication de l'entier par delta. Pour v, pas fixe `0.05`, même règle. Pas de clipping : les valeurs hors plage observée en ajustement restent codables, avec un mécanisme d'entier ou d'échappement explicite.

Sans saturation, les bornes locales d'erreur logarithmique sont : O au plus 5 points de base ; C au plus 10 ; H et L au plus 15. Ces bornes résultent de l'addition de plusieurs coordonnées quantifiées. Pour v, `abs(v_hat-v) <= 0.025` ; cela ne signifie pas une erreur relative universelle de 2,5 % sur V, notamment près de zéro.

### C2 — Quantiles, au plus 64 codes par champ

Pour g et b, construire les coupures de 64 intervalles à partir des données d'ajustement de l'actif/fréquence. Pour u,d,v, réserver un code à zéro et répartir les valeurs strictement positives dans au plus 63 intervalles. Une valeur nulle et une absence de donnée ne partagent pas le même code.

Calculer les quantiles par interpolation linéaire : pour n valeurs triées et une probabilité p, position `h=(n-1)p`, interpolation entre les indices `floor(h)` et `ceil(h)`. Supprimer les coupures identiques. Avec des données discrètes ou une masse en zéro, le nombre effectif d'intervalles peut être inférieur au maximum. Une valeur exactement égale à une coupure appartient à l'intervalle supérieur ; les extrémités sont ouvertes vers l'infini. Chaque code se décode par la médiane de ses valeurs d'ajustement, et non par une médiane recalculée en développement. La convention pour une médiane d'effectif pair est la moyenne des deux valeurs centrales.

Après suppression des coupures identiques, fusionner tout intervalle sans observation d'ajustement avec son voisin inférieur ; pour le premier intervalle, choisir le voisin supérieur. Répéter jusqu'à ce que chaque code ordinaire possède un représentant. Ce traitement est ajusté exclusivement sur janvier–août ; les effectifs et frontières réels sont conservés.

Compter séparément les valeurs de développement hors minimum/maximum d'ajustement. Elles ne créent pas de nouveaux codes ; l'erreur de reconstruction avec le représentant extrême est conservée. Si une composante n'avait aucune valeur positive en ajustement puis en présente une en développement, enregistrer un hors-support explicite ; le décodage de secours annoncé peut être zéro, mais son erreur compte pleinement. Ne jamais exclure ces lignes pour améliorer le score.

### C3 — Signes et présence, contrôle fortement compressé

Codes ternaires pour g et b : négatif, zéro, positif. Codes binaires pour u,d,v : nul ou strictement positif. Chaque état se décode par la médiane conditionnelle de janvier–août de la composante correspondante. L'état zéro se décode exactement à zéro. Un état sans observation d'ajustement est déclaré hors-support ; le secours à zéro et l'erreur correspondante sont enregistrés.

Ce codec perd beaucoup d'information. En particulier, la présence de volume sera presque toujours positive ; le volume reconstruit sera alors essentiellement un prototype constant. Cette faiblesse est intentionnelle : il s'agit d'un contrôle de la perte de magnitude, pas d'une proposition présumée compétitive. Les médianes u,d,v restent non négatives, ce qui garantit la cohérence OHLC après inverse.

### C4 — Bins en volatilité passée

Définir `sigma_eff = max(sigma64, 1e-6)`, diviser g,b,u,d par sigma_eff, quantifier au pas `0.1`, puis restituer avec **la même référence**. Pour v, employer le pas `0.05` et le V_ref commun. La référence sigma_eff est un champ auxiliaire nécessaire au décodage et doit apparaître dans le coût.

La précision économique varie avec la volatilité : un cran vaut `0.1 × sigma_eff` en log-rendement. Les bornes locales d'erreur sont donc O ≤ `0.05 × sigma_eff`, C ≤ `0.1 × sigma_eff`, H/L ≤ `0.15 × sigma_eff`. Publier ces résolutions en points de base par régime, plutôt qu'annoncer un unique pas fixe.

Dans POC0, sigma provient du passé réel observé et accompagne le codec. Il s'agit d'une **reconstruction conditionnée sur les références observées**, pas d'une génération future autonome. Un futur modèle devra soit figer sigma au temps de prévision, soit le recalculer sur les trajectoires générées. L'expérience présente ne valide aucune de ces deux stratégies.

## 8. Diagnostic palier séparé

Utiliser uniquement les clôtures observées à l'heure, avec seuil fixe `delta_event = 0.005` en log-prix, soit 50 points de base logarithmiques. C'est environ +0,50125 % en rendement simple, et non exactement +0,5 %.

À chaque nouvelle clôture, comparer `ln(C_t / P_anchor)` au seuil en valeur absolue. Si le seuil est atteint, enregistrer **un seul événement agrégé pour cette bougie** : signe, log-amplitude complète, dépassement du seuil, durée depuis le dernier événement et timestamp de détection. L'ancre devient C_t. Sinon, l'état conserve l'ancre et augmente son âge.

Même si le prix a parcouru plusieurs seuils dans une heure, ne pas inventer leurs instants ni leur ordre. H/L ne permet pas de reconstituer un trajet. La magnitude complète conservée rend les clôtures d'événement exactement reconstructibles ; les clôtures intermédiaires restent perdues. Un décodage causal simple maintient la dernière ancre jusqu'au prochain événement, sans interpolation par un point futur.

Rapporter proportion d'heures contenant un événement, durée, dépassement, âge courant, erreur de la clôture maintenue et compression indicative. À la fin d'un bloc ou avant un trou, l'événement inachevé est **censuré** ; ne pas créer artificiellement une clôture d'événement favorable. Les frontières de partition ne sont pas des mouvements de marché.

Ce diagnostic ne rejoint pas le classement OHLCV des cinq codecs : il ne retient ni mèches ni volumes intrabougie. Un palier peut avoir une erreur de clôture intéressante sans préserver les franchissements observés entre les clôtures. La comparaison prédictive ultérieure devra définir une cible commune et un traitement probabiliste des chemins compatibles.

## 9. Deux reconstructions qu'il ne faut pas confondre

### 9.1 Reconstruction locale par bougie

À chaque t, décoder avec **A réel précédent**, connu avant la bougie. Cela mesure la perte propre à l'encodage de cette observation. Les bornes de C1/C4 ci-dessus s'appliquent à cette reconstruction locale.

### 9.2 Reconstruction en chaîne

Pour des segments calendaires préétablis de 24 heures et 168 heures, conserver une seule ancre réelle au début, puis utiliser chaque clôture décodée comme ancre suivante. Les coordonnées encodées proviennent toujours des données réelles observées : c'est une mesure de dérive de codec, **pas une prévision récursive**.

Les segments de 24 heures sont alignés à 00 h UTC ; ceux de 168 heures au lundi 00 h UTC. Sur H4, cela correspond respectivement à 6 et 42 bougies, et non à 24 et 168 bougies. Conserver seulement les segments complets, contigus et entièrement dans une partition, avec les mêmes exclusions pour les cinq codecs. Les segments de 24 et 168 heures se chevauchent entre diagnostics et ne sont pas deux jeux indépendants.

C4 conserve ses sigma observés en tant que champs auxiliaires dans cette reconstruction en chaîne. Une seconde expérience qui recalculerait sigma sur la trajectoire décodée serait un autre codec dynamique et un essai supplémentaire ; elle n'appartient pas à POC0.

## 10. Mesures et tableaux de résultats à produire

### 10.1 Erreur, structure et queues

Pour chaque prix P dans O,H,L,C : `e_P = 10 000 × ln(P_hat/P)`. Rapporter biais signé, moyenne absolue, médiane absolue, quantiles 95 % et 99 %, et maximum absolu. Ces unités sont des **points de base logarithmiques**, pas un PnL.

Mesure principale de reconstruction : moyenne absolue d'erreur de clôture sur développement H1, calculée par actif puis moyennée avec poids 1/8. Elle est accompagnée de l'erreur sur H et L ; elle ne doit pas écraser les mèches au profit d'une belle clôture. H4 figure séparément.

Pour le volume, rapporter `abs(v_hat-v)`, une erreur relative sur les observations V > 0 et le taux de zéro réel correctement reconstruit. Publier les effectifs ; ne pas faire disparaître V = 0 dans un calcul de pourcentage. On peut également rapporter `abs(V_hat-V)/max(V,V_ref)` comme erreur sans dimension avec dénominateur annoncé.

Définir un seuil de queue à partir du quantile 99 % de `ln(H/L)` sur **ajustement**, séparément par actif/fréquence. Appliquer ce seuil figé à septembre–octobre et publier toutes les erreurs dans ce sous-ensemble, avec sa taille. Ce conditionnement décrit la difficulté d'une reconstruction observée ; il ne prétend pas anticiper un régime de crise. Une seconde définition de queue ne sera pas cherchée après lecture d'un résultat décevant.

Compter également violations OHLC, reconstructions négatives, champs non finis, codes hors-support, saturation éventuelle, présence exacte des zéros, fréquence du plancher sigma et erreur maximale en chaîne. Publier les résultats par actif, fréquence et partition, y compris les échecs.

### 10.2 Coût de représentation

Ne pas choisir un vainqueur uniquement sur l'erreur : le continu sans perte gagnerait par définition. Rapporter codebook, références, ancre, masques, nombres de codes et coût de décodage.

À titre de budget théorique **sans prétendre avoir construit un format binaire** : cinq float64 coûtent 320 bits ; cinq entiers int32, 160 bits ; cinq codes à 64 états, au plus 30 bits ; les deux signes ternaires et trois présences, 7 bits dans un emballage simple ; les bins normalisés ajoutent la référence sigma, par exemple 64 bits par bougie si elle est stockée en float64. Ajouter V_ref, prototypes, frontières, timestamps, ancre et indicateurs selon leur amortissement réel.

Ces comptes nominaux ne prouvent pas un taux de compression obtenu. Une taille CSV ou JSON compare surtout les choix de sérialisation. Un futur codec binaire devra préciser échappements, bornes d'entiers, exactitude des sidecars et encodage des valeurs manquantes. La quantification vectorielle apprise et la compression entropique ne sont pas incluses ici.

### 10.3 Portée statistique

POC0 ne publie pas de p-value de rentabilité ni de Sharpe. Le nombre de représentations est petit et gelé ; tous les résultats seront montrés. Une différence d'erreur de reconstruction n'est pas un test d'hypothèse sur l'alpha. Les fenêtres adjacentes et actifs sont dépendants ; le nombre de lignes ne doit pas devenir un nombre supposé d'expériences indépendantes.

## 11. Nombre d'essais, réglages interdits et registre

Le plan principal comporte **5 codecs × 2 fréquences = 10 évaluations de représentation**, plus **1 diagnostic palier H1**. Les deux modes de reconstruction et les mesures de queues sont des diagnostics prédéfinis de ces mêmes objets. Le mot « essai » doit aussi inclure tout réglage additionnel examiné après résultat, même si le code n'a presque pas changé.

Paramètres figés : univers, dates, pas de bins 0.001, pas v 0.05, limite de 64 codes, sigma64 excluant le courant, plancher 1e-6, pas normalisé 0.1, seuil palier 0.005, arrondi, convention des quantiles, représentants, zéros, secours hors-support, fenêtres 24/168 heures et seuil de queue 99 %.

Interdictions de réglage implicite : choisir un autre pas parce qu'il améliore septembre ; sélectionner seulement les actifs faciles ; retirer un extrême parce qu'il gêne la quantification ; modifier la règle de trous en fonction des erreurs ; donner davantage de précision aux cas dont on a déjà vu les résultats. Une anomalie de logiciel se corrige, mais les résultats affectés sont marqués invalides et remplacés de façon traçable.

Les quantiles et médianes sont des paramètres appris sur ajustement. Ils ne doivent pas être rebaptisés « sans entraînement » au sens de « sans aucun ajustement aux données ». Formulation correcte : **aucun prédicteur n'est entraîné ; certains codecs sont ajustés sur janvier–août**.

## 12. Conditions de passage

| Gate | Condition avant suite | Décision si non remplie |
|---|---|---|
| P0-A — Provenance | Fichiers et CHECKSUM vérifiés, mois autorisés seulement, droits enregistrés | Corriger la collecte ou la source ; ne pas comparer des codecs sur une base non identifiée |
| P0-B — Structure | Trous et invalides tracés ; H4 complet uniquement ; cohortes comparables | Réparer les règles, jamais inventer une couverture |
| P0-C — Identité | C0 respecte OHLC et reconstruit à précision numérique ; proposition : erreur relative prix ≤ 1e-10, erreur volume divisée par max(V,V_ref) ≤ 1e-10 | Auditer unités, inverse, arrondis et schéma avant toute interprétation |
| P0-D — Causalité | Sigma sans courant/futur, références apprises uniquement sur ajustement, aucune lecture de la réserve | Invalider et reprendre les résultats concernés |
| P0-E — Bornes | C1/C4 respectent leurs bornes analytiques sans clipping ; zéros et hors-support traités selon contrat | Corriger le codec ou documenter une autre représentation comme nouvel essai |
| P0-F — Audit complet | Erreurs, extrêmes, dérive, coûts et couverture de tous les codecs publiés | Pas de sélection silencieuse ni de lancement de grand entraînement |

**Sortie possible :** une ou deux langues méritent un concours prédictif, parce que leur compression et leurs propriétés paraissent adaptées. Cela ne nécessite pas qu'elles battent C0 en reconstruction, ce qui serait impossible. Un codec perdant en reconstruction peut encore être une régularisation utile ; seule une expérience prédictive pourra l'établir.

Éviter un seuil universel du type « moins de 10 bps donc utilisable en trading ». La résolution doit être comparée à la tâche future, au tick, aux amplitudes des cibles et aux coûts réels. POC0 n'identifie pas encore cette utilité économique.

## 13. Étape ultérieure explicitement hors POC0

Une fois les gates ci-dessus satisfaits, une fiche POC1 pourra figer des cibles de rendement réel à **1, 4 et 24 heures**, une métrique principale, des baselines et un nombre d'essais limité. Les modèles linéaires serviront à vérifier la chaîne avant un Transformer. Les labels devront alors être purgés selon leur maturité, globalement entre actifs ; le dernier jour d'ajustement ne peut pas fournir de cible à 24 heures encore inconnue à la date de gel.

Une proposition sobre serait un modèle ridge continu à budget fixe et des versions comparables des langues finalistes, sans stratégie de trading. L'ordre des choix serait : horizon principal ; contexte commun ; normalisation ; grille de régularisation limitée ; règle de sélection ; métriques ; traitement de dépendance ; puis seulement ouverture d'une période d'évaluation autorisée. Une AUC directionnelle isolée serait insuffisante et aucune comparaison sur des trajectoires imputées comme si elles étaient vraies ne serait admise.

Ne pas introduire un prédicteur « pour voir » pendant POC0 : cela ajouterait des décisions de recherche avant leur protocole et transformerait la reconstruction en recherche opportuniste de signal. Les documents généraux demeurent la vision de long terme ; cette note réduit volontairement la prochaine expérience à ce qui est vérifiable immédiatement.

## 14. Livrables attendus du futur exécutant

1. Manifeste des paramètres et registre des éventuels amendements.
2. Manifeste des archives autorisées avec hashes et source des droits.
3. Rapport de qualité H1 et H4, avec couverture commune et motifs d'exclusion.
4. Paramètres de codecs ajustés seulement sur janvier–août et leur empreinte.
5. Tableau complet des erreurs locales, de chaînes et de queues par codec, actif et fréquence.
6. Diagnostic des paliers, explicitement distinct de la reconstruction OHLCV.
7. Comparaison du coût de représentation avec hypothèses de stockage visibles.
8. Rapport de passage ou de blocage aux gates, sans transformer les erreurs de reconstruction en résultats de prévision.

**Priorité scientifique :** garder le futur inaccessible, rendre chaque transformation réversible ou déclarer précisément sa perte, vérifier les bornes analytiques avant d'expliquer les résultats, puis seulement décider de la prochaine expérience.
