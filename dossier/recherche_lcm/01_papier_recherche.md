# TRAME : langage, état de marché et prévision des trajectoires

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
