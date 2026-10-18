# TRAME et les langages possibles du marché

## Atlas des représentations et conversion des courbes en tokens

**14 octobre 2026. Recherche conceptuelle. TRAME est un nom de travail proposé, sans affirmation de disponibilité de marque.** Le nom renvoie à une structure qui se construit dans le temps et à plusieurs fils d'information. Le projet cherche une grammaire des marchés, pas seulement des chandeliers. Alternatives envisagées : Palimpseste, pour les lectures superposées d'une même histoire ; et Morphose, pour les transformations de régime. TRAME est retenu dans ce dossier pour sa simplicité.

**Mise à jour scientifique 2, 14 octobre 2026. L'exemple historique reste une démonstration de conversion. Le document 07 ajoute une mesure réelle de distorsion ; le document 08 ouvre la comparaison GPT et marché latent.**

## 1 La question essentielle

Un token n'est pas nécessairement un mot, ni un prix, ni une bougie. C'est une unité de représentation donnée à un modèle de séquences. Il peut être un identifiant discret appris, un vecteur continu de plusieurs observations, un événement ou une combinaison de ces éléments. Le mot « langage » désigne l'alphabet, la structure des unités, l'ordre des éléments et leurs dépendances.

Un LLM qui lit le texte « le prix augmente de 2 % » utilise un tokenizer de texte. Un modèle financier peut recevoir directement un identifiant qui signifie une zone de rendement, ou un vecteur contenant rendement et durée. Dans ce second cas, aucun détour par le français n'est nécessaire. Les embeddings et la tête de sortie sont propres au domaine ; réutiliser une architecture Transformer ne signifie pas conserver le vocabulaire ou les poids d'un assistant conversationnel.

Notre proposition est de ne pas choisir immédiatement un seul alphabet. Il faut constituer une **bibliothèque de transpositions**, comparer ce qu'elles préservent, puis apprendre éventuellement à combiner celles qui apportent des informations complémentaires. Le modèle peut apprendre des régularités que nous n'avons pas nommées. Cette capacité doit être mesurée sur un futur non utilisé pour les découvrir.

## 2 Le contrat d'une langue de marché

Chaque langue candidate est décrite par neuf champs : observation source ; transformation ; instant auquel elle devient calculable ; unité et durée ; état auxiliaire nécessaire ; information perdue ; reconstruction ; événements impossibles ; tâche de validation. Ce contrat empêche une représentation séduisante de masquer une fuite ou une perte décisive.

Exemple : « hausse » représente le signe d'une variation. Pour reconstruire un prix, il manque la magnitude, la durée et un niveau initial. Un vocabulaire hausse/baisse peut reconnaître des séquences de signes ; il ne décrit pas une trajectoire de risque complète. On peut l'enrichir par durée et amplitude, ou le conserver volontairement pauvre comme expérience de contrôle.

Les champs inconnus ne deviennent pas zéro. Zéro volume, aucun événement, capteur absent, session fermée et réponse perdue sont cinq situations différentes. Une grammaire doit disposer de masques et de marqueurs explicites. Elle doit aussi distinguer prix de transaction, bid, ask, mid, mark et oracle.

## 3 Une vraie bougie transformée pas à pas

### 3.1 Provenance et limite de cet exemple

Pour sortir de l'exemple inventé, un petit fichier historique réel a été inspecté : archive Binance Vision BTCUSDT spot, bougies horaires de mars 2020. Le fichier et son CHECKSUM ont été téléchargés pour cette étude documentaire ; leur SHA-256 correspond. Il contient **743 bougies uniques**, avec une interruption entre les ouvertures du 4 mars à 09:00 et 11:00 UTC. La cause du trou n'a pas été établie. Le mois théorique comporte 744 heures : une archive authentique n'est donc pas automatiquement une grille complète.

La bougie choisie commence le **12 mars 2020 à 12:00 UTC**, soit 13:00 à Paris ce jour-là. Son choix illustre la représentation d'une forte amplitude ; il ne constitue pas une sélection d'évaluation. L'archive a été reçue en octobre 2026 : elle n'atteste pas la latence de publication en 2020. Aucun modèle n'a été entraîné, aucun résultat prédictif calculé sur ce fichier.

Source : [archive réelle Binance Vision](https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1h/BTCUSDT-1h-2020-03.zip), [description des champs](https://github.com/binance/binance-public-data). Les conditions consultées distinguent recherche personnelle hors production et usages nécessitant des droits supplémentaires : cet exemple reste limité à la recherche personnelle. Il ne définit pas le corpus multi-marchés visé. [Conditions de données](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md).

### 3.2 Données brutes

| Champ | Valeur réelle | Sens |
|---|---:|---|
| Clôture précédente | 6 067,01 USDT | Ancre de reconstruction |
| Ouverture O | 6 064,27 USDT | Première valeur de la bougie |
| Haut H | 6 307,59 USDT | Extrême supérieur observé |
| Bas L | 5 900,00 USDT | Extrême inférieur observé |
| Clôture C | 6 028,10 USDT | Dernière valeur de la bougie |
| Volume V | 18 013,68913 BTC | Quantité de l'actif de base |
| Transactions | 137 478 | Nombre fourni par l'archive |

Ces nombres décrivent une heure. Ils ne disent pas dans quel ordre le haut et le bas ont été touchés. Plusieurs chemins opposés de stop et de profit sont compatibles avec la même ligne. Aucun tokenizer ne peut récupérer une information absente de sa source.

### 3.3 Anatomie relative inversible

Avec A la clôture précédente, nous définissons :

`g = ln(O/A)`

`b = ln(C/O)`

`u = ln(H/max(O,C)) >= 0`

`d = ln(min(O,C)/L) >= 0`

`v = ln(1 + V/V_ref)`

V_ref est une unité ou une échelle de volume documentée. Pour l'exemple seulement, V_ref vaut 1 BTC. Pour transférer entre actifs, on utilisera une référence calculée sur le passé disponible et on conservera cette référence. Le « 1 » dans un logarithme doit correspondre à une quantité sans dimension.

Sur la ligne réelle, les résultats sont : g = -0,0004517248 ; b = -0,0059823025 ; u = 0,0393394977 ; d = 0,0214795190 ; v = 9,7989427669. Les quatre premiers nombres sont des log-ratios, pas exactement des pourcentages usuels. Par exemple, un rendement logarithmique r devient un rendement simple `exp(r)-1`.

La reconstruction est déterministe si les nombres ne sont pas quantifiés :

`O = A × exp(g)`

`C = O × exp(b)`

`H = max(O,C) × exp(u)`

`L = min(O,C) × exp(-d)`

`V = V_ref × (exp(v)-1)`

Les contraintes OHLC sont alors respectées lorsque u,d,v sont non négatifs. Un modèle doit aussi pouvoir représenter exactement une mèche ou un volume nul : prévoir une masse en zéro, et non seulement une fonction strictement positive. Ce type de représentation structurée possède déjà des antériorités, dont KiT ; il s'agit ici d'un exemple de conception, pas d'une revendication d'invention.

### 3.4 De la géométrie au vocabulaire discret

Prenons volontairement un alphabet simple : arrondir les quatre log-ratios au multiple de 0,001 le plus proche. Le mot devient `G_0 B_-6 U_39 D_21`. La taille d'un cran est environ dix points de base pour les petites variations. Pour v, une grille de 0,01 donne `V_980`. Ces identifiants sont illustratifs ; ils ne sont ni un tokenizer entraîné ni une grille recommandée.

Avec A = 6 067,01, les prix décodés sont O = 6 067,01 ; C ≈ 6 030,7169 ; H ≈ 6 308,2979 ; L ≈ 5 905,3924. L'erreur logarithmique de clôture vaut environ **4,34 points de base**. La chart ressemble à l'originale, mais la différence peut être plus grande qu'une variation que nous cherchons à prévoir. Le critère « la forme est bien reconstruite » est insuffisant.

Une branche de résidu conserverait les écarts entre coordonnées exactes et coordonnées quantifiées. Une hiérarchie grossier/fin permet aussi d'affiner seulement certaines dimensions. Une autre possibilité est de quantifier en unités de volatilité passée : la résolution suit alors le régime, mais il faut conserver cette volatilité et les unités de prix dans le contexte. Pour générer plusieurs pas, V_ref et la volatilité sont soit figés à l'émission, soit mis à jour à partir du passé généré selon une règle documentée. Une échelle future calculée sur la trajectoire réelle ne doit jamais être fournie au décodeur.

### 3.5 Du mot à la phrase

La séquence abstraite peut se lire ainsi : `DEBUT_EPISODE, PLACE, INSTRUMENT, UNITE, INTERVALLE, CONTEXTE, MOT_t-255, ..., MOT_t, FIN_CONTEXTE`. Le modèle prédit ensuite une distribution sur MOT_t+1 et ses composantes. Les tokens de métadonnées ne doivent pas utiliser des propriétés calculées avec le futur. L'identité de l'actif peut être masquée dans certaines expériences pour tester si le modèle mémorise plutôt qu'il ne transfère.

Les noms explicites ci-dessus servent au lecteur. En pratique, un codebook appris peut donner un numéro 713 à une région du latent sans signification humaine unique. La bonne interprétation d'un code se fait après entraînement par ses exemples, sa reconstruction et ses effets mesurés, pas en lui attribuant un récit psychologique.

## 4 Les principales familles de langues

| Langue candidate | Ce qu'elle rend facile | Information perdue ou piège | Premier test utile |
|---|---|---|---|
| Prix absolus | Niveaux ronds, tick, barrières nominales | Dépendance aux unités et niveaux historiques | Transfert avec changement d'échelle |
| Écarts de prix | Mouvement local en monnaie | Comparabilité faible entre actifs | Écarts en tick contre monnaie |
| Rendements simples | Comparaison d'amplitudes relatives | Asymétrie hausse/baisse et composition | Retour à l'unité de prix |
| Log-rendements | Additivité dans le temps | Prix nul ou négatif incompatible | Branche spéciale pour instruments concernés |
| Signes hausse baisse stable | Persistance et alternance | Magnitudes et risque supprimés | Même modèle avec amplitude réintroduite |
| Quantiles ou rangs | Robustesse à l'échelle | Extrêmes écrasés et seuils instables | Quantiles appris sur train et queues séparées |
| Écarts en volatilité passée | Formes comparables entre régimes | L'échelle absolue disparaît | Échelle jointe contre échelle omise |
| Distance aux niveaux | Approches et franchissements | Niveaux définis après coup | Niveaux connus avant chaque observation |
| Bougie structurée | Relations ouverture corps mèches | Chemin intrabougie absent | Reconstruction et franchissements bornés |
| Paliers et changements directionnels | Temps intrinsèque et persistance | Durée variable et événements censurés | Prévision conjointe direction durée amplitude |
| Segments appris | Motifs locaux plus compacts | Frontières qui regardent l'avenir | Segmentation causale en flux |
| Événements du carnet | Offre demande et files d'attente | Flux incomplet et règles de place | Rejeu déterministe avec continuité |
| Relations entre actifs | Retards, écarts et facteurs communs | Synchronisation et corrélation de corpus | Familles/calendriers exclus du train |
| Images de courbes | Inductif spatial et reconnaissance visuelle | Axes, pixels, couleurs et précision | Rendu standardisé à information identique |

Les représentations peuvent coexister. Le prix absolu n'est pas « faux » parce que le rendement transfère mieux ; il peut porter une information de tick ou de niveau rond. À l'inverse, lui donner une place dominante peut faire mémoriser les identités. Un canal relatif principal et des canaux absolus documentés constituent une hypothèse de compromis.

Les prix logarithmiques ne sont pas universels : certains instruments ou épisodes ont des prix non positifs. Une alternative est l'écart divisé par une échelle positive passée, ou une transformation signée de type asinh. On doit documenter son inverse et ses unités. Exclure silencieusement ces observations produirait un corpus artificiellement confortable.

## 5 Comment apprendre un vocabulaire

### 5.1 Bins définis à la main

Des intervalles fixes de rendements ou d'amplitudes donnent une référence lisible et reproductible. Ils rendent visibles la résolution et le clipping. Des bins de quantiles occupent le vocabulaire plus uniformément mais changent le amplitude physique des crans et écrasent parfois les queues. Les frontières sont apprises sur entraînement, puis gelées pour validation et test.

Un code d'extrême ne doit pas transformer toutes les crises en une valeur unique. On peut lui associer un résidu, une amplitude logarithmique supplémentaire ou des classes ouvertes avec une distribution conditionnelle. Le taux de saturation sera un diagnostic obligatoire.

### 5.2 Vocabulaire conjoint par quantification vectorielle

Un encodeur e transforme la bougie en vecteur ; un codebook choisit un prototype ; un décodeur reconstruit. L'apprentissage équilibre reconstruction, engagement vers les codes et diversité d'occupation. Le code peut capturer une relation corps/mèches/activité difficile à fixer à la main.

Ses risques sont le codebook peu utilisé, la quantification d'artefacts de source et la perte d'événements rares. Il faut mesurer l'entropie d'occupation, les codes morts, la stabilité par régime, la reconstruction extrême et la précision des petits écarts de prix et des extrêmes. On ne choisira pas la taille du vocabulaire par perplexité de token seulement.

### 5.3 Codes factorisés et hiérarchiques

Si cinq dimensions ont chacune 256 valeurs, le vocabulaire cartésien contient 256 puissance 5 possibilités : plus d'un billion. Une table d'embeddings exhaustive serait absurde. Une séquence de cinq codes ou des têtes factorisées évitent ce produit, au prix d'une dépendance à l'ordre et de davantage de positions. Un code grossier partagé et des raffinements spécialisés offrent une troisième voie.

Comparer les coûts en observations sources, nombre de tokens, opérations et latence. Un modèle qui consomme dix tokens par bougie n'est pas comparé honnêtement à un autre en leur attribuant simplement le même nombre de tokens d'entraînement.

### 5.4 Vocabulaire de segments

Un équivalent de BPE pourrait fusionner des séquences fréquentes de symboles financiers. C'est une piste spéculative : les mots n'auraient pas de longueur calendaire fixe. Apprendre les fusions uniquement sur entraînement est nécessaire mais ne suffit pas ; il faut une règle causale de fermeture des mots. Attendre de connaître le mouvement suivant pour déclarer la fin du motif crée un délai qui doit apparaître dans la décision.

Les meilleurs segments de reconstruction peuvent ignorer les zones où le futur se décide. Une segmentation par changement statistique causal, une durée maximale et un marqueur de segment non terminé doivent être comparés à des patches fixes. Les frontières ne seront jamais optimisées rétrospectivement puis présentées comme connues en direct. À chaque décision, le tokenizer ne reçoit que le préfixe disponible : soit on retokenise ce préfixe, soit une règle en flux ferme les mots avec un état incomplet explicite. Un BPE hors ligne appliqué à toute l'histoire future peut changer le suffixe des tokens passés et viole ce contrat.

### 5.5 Tokens continus

Un vecteur continu projeté dans l'espace d'embedding joue le rôle d'un token sans dictionnaire discret. Cela simplifie la précision numérique et évite les codes morts. Le modèle doit alors produire une distribution continue, une trajectoire générée ou des quantiles. « Transformer le marché en langage » n'impose donc pas de discrétiser : c'est une des hypothèses du concours.

## 6 Le temps fait partie du langage

Un mouvement de 1 % en une seconde et en trois semaines ne porte pas le même risque. Une langue à intervalles réguliers conserve implicitement une durée fixe, mais doit marquer sessions et interruptions. Une langue à événements doit conserver le délai depuis le dernier événement et la durée passée sans événement.

Les paliers peuvent définir le prochain mot quand le prix s'écarte d'un seuil. On doit prédire **la direction, l'amplitude éventuelle du dépassement et la durée d'attente**. Le seuil utilisé pour ouvrir un événement est fixé avec l'information courante ; l'ajuster rétrospectivement à la volatilité future est une fuite. À la fin d'un échantillon, un événement non terminé est censuré, pas absent.

Le nombre H d'événements futurs n'est pas l'horizon H minutes. L'évaluation commune doit revenir à des horizons calendaires choisis : distribution à une heure, probabilité de franchissement en quatre heures, maximum de perte en une journée. Autrement, chaque alphabet pourrait choisir implicitement sa propre difficulté. Direction, durée et dépassement ne déterminent cependant pas le chemin intrapalier ni les OHLC horaires. Il faut un décodeur probabiliste de chemins compatibles, des observations auxiliaires ou des métriques limitées aux événements identifiables ; changer d'horloge ne restitue pas l'information perdue.

À plusieurs échelles, une bougie de quatre heures n'est disponible qu'après sa clôture et réception. Pendant sa formation, on peut utiliser une bougie partielle identifiée comme telle, avec âge et couverture ; on ne peut pas lui attribuer son haut, son bas et son volume finaux. Une attention interéchelles ne corrige pas une jointure temporelle erronée.

## 7 Les hypothèses inhabituelles méritant une expérience

### La partition musicale

Interpréter la variation comme hauteur, l'activité comme intensité et le temps entre événements comme rythme. Un réseau pourrait détecter des motifs de répétition ou de rupture mieux qu'avec les nombres bruts. La version raisonnable utilise ces canaux numériques, sans fabriquer un fichier audio. Un préentraînement sur musique ne sera testé que si l'on peut isoler un gain de représentation : la similarité poétique n'est pas une preuve de transfert. Comparaison : même information sous forme de canaux numériques, spectral et audio, à budget égal.

### La physique locale

Ajouter vitesse, accélération, courbure, « énergie » de variation ou friction normalisée. Les dérivées discrètes amplifient le bruit ; des filtres centrés regardent le futur. Seuls des filtres unilatéraux sont admissibles en entrée live. Les termes énergie et force sont des analogies calculatoires, sans supposer une loi de Newton pour les prix. Test : bénéfice incrémental au-delà des mêmes retards de rendement.

### Une trajectoire géométrique

Traiter prix, volume et temps comme un chemin multidimensionnel, puis représenter son ordre par intégrales itérées ou signatures tronquées. Ces objets peuvent encoder l'ordre et les interactions ; l'ajout du temps empêche certaines invariances d'effacer le rythme. Leur dimension augmente vite et des ambiguïtés demeurent avec troncature. On comparera quelques ordres faibles à des patches simples. Cette piste s'inspire de la littérature des signatures de chemins, pas d'une découverte revendiquée ici. [Présentation primaire des signatures](https://arxiv.org/abs/1603.03788).

### Topologie et formes persistantes

Construire un nuage de fenêtres passées et chercher des structures qui persistent à plusieurs échelles. Hypothèse : ces descripteurs peuvent signaler des régimes ou transitions. Risques : hyperparamètres nombreux, coût et faible lien avec la cible future. La première expérience vise la détection de régime, puis vérifie si elle ajoute quelque chose à volatilité et corrélation. Une jolie carte de clusters ne suffit pas.

### Le langage des contraintes

Prédire des relations ordinales plutôt que des prix : prochain haut supérieur au précédent, clôture dans le quart supérieur, volume au-dessus de sa médiane passée, spread sous un seuil. Une logique de contraintes assemble des scénarios compatibles. Cette langue pourrait être robuste mais grossière. Il faut mesurer sa perte d'amplitude et vérifier que les propositions marginalement probables ont une distribution jointe cohérente.

### Le marché comme conversation entre actifs

Représenter chaque actif comme un interlocuteur qui émet un changement de prix et une mesure d'activité ; apprendre quels autres actifs il « écoute » selon le régime. Le graphe doit être appris sur le passé et utiliser les heures de réception. Un lien d'attention ou un retard statistique n'établit pas une causalité économique. Test : actif cible tenu à l'écart, puis familles entières, délais réalistes et interdiction des valeurs contemporaines non reçues.

### Les langues parallèles et la traduction

Présenter le même épisode en rendements, bougies et événements. Entraîner une représentation partagée à traduire une vue vers une autre et à prévoir le futur. C'est la piste spéculative prioritaire : elle peut encourager des invariances utiles et détecter des données incohérentes. Les transformations du même OHLCV changent l'inductif ; les événements réellement observés ajoutent de l'information source. Deux ablations séparées doivent mesurer ces effets. Une traduction aller-retour entre vues avec perte ne constitue pas une preuve de réversibilité. Mais traduire OHLC en événements exacts est impossible sans information supplémentaire ; la sortie doit alors être une distribution de réalisations compatibles, jamais une reconstruction unique annoncée exacte.

### La grammaire minimale et la surprise

Chercher des descriptions courtes qui compressent un épisode et détecter les ruptures quand la description échoue. Une surprise élevée pourrait annoncer un changement de régime et justifier l'abstention. Elle peut aussi refléter une panne de données ou un simple événement rare sans suite prédictible. Test : capacité à prévoir des erreurs futures du modèle, au-delà des contrôles de fraîcheur et de volatilité.

### La symétrie et son contraire

Inverser le signe, changer l'échelle ou accélérer le temps pour tester les invariances. Certaines augmentations sont utiles pour la robustesse, d'autres détruisent la sémantique : hausses et baisses peuvent présenter des dynamiques et des queues différentes ; inverser le temps peut détruire les dépendances temporelles et la chronologie des événements. Les données transformées sont des augmentations identifiées, pas de nouvelles observations réelles, et elles ne remplacent jamais le test réel.

## 8 Trouver des motifs réellement nouveaux

Le réseau n'a pas besoin de connaître les figures traditionnelles. Il peut apprendre des relations entre amplitude, activité, contexte et durée que l'humain n'a pas nommées. Pour étudier cela, on peut regrouper ses états latents, examiner des exemples proches, entraîner des sondes simples sur des cibles indépendantes et masquer certaines entrées pour mesurer la variation de prédiction.

Ces outils expliquent une dépendance du modèle, pas nécessairement le mécanisme du marché. On exigera trois preuves séparées pour un motif candidat : il se retrouve sur des données indépendantes ; sa valeur survit à des variables de contrôle et à un modèle simple ; son information prédictive se retrouve sur des actifs et périodes réservés. Découvrir un cluster après avoir vu ses rendements puis tester sur les mêmes rendements n'est pas une découverte validée.

Une analyse de compression peut découvrir une structure non aléatoire sans prédictivité directionnelle. Des alternances de volatilité, rythmes de sessions ou dépendances de volumes constituent déjà des régularités. L'ambition supplémentaire est de montrer qu'une partie de cette structure informe une tâche future utile. Le dossier ne postule ni marché entièrement aléatoire ni prédictibilité universelle.

## 9 Concours initial de langues et priorités

La première ronde comporte quatre familles : rendements continus avec canaux auxiliaires ; bins structurés simples ; vocabulaire vectoriel appris ; langage de paliers avec durée. Même corpus réel, mêmes instants de décision, mêmes horizons, budgets documentés et même nombre d'essais. Les comparaisons porteront sur scores de prévision décodés, calibration, reconstruction et transfert entre marchés.

Les rondes suivantes comparent continu, discret et hybride à plusieurs tailles de GPT et volumes de données. Une faible performance initiale ne suffit pas à éliminer une famille : on étudie sa courbe de progression et ses pertes d'information. Les langues parallèles et le contexte entre actifs sont des axes distincts. La microstructure complète est une branche autonome conditionnée par les données, pas un canal supposé disponible. Les pistes musicales, topologiques et signatures reçoivent de petits budgets exploratoires prédéfinis.

Un résultat est invalidé si son avantage vient d'une information future ou d'une comparaison inégale. Une résolution inadéquate ou un effet non reproduit motive un diagnostic et une nouvelle version de l'expérience ; cela ne réfute pas tous les modèles possibles de cette famille. Il peut être conservé pour une autre tâche si cette utilité est explicitement séparée. L'ouverture aux idées inhabituelles exige cette discipline pour ne pas transformer la recherche en sélection infinie de coïncidences.

## 10 La proposition retenue à ce stade

TRAME désigne un **programme d'apprentissage du langage des marchés réels**, potentiellement multiactifs et multiéchelles. Sa langue de référence initiale utilise une géométrie relative réversible, le contexte d'échelle, la durée et l'activité. Les versions discrète et continue restent en concurrence. Des langues supplémentaires doivent démontrer leur contribution.

Le point de recherche le plus prometteur est moins « transformer chaque bougie en un mot » que **choisir ce qu'un mot doit conserver pour que sa suite reste prévisible et utile**. Les données réelles, la reconstruction en prix et la prévision hors échantillon constituent le lien permanent entre l'analogie linguistique et le marché.


## 11 Nouvelle piste : un langage à précision progressive

La comparaison réelle du document 07 montre un piège : des quantiles par champ peuvent bien restituer la majorité des petites variations et beaucoup moins bien certains mouvements rares. Cette observation ne réfute pas les vocabulaires appris. Elle indique que le débit alloué aux queues et la représentation des valeurs hors plage doivent être des paramètres explicites.

Une piste hybride représente chaque coordonnée par un signe, une classe d'ordre de grandeur, un code de forme et un résidu. Une autre réserve un symbole d'échappement aux extrêmes, suivi d'une amplitude continue. Une troisième utilise plusieurs couches de précision, où l'on ne termine le mot qu'après un nombre maximal de raffinements. Ces langages sont des propositions nouvelles pour l'expérience suivante, pas des mécanismes déjà entraînés ou validés.

Le coût doit inclure les échelles, l'ancre, la durée, le codebook et les résidus. Une faible erreur obtenue avec cinq nombres continus supplémentaires par bougie n'est pas une compression gratuite. On cherchera un front précision/débit, puis un front prévision/calcul, à plusieurs tailles de modèle. La reconstruction isolée ne suffit pas à choisir le meilleur langage prédictif.

Le niveau zéro d'une mèche, l'absence de transaction et l'absence de mesure restent des états différents. Un token rare ne doit pas servir indistinctement pour une crise réelle, une valeur impossible et une panne de source. Ces distinctions sont sémantiques avant d'être architecturales.
