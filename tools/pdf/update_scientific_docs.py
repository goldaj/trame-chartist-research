from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'dossier/recherche_lcm'
docs={}
docs['00_synthese_accessible.md']='''# TRAME : apprendre les structures du Marché

## La recherche en trois pages

**Version scientifique 2, 14 octobre 2026. Le dossier précédent reste archivé ; ses conclusions sont révisables. Aucun modèle prédictif n'a encore été entraîné.**

Votre demande est de construire une théorie puis un programme expérimental pour apprendre les courbes comme un modèle GPT apprend des séquences. Il faut trouver le langage numérique, les données et l'architecture permettant d'anticiper la suite des prix. L'objet est scientifique : quelles structures existent, lesquelles sont apprenables et comment les mesurer sur des observations nouvelles ?

**TRAME** reste un nom de travail. Il évoque les relations entre actifs, époques et échelles de temps. Le projet doit pouvoir porter sur l'or, les indices, les actions, les devises et d'autres marchés suffisamment documentés. Les choix du premier petit échantillon ne fixent pas sa destination.

### Deux intuitions deviennent deux expériences

Première possibilité : chaque actif parle sa langue. Un modèle commun apprend plusieurs langues, mais utilise surtout le passé de l'actif qu'il doit prévoir. Cette mise en commun peut aider un instrument peu documenté grâce aux motifs appris ailleurs.

Deuxième possibilité : les actifs sont des observations différentes d'un état de marché partagé. Ils ne racontent pas exactement la même chose : certains réagissent à la monnaie, d'autres à la croissance, à une entreprise ou à une offre physique. Le modèle chercherait ce qu'ils partagent tout en conservant leurs particularités.

Nous comparerons donc un modèle par actif, un modèle partagé sans information croisée, puis un modèle qui observe plusieurs actifs simultanément. Cette distinction est essentielle : bénéficier de beaucoup de courbes pendant l'entraînement ne prouve pas que leurs mouvements simultanés aident à prédire.

### À quoi ressemble le langage ?

Une bougie devient un objet structuré : ouverture relative au dernier prix, corps signé, mèches, activité, durée et état de disponibilité. On peut représenter ses nombres continûment, les découper en paliers ou apprendre un vocabulaire. Les horizons et les unités accompagnent le contenu.

Une image de courbe, des pourcentages et une suite de signes mettent en valeur des propriétés différentes. Leur qualité se mesure par leur capacité à faciliter l'apprentissage. Une représentation simple peut bien généraliser ; une représentation détaillée peut préserver un petit signal que la première efface. Nous ne choisissons pas par analogie littéraire seule.

<!-- pagebreak -->

## Pourquoi privilégier un GPT et beaucoup de données ?

Un Transformer peut apprendre des dépendances entre des événements éloignés et entre plusieurs séries. Nous le retenons comme architecture principale à étudier. L'idée proposée est un GPT hiérarchique : détails récents à la seconde si disponibles, passé plus ancien regroupé en minutes, heures et journées, puis échanges d'information entre actifs. Les fenêtres ne contiennent que ce qui était observable à leur date.

Il ne faut pas confondre le principe GPT avec l'obligation de transformer chaque nombre en mot ou de générer un symbole à la fois. Des sorties continues et des prévisions par blocs restent possibles. Des architectures récurrentes et des modèles simples serviront de comparaisons, sans devenir le centre du projet.

**Votre objection au petit POC est retenue : une mauvaise prévision avec un petit réseau ne condamne pas son langage.** Il faut varier séparément taille du réseau, quantité de données, diversité des actifs, longueur du passé et précision de l'encodage. Nous chercherons des courbes de progression, pas un verdict après un seul essai.

La littérature observe déjà des effets d'échelle sur des séries temporelles, mais pas une garantie universelle sur les prix financiers. Plus de calcul peut aider à exploiter une information difficile ; il ne suffit pas à recréer une amplitude effacée par un encodage, ni une nouvelle extérieure jamais observée. Les documents 01, 05 et 08 développent cette distinction.

### Plusieurs histoires et plusieurs vitesses

Les épisodes de 2000, de 2008 et de la pandémie sont des contextes utiles. Nous voulons aussi des périodes ordinaires : un modèle entraîné presque uniquement sur les crises apprendrait une fréquence de crise artificielle. Les événements servent à vérifier la robustesse ; leurs noms attribués après coup ne deviennent pas des informations disponibles avant qu'ils surviennent.

Une longue histoire quotidienne et une histoire plus récente à la seconde sont complémentaires. Transformer artificiellement une observation quotidienne en milliers de secondes n'ajoute rien. À une seconde, les pauses de cotation, les observations inchangées et les différences de calendrier doivent être représentées explicitement.

<!-- pagebreak -->

## Ce que cette mise à jour apporte réellement

Le dossier donne maintenant une formulation du Marché latent, une architecture GPT à tester, un programme d'étude du passage à l'échelle et une séparation nette entre qualité du langage et qualité de prévision. Le document 08 est le nouveau centre théorique ; les documents 03 et 04 décrivent les moyens et l'ordre des expériences.

Une première étude de mesure a été effectuée sur des observations réelles. Elle encode des bougies puis les reconstruit : elle ne prévoit pas leur suite. Le document 07 rapporte les résultats, les données exclues et les limites. Les scripts utilisés sont des instruments de cette analyse, pas un prototype de modèle entraîné.

Un résultat mérite déjà notre attention : un vocabulaire peut être précis en moyenne et déformer fortement des mouvements rares. Cela motive des mots spéciaux pour les extrêmes, des résidus continus ou plusieurs niveaux de précision. Ces propositions doivent être testées ; elles ne sont pas déjà validées.

### Comment lire et contester le dossier

Lisez ensuite le document 08 pour les deux hypothèses sur les actifs et l'architecture, puis l'atlas 02 pour les encodages. Le papier 01 pose les objectifs et les équations ; le document 05 explique comment éviter les mauvaises conclusions. Le document 06 situe les antériorités et les sources. Le tutoriel 04 ordonne le travail futur.

Les points de vue du panel sont simulés et les relectures entre agents logiciels sont identifiées. Aucune consultation d'experts humains ni validation par les pairs n'est revendiquée. Une convergence entre ces avis ne remplace pas une expérience.

La prochaine preuve importante sera une amélioration de prévision hors échantillon, attribuable à une représentation ou à une architecture donnée. Pour cela, il faut un corpus multi-marchés correctement documenté, des sorties comparables et une expérience qui sépare l'effet du langage de celui de la puissance. Une conclusion négative précise sera conservée comme une information sur les conditions testées ; elle ne mettra pas automatiquement fin au programme.
'''

docs['01_papier_recherche.md']='''# TRAME : langage, état de marché et prévision des trajectoires

## Proposition scientifique révisée

**Version 2 du 14 octobre 2026. Programme de recherche, résultats descriptifs limités au document 07, aucune expérience prédictive exécutée. Cette version remplace le cadrage applicatif de la première étude.**

## Résumé

Nous étudions l'apprentissage auto-supervisé des trajectoires de prix au moyen de modèles de séquences de type GPT. L'hypothèse centrale n'est pas qu'une figure chartiste possède un nom, mais qu'une représentation adéquate d'observations multi-actifs et multi-échelles permet d'apprendre des régularités transférables. Deux mécanismes sont distingués : mutualiser l'apprentissage de langues propres aux actifs ; inférer un état latent partagé dont chaque actif constitue une observation partielle. Ils exigent des expériences différentes.

La contribution proposée est un programme reliant précision de représentation, prévision probabiliste, information inter-actifs et passage à l'échelle. Le langage peut être discret, continu ou hybride. L'architecture principale proposée est un Transformer hiérarchique à attention temporelle et inter-actifs, avec masques de disponibilité et sorties géométriquement cohérentes. La priorité au GPT est une hypothèse de travail, pas un résultat comparatif.

Le programme vise les prix observés et leurs trajectoires futures sur plusieurs familles de marchés. Les critères sont l'exactitude, la calibration, la dépendance temporelle, le transfert et la robustesse. Aucun résultat présenté ici n'établit l'existence d'une régularité prédictive nouvelle. Une expérience de reconstruction vérifie seulement certaines propriétés des langages proposés.

## 1 Ce qui est transposé du langage

L'analogie comporte quatre objets : un corpus d'observations, des unités de représentation, un objectif de prédiction et des compétences transférables. Elle n'exige ni mots français, ni modèle préentraîné sur Internet. Une bougie est un paquet de mesures ; un segment est un groupe d'observations ; une séquence est un contexte historique. Une série entière ne correspond donc pas naturellement à un unique token ni nécessairement à une unique langue.

Le préentraînement génératif de GPT était déjà conçu pour transférer des représentations vers d'autres tâches. L'émergence ultérieure de capacités complexes motive l'étude d'autres domaines, mais n'implique aucun théorème d'émergence universelle. [GPT, travail initial](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf).

Le texte et les prix sont produits par des processus différents. Les prix reflètent des interactions, des règles institutionnelles et des informations extérieures incomplètement observées. Une distribution prévisible peut porter sur la dispersion ou les dépendances sans rendre la prochaine variation déterministe. Nous devons mesurer les composantes prévisibles séparément, au lieu de demander au score global de répondre à toutes les questions.

## 2 Objet mathématique et information disponible

Pour l'actif a, X[a,t] regroupe les observations portant sur un intervalle terminé à t. Chaque observation possède aussi une date de disponibilité d[a,t]. La filtration F_t contient seulement les observations dont d[a,s] <= t, ainsi que les métadonnées connues à t. Nous visons une loi jointe :

`p_theta({P[a,t+h]} pour a dans A et h dans H | F_t)`

P est un prix observé précisément défini : dernière transaction, cours de référence, indice calculé ou autre mesure documentée. Ces objets ne sont pas interchangeables. H contient des horizons physiques, par exemple 1, 10 et 60 secondes sur une branche fine, puis 5 minutes, 1 heure et 1 jour sur d'autres expériences. Ces valeurs sont des propositions, pas les horizons d'un test déjà effectué.

Pour un prix strictement positif, on peut prévoir les accroissements `r[a,t,h]=ln(P[a,t+h]/P[a,t])`, puis reconstruire les prix par l'ancre P[a,t]. Cela conserve l'objectif prix brut tout en contrôlant les différences d'échelle. Si un instrument peut prendre une valeur nulle ou négative, une transformation adaptée telle qu'asinh et son échelle passée doivent être définies ; appliquer log de force serait une erreur de domaine.

Les scores seront publiés à la fois dans les unités natives de chaque actif et dans une unité normalisée définie avant le test. Une moyenne d'erreurs en dollars entre des actifs de prix très différents n'est pas un score universel. Une moyenne normalisée seule peut, inversement, masquer une erreur absolue importante. Les deux lectures sont nécessaires.

## 3 Deux hypothèses sur les langues

### H1 : une grammaire partagée, des histoires séparées

On apprend un paramètre commun theta sur de nombreuses séries, mais la prévision de l'actif a utilise uniquement son histoire et ses métadonnées. Des adaptateurs peuvent capturer ses particularités. Ce modèle teste un transfert de paramètres : les courbes d'autres actifs servent de données d'apprentissage, sans apporter nécessairement une observation contemporaine supplémentaire.

Une amélioration de H1 face à des modèles individuels soutiendrait l'existence de régularités réutilisables. Elle ne démontrerait ni un état global du Marché ni des causalités entre actifs. Il faut contrôler le nombre total d'observations, le budget d'optimisation et la taille des réseaux pour attribuer correctement le gain.

### H2 : plusieurs observations d'un état commun

Considérons un état global S_t et un état spécifique U[a,t]. Une écriture conceptuelle est :

`S[t+1] ~ p(S[t+1] | S[<=t], E[<=t])`

`U[a,t+1] ~ p(U[a,t+1] | U[a,<=t], S[<=t], M[a])`

`X[a,t] ~ p(X[a,t] | S[t], U[a,t], M[a], masque[a,t])`

E représente un contexte extérieur disponible ; M les propriétés de l'instrument. Ce modèle n'affirme pas que toutes les courbes sont des traductions exactes. Une information spécifique, un bruit d'observation et un calendrier propre restent nécessaires. L'état commun peut avoir plusieurs facteurs et plusieurs vitesses.

Les modèles à facteurs constituent une antériorité importante : résumer de nombreux prédicteurs par des facteurs puis prévoir une série a été étudié bien avant les Transformers. Notre piste étendrait ce principe par des observations hétérogènes et une dynamique non linéaire, sans revendiquer l'invention de l'idée de facteur commun. [Stock et Watson, 2002](https://www.princeton.edu/~mwatson/papers/Stock_Watson_JASA_2002.pdf).

H2 sera comparée à H1 avec une information croisée autorisée puis supprimée, décalée ou permutée selon des contrôles explicités. Si l'alignement des autres actifs n'apporte rien, la version testée de H2 perd du soutien. Un résultat positif exige de vérifier les décalages de publication et les dépendances triviales entre instruments.

## 4 Ce que puissance et langage peuvent changer

Soit X le passé observé, Z=f(X) son encodage et Y une cible future. À distribution fixe, avec une densité et des entropies finies, la perte logarithmique idéale d'un prédicteur q s'écrit :

`E[-log q(Y|Z)] = H(Y|X) + I(Y;X|Z) + E_Z KL(p(Y|Z) || q(Y|Z))`.

Cette identité suppose Z déterministe de X, ou une randomisation indépendante de Y conditionnellement à X. Elle distingue l'incertitude restante même avec X, l'information prédictive perdue par l'encodage, et l'écart du prédicteur à la meilleure loi conditionnelle basée sur Z. Pour des variables continues, il s'agit de densités relatives à une mesure commune ; des losses de tokens de vocabulaires différents ne sont pas automatiquement comparables.

Augmenter les paramètres, les données et le calcul peut réduire le dernier terme. Ajouter de vraies observations complémentaires peut réduire le premier. Remplacer une quantification destructrice par une représentation plus précise peut réduire le deuxième. À l'inverse, conserver toute l'information n'assure pas qu'un petit réseau saura l'exploiter efficacement.

Le résultat fondamental pour ce projet est donc double : **un échec à petite échelle ne réfute pas un langage ; une promesse de calcul illimité ne prouve pas qu'une information existe dans ce langage.** Aucun des termes idéaux n'est connu exactement sur les marchés réels. Nous étudierons leurs manifestations par ablations et courbes de progression, sans annoncer avoir mesuré l'incertitude irréductible du Marché.

## 5 Construction du langage

Pour une bougie positive, un encodage de base comprend g=ln(O/C_précédent), b=ln(C/O), u=ln(H/max(O,C)), d=ln(min(O,C)/L). Les mèches u et d sont non négatives et peuvent être exactement nulles. Le volume, s'il existe avec une définition fiable, devient v=ln(1+V/V_ref). La référence V_ref et une éventuelle échelle de volatilité sont calculées sur le passé strict.

La reconstruction conserve une géométrie valide par construction. Les marqueurs de zéro, d'absence de donnée, d'absence de transaction et de fermeture du marché restent différents. Une série de cours de référence sans volume ne reçoit pas un volume inventé. Les temps de début, de fin, de disponibilité et le type de mesure sont partie intégrante du langage.

Trois familles principales sont étudiées : vecteurs continus ; vocabulaire appris ou quantifié ; symboles discrets accompagnés d'un résidu continu. Les mots peuvent porter sur un champ, une bougie, un patch ou un événement. Les représentations par signes, ordre, rythme, spectre, graphe ou figures sont des branches d'ablation, avec leur information perdue explicitée dans l'atlas 02.

Une hypothèse nouvelle à éprouver est le **vocabulaire progressif** : un symbole décrit la forme grossière ; des symboles supplémentaires décrivent l'amplitude et un résidu rare. Le nombre de symboles devient variable, mais doit être borné et son coût mesuré. Les détails d'une bougie close peuvent être encodés ensemble ; aucun token disponible avant sa clôture ne doit dépendre de son extrême final.

## 6 Architecture proposée et ordre de génération

La branche principale est un Transformer de type GPT, initialisé pour le domaine temporel. Un encodeur local produit des tokens par actif et par patch déjà achevé. Une attention temporelle accède au passé autorisé. Une attention entre actifs fusionne les observations simultanément disponibles, avec âge de la dernière observation et masque de marché fermé. Des tokens de mémoire à différentes résolutions résument le passé ancien.

La prévision jointe pose une difficulté : un ordre arbitraire des actifs peut introduire un biais. Deux solutions seront confrontées. La première génère un état commun futur puis des états spécifiques, avec dépendances résiduelles autorisées. La seconde génère un bloc de futurs avec un mécanisme joint continu ou discret, en testant sa sensibilité à l'ordre des actifs. Une simple tête indépendante par actif ne suffit pas à revendiquer une loi jointe expressive.

L'attention bidirectionnelle entre données toutes déjà observées peut être admissible. En revanche, un décalage d'une seconde dans la disponibilité réelle peut invalider une relation anticipatrice apparente. Les masques doivent porter sur les dates de disponibilité, pas seulement les indices du tableau. L'agrégation d'une heure ne peut être consultée pendant cette heure comme si son cours de clôture était connu.

La proposition se situe dans une littérature active. Moirai traite plusieurs variables, Chronos-2 étudie le contexte multivarié ; TimesFM-3 propose une alternance d'attention temporelle et inter-séries. Ces références soutiennent des composants possibles, pas une supériorité démontrée pour nos prix. Le document 08 détaille les choix et leurs antériorités. [Moirai](https://arxiv.org/abs/2402.02592), [Chronos-2](https://arxiv.org/abs/2510.15821), [TimesFM-3](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/).

## 7 Objectifs d'apprentissage et évaluation

L'objectif principal sera une prévision probabiliste sur la même cible physique pour tous les langages. Une perte auxiliaire de reconstruction peut stabiliser l'encodeur ; une tâche de correspondance entre vues peut tester le transfert. Leurs poids sont choisis sur validation et publiés. Une tâche auxiliaire facile ne doit pas masquer un mauvais score de prévision.

Une densité continue permet le log-score si ses conventions sont fixées. Des échantillons de trajectoires peuvent être évalués par CRPS marginal et scores multivariés complémentaires ; des quantiles marginaux seuls ne définissent pas la dépendance entre pas futurs. Les erreurs de moyenne, médiane, dispersion et direction seront séparées. Le score principal et ses agrégations sont fixés avant l'ouverture du test.

Un modèle de persistance, des modèles linéaires/factoriels et des modèles de volatilité constituent des références scientifiques. Les Transformers seront comparés à quantité d'information et budget documentés. Une branche récurrente peut mesurer un contraste architectural ; la priorité de travail au GPT ne transforme pas cette préférence en preuve.

Les séparations comportent des dates futures, des actifs non utilisés, une famille de marché réservée et une évaluation prospective. Les changements d'indice, de symbole, de contrat et les actifs disparus sont conservés. Une archive actuelle ne certifie pas à elle seule la version exacte d'une donnée disponible en 2008.

## 8 Étudier les effets d'échelle sans enfermer l'hypothèse

Le plan varie paramètres N, observations originales D, diversité V, contexte L et précision R. Une famille de courbes `loss(N,D,V,L,R)` est plus informative qu'un classement de trois tokenizers à une seule taille. On distinguera budget égal et taille égale, répétitions des mêmes fenêtres et nouvelles observations, apprentissage insuffisamment optimisé et saturation apparente.

Des lois d'échelle ont été observées pour des Transformers temporels. Les expériences d'Edwards et collaborateurs motivent ce programme ; celles de Yao et collaborateurs soulignent aussi que l'architecture modifie le comportement. Elles ne fournissent pas des exposants universels à copier pour les prix à la seconde. [Edwards et al.](https://arxiv.org/abs/2405.13867v2), [Yao et al.](https://arxiv.org/abs/2410.12360v3).

Une courbe plate sur une petite plage de tailles restera un résultat local. Il faudra examiner l'optimisation, l'information, le mélange de domaines et les limites de contexte. Une poursuite peut être justifiée par une hypothèse nouvelle précise ; multiplier les calculs sans diagnostic rendrait l'hypothèse impossible à distinguer d'une affirmation irréfutable. Le document 05 définit cette discipline.

## 9 Ce qui rendrait la recherche nouvelle

Ni le Transformer temporel, ni la tokenisation de bougies, ni le facteur de marché ne sont nouveaux isolément. La contribution pourrait être une expérience démontrant qu'un langage progressif conserve mieux une information prédictive transférable ; une factorisation commune/spécifique améliorant des actifs jamais vus ; ou une loi empirique reliant diversité réelle, résolution et capacité sur plusieurs familles de prix.

Des motifs sans nom humain peuvent être découverts, mais leur nouveauté devra être distinguée de saisonnalités, d'une volatilité persistante et d'artefacts de source. Un catalogue de motifs sera accompagné d'exemples éloignés dans le temps, de contre-exemples et de tests sur des séries réservées. Une attention élevée sur un motif ne constitue ni une explication causale ni une validation de sa prédictivité.

## 10 État des preuves et questions ouvertes

Le programme possède désormais un appareil de reconstruction vérifié sur un petit corpus réel, présenté au document 07. Il ne possède pas encore de résultat de prévision, de transfert multi-marchés ou de passage à l'échelle. Le jeu de calibration initial ne couvre ni la seconde ni les grandes familles d'actifs proposées. Il constitue une vérification méthodologique, pas une réduction de l'ambition.

Les principaux inconnus sont la quantité d'information prédictive accessible, le vocabulaire permettant de l'apprendre efficacement, le degré de partage entre actifs et les besoins de données pour les régimes rares. Ils sont transformés en questions expérimentales dans les documents 04, 05 et 08. Le projet continue en révisant les hypothèses à partir des résultats, sans transformer une intuition prometteuse en certitude préalable.
'''

docs['03_faisabilite.md']='''# Faisabilité scientifique et technique de TRAME

**Version 2, 14 octobre 2026. Cette analyse dimensionne une recherche multi-marchés sur les prix. Les contraintes de l'ancien projet applicatif ne définissent pas le programme. Aucun entraînement neuronal n'est exécuté à ce stade.**

## 1 Ce qui est réalisable, ce qui reste à établir

Constituer des séquences numériques, entraîner un Transformer et prévoir des distributions de prix est techniquement possible. Les incertitudes portent sur l'information disponible, les erreurs d'observation, le transfert entre familles et le comportement avec la taille. Une infrastructure plus puissante traite plus de séquences ; elle ne suffit pas à établir leur diversité ni leur pouvoir prédictif.

Le premier appareil d'analyse a fonctionné localement sur CPU et environ 16 Gio de mémoire physique. Il compare cinq encodages sur des bougies réelles. Cette mesure de faisabilité concerne la préparation des observations et la reconstruction ; elle ne mesure pas le débit d'entraînement d'un GPT. Aucun budget GPU complet ne peut être déduit de cette exécution.

## 2 Construire trois couches d'histoire

| Couche | Question scientifique | Données souhaitées | Limite à traiter |
|---|---|---|---|
| Longue histoire | Transfert entre régimes et décennies | Prix quotidiens ou horaires multi-familles, incluant 2000, 2008 et 2020 lorsque disponibles | Révisions, instruments disparus, changements institutionnels |
| Histoire intermédiaire | Formes, rythmes et dépendances | Minutes et heures sur de nombreux instruments | Calendriers et changements de contrats |
| Détail récent | Information ajoutée par la finesse | Transactions ou cotations permettant des observations à la seconde | Volume massif, prix inchangés, asynchronisme et disponibilité réelle |

Ces couches doivent coexister avec des masques de modalité. On ne fabrique pas une histoire à la seconde à partir de clôtures quotidiennes. Un indice calculé, un futur, un cours de référence et un prix d'action possèdent des conventions différentes. Les instruments apparentés peuvent renseigner un même phénomène sans être des doublons interchangeables.

Une profondeur historique réelle existe au-delà des cryptomonnaies. Le catalogue NYSE Daily TAQ annonce des transactions et cotations historiques depuis 1993, sous accès commercial à qualifier. Cela rend l'étude des années 2000 plausible pour certaines actions, sans certifier que toutes les résolutions et tous les champs aient la même qualité sur chaque période. Aucun achat n'a été effectué. [Catalogue primaire NYSE](https://www.nyse.com/data-products/catalog/daily-taq).

La BCE fournit des cours de référence quotidiens pour de nombreuses devises ; ils offrent une autre famille et une longue histoire. Ils ne possèdent pas une bougie OHLCV native ni un volume de transactions. Le manifeste de la collecte exploratoire, s'il est présent, distingue données reçues et catalogue théorique. Les références scientifiques des sources et leur état d'accès sont au document 06.

Pour l'or et les indices, la prochaine acquisition doit préciser l'instrument visé : référence spot, contrat daté, série de contrats, indice officiel ou autre mesure. Une série continue de futures résulte d'une règle de raccordement ; un ajustement utilisant des contrats futurs peut introduire une information rétrospective. Le raccordement et les prix d'origine doivent rester audités séparément.

## 3 Ordres de grandeur de la seconde

Ces calculs sont des scénarios, pas des volumes déjà acquis. Pour 100 actifs ouverts 24 h sur 24 pendant dix années de 365 jours : 31,536 milliards d'observations à la seconde. Avec vingt champs float32, leur seul payload numérique vaut environ 2,52 To décimaux, avant horodatages, identifiants, masques, index et copies. Pour 1 000 actifs, ce payload devient environ 25,2 To. Une archive comprimée peut être plus petite ; l'espace de travail peut être plusieurs fois plus grand.

Pour 1 000 instruments sur 252 séances annuelles de 6,5 heures pendant dix ans : environ 58,968 milliards d'observations, soit 4,72 To de payload à vingt champs float32. Ce calcul illustre l'effet du calendrier ; il ne représente pas l'ensemble des horaires mondiaux. Le carnet et les messages événementiels peuvent dépasser largement ces tailles.

Le nombre d'observations n'est pas le nombre d'expériences indépendantes. Des secondes sans changement et des centaines d'instruments exposés au même facteur répètent une information. La diversité se mesure par actifs, familles, calendriers, régimes et sources, avec dépendance temporelle et transversale documentée.

## 4 Pourquoi un GPT naïf ne suffit pas

Une journée de 86 400 tokens produit environ 7,46 milliards de paires d'attention par tête et par couche dans une attention dense. Un tableau matérialisé en deux octets par paire représente environ 14,9 Go. Des noyaux efficaces évitent de matérialiser ce tableau entier, mais ne suppriment pas le coût arithmétique quadratique de l'attention dense. Ce calcul exclut projections et activations.

La piste proposée consiste à garder la haute résolution dans un voisinage récent, puis des patches et mémoires plus espacées dans le passé. L'attention inter-actifs doit également être structurée : groupes, facteurs latents ou agrégation en ensembles, plutôt qu'un aplatissement aveugle de toutes les secondes de tous les instruments. Toute compression devient une hypothèse de langage à tester.

Un contexte récent à la seconde, un contexte moyen à la minute et un contexte long quotidien peuvent couvrir des échelles très différentes. Les résumés anciens sont calculés sur des intervalles déjà achevés. Leur qualité se mesure par ce qu'ils permettent de prévoir, pas seulement par leur capacité à restituer les données.

## 5 Calcul et mémoire d'entraînement

L'ordre de grandeur `6 × N × D` opérations pour un entraînement dense de Transformer est un outil de planification approximatif, N étant le nombre de paramètres et D le nombre de tokens effectivement traités. Le coût exact dépend notamment de la longueur du contexte, de l'attention, du batch, des objectifs et du recomputing. Un token financier n'a pas une valeur informationnelle fixe.

À titre arithmétique : 100 millions de paramètres et un milliard de tokens donnent environ 6 × 10^17 opérations selon cette approximation. À 100 téra-opérations soutenues par seconde, cela représente environ 1,7 heure de calcul idéal ; à 10 téra-opérations soutenues, environ 16,7 heures. Ces débits sont des hypothèses, pas une mesure ni une promesse de machine. Chargement, attention longue, évaluations, réplications et essais multiplient le temps total.

La mémoire des seuls états entraînables peut atteindre de l'ordre de 16 à 20 octets par paramètre selon les conventions d'optimiseur et précision ; il faut ajouter activations et buffers. Le débit réel doit être mesuré sur un batch représentatif, avec les masques et la longueur de contexte prévus. Aucun choix définitif de fournisseur ou d'accélérateur ne précède ce microbenchmark.

## 6 Ce qu'un échec signifierait

| Observation | Interprétations possibles | Expérience suivante utile |
|---|---|---|
| Entraînement et validation faibles | Optimisation, capacité, représentation, cible difficile | Vérification sur tâche contrôlée et courbe de taille |
| Entraînement bon, validation faible | Surapprentissage, dérive, fuite de sélection, manque de diversité | Nouveaux blocs temporels et famille réservée |
| Taille accrue sans gain | Données répétées, budget d'optimisation insuffisant, saturation locale | Augmenter nouvelles observations et comparer à calcul équilibré |
| Reconstruction bonne, prévision faible | Préservation d'information sans apprentissage utile | Langage plus structuré, cibles et références séparées |
| Échec d'un vocabulaire grossier | Résidus perdus, pas nécessairement échec du discret | Symbole extrême, précision progressive, résidu continu |

Aucune ligne ne prouve à elle seule que le projet est impossible. En revanche, une suite d'essais doit produire des diagnostics enregistrés. Poursuivre la recherche peut signifier modifier la cible, le corpus ou le mécanisme partagé, et non répéter le même calcul plus longtemps.

## 7 Blocages réels et pistes ambitieuses

Les obstacles concrets sont l'obtention d'une histoire large de qualité, la cohérence des dates de disponibilité, la reconstruction de calendriers et la séparation entre instruments dépendants. La densité à une seconde accroît les exigences de provenance ; elle ne résout pas les ruptures historiques.

Les pistes les plus ambitieuses sont un vocabulaire à précision progressive, un état partagé avec résidu spécifique, une mémoire multi-échelle et une étude conjointe de capacité et diversité. Elles restent techniquement plausibles. Leur valeur scientifique devra être établie face à des modèles plus simples et sur des observations effectivement nouvelles.
'''

docs['04_tutoriel_du_poc_au_systeme.md']='''# Construire TRAME comme programme scientifique

## Tutoriel du premier appareil de mesure au modèle reproductible

**Version 2, 14 octobre 2026. La cible est la prévision des prix sur plusieurs marchés. Les étapes prédictives ci-dessous restent à réaliser ; l'étude de reconstruction du document 07 est la seule expérience quantitative achevée à ce stade.**

## Étape 1 Écrire une question qui puisse recevoir une réponse

Nous commençons par deux questions distinctes. Le partage d'un modèle entre actifs améliore-t-il les prévisions ? L'observation simultanée des autres actifs apporte-t-elle ensuite une information supplémentaire ? La première teste le transfert de grammaire ; la seconde teste une représentation commune de l'état de marché.

La fiche de chaque expérience précise variable de prix, horizon, dates d'information, représentation, architecture, budget, métrique principale et comparaisons. Une hypothèse plus ambitieuse peut rester ouverte après un échec local ; la fiche doit annoncer exactement ce qui est testé pour ne pas lui attribuer une portée universelle.

**Livrable :** fiche d'expérience versionnée avec date de gel. **État :** protocole de reconstruction gelé puis amendé de façon tracée ; fiche de prévision multi-marchés encore à figer.

## Étape 2 Définir les instruments et trois profondeurs historiques

Construire un registre d'actions, d'indices, d'or ou autres matières, de devises et éventuellement d'autres actifs. Pour chacun : type exact de prix, calendrier, devise, unité, durée de disponibilité, champs et droits de recherche. Le choix n'est pas fondé sur le résultat d'un modèle.

Prévoir une couche historique longue, une couche intrajournalière intermédiaire et une couche récente fine. Réserver des familles entières et des dates futures avant d'optimiser les langages. Les épisodes historiques servent à analyser les différences de comportement ; ils ne remplacent pas les périodes ordinaires.

**Livrable :** matrice instruments × périodes × résolutions, où disponible, acquis et validé sont trois états différents. **État :** petit corpus témoin réel vérifié ; corpus scientifique général incomplet.

## Étape 3 Rendre chaque observation traçable

Conserver les fichiers bruts avec URL, date, taille et empreinte ; enregistrer les versions et les corrections. Le schéma normalisé distingue date du phénomène, fin de bougie et première disponibilité connue. Une donnée historique sans heure de publication attestée reste marquée comme telle.

Contrôler doublons, valeurs non finies, unités, ordre temporel, cohérence OHLC, heures absentes et intervalles incomplets. Une fermeture du marché n'est pas une panne de collecte. Les changements de contrat, de symbole et d'indice ont leurs propres métadonnées.

Le premier appareil de mesure a rencontré des bougies qui se terminent avant leur heure attendue. Elles ont été conservées dans le brut, exclues de la comparaison à durée fixe et consignées avant le calcul des métriques. Cet exemple montre pourquoi un checksum ne certifie pas la cohérence temporelle.

**Livrable :** manifeste et rapport de qualité. **État :** réalisés pour le témoin décrit dans le document 07 ; à étendre aux autres familles.

## Étape 4 Tester les langues sans encore confondre avec prévision

Encoder et reconstruire les mêmes observations avec une branche continue, des quantifications fixes ou adaptées, un vocabulaire empirique et un contrôle volontairement pauvre comme les signes. Mesurer la distorsion, en particulier dans les queues, le nombre de symboles et les informations latérales nécessaires.

L'appareil POC0 et ses tests se trouvent dans research/trame_poc0. Le protocole, les empreintes et les résultats JSON permettent de vérifier le document 07. Les données synthétiques présentes dans les tests servent uniquement à contrôler les calculs ; les résultats scientifiques descriptifs utilisent des observations réelles.

Les prochaines variantes de langage ne seront pas ajustées discrètement sur la même validation. Un protocole suivant pourra ajouter un symbole hors plage, une quantification logarithmique des extrêmes et un résidu continu. Il conservera une référence de débit pour inclure l'ancre, les échelles et le codebook.

**Livrable :** atlas expérimental des pertes et invariances. **État :** première comparaison réalisée ; aucun vocabulaire déclaré gagnant pour prévoir.

## Étape 5 Préparer des cibles identiques pour tous les modèles

Séparer input et cible future avec une convention explicite de disponibilité. À la seconde, une cotation arrivée plus tard que la date de prédiction est interdite même si son timestamp d'événement est antérieur. À l'heure, une bougie partiellement observée ne peut être remplacée par sa valeur finale.

Choisir une première cible principale et quelques diagnostics. Les candidats doivent prévoir les mêmes prix ou accroissements aux mêmes horizons. Les losses internes par token restent des diagnostics propres à chaque langage ; le score commun porte sur les valeurs physiques décodées.

**Livrable :** constructeur de cibles audité, inventaire des fenêtres et contrôle des dates. **État :** spécification ; aucun label prédictif n'a été calculé pour les mesures du document 07.

## Étape 6 Construire les références et le premier GPT

Entraîner des références simples puis un premier Transformer de taille modeste. Le choix d'une taille initiale vise à vérifier l'expérience et l'optimisation. Il ne vise pas à prouver qu'un langage échouera à grande échelle.

Comparer A, modèles par actif ; B, paramètres partagés sans contexte d'autres actifs ; C, paramètres partagés avec contexte inter-actifs ; D, facteurs communs et états spécifiques explicites. Conserver les entrées physiques et rendre visibles les différences de budget. Le document 08 fournit les masques, les mécanismes et les ablations proposées.

**Livrable :** prévisions sauvegardées, checkpoints, courbes d'apprentissage et scores. **État :** futur. Aucun réseau n'est encore développé ou entraîné dans cette phase.

## Étape 7 Mesurer le passage à l'échelle

Prendre plusieurs tailles de GPT, plusieurs volumes d'observations originales et plusieurs niveaux de diversité. Mesurer leur interaction au lieu d'augmenter toutes les dimensions à la fois. Conserver une précision d'encodage suffisante ou la faire varier comme un facteur expérimental séparé.

La première grille complète peut coûter cher ; un plan partiel équilibré sert à estimer les tendances, avec répétitions et points de confirmation. Réserver des configurations pour vérifier l'extrapolation. Les exposants d'une loi de puissance resteront empiriques, limités à la plage observée. Ne pas leur faire prédire mécaniquement une capacité future à une taille mille fois supérieure.

**Livrable :** courbes loss/capacité/données/diversité et diagnostic d'optimisation. **État :** programme proposé, développé au document 05.

## Étape 8 Tester le transfert et les événements rares

Évaluer des actifs et familles réservés, puis des périodes non utilisées. Les observations d'une même crise sur cent actifs partagent un contexte ; elles ne donnent pas cent crises indépendantes. Les intervalles d'incertitude doivent respecter la dépendance en blocs temporels et entre actifs.

Tester la calibration, les queues et les dépendances de trajectoire séparément. Une moyenne favorable peut cacher un échec sur une famille. Une mauvaise moyenne sur un régime nouveau ne dit pas automatiquement si le langage est mauvais : étudier l'information manquante, la représentation et l'adaptation autorisée.

**Livrable :** rapport de transfert et de robustesse, y compris résultats négatifs. **État :** futur.

## Étape 9 Confirmer avec des observations futures

Enregistrer les distributions avant que leurs cibles ne soient observées. Geler les versions, la fréquence des rapports et les critères d'analyse. Une prévision postérieurement reconstruite à partir d'une archive actuelle ne remplace pas cette étape.

**Livrable :** expérience prospective de prévision, reproductible et datée. **État :** futur. Son rôle est scientifique : mesurer hors des choix rétrospectifs de la recherche.

## Étape 10 Mettre à jour les documents après chaque expérience

Pour chaque itération, conserver la version précédente puis mettre à jour la synthèse, le papier, l'atlas, la faisabilité, le tutoriel, le panel et les sources. Ajouter un rapport distinguant prévu, exécuté, observé et interprété. Tout amendement indique son motif et ce qui avait déjà été vu au moment du changement.

Le journal d'expérience doit permettre de répondre à trois questions : quelle observation a fait changer d'avis ; quelle explication concurrente reste possible ; quelle expérience pourrait la départager ? Cette pratique rend les documents révisables et utiles, au lieu de les transformer en conclusions figées.
'''

for name,body in docs.items():
    (D/name).write_text(body,encoding='utf-8')
    print(name,len(body.split()))
