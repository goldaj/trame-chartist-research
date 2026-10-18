# Du langage à l'expérience contrôlée

## 1. Portée de cette édition

**TRAME, édition 2.2 du 15 octobre 2026. Consolidation scientifique du candidat P1-D 0.3.** Ce texte rassemble les cinq notes de travail du 15 octobre. Il amende les propositions expérimentales des documents 01 à 09 quand elles divergent. Les anciennes versions restent archivées ; leurs résultats effectivement mesurés ne sont pas réécrits.

L'idée directrice demeure un modèle de séquences de type GPT capable d'apprendre des relations entre prix. Le langage peut combiner nombres, géométrie, durée, événements, états de disponibilité et relations entre actifs. La question actuelle est plus précise : comment comparer des écritures sans confondre l'information disponible, leur facilité d'apprentissage et la puissance du modèle ?

Trois avancées structurent la réponse. Des codes contenant exactement la même information n'ont pas nécessairement la même efficacité avec un modèle fini. Un encodage doit être causal par sa construction, pas seulement par le masque du Transformer. Enfin, l'audit réel a révélé une voie de traitement qui n'aurait pas été entraînée, ce qui oblige à corriger le candidat avant son évaluation.

| Statut | Ce qui appartient à cette catégorie |
|---|---|
| Mesuré | Calendriers, précision numérique, support des codes et échappements sur les données BCE existantes. |
| Déduit | Bijections entre codes, comptes de paramètres, conditions de causalité et borne conditionnelle d'un codec différentiel. |
| Proposé | Encodeurs hybrides, GPT, témoins, sorties et programme de comparaison. |
| Non établi | Gain prédictif, découverte de nouveaux motifs, avantage universel d'une langue ou émergence avec la taille. |

Le protocole prédictif reste un **candidat documentaire** : il n'est ni préenregistré, ni entièrement gelé, ni implémenté. Le gel réalisé avant l'audit descriptif ne concerne que cet audit. Aucun modèle prédictif ou tokenizer appris n'a été construit ou entraîné.

Cette étape quotidienne est un banc d'essai de concepts. Elle ne remplace pas le futur corpus d'or, d'indices, d'actions et d'autres marchés, ni l'étude de données fines. Les observations réelles déjà disponibles servent à éliminer des ambiguïtés avant d'augmenter les moyens.

<!-- pagebreak -->

## 2. Même information, apprentissages différents

Notons X le passé numérique, S les informations auxiliaires communes et Y le prix futur. Une écriture discrète K=T(X) peut perdre de l'information. Une autre écriture H=f(K), si f est bijective, ne perd rien par rapport à K. Cette distinction porte sur les données avant l'encodeur appris.

**Proposition conditionnelle.** Si K et H se déduisent exactement l'un de l'autre, conditionnellement à S, les ensembles de prédicteurs mesurables fondés sur (K,S) et (H,S) sont identiques par composition. Pour une même perte, l'infimum de risque sur une classe non restreinte est donc identique. Un réseau fini n'atteint pas nécessairement cet infimum.

La preuve est constructive : à tout prédicteur g(K,S), associer g(f inverse(H),S), et réciproquement. Si K efface des détails de X, un prédicteur sur X peut toujours reproduire celui sur K ; son risque idéal ne peut donc pas être supérieur, avec les mêmes informations auxiliaires et une classe libre. Une meilleure performance pratique du discret peut venir de la régularisation ou de l'optimisation.

| Comparaison proposée | Question effectivement posée |
|---|---|
| C contre Q | Effet de la quantification avec des encodeurs numériques minimaux comparables. |
| Q contre H+ | Intérêt de corrections hiérarchiques au-delà d'une base numérique, pour les mêmes cellules. |
| F+ contre H+ | Effet du partage entre composants, à cœur GPT identique mais à nombre total de paramètres différent. |

La bijection des codes ne garantit pas l'injectivité des vecteurs appris : une table ou une somme de composants peut fusionner des codes. Une conclusion doit donc porter sur un système d'encodage et d'apprentissage, pas sur une information abstraite seule.

[xVal, version 2](https://arxiv.org/html/2310.02989v2), montre comment intégrer directement une valeur dans un embedding et une tête numérique. Les [embeddings numériques de Gorishniy et al.](https://papers.nips.cc/paper/2022/file/9e9f0ffc3d836836ca96cbf8fe14b105-Paper-Conference.pdf) motivent des témoins non linéaires ou périodiques. Ces travaux sur d'autres tâches ne démontrent aucun avantage sur les prix.

L'espace de recherche reste ouvert : arithmétique explicite, coordonnées ordinales, franchissements de seuil, raffinements progressifs et plusieurs écritures d'un même passé. Leurs bénéfices devront être attribués au bon mécanisme, sans compter leurs transformations comme de nouvelles observations indépendantes.

<!-- pagebreak -->

## 3. Causalité et informations auxiliaires

À l'origine i, le candidat reçoit 256 références positives, de P_(i-255) à P_i. Il calcule une unité s_i sur le passé et recentre l'histoire sur P_i : `x_(j;i)=log(P_j/P_i)/s_i`. Cette entrée est disponible pour prévoir après i.

Elle n'est pas causale à chaque ancienne position j. Pour j inférieur à i, P_i et une partie des observations de s_i appartiennent à son futur. Un masque triangulaire appliqué aux embeddings ne retire pas cette information déjà introduite par le prétraitement.

**Conséquence pour P1-A :** la perte ne porte que sur des cibles postérieures à l'origine i. On ne transforme pas cette même fenêtre recentrée en exemples next-token à toutes ses positions. Pour P1-B, qui générera un flux de symboles, chaque état et chaque normalisation devront être calculables à partir du préfixe réellement connu ou généré.

Un autre problème, distinct du futur, concerne le contraste entre langages. Si chaque symbole historique reçoit le prix exact précédent, ces ancres répétées réintroduisent presque tout le passé ; avec le dernier prix exact, elles peuvent le restituer entièrement. Le prétendu langage « signe seulement » n'est alors plus la seule source de l'historique.

Le contrat retient une seule ancre P_i et une seule échelle s_i par actif et origine, plus identité, unité, type d'observation et intervalles calendaires passés. Une statistique continue supplémentaire par ancien point modifierait ce contrat. Un indicateur d'échappement dérivé du code n'est pas, lui, une information extérieure au code.

Les cibles sont les prix aux prochaines 1, 5 et 20 publications valides : des horizons d'observation, pas des durées physiques constantes. La date future effectivement observée ne devient pas une entrée. Les absences ne sont pas remplies par des cours inventés.

L'historique BCE a été reçu en 2026. Respecter l'ordre des dates ne certifie pas les versions disponibles lors des premières publications. Le [cadre BCE de juin 2026](https://www.ecb.europa.eu/stats/pdf/exchange/Frameworkfortheeuroforeignexchangereferencerates.en.pdf) n'est pas rétroprojeté sur 1999-2020. L'expérience reste rétrospective et conditionnelle à cette version.

### Conséquence pour le modèle de langage

La causalité doit être définie au niveau du pipeline entier : acquisition, révision, normalisation, découpage et état de génération. Le Transformer causal est nécessaire pour certaines architectures ; il ne certifie pas à lui seul le respect de cette chaîne.

<!-- pagebreak -->

## 4. Une cellule, plusieurs écritures exactes

Le candidat utilise l'écart-type de population des 64 derniers incréments logarithmiques, centré par leur moyenne, avec plancher 10^-6. La normalisation est calculée en float64 ; chaque coordonnée est ensuite arrondie une fois en float32. Toutes les variantes partent de ce même x32.

Le code est `k=floor(8*float64(x32))` ; le milieu est `m=(2k+1)/16`. La largeur de cellule vaut 1/8. C reçoit x32 ; Q reçoit m. Quantifier directement x64 alors que C reçoit x32 aurait pu donner au code une distinction que C n'a plus : l'ordre des conversions fait partie de l'expérience.

F écrit l'entier k. H écrit `q=floor(k/8)` et les trois bits de `r=k-8q`, avec r entre 0 et 7. La division avec plancher vaut aussi pour les négatifs. Exemple construit : pour k=-1, q=-1 et r=7 ; une division tronquée vers zéro ne respecte pas cette convention.

Le dictionnaire ordinaire comprend k de -2048 à 2047, soit 4 096 cellules. Le composant grossier q comprend 512 valeurs, de -256 à 255. Hors dictionnaire, une écriture canonique d'échappement conserve l'entier : signe, chiffres décimaux et terminaison, sans zéro initial superflu ni zéro négatif. Sa décodabilité ne garantit pas l'apprentissage du traitement correspondant.

Sous la condition suffisante `-2^23 <= k <= 2^23-1`, m est exactement représentable en float32. Il permet de retrouver k ; Q, F et H contiennent donc les mêmes cellules. Cette condition a été vérifiée sur les fenêtres réelles. Un dépassement futur imposerait un arrêt et un amendement, sans écrêtage ni suppression silencieuse.

La discrétisation donne une erreur maximale 1/16 entre x32 et m. C'est une borne de reconstruction d'une coordonnée, pas de prévision. Elle s'ajoute à l'arrondi préalable et dépend, pour un retour au prix, de l'ancre et de l'échelle.

P1-A fusionne les composants en **un vecteur par observation physique**. Il n'augmente donc pas artificiellement la longueur du contexte Transformer pour H. Tables, opérations locales et tailles de code doivent néanmoins être comptées. Ce n'est pas encore un générateur autorégressif de chiffres ou de bits.

Les mêmes conditions de précision doivent être vérifiées avant toute extension à d'autres actifs. Leur satisfaction sur six séries quotidiennes n'est pas une garantie universelle pour des bougies à la seconde, des prix très faibles ou une autre normalisation.

<!-- pagebreak -->

## 5. Audit réel des fenêtres et des codes

L'audit descriptif a été figé localement le 15 octobre à 14:38:46 UTC, avant exécution. Il lit la version existante de six séries BCE contre EUR : USD, JPY, GBP, CHF, CAD et AUD, de 1999 à 2020. Aucun téléchargement ni ajustement de modèle n'intervient.

Les fenêtres de 256 prix et les horizons communs produisent les effectifs suivants. Une origine compte ici une date par actif ; les présentations comptent toutes les répétitions dans les contextes.

| Période et usage | Origines par actif | Présentations | Échappements |
|---|---:|---:|---:|
| 1999-2009, ajustement futur | 2 541 | 3 902 976 | 0 |
| 2010-2014, développement | 1 261 | 1 936 896 | 195 |
| 2015-2020, pseudo-test | 1 515 | 2 327 040 | 0 |

Les 8 166 912 présentations proviennent de **33 672 prix sources distincts** dans l'union des contextes. Leur répétition ne constitue pas une augmentation équivalente de l'information historique. Aucun échec de décodage ou d'exactitude du milieu, ni activation du plancher de volatilité n'a été observé. L'ordre d'arrondi modifie 24 cellules, réparties 10/7/7 entre périodes.

Dans l'ajustement partagé entre six actifs, 735 codes plats et 96 codes grossiers sont observés. Au développement, 9 514 présentations ordinaires correspondent à des codes plats absents de l'ajustement ; 8 202 ont un composant grossier absent. Les bits sont tous déjà apparus. Au pseudo-test, ces comptes deviennent 69 et zéro. Les 195 échappements ne sont pas inclus dans ces cellules ordinaires.

Ces résultats renseignent le support des paramètres de tables ; ils ne mesurent ni prévisibilité, ni entropie conditionnelle, ni composition apprise. Ils révèlent cependant un défaut concret du candidat 0.2 : sa branche affine réservée aux seuls échappements n'aurait reçu **aucun gradient de tâche** à l'ajustement. Un module de même forme dans Q ne lui transmet pas automatiquement ses poids.

Le pseudo-test est exploratoire, déjà connu par provenance et désormais examiné pour ses représentations. Il ne sera pas renommé « test final intact ». Le rapport, le protocole d'audit, son script et le snapshot 0.2 sont conservés dans `research/trame_protocol_p1d/audits/preflight_01`.

<!-- pagebreak -->

## 6. Un extrême de langage et son unité

Les 195 échappements concernent 40 contextes CHF, d'origines comprises entre le 15 juin et le 9 août 2012. Après lecture des agrégats, un diagnostic ciblé a été déclaré puis exécuté. Il est **exploratoire et postérieur** à l'audit initial ; le choix de ce cas n'est pas indépendant des observations.

Le minimum de coordonnée apparaît à l'origine du 1er août 2012, pour le prix historique du 10 août 2011. Les valeurs suivantes viennent du rapport conservé, sans simulation de prix.

| Élément du calcul réel | Valeur |
|---|---:|
| Prix historique, CHF par EUR | 1,0451 |
| Prix à l'origine, CHF par EUR | 1,2013 |
| Logarithme du ratio | -0,1392917291 |
| Écart-type des 64 derniers incréments | 0,0003005311 |
| Coordonnée normalisée float64 | -463,4853067 |
| Cellule k | -3 708 |
| Écart-type des 255 incréments du contexte | 0,0075289986 |
| Rapport des échelles longue/courte | 25,0523 |

Le nombre -463 n'est pas une variation sur une publication de 463 écarts-types. C'est une différence entre niveaux éloignés, divisée par une très petite unité récente. Une vérification scalaire distincte concorde avec le calcul vectorisé dans les tolérances déclarées.

La BNS a annoncé le cours minimum de 1,20 CHF par EUR le [6 septembre 2011](https://www.snb.ch/en/publications/communication/press-releases/2011/pre_20110906), puis confirmé sa politique en [février 2012](https://www.snb.ch/en/publications/communication/speeches/2012/ref_20120207_tjn). Ce contexte est compatible avec l'interprétation d'une faible volatilité récente ; l'audit n'identifie pas causalement l'effet de cette politique.

La normalisation définit donc une partie de la difficulté du langage. Si s_i devient petit, un écart de niveau fini peut produire un x très grand. Une représentation combinant échelle courte et longue mérite une expérience séparée. Elle apporterait d'autres statistiques ou une autre résolution ; elle ne serait plus exactement le contraste présent. Aucune date ni unité n'a été modifiée pour faire disparaître ce cas.

<!-- pagebreak -->

## 7. Le candidat 0.3 : base numérique et corrections

La correction proposée remplace la branche isolée par une base numérique utilisée sur toutes les valeurs. Pour une largeur d, écrire `N(m)=a*m+b`. À l'intérieur de chaque modèle, N est le même module dans et hors du dictionnaire.

| Variante active | Vecteur de valeur proposé |
|---|---|
| Q | N(m), partout. |
| F+ | N(m)+T[k] dans le dictionnaire ; N(m) hors dictionnaire. |
| H+ | N(m)+A[q]+B2[b2]+B1[b1]+B0[b0] dans le dictionnaire ; N(m) hors dictionnaire. |

Les tables T, A et B sont initialisées à zéro. Pour chaque répétition, Q, F+ et H+ partent du même cœur GPT et de la même initialisation de N. Ils ont ensuite leurs propres paramètres : pas de transfert de poids entraînés depuis Q ni de partage des poids entre concurrents pendant l'ajustement.

À cette initialisation, leurs vecteurs sont mathématiquement identiques. Les corrections additives peuvent recevoir un gradient même nulles ; aucune seconde porte nulle ne les multiplie. Les lignes jamais visitées doivent rester nulles sous l'optimiseur futur, à vérifier lors d'une implémentation ultérieure.

Une cellule plate inédite reçoit la base seule. Dans H+, un composant grossier inédit peut rester nul tandis que des bits déjà entraînés contribuent. Cette composition peut être utile ou nuisible : couvrir les composants ne prouve pas une bonne extrapolation.

N voit désormais les données ordinaires. Cela corrige l'absence d'exemples pour ses paramètres, sans garantir son extrapolation ni la répartition de l'apprentissage face aux tables. Les paramètres numériques et symboliques peuvent se compenser ; leurs valeurs ne seront pas interprétées directement comme des causes de marché.

**F+ et H+ sont hybrides.** m provient exactement des mêmes codes : il ne restitue pas l'information continue perdue par quantification, mais donne explicitement une relation numérique au réseau. Q-H+ teste l'intérêt d'une correction hiérarchique au-dessus de cette base, pas la supériorité d'un alphabet purement symbolique.

Les anciens F/H 0.2 restent archivés. Une voie symbolique pure pourrait employer des chiffres partagés dans toutes les valeurs, y compris ordinaires. Il faudrait documenter leur apprentissage, l'ordre de génération et le coût des séquences. Aucun résultat présent ne réfute universellement cette voie.

<!-- pagebreak -->

## 8. GPT principal et comptes de paramètres

Le gabarit proposé est un Transformer causal pré-normalisé : attention dense avec projections et biais, MLP d vers 4d puis d avec GELU, deux normalisations affines par bloc et une finale, positions sinusoïdales fixes. Il reçoit un vecteur par observation, une identité d'actif et les métadonnées communes. Il reste entièrement sur papier.

Un bloc possède `12*d*d+13*d` paramètres. Avec L blocs, identité, projection de quatre métadonnées, normalisation finale et tête de 21 sorties, le total commun vaut `12*L*d*d+13*L*d+34*d+21`, avant l'encodeur de valeur. C/Q ajoutent 2d ; H+ ajoute 520d ; F+ ajoute 4 098d.

| Gabarit proposé | C ou Q | H+ | F+ |
|---|---:|---:|---:|
| L=4, d=128, 4 têtes | 797 717 | 864 021 | 1 322 005 |
| L=6, d=256, 8 têtes | 4 747 797 | 4 880 405 | 5 796 373 |
| L=8, d=512, 8 têtes | 25 237 525 | 25 502 741 | 27 334 677 |

Les comptes restent ceux de 0.2 : la base affine existante est utilisée plus souvent, sans ajout de paramètres. Les opérations locales changent néanmoins. Ces nombres ne sont ni une mesure de mémoire réelle, ni un chronométrage, ni une estimation ferme de coût d'entraînement.

Comparer à cœur identique répond à une question d'architecture contrôlée, sans égaliser paramètres totaux ou calcul. Une seconde comparaison pourrait ajuster largeur ou budget sous une contrainte de ressources commune ; elle modifierait alors le cœur. Ajouter des paramètres inutilisés pour afficher des totaux égaux ne serait pas un contrôle valable.

Une base affine peut constituer un témoin trop faible pour conclure à l'intérêt général du symbolique. Des encodeurs numériques non linéaires et périodiques doivent être spécifiés avant une affirmation plus large. Le [Number Cookbook, version 2](https://arxiv.org/html/2411.03766v2) nourrit la réflexion sur écriture et capacité en arithmétique, sans fournir un résultat de prévision financière.

Cinq initialisations sont proposées. Elles mesureraient une variabilité d'optimisation ; elles ne créeraient pas cinq histoires de marché indépendantes. Budgets, distributions d'initialisation, optimiseur, arrêt et diagnostics de convergence restent à fixer avant le gel prédictif.

<!-- pagebreak -->

## 9. Sorties, pertes et témoins

Les sorties sont sept quantiles du prix brut : 0,05 ; 0,10 ; 0,25 ; 0,50 ; 0,75 ; 0,90 ; 0,95, pour trois horizons. Une tête de 21 nombres génère des coordonnées ordonnées par incréments softplus ; le retour au prix est `q=P_i*exp(s_i*sqrt(h)*z)`. La médiane n'est pas assimilée à une espérance.

L'objectif proposé moyenne la perte pinball sur actifs, horizons et quantiles, divisée par `P_i*s_i*sqrt(h)`. Le critère primaire reste l'horizon 1. Pertes natives, MAE de médiane, couverture et largeur des intervalles complètent ce score. Sept quantiles ne décrivent ni toute la distribution, ni une loi jointe de trajectoires. La [théorie des scores propres](https://doi.org/10.1198/016214506000001437) ne rend pas cette sortie partielle complète.

| Témoin non exécuté | Définition et rôle |
|---|---|
| B0 | Quantiles tous égaux à P_i : persistance, distribution dégénérée. |
| B1 | Logarithme à drift nul : q=P_i exp(s_i sqrt(h) Phi inverse(tau)). Médiane P_i ; moyenne P_i exp(h s_i²/2). |
| B1m | Retirer h s_i²/2 dans l'exponentielle de B1 : moyenne P_i sous la loi supposée. |
| B2 | Quantiles de 256-h variations historiques transformées en prix terminaux ; interpolation linéaire dans l'espace des prix. |
| B3 | Ridge sur 20 incréments récents standardisés et log(s_i), avec résidus de prévisions chronologiques pour les quantiles. |

B3 possède 21 caractéristiques avec l'actif seul, 126 avec six actifs. Sa standardisation utilise seulement l'ajustement. Les résidus de calibration sont prévus sur 2005-2009 ; chaque ajustement ne voit que les cibles antérieures à l'année prévue. Les calendriers donnent par actif 1 255 / 1 239 / 1 179 résidus potentiels aux horizons 1/5/20. Aucun résidu ni coefficient n'a été calculé.

Le développement choisira alpha parmi 0,0001 ; 0,01 ; 1 ; 100, séparément pour B3 propre et croisé, avant gel. Les formules intégrales restent dans la note des témoins. B2 suit [NumPy, méthode linear](https://numpy.org/doc/2.3/reference/generated/numpy.quantile.html) ; interpoler les logarithmes puis exponentier donnerait en général un autre témoin.

Ces témoins sur prix non quantifiés évaluent le dispositif complet, sans avoir exactement l'information de Q/H+. Des blocs de 60 publications, sensibilités 20/120 et rééchantillonnage conjoint des actifs sont proposés pour l'incertitude ; cela ne supprime ni dépendances résiduelles ni effets des essais multiples.

<!-- pagebreak -->

## 10. Revenir ensuite au prochain token

P1-A étudie l'écriture du passé avec une tête commune. P1-B doit reprendre l'intuition complète : produire les éléments suivants d'une trajectoire. Le découpage est méthodologique ; il ne remplace pas l'ambition du modèle de langage de marché.

Le flux doit préciser son token : variation, palier, composant de bougie, événement ou paquet temporel. Un vocabulaire appris pourrait retenir des motifs, mais devrait être construit seulement sur l'ajustement, en distinguant reconstruction et prévision. Les schémas grossier/fin ont une antériorité dans [Kronos](https://arxiv.org/html/2508.02739v1) : leur simple présence ne constitue pas une invention nouvelle.

Une piste conceptuelle est un codage différentiel à état reconstruit. Pour u_t=log(P_t), calculer `e_t=u_t-u_hat_(t-1)`, quantifier e_t en q_t au pas delta, puis mettre à jour `u_hat_t=u_hat_(t-1)+q_t`. Avec état synchronisé, sans saturation ni erreur de transmission, l'erreur est `u_hat_t-u_t=q_t-e_t`, de valeur absolue au plus delta/2. Elle ne s'accumule pas comme les erreurs de quantification de vrais incréments.

Cette propriété relève du codage prédictif classique, dont [Gray, chapitre 10](https://ee.stanford.edu/~gray/lpcip.pdf) fournit une référence. Elle ne borne pas l'erreur quand un modèle devine q_t. L'encodeur historique voit u_t ; le prédicteur futur ne le voit pas. Une preuve de codec n'est donc pas une preuve de prévision.

Pour un flux progressif, l'état grossier doit être reproductible sans les détails fins omis. Un résidu grossier calculé depuis un état fin inconnu du décodeur casserait ce contrat. Plusieurs états synchronisés ou une construction fondée sur l'état grossier sont des options à formaliser.

D'autres pistes restent recevables : franchissements de seuil plutôt que secondes régulières, cohérence entre plusieurs écritures, tâches auxiliaires d'addition ou de reconstruction géométrique. Elles peuvent modifier optimisation et résolution, sans créer les nouvelles observations indépendantes nécessaires à une preuve de généralisation.

Avant P1-B, il faudra arrêter la comparaison entre vraisemblance de symboles, trajectoires reconstruites et scores du prix. Un vocabulaire plus fin augmente certaines difficultés de codage ; comparer uniquement les pertes next-token de vocabulaires différents serait insuffisant.

<!-- pagebreak -->

## 11. Diversité, puissance et décisions scientifiques

H1 compare partage de paramètres entre actifs et modèles séparés, avec le seul passé de l'actif cible. H2 compare contexte croisé et contexte masqué, dans des modèles entraînés séparément selon leurs entrées autorisées. Une permutation arbitraire d'actifs n'est pas automatiquement un témoin nul valide : leurs dépendances et calendriers comptent.

Changer de numéraire produit des relations algébriques, sans créer des marchés indépendants. Un état latent partagé peut être une représentation efficace sans identifier une cause économique unique. Gain prédictif, cohérence entre actifs et interprétation causale sont trois conclusions différentes.

Les six histoires mensuelles de matières premières 1960-2020, dont l'or, ne contiennent pas le chemin intramensuel. Métadonnées et changements de définition font partie du langage. Les sources fines qualifiées dans 09 doivent encore fournir des échantillons contrôlés avant de conclure à une couverture à la seconde pour les crises envisagées.

Le passage à l'échelle devra varier capacité, observations distinctes, diversité, contexte et précision. Répétitions et actifs fortement corrélés doivent être comptés à part. Il faut rechercher courbes d'apprentissage, saturation et changements de classement entre langues, avec budgets de recherche comparables et trace des essais.

| Observation future | Conclusion autorisée et suite |
|---|---|
| Condition d'information ou de causalité violée | Réviser le protocole avant d'attribuer un score au langage. |
| Apprentissage insuffisant même sur l'ajustement | Examiner optimisation et capacité ; le test ne réfute pas la langue. |
| Ajustement bon, développement décevant | Examiner surajustement, régimes et représentation dans les conditions testées. |
| Gain sur corpus déjà exploré | Résultat exploratoire à reproduire après gel sur observations indépendantes. |
| Gain robuste après réplications prévues | Preuve locale pour le dispositif testé ; aucune universalité automatique. |

Le droit de réviser un langage doit s'accompagner de règles de poursuite annoncées. Sinon chaque déception pourrait être attribuée indéfiniment au manque de calcul, rendant l'hypothèse impossible à confronter aux observations. Les seuils chiffrés ne sont pas encore arrêtés : aucun budget ou niveau de puissance statistique n'est inventé sans étude de son adéquation.

<!-- pagebreak -->

## 12. Panel, traçabilité et prochaine étape

Le neuvième passage du panel est **simulé**, conduit par le principal. Les profils des documents 05 et des notes sont des rôles critiques, pas des experts humains consultés. Les récentes tentatives de relecture par agents auxiliaires ont échoué sur une limite de service ; aucune approbation indépendante n'en est déduite.

| Objection du panel simulé | Réponse retenue |
|---|---|
| « Le vocabulaire écrit l'extrême, donc le cas est traité. » | Vérifier aussi que les paramètres utilisés ont reçu des exemples de la tâche. |
| « L'hybride résout la prévision. » | Il corrige une confusion ; aucune performance n'est mesurée. |
| « Même information implique même score. » | Même risque idéal sous bijection, mais pas même apprentissage à capacité et données finies. |
| « Huit millions de valeurs font un grand corpus. » | Ce sont des présentations répétées de 33 672 prix distincts. |
| « Réviser après lecture des données invalide tout. » | La révision est exploratoire et archivée ; une confirmation indépendante reste nécessaire. |

Le protocole courant est `research/trame_protocol_p1d/protocol_candidate.json`, identifié 0.3. Ses versions 0.1 et 0.2 sont conservées. L'audit descriptif et son diagnostic postérieur ont leurs propres plans, snapshots, empreintes et rapports dans audits/preflight_01. Les cinq notes du 15 octobre conservent dérivations et formules détaillées, avec avertissement sur l'ancienne proposition 0.2.

Les tests de calendrier, d'arithmétique et d'intégrité déjà réalisés ne sont pas des tests de modèle. Cette publication consolide les résultats sans refaire les acquisitions ou mesures. Les anciens dossiers et archives restent conservés. Les mois réservés du premier corpus de reconstruction restent non ouverts.

**Prochaine étape de conception :** fixer sensibilités numériques, initialisations, budgets d'optimisation, diagnostics de convergence et règles de sélection, puis préciser P1-B avec un état causal autonome. Le contrat d'évaluation indépendante et l'extension multi-marchés devront être résolus avant toute affirmation de fiabilité.

La proposition actuelle est un programme de comparaison contrôlée, appuyé sur des données réelles et déjà amendé par elles. Le langage final reste à découvrir. La preuve recherchée porte sur la prévision de nouveaux prix, avec une chaîne explicite entre information, représentation, apprentissage et évaluation.
