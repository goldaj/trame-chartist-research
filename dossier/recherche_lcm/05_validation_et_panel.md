# TRAME — Validation scientifique, panel critique et programme d'échelle

**14 octobre 2026. Version révisée selon le recadrage scientifique du projet.** Les prix réels bruts, la généralisation entre actifs et temporalités, et l'apprentissage par GPT constituent le cœur de l'étude. Le panel est simulé ; les échanges entre agents logiciels sont identifiés séparément. Les expériences proposées ne sont pas présentées comme réalisées.

## 1. Contrat scientifique de cette version

L'objet est de comprendre ce qu'un modèle génératif peut apprendre des structures du marché, depuis des observations à la seconde jusqu'à une histoire longue, sur plusieurs familles d'actifs. Les métaux, indices, devises et autres marchés ne doivent pas être traités comme de simples copies de la crypto. Leurs unités, calendriers, sources et fréquences de publication font partie de la définition des observations.

Le choix prioritaire est un Transformer décodeur causal de type GPT. Il n'est pas nécessaire qu'un RNN ou une régression réussisse auparavant pour que cette hypothèse mérite une expérience. Les modèles simples sont des repères pour mesurer un gain ; ils ne décident pas du potentiel ultime d'un langage. Une erreur de reconstruction, un échec à petite capacité et une absence d'amélioration avec beaucoup de données sont trois résultats différents.

Les critères de cette version portent exclusivement sur la validité de l'information, la prévision probabiliste, la représentation, le transfert et les lois d'échelle. Une plage de calcul bornée fixe ce que nous pouvons mesurer ; elle ne fixe pas une limite arbitraire à ce qui pourrait être appris au-delà. La note théorique intégrée à partir de la section 5 fournit les équations, les expériences et les conditions d'invalidation.

## 2. Dix profils fictifs pour une contradiction structurée

**Aucun des profils suivants n'est une personne interrogée.** Ce sont des rôles imaginaires qui organisent des objections complémentaires. Leurs arguments sont rédigés par l'assistant ; ils ne constituent ni dix avis indépendants ni une revue par les pairs.

| Profil fictif | Compétence et usage du projet | Objection centrale | Preuve qu'il demanderait |
|---|---|---|---|
| **Léa, probabiliste et théoricienne de l'information** | Étudie ce qui peut être conservé par une transformation du passé et prédit par une distribution conditionnelle. | « Un plateau d'un réseau ne mesure pas l'entropie irréductible du processus. » | Une décomposition des risques, des hypothèses explicites et une distinction entre borne mesurée et limite démontrée. |
| **Malik, chercheur en Transformers génératifs** | Conçoit des GPT qui apprennent des séquences numériques à plusieurs tailles et longueurs de contexte. | « Une langue peut être difficile pour le petit réseau et devenir efficace quand sa capacité augmente. » | Croisement langue × capacité, optimisation qualifiée, courbes complètes et cellules supérieures réservées à la vérification. |
| **Nadia, statisticienne des plans d'expérience** | Veut attribuer un gain à une cause et estimer la précision de cette attribution. | « Si modèle, données, contexte et budget changent simultanément, le résultat n'explique rien. » | Plan factoriel, comparaisons appariées, réplications, tests extérieurs et registre des choix. |
| **Inès, spécialiste des observations de marché** | Réconcilie prix publiés, timestamps, unités, calendriers et modifications historiques entre sources. | « Une seconde dans un fichier n'est pas nécessairement une nouvelle mesure du prix. » | Provenance, fréquence réelle, masques de disponibilité, distinction entre valeur inchangée, valeur maintenue et absence d'observation. |
| **Clément, physicien des systèmes complexes** | Recherche des régularités communes, des états latents et des transitions de régime. | « Un latent utile n'est pas nécessairement l'unique état causal du marché. » | Hypothèses d'identifiabilité, prédictions réfutables et bénéfice de transfert au-delà d'une visualisation de clusters. |
| **Jonas, chercheur en apprentissage multilingue et multitâche** | Examine les actifs comme langues ou dialectes et mesure les gains de partage. | « Ajouter des domaines peut aider la généralisation ou créer du transfert négatif. » | Courbes de quantité locale, familles entièrement exclues, mêmes budgets et scores par domaine. |
| **Mei, chercheuse en séries temporelles à haute résolution** | Étudie les dépendances entre observations rapprochées et l'effet du choix d'horloge. | « Davantage de points très corrélés ne remplace pas une histoire plus diverse. » | Comparaison de durée, résolution et contexte ; horizons calendaires communs ; absence de données fines inventées par interpolation. |
| **Sara, responsable de reproductibilité scientifique** | Cherche à reproduire chaque courbe d'échelle et chaque représentation avec les mêmes observations. | « Un codebook, une partition ou un schedule modifié silencieusement suffit à changer la conclusion. » | Versions, hashes, règles d'ajustement, seeds, exposition réelle aux données et conservation des essais non retenus. |
| **Georges, historien quantitatif des marchés** | Compare les mécanismes et régimes sur des périodes longues et plusieurs classes d'actifs. | « Une décennie et une famille ne constituent pas un univers représentatif de toutes les structures possibles. » | Calendriers et familles exclus, corpus décrit par mécanismes et périodes, limites explicites des généralisations. |
| **Élodie, porteuse du projet et lectrice non spécialiste** | Veut comprendre pourquoi une expérience réussit, échoue ou reste indéterminée sans devoir accepter un jargon comme preuve. | « Comment distinguer un mauvais alphabet, un modèle trop petit et un futur simplement encore mal expliqué ? » | Expériences qui isolent ces causes, résultats en prix compréhensibles et formulation précise de ce qui est acquis ou encore ouvert. |

## 3. Six cycles conceptuels de contradiction

Les cycles ci-dessous constituent une structuration explicite du raisonnement et de ses révisions. Ils ne simulent pas des résultats de calcul. Les objections attribuées aux profils sont fictives ; les décisions de conception sont les recommandations du dossier.

### Cycle 1 — Passer de l'analogie à une question mesurable

**Hypothèse :** une succession de prix peut être apprise comme une succession de mots.

**Objections simulées :** Léa demande quelle variable est prédite et quelle information est disponible ; Élodie demande ce qui compterait comme une réussite. Malik rappelle que l'architecture GPT peut être utilisée sans mots français ni tokenizer linguistique.

**Révision :** définir une distribution de futurs prix conditionnée par un passé admissible ; conserver une cible commune pour comparer les langues. L'analogie guide une architecture et un objectif d'apprentissage, mais ne démontre pas l'existence d'une grammaire universelle.

**Inconnue :** quelles structures du corpus seront apprises et transférables ?

### Cycle 2 — Séparer information conservée et facilité d'apprentissage

**Hypothèse :** la meilleure langue est celle qui reconstruit le mieux les prix.

**Objections simulées :** Léa distingue réversibilité et suffisance prédictive ; Malik souligne qu'un encodage exact peut être difficile à apprendre ; Nadia demande une comparaison à capacité et histoire source définies.

**Révision :** garder un canal de prix brut exact comme référence, mesurer la perte des autres langues et comparer leurs courbes à plusieurs capacités. La reconstruction devient un diagnostic, jamais le classement final des facultés prédictives.

**Inconnue :** quelle compression élimine du détail inutile et laquelle supprime une information réellement prédictive ?

### Cycle 3 — Rendre les temps et les corpus admissibles

**Hypothèse :** davantage de séries et des points à la seconde suffisent à fournir beaucoup plus de données.

**Objections simulées :** Inès distingue observations, remplissage et répétitions ; Mei distingue densité temporelle et histoire ; Sara relève les fuites par normalisation, segmentation et séries corrélées contemporaines.

**Révision :** enregistrer les temps de publication, la disponibilité et la résolution réelle ; employer des coupures calendaires globales ; compter séparément observations uniques, tokens présentés et périodes représentées. Une courbe quotidienne ne devient pas un historique réel à la seconde par interpolation.

**Inconnue :** quelle couverture fine et longue existe réellement pour chaque famille, et quel contexte le modèle peut-il exploiter ?

### Cycle 4 — Mettre les langues et le marché latent en concurrence

**Hypothèse :** chaque actif constitue une langue, ou toutes les séries expriment un Marché latent commun.

**Objections simulées :** Jonas demande des tests de transfert et de transfert négatif ; Clément rappelle la non-identifiabilité possible du latent ; Georges réclame des familles et régimes réellement différents.

**Révision :** comparer modèles locaux, backbone partagé avec dialectes et représentation commune ; mesurer les courbes d'adaptation sur familles tenues à l'écart. Un latent partagé qui prédit bien peut être scientifiquement utile sans prétendre être l'état véritable et unique du marché.

**Inconnue :** quelle part des structures est commune, spécifique ou variable dans le temps ?

### Cycle 5 — Ne pas condamner une langue avec un petit modèle

**Hypothèse :** une représentation faible dans le premier POC doit être écartée.

**Objections simulées :** Malik demande le contraste langue × capacité ; Nadia sépare quantité, diversité et optimisation ; Léa refuse d'identifier le plateau à une limite fondamentale.

**Révision :** conserver des langues contrastées dans plusieurs régimes de capacité et de données, qualifier l'entraînement, tester le contexte et réserver des cellules supérieures pour évaluer les extrapolations. Les modèles simples restent des contrôles de mesure ; ils ne disposent d'aucun droit de veto sur l'hypothèse GPT.

**Inconnue :** le classement des langues se stabilisera-t-il, se croisera-t-il, ou dépendra-t-il durablement de la famille et de l'horizon ?

### Cycle 6 — Recadrage explicite vers la science des prix et de l'échelle

**Nouvelle priorité de l'utilisateur :** étudier les prix bruts de plusieurs marchés, leur histoire longue et leurs observations fines ; privilégier GPT ; garder ouvertes les hypothèses de langues distinctes et d'une structure latente commune.

**Objections simulées :** Georges refuse que la seule disponibilité initiale d'un corpus définisse tout l'objet scientifique ; Mei demande des temporalités réellement observées ; Élodie veut que la puissance de calcul ne soit ni ignorée ni invoquée comme promesse infinie.

**Révision :** le programme central devient l'étude des interactions représentation × capacité × quantité × diversité × contexte. Les critères portent sur information, généralisation, calibration, transfert et prédiction des lois d'échelle. Les budgets définissent une plage d'expérience ; les verdicts décrivent cette plage. Le prochain essai est choisi pour départager les explications restantes, sans abandon arbitraire ni certitude de réussite universelle.

**Inconnue :** quelles facultés apparaîtront à une autre échelle, avec quelles données et quelles limites ? La note intégrée ci-dessous fournit le dispositif pour répondre progressivement à cette question.

## 4. Ce qui a réellement été fait et ce qui reste proposé

Des agents logiciels ont effectivement mené des recherches bibliographiques, écrit des analyses distinctes et échangé des critiques. La relecture de l'article de conception a demandé de préciser le sens d'intégration du flow matching, la différence entre horizons événementiels et calendaires, et les informations nécessaires aux sorties étudiées. La relecture de l'atlas a contrôlé numériquement un exemple d'encodage et relevé les problèmes de références futures, de segmentation BPE et de réversibilité des langues parallèles.

Le présent recadrage a ensuite conduit à une nouvelle analyse théorique et à un plan factoriel. Les références primaires ont été consultées ; aucun corpus n'a été acquis et aucun modèle n'a été entraîné pour cette note d'échelle. Ces échanges logiciels peuvent partager des angles morts : ils ne remplacent pas des expériences, une réplication indépendante ou une revue académique.

Les équations qui suivent sont des identités sous hypothèses explicites ; les plages de modèle, nombres d'expériences et critères proposés restent à fixer dans un protocole avant exécution. Le panel organise la contradiction, mais seul le travail empirique permettra de départager les hypothèses.

## 5. La conclusion à préserver

**L'échec d'un petit modèle ne réfute pas un langage.** Il établit seulement qu'un certain couple représentation–modèle, entraîné avec certaines données, un certain contexte et un certain effort d'optimisation, n'a pas démontré la compétence recherchée dans le domaine testé.

La conclusion inverse serait tout aussi excessive : aucune observation ne garantit qu'un accroissement indéfini de puissance finira par rendre le futur entièrement prévisible. Un programme scientifique doit pouvoir distinguer les causes d'un plateau, quantifier les tendances, reconnaître ce qui reste indéterminé et concevoir l'expérience suivante qui départagera les explications.

L'objectif proposé est donc double : apprendre une distribution des futurs prix et découvrir une représentation transférable des structures du marché. On peut tester si chaque actif se comporte comme une langue distincte, si plusieurs familles partagent des dialectes, ou si les séries observées sont des expressions partielles d'un état latent commun. Ces trois possibilités deviennent des hypothèses concurrentes, et non des métaphores tenues pour vraies.

## 6. Objet scientifique : les prix observés et leur histoire

Notons X l'ensemble du passé admissible : prix bruts réellement observés, horodatages, instrument, unité, fréquence de publication, calendrier de session et masque de disponibilité. Notons Y une trajectoire future définie à une résolution et à des horizons annoncés avant l'expérience. Le modèle apprend une distribution `q(Y | X)`.

La donnée canonique reste le prix brut tel qu'il est publié. L'encodeur peut recevoir un entier décimal exact, des chiffres, des segments de valeurs ou d'autres représentations ; les sorties sont ramenées à la même variable Y pour l'évaluation. Préserver les prix bruts ne signifie pas ignorer leur unité : 100 points d'indice, 100 unités monétaires d'or et un taux de change de 100 ne sont pas la même observation.

Une fréquence de stockage d'une seconde ne prouve pas une nouvelle observation chaque seconde. Une valeur répétée peut être une cotation inchangée, une publication plus lente maintenue à l'écran, une session fermée ou une source interrompue. Le modèle doit distinguer ces situations. Il n'est pas admissible de transformer un historique quotidien ancien en observations « réelles à la seconde » par interpolation, puis de compter ces valeurs comme de nouvelles données.

Un corpus long et un corpus fin répondent à des questions complémentaires. Les données anciennes renseignent des régimes et transitions ; les observations à la seconde révèlent des structures locales. L'architecture peut combiner des fenêtres fines et des descriptions plus lentes de l'histoire, sans prétendre que toutes les résolutions existent sur toute la durée.

## 7. Une décomposition mathématique de la difficulté

### 7.1 Décomposition exacte sous score logarithmique

Fixons une représentation `Z = e_R(X)`, où R désigne la langue. Tous les éléments auxiliaires nécessaires à son interprétation doivent être inclus dans Z. Pour une cible discrète Y évaluée sur une grille commune, et sous les conditions d'intégrabilité usuelles :

`E[-log q(Y|Z)] = H(Y|X) + I(Y;X|Z) + E_Z KL(p(Y|Z) || q(Y|Z))`.

Cette identité s'obtient en ajoutant puis retranchant `log p(Y|Z)` dans le score, et en utilisant `H(Y|Z) - H(Y|X) = I(Y;X|Z)` lorsque Z est une fonction de X.

| Terme | Interprétation | Ce qu'il faut éviter d'en conclure |
|---|---|---|
| `H(Y|X)` | Incertitude restante compte tenu des observations X choisies | Ce n'est pas une propriété métaphysique du marché ; d'autres observations pourraient la réduire. |
| `I(Y;X|Z)` | Information sur Y perdue lorsque le passé X devient la représentation Z | Une mauvaise reconstruction de X ne signifie pas nécessairement une grande perte sur Y. |
| `E KL(p(Y|Z)||q(Y|Z))` | Écart du prédicteur appris à la meilleure distribution accessible à partir de Z | Il mêle capacité, données, optimisation et choix de modèle ; un seul essai ne les sépare pas. |

L'identité suppose **la même cible et la même mesure**. On ne peut pas remplacer le premier membre par des perplexités provenant de vocabulaires financiers différents puis comparer leurs valeurs directement. Pour une cible continue, on travaille avec des densités par rapport à une mesure commune, et des entropies différentielles éventuellement négatives ; les transformations de cible exigent leurs Jacobiennes. Une solution plus facile à auditer consiste à convertir toutes les prévisions en probabilités sur les mêmes intervalles de prix, avec résolution documentée.

Ces identités appliquent les notions d'entropie et d'information ; leur interprétation ne fournit pas un estimateur magique des trois termes. [Shannon, théorie de l'information](https://www.princeton.edu/~wbialek/rome/refs/shannon_48.pdf). Les scores propres donnent un cadre pour évaluer les distributions sans récompenser des probabilités volontairement déformées. [Gneiting et Raftery, 2007](https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf).

### 7.2 Une version sous erreur quadratique

Si Y est un prix futur scalaire de second moment fini, posons `m_X = E[Y|X]` et `m_Z = E[Y|Z]`. Alors :

`E[(Y-f(Z))²] = E[Var(Y|X)] + E[(m_X-m_Z)²] + E[(m_Z-f(Z))²]`.

L'orthogonalité des espérances conditionnelles fait disparaître les termes croisés. Cette version illustre bien les trois niveaux, mais ne mesure que la prévision de moyenne. Une représentation peut conserver la moyenne conditionnelle tout en perdant de l'information sur variance, asymétrie ou dépendances entre horizons. Une étude de distributions ne doit donc pas se limiter à la MSE.

### 7.3 Ce que capacité, données et optimisation ajoutent

Soit `Q_N` une famille de GPT de capacité N, avec représentation R fixée. La meilleure perte théorique dans cette famille vaut `inf_(q dans Q_N) E[-log q(Y|Z)]`. L'écart à `H(Y|Z)` est une erreur d'approximation de la famille.

Le modèle effectivement entraîné subit ensuite l'effet d'un échantillon fini et d'un algorithme d'optimisation. Ces effets se diagnostiquent par interventions expérimentales. Il serait incorrect d'écrire sans conditions une somme de trois erreurs toutes positives « capacité + estimation + optimisation » : un algorithme qui ne minimise pas parfaitement la perte empirique peut mieux généraliser grâce à sa régularisation implicite. La différence de risque entre un modèle optimisé et le minimiseur empirique exact n'est pas nécessairement positive.

On peut toutefois mesurer des contrastes contrôlés : changer N à corpus fixe ; changer le corpus à N fixe ; prolonger l'optimisation à N et corpus fixes ; répéter avec plusieurs initialisations ; modifier seulement la représentation. Le plan factoriel sert à séparer ces effets et leurs interactions.

### 7.4 Pourquoi un plateau ne mesure pas l'incertitude irréductible

La perte d'un prédicteur donne, au mieux et sous incertitude d'estimation, une **borne supérieure** de la meilleure perte possible à partir des observations. Elle ne fournit pas une borne inférieure certifiant qu'aucun meilleur modèle ne pourrait faire mieux.

De nombreuses lois du futur peuvent être compatibles avec une même histoire finie. Sans hypothèses sur la famille de processus, une période sans amélioration ne prouve ni hasard fondamental ni absence d'une structure inaccessible au modèle essayé. Il faut donc utiliser le terme **plancher observé dans le régime expérimental**. Le paramètre de plateau d'une loi ajustée ne doit pas être rebaptisé « entropie véritable du marché ».

## 8. Quatre questions différentes sur le langage

### Réversibilité

Une langue exacte, munie de son état auxiliaire, peut conserver intégralement l'information de X. Cela ne la rend pas facile à apprendre. Des prix encodés chiffre par chiffre peuvent être réversibles mais nécessiter des dépendances différentes d'une projection numérique. Inversement, une représentation compacte avec perte peut rendre une structure plus accessible à un modèle fini.

### Suffisance prédictive

L'idéal est `Y indépendant de X conditionnellement à Z`, équivalent ici à `I(Y;X|Z)=0`. Cela signifie que la langue conserve l'information pertinente pour Y, sans devoir conserver chaque détail de X. Une bonne reconstruction est un diagnostic utile, pas une preuve de suffisance prédictive.

### Accessibilité à capacité finie

Deux langues théoriquement équivalentes peuvent demander des tailles de réseau différentes. Une langue peut perdre avec 8 millions de paramètres et gagner avec 128 millions. Il faut donc rechercher une interaction **langue × capacité**, plutôt que classer une fois pour toutes les langues avec un seul petit modèle.

### Transfert

Une représentation peut mieux généraliser vers une nouvelle famille d'actifs ou une fréquence différente, tout en étant moins bonne sur la famille dominante du corpus. Le classement dépend de la tâche annoncée. Une moyenne globale ne doit pas masquer une détérioration sur un domaine tenu à l'écart.

## 9. Comment distinguer empiriquement les causes d'un plateau

| Explication candidate | Intervention prioritaire | Observation compatible | Ce qu'elle ne prouve pas |
|---|---|---|---|
| Information perdue par le langage | Ajouter le résidu exact ou une vue brute au même encodeur ; comparer plusieurs capacités | Gain persistant des informations omises | La quantité exacte d'information conditionnelle perdue ; une vue supplémentaire peut aussi faciliter l'optimisation. |
| Capacité insuffisante | Augmenter N sur même corpus et même contexte, avec optimisation qualifiée | Meilleure perte extérieure et écart de langue qui se réduit ou s'inverse | Qu'une progression continuera indéfiniment. |
| Quantité insuffisante | Ajouter des observations uniques, même mélange et mêmes périodes admissibles | Courbe de généralisation qui progresse à N fixé | Que répéter les mêmes observations fournirait le même gain. |
| Diversité insuffisante | Remplacer une part du corpus par d'autres familles à volume et temps comparables | Meilleur transfert vers familles exclues | Que chaque domaine bénéficie du mélange. |
| Histoire trop courte | Augmenter l'histoire visible en distinguant résolution et durée | Gain à capacité comparable, surtout sur certaines dépendances | Que tout le passé lointain est utile ou stationnaire. |
| Optimisation insuffisante | Temps d'entraînement accru, schedule qualifié, contrôles d'initialisation | Baisse encore substantielle des pertes de développement | Que le langage était dépourvu d'information. |
| Changement de distribution | Évaluer plusieurs origines temporelles et groupes de régimes | Variations structurées des gains selon les périodes | Un plafond fondamental de prévisibilité. |
| Plafond non identifié | Tous les contrastes mesurés deviennent petits et précis | Saturation empirique dans la plage testée | L'atteinte démontrée du risque de Bayes. |

Les tests de résidu doivent être conçus avec soin. Réencoder une vue brute en parallèle ajoute aussi des paramètres ou des chemins d'optimisation. Ajouter un canal neutre de taille comparable, maintenir l'effort de réglage et répéter sur plusieurs capacités aide à isoler l'information supplémentaire. Aucun contrôle unique n'identifie parfaitement la cause.

## 10. Ce que les travaux d'échelle apportent réellement

| Source primaire | Résultat pertinent | Limite pour TRAME |
|---|---|---|
| Kaplan et al., 2020 | Relations empiriques entre perte, paramètres, données et calcul pour des modèles de langage | Les exposants et allocations ne se transfèrent pas automatiquement aux prix. |
| Hoffmann et al., 2022 | Étude de l'allocation du calcul entre nombre de paramètres et quantité de tokens ; les grands réseaux peuvent être insuffisamment entraînés | Le ratio de tokens par paramètre n'est pas une constante universelle. |
| Muennighoff et al., 2023 | La répétition peut aider dans un régime limité en données, avec valeur marginale décroissante | Des époques répétées ne deviennent pas des années nouvelles de marché. |
| Edwards et al., 2024–2025 | Des Transformers décodeurs temporels présentent des relations d'échelle sur un corpus hétérogène | Ce n'est pas une démonstration d'une loi universelle pour toute famille de prix et toute fréquence. |
| Yao et al., ICLR 2025 | Étudie les comportements dans et hors distribution ; l'architecture influence l'échelle | Le choix GPT est défendable comme axe de recherche, mais sa supériorité générale n'est pas acquise. |
| Dai et al., prépublication du 4 octobre 2026 | Étudie l'interaction de capacité, contexte et horizon ; propose une loi ajustée et une analyse théorique sous régression gaussienne | Travail très récent, hypothèses particulières ; aucune certification d'un plafond des marchés. |

Liens : [Kaplan](https://arxiv.org/abs/2001.08361), [Hoffmann](https://arxiv.org/abs/2203.15556), [Muennighoff](https://arxiv.org/abs/2305.16264), [Edwards, version 2](https://arxiv.org/abs/2405.13867v2), [Yao, version 3](https://arxiv.org/abs/2410.12360v3), [Dai, version 1](https://arxiv.org/abs/2610.05269v1).

Le programme principal peut donc utiliser un **Transformer décodeur causal de type GPT**, sans exiger qu'un RNN réussisse d'abord. Les références simples restent des instruments de mesure : leur victoire sur une petite expérience ne ferme pas l'hypothèse d'un modèle de fondation. Une comparaison d'architecture secondaire peut venir ensuite, à données et calcul documentés.

## 11. Le marché latent commun comme hypothèse mesurable

### 11.1 Trois organisations concurrentes

**M1 — Langues distinctes.** Des modèles ou adaptateurs apprennent surtout des dynamiques propres à chaque actif ou famille. Un apprentissage commun n'apporte qu'un gain faible, voire provoque un transfert négatif.

**M2 — Grammaire partagée et dialectes.** Un backbone GPT apprend des régularités communes ; des identités, embeddings, têtes ou adaptateurs portent les unités, calendriers et particularités locales. Le bénéfice du partage dépend de la famille et de la quantité de données locales.

**M3 — État latent commun.** Les observations sont engendrées par un état partagé et des composantes spécifiques :

`S_(t+1) ~ p(S_(t+1)|S_<=t)`

`U_(i,t+1) ~ p_i(U_(i,t+1)|U_(i,<=t),S_<=t)`

`P_(i,t) ~ g_i(S_t,U_(i,t),metadata_i)`.

Ce modèle est un cadre d'hypothèses. Rien n'impose que S soit unique, de faible dimension, stationnaire ou parfaitement identifiable. Les marchés peuvent partager certains facteurs tout en conservant des composantes indépendantes et des couplages qui changent.

### 11.2 Une bonne représentation n'est pas l'état « vrai »

Si une transformation inversible change les coordonnées du latent et que le décodeur compense, les observations peuvent rester identiques. La qualité prédictive ne sélectionne donc pas nécessairement une interprétation unique de S. Les résultats sur la non-identifiabilité des représentations désentrelacées sans hypothèses supplémentaires renforcent cette prudence ; ils ne constituent pas un théorème spécifique aux marchés. [Locatello et al., ICML 2019](https://proceedings.mlr.press/v97/locatello19a.html).

Le terme « latent commun » devrait désigner une structure transférable et utile aux tâches mesurées. Prétendre avoir retrouvé la cause réelle des prix exigerait d'autres hypothèses et d'autres preuves.

### 11.3 Expériences de séparation

1. **Apprentissage local contre partagé.** Comparer performances par domaine avec budget total documenté et effort de réglage comparable. Rapporter aussi les paramètres actifs par prévision : huit modèles distincts de N paramètres ne coûtent pas la même chose qu'un seul modèle de N.
2. **Courbe de données locales.** Adapter un modèle partagé à une famille tenue à l'écart avec plusieurs quantités de données locales ; comparer au même GPT initialisé aléatoirement. Un gain régulier à faible quantité soutient une représentation transférable.
3. **Famille entière exclue.** Garder, par exemple, les métaux, les indices ou le change hors préentraînement selon le fold. Des actifs proches d'une même famille ne suffisent pas à prouver une universalité.
4. **Calendrier global exclu.** Aucune série corrélée ne doit révéler au préentraînement les dates futures utilisées comme test. La séparation entre actifs ne remplace pas la séparation dans le temps.
5. **Perturbation de l'identité.** Masquer ou permuter les identifiants en conservant les unités nécessaires ; examiner la baisse de performance. Une dépendance à l'identité peut être légitime, mais elle doit être distinguée de la mémorisation d'une période.
6. **Ablation du contexte d'autres actifs.** Autoriser uniquement les observations déjà publiées. Mesurer le gain des autres séries, puis la sensibilité à des délais réalistes de publication. Un lien d'attention n'est pas une preuve causale.

Une réussite soutiendrait M2 ou une version opérationnelle de M3. Une absence de gain dans un petit régime ne prouverait pas M1 à toutes les échelles ; elle préciserait où le partage n'a pas encore apporté d'avantage.

## 12. Plan factoriel à budget borné

Le plan suivant est une **proposition dimensionnelle**, pas une réservation de ressources ni une exigence de disposer déjà de ces volumes. Ses niveaux peuvent être réduits avant toute expérience si la couverture réelle ne les permet pas. L'important est de conserver les contrastes, de publier la plage explorée et de ne pas transformer une limite de budget en loi scientifique.

### 12.1 Axes à mesurer séparément

| Axe | Symbole | Mesure à publier |
|---|---|---|
| Langue | R | Représentation exacte ou avec perte, vocabulaire, longueur, état auxiliaire |
| Capacité | N | Paramètres totaux, hors embeddings et actifs par prédiction |
| Quantité unique | U | Identifiants d'observations sources uniques réellement rencontrées |
| Exposition d'entraînement | T | Tokens traités, répétitions et chevauchements de contexte inclus |
| Diversité | M | Familles, instruments, années, sessions et régimes représentés |
| Contexte | K et durée | Nombre d'observations, nombre de tokens et durée réelle du passé |
| Résolution | delta_t | Fréquence d'observation réelle, pas seulement fréquence du fichier |
| Calcul | C | FLOPs estimés, durée, matériel, mémoire et efficacité observée |
| Optimisation | O | Algorithme, schedule, batch, précision, critères d'arrêt et instabilités |

Une quantité d'observations U n'est pas un effectif statistique indépendant. Des fenêtres répétées, des actifs corrélés et plusieurs agrégations d'un même intervalle augmentent T sans créer autant d'épisodes nouveaux. Ne pas inventer un unique « nombre effectif de tokens » censé résoudre toutes ces dépendances ; publier plusieurs dimensions de couverture.

### 12.2 Bloc A — Langue × capacité × quantité

Choisir **trois langues suffisamment définies**, dont un canal de prix brut à précision source, une représentation réversible ou quasi réversible avec son état auxiliaire et une représentation volontairement comprimée. Ce ne sont pas trois vainqueurs présélectionnés par les résultats d'un petit prédicteur.

Proposition de niveaux GPT : **8, 32 et 128 millions de paramètres**. Proposition de quantités uniques : **10, 40 et 160 millions d'observations sources**, si des données réelles adéquates existent. Mélange de familles, contexte calendaire, périodes et objectifs fixés. Les volumes inférieurs doivent être construits comme sous-ensembles imbriqués et équilibrés du plus grand, sans réduire silencieusement le nombre de familles.

Le croisement `3 langues × 3 capacités × 3 quantités × 2 initialisations` donne **54 entraînements**. Il permet de mesurer un changement de classement des langues avec N ou U. Deux initialisations constituent un minimum de diagnostic, pas une estimation précise de toute la variabilité ; une troisième est réservée à des comparaisons décisives et compte comme essai supplémentaire.

Si ce plan dépasse le budget, un premier bloc `3 langues × 2 capacités × 2 quantités × 2 initialisations` donne **24 entraînements**, puis des niveaux intermédiaires ou supérieurs sont ajoutés selon la question la moins identifiée. Ce plan réduit ne permet pas d'annoncer des exposants asymptotiques fiables. Il sert à choisir l'expérience suivante.

### 12.3 Bloc B — Quantité contre diversité

Au niveau intermédiaire de N et de U, comparer un corpus concentré et un corpus diversifié, de même volume unique et de mêmes périodes admissibles, pour les trois langues et deux initialisations : **12 entraînements au maximum**, dont certains peuvent être partagés avec le bloc A si les conditions sont identiques.

Pour isoler l'effet de diversité, tenir fixe la dose de données d'un domaine cible et remplacer une quantité égale de données auxiliaires par d'autres familles. Une seconde comparaison peut tenir fixe le volume total en réduisant la dose du domaine dominant. Ces deux questions ne doivent pas être confondues.

Les mots « diversifié » et « concentré » doivent être définis par les proportions de familles et de périodes, pas par le seul nombre de symboles. Cent séries très corrélées à la même date ne constituent pas la même intervention que plusieurs mécanismes de cotation sur des décennies.

### 12.4 Bloc C — Capacité contre histoire visible

Pour deux langues contrastées, deux capacités et trois durées de contexte, avec deux initialisations : **24 entraînements au maximum**, à retrancher des doublons exacts avec le bloc A. Choisir les niveaux de contexte en durée réelle et en résolution, puis publier leur traduction en tokens pour chaque langue.

À une seconde, 1 024 observations ne couvrent qu'environ 17 minutes ; ce n'est pas une histoire longue. Une variante hiérarchique peut montrer le passé récent à la seconde et des fenêtres plus anciennes à la minute, à l'heure ou au jour. Elle ajoute une hypothèse d'agrégation qu'il faudra comparer à une fenêtre unique, en gardant explicite la perte de précision ancienne.

Le bloc A peut employer un contexte fixe relativement modeste pour maîtriser le croisement N×U ; le bloc C teste précisément si ce choix limitait les langues ou les grandes capacités. Un plateau au bloc A ne doit pas être proclamé plafond du modèle avant ce contraste.

### 12.5 Plafond d'essais et d'effort

Le programme complet comporte au plus **90 entraînements de base** avant mutualisation des cellules identiques : 54 + 12 + 24. Un budget de réplications, de qualifications d'optimiseur et d'extensions doit être annoncé séparément. Les chiffres proposés bornent le programme de mesure ; ils ne sont pas des règles d'arrêt du phénomène étudié.

Une approximation courante du calcul d'un Transformer dense est proportionnelle à `N × T`, parfois résumée par `6NT` pour l'entraînement. Ce n'est qu'un ordre de grandeur : coût d'attention avec longues séquences, embeddings, projections, pertes et matériel modifient la facture. Utiliser les FLOPs ou temps réellement mesurés pour les comparaisons finales. Le nombre de tokens varie selon la langue ; égaliser seulement T pourrait donner à l'une beaucoup moins de temps de marché.

Deux résultats doivent donc coexister : **à même histoire source et même capacité**, puis **à même budget de calcul**. Le premier étudie l'accessibilité d'une information ; le second l'efficacité d'un système. Aucun ne remplace l'autre.

## 13. Qualification de l'entraînement avant conclusion sur le langage

Pour chaque taille, qualifier le domaine raisonnable du taux d'apprentissage et du batch avec un petit budget commun de développement. Conserver la même règle de qualification entre langues ; une seule architecture mal réglée ne doit pas condamner la représentation qu'elle utilise. Rapporter le nombre de réglages essayés, y compris ceux qui divergent.

Comparer courbes de pertes train et développement, gradient, instabilités numériques, sensibilité à l'initialisation et réponse à une prolongation d'entraînement. Une perte train élevée peut venir d'une limite de capacité, d'une optimisation insuffisante ou d'une cible difficile. Une faible perte train et une forte perte extérieure suggèrent plutôt estimation, décalage ou fuite, sans identifier automatiquement une cause unique.

Des checkpoints précoces ne sont pas toujours substituables à des entraînements courts dont le schedule a été conçu pour un budget plus faible. Une comparaison d'échelle doit contrôler cette différence. Les politiques d'arrêt et de schedule ne doivent pas varier librement après consultation du résultat attendu.

Les réplications doivent partager, lorsque possible, les mêmes partitions, périodes et tirages de sous-corpus. Elles comparent des méthodes sur les mêmes difficultés. Un journal conserve toutes les expositions de données et les décisions de sélection.

## 14. Mesures scientifiques communes

### 14.1 Scores sur la même variable

- Score logarithmique sur probabilités de mêmes cellules de prix ou densités correctement transformées.
- CRPS sur le prix futur, avec unités de l'instrument affichées ; comparaisons entre actifs par scores relatifs à une référence commune ou par pondération fixée avant test.
- Calibration des probabilités et couverture/largeur des intervalles.
- Qualité des distributions à plusieurs horizons et des dépendances de trajectoire : distribution de maximum, minimum et amplitude, ordre de franchissement de niveaux prédéfinis, corrélations entre pas futurs.
- Robustesse à des familles exclues, nouvelles périodes et résolutions différentes.

La dernière valeur et une distribution empirique historique constituent des références de mesure. À une seconde, prédire beaucoup de prix inchangés peut être facile ; publier la probabilité de changement et la distribution conditionnelle de son amplitude évite qu'une métrique globale cache cette difficulté. Le sous-ensemble où le prix changera n'est connu qu'après coup : il peut servir au diagnostic, pas à choisir les instants de prévision.

L'évaluation en prix brut doit rester centrale. Une métrique normalisée sert à comparer des unités différentes ; elle n'impose pas que l'entrée du GPT soit elle-même normalisée. Les constantes de normalisation de score sont apprises sur le passé autorisé, jamais sur le test futur.

### 14.2 Tester la langue, pas seulement le style de sortie

Une image plausible ou une série lisse ne prouve pas une bonne distribution conditionnelle. Une génération inconditionnelle qui reproduit des statistiques historiques et une prévision du futur effectivement observé sont deux tâches distinctes. Il faut tester l'apport du contexte : masque, contexte provenant d'une autre période, contexte lointain, contexte véritable, toujours avec contrôles de dépendance adaptés.

Si toutes les langues convergent vers le même score extérieur à capacité suffisante, elles peuvent rester très différentes en efficacité ou en stabilité. Si leurs classements se croisent, le croisement est un résultat scientifique à conserver. Le concours ne doit pas éliminer à faible N la langue dont la question centrale est précisément l'effet d'une plus grande capacité.

### 14.3 Incertitude et sélection

Les comparaisons sont appariées sur les mêmes instants. Rééchantillonner des blocs temporels qui conservent ensemble les actifs contemporains ; publier la sensibilité à la longueur de blocs et la dispersion entre périodes. Une distribution non stationnaire ne devient pas stationnaire parce qu'on a appliqué un bootstrap.

Garder une grille de développement pour choisir les expériences, puis des périodes et familles extérieures pour évaluer les conclusions annoncées. Le nombre total de variantes, architectures, langues et métriques explorées doit être visible. Une identité de source exclue du train ne protège pas contre un choc historique déjà vu dans d'autres séries.

## 15. Ajuster une loi d'échelle sans transformer l'extrapolation en vérité

Une forme de départ est :

`L_R(N,U) = A_R + B_R N^(-alpha_R) + D_R U^(-beta_R)`.

C'est une hypothèse de modèle statistique, pas une loi physique. Elle ignore notamment contexte, diversité, répétition, optimisation et interactions. Une extension peut inclure ces facteurs, mais ajouter plus de paramètres que les contrastes ne permettent d'identifier produit une formule décorative.

Pratiques proposées :

1. Ajuster d'abord des tendances locales et une forme en puissance simple ; montrer les résidus et incertitudes.
2. Réserver une ou plusieurs cellules à plus grande capacité/quantité pour tester l'extrapolation avant d'utiliser toute la grille pour ajuster la loi.
3. Comparer une forme avec et sans plateau estimé ; vérifier si A_R change fortement quand un niveau est retiré.
4. Rapporter des intervalles sur les gains prévus au **prochain facteur d'échelle**, sans extrapoler plusieurs ordres de grandeur à partir de trois tailles.
5. Traiter un échec de prédiction de la cellule réservée comme une réfutation de la forme ajustée dans ce domaine, pas comme une réfutation du langage.

Les choix de fonction, de points ajustés et d'optimisation modifient parfois fortement les conclusions d'une étude d'échelle. Une analyse méthodologique récente insiste sur cette sensibilité et la documentation nécessaire. [(Mis)Fitting: A Survey of Scaling Laws](https://arxiv.org/abs/2502.18969).

## 16. Critères scientifiques de révision, sans arrêt arbitraire

### 16.1 Ce qui peut être invalidé nettement

| Affirmation | Condition qui l'invalide ou impose une correction |
|---|---|
| « Cette langue est réversible » | Deux entrées différentes deviennent indiscernables avec tout l'état déclaré, ou l'inverse ne restitue pas la précision annoncée. |
| « Le modèle n'a pas vu le futur » | Une valeur, normalisation, tokenisation, segmentation ou série corrélée introduit des dates non admissibles. |
| « La langue R est supérieure dans la plage étudiée » | La supériorité disparaît dans les réplications et tests annoncés, ou le classement s'inverse selon des cellules omises de la conclusion. |
| « La croissance de capacité améliore le score dans cette plage » | Une comparaison qualifiée et suffisamment précise exclut le gain minimal annoncé sur cette plage. |
| « Une représentation partagée transfère vers cette famille » | À budget et dose locale comparables, le gain extérieur annoncé est absent avec une précision suffisante ou le transfert est négatif. |
| « La loi ajustée prédit le niveau supérieur » | La cellule réservée sort systématiquement de la plage de prédiction documentée. |
| « Des capacités émergent brutalement » | La rupture disparaît avec un score continu approprié ou dépend d'un seuil de métrique choisi après résultat. |

Une étude sur l'émergence montre que des seuils de métriques peuvent créer l'apparence d'un saut abrupt. Cela justifie des mesures continues et un examen des effets de seuil ; cela ne prouve pas que toute nouvelle capacité soit illusoire. [Schaeffer, Miranda et Koyejo, 2023](https://arxiv.org/abs/2304.15004).

### 16.2 Gain absent, trop petit ou mal mesuré

Fixer un **gain minimal scientifiquement pertinent epsilon** avant de consulter le résultat : par exemple une amélioration de log-score dont l'amplitude serait distinguable du bruit de mesure et intéressante pour l'hypothèse d'échelle. Sa valeur doit être motivée par la question et la précision accessible, pas par un résultat que l'on espère faire passer.

- Si l'intervalle du gain reste large et inclut des améliorations substantielles, verdict **indéterminé** ; l'expérience suivante devrait réduire cette incertitude ou explorer l'axe confondu.
- Si l'intervalle entier se trouve dans une zone d'équivalence prédéfinie autour de zéro, conclure à une **absence de différence pertinente dans cette plage**.
- Si le gain existe mais sa pente décroît, conclure à une **progression mesurée avec rendement marginal réduit**, sans annoncer sa fin.
- Si le gain augmente avec N pour une langue auparavant faible, conserver l'hypothèse d'un besoin de capacité ; tester un niveau supérieur selon le budget de recherche.

Des consultations répétées d'intervalles ordinaires jusqu'à l'apparition d'un résultat favorable ne constituent pas un protocole valide. Fixer les bilans à l'avance ou utiliser une méthode séquentielle appropriée. La durée et les ressources d'un bloc bornent les connaissances produites ; elles ne décident pas de l'existence d'une structure au-delà.

### 16.3 Décider de l'expérience suivante

La décision doit être fondée sur la **valeur d'information** : quel contraste départagerait les explications restantes ? Si N et U étaient confondus, les séparer. Si la langue n'a pas accès à une histoire longue, agrandir l'histoire. Si la perte de reconstruction est massive, ajouter un résidu ou une vue exacte. Si le corpus est homogène, tester la diversité à volume constant. Si l'optimisation n'est pas qualifiée, la corriger avant d'acheter de la capacité supplémentaire.

Il est légitime de clôturer un bloc expérimental avec « hypothèse encore ouverte au-delà de la plage testée ». Ce n'est pas une conclusion d'impossibilité. Poursuivre peut signifier changer l'expérience pour apprendre davantage, plutôt que répéter aveuglément la même opération à une taille plus grande.

## 17. Questions de recherche prioritaires

1. **Existe-t-il une interaction robuste langue × capacité ?** C'est la protection la plus directe contre l'élimination prématurée d'un encodage.
2. **Le partage de familles réduit-il la quantité locale nécessaire ?** La courbe d'adaptation est plus informative qu'une victoire moyenne unique.
3. **Le contexte supplémentaire apporte-t-il de l'information ou seulement des répétitions ?** Séparer durée, résolution et tokens.
4. **Les prix bruts exacts deviennent-ils plus compétitifs avec la capacité ?** Le modèle pourrait apprendre lui-même des invariances qu'un petit réseau exige qu'on lui fournisse ; cette idée mérite un test.
5. **Quelles structures se transfèrent entre prix à la seconde et histoire longue ?** Une architecture hiérarchique peut aider, mais l'agrégation doit rester un choix expérimental explicite.
6. **Peut-on prédire le prochain palier d'échelle avant de l'entraîner ?** Une loi qui anticipe correctement une cellule réservée apporte plus de preuve qu'une courbe ajustée après coup à tous les points.
7. **Un latent partagé soutient-il des tâches multiples sans devenir une simple mémorisation d'identités et de dates ?** Le test doit exclure à la fois des familles et des calendriers.

## 18. Portée de cette note

Le programme recommandé respecte l'ambition d'un GPT des structures de marché. Il lui donne un dispositif pour apprendre de ses échecs sans les surinterpréter et pour mesurer ses progrès sans présupposer une puissance infinie. Les critères portent sur représentation, généralisation, transfert, incertitude et validité des lois d'échelle.

Les références vérifiées soutiennent l'existence de relations d'échelle dans des modèles séquentiels et temporels, ainsi que la nécessité d'expériences contrôlées. Elles ne démontrent ni la taille nécessaire pour TRAME, ni la quantité minimale universelle de données, ni l'identifiabilité d'un unique état latent du marché. Les expériences proposées sont précisément destinées à réduire ces inconnues, une par une.

