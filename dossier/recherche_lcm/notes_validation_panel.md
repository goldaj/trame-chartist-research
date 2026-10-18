# TRAME — Contre-expertise scientifique, protocole de validation et panel simulé

**Version finale de cette note : 14 octobre 2026. Statut : étude conceptuelle et protocole proposé, sans entraînement, sans backtest exécuté et sans modification du bot. TRAME est un nom de travail, sans vérification de disponibilité commerciale. LCM désigne ci-dessous l'hypothèse initiale de modèle chartiste.**

Ce document cherche les conditions dans lesquelles l'idée d'un modèle de courbes peut être réfutée, améliorée ou conservée. Le panel ci-dessous est une **simulation explicite de points de vue**, construite pour éprouver le raisonnement. Aucune personne réelle n'a été interrogée ; aucun avis d'expert externe ni résultat expérimental n'est revendiqué. Les itérations sont des révisions argumentées du projet, pas des tests ayant démontré sa rentabilité.

## 1. Position de départ : une idée réalisable, trois promesses différentes

Il est techniquement possible de construire un modèle qui apprend une distribution de prochains éléments d'une série financière. La question décisive est ce que cette distribution permettra de faire hors de l'échantillon d'entraînement, une fois l'information disponible à chaque instant et les contraintes d'exécution respectées.

Il faut séparer trois affirmations :

1. **Faisabilité de représentation** : des courbes peuvent devenir une séquence de tokens et un modèle peut apprendre à en générer des suites statistiquement cohérentes.
2. **Utilité prédictive** : le modèle prédit mieux que des références simples certaines variables futures, par exemple une distribution de rendement, la volatilité ou la probabilité de franchissement d'un seuil.
3. **Utilité économique** : une règle de décision arrêtée à l'avance transforme ces prévisions en résultat net supérieur à un benchmark pertinent, à risque comparable et avec une exécution réalisable.

La première ne démontre ni la deuxième ni la troisième. La poursuite de la recherche peut être rationnelle même si une variante échoue. En revanche, l'hypothèse « une solution rentable existe nécessairement » ne peut être un postulat scientifique : elle rendrait la recherche impossible à falsifier. La persévérance consiste ici à distinguer ce qui fonctionne, ce qui échoue et ce qui manque pour décider.

### 1.1 Pourquoi « prévoir le prochain token » ne suffit pas

Considérons une série de rendements `r[t+1] = sigma[t] × epsilon[t+1]`, où `epsilon` a une moyenne conditionnelle nulle et `sigma[t]` est prévisible. Un modèle peut apprendre à anticiper les périodes agitées, améliorer fortement une vraisemblance et générer des trajectoires réalistes, sans prévoir le signe du prochain rendement. Une stratégie directionnelle qui paie des coûts peut alors rester perdante. Ce contre-exemple théorique ne dit pas que tout signal est impossible ; il empêche de confondre génération plausible, qualité probabiliste et avantage économique.

La loss de tokens mêle plusieurs composantes : précision de la géométrie, volatilité, volume, fréquence des états, et parfois direction. Une amélioration globale peut provenir uniquement de composants sans valeur pour la décision envisagée. Il faut donc publier les scores par variable, horizon et régime, puis évaluer séparément la politique de trading.

Une loss de tokens n'est comparable entre deux modèles que si la cible, le découpage et le vocabulaire sont les mêmes. Une perplexité plus basse avec un autre codebook n'est pas une preuve de supériorité. Les sorties doivent également être évaluées dans les unités économiques d'origine : rendements, fourchettes de prix, probabilités d'événements et coûts.

### 1.2 Les limites informatives de la chart

Une image calculée exclusivement à partir d'un historique OHLCV ne crée pas d'information nouvelle sur le futur. Elle peut améliorer l'apprentissage en donnant au modèle une représentation plus adaptée, une régularisation ou des invariances utiles. Le choix image contre numérique reste donc une question empirique d'efficacité de représentation, pas une manière d'ajouter un signal absent des données.

Un carnet d'ordres, des transactions, le funding ou des variables de liquidité peuvent ajouter une information qui n'est pas récupérable dans une bougie. Mais cette extension change la question de recherche : le gain ne doit pas être attribué au « langage chartiste » si les variables nouvelles l'expliquent. Une ablation à information identique est indispensable.

Enfin, des images identiques après changement d'échelle peuvent correspondre à des coûts relatifs très différents. Une même forme sur un actif liquide et sur un actif illiquide n'appelle pas la même décision. Une normalisation utile à la reconnaissance des formes doit préserver, dans des canaux auxiliaires, les grandeurs dont la politique a besoin : volatilité absolue, tick, spread, volume, profondeur et coûts.

## 2. Repères scientifiques vérifiés et portée exacte

Les sources suivantes sont primaires : articles, prépublications des auteurs ou documentation officielle. Une publication évaluée par les pairs, une prépublication et une documentation technique n'apportent pas le même niveau de preuve.

| Travail | Ce qu'il établit dans son cadre | Ce qu'il ne démontre pas pour ce projet |
|---|---|---|
| Jiang, Kelly et Xiu, 2023, *Journal of Finance* | Des CNN sur images de prix/volumes apprennent des motifs prédictifs dans une étude sur actions, avec transferts étudiés entre marchés et horizons. Les fenêtres principales sont de 5, 20 et 60 jours. | Ni un avantage de l'autorégression de tokens, ni une supériorité universelle de l'image, ni un rendement net transposable aux perpétuels Hyperliquid. |
| Zhang, Zohren et Roberts, DeepLOB, 2018–2020 | Une architecture convolutionnelle et LSTM extrait des informations spatiales et temporelles de carnets et prédit des mouvements de prix dans les données étudiées. | Que l'accuracy du mid-price équivaut à une politique exécutable et rentable, ou que les mêmes résultats se transfèrent à Hyperliquid. |
| Gneiting et Raftery, 2007 | Les règles de score propres permettent d'évaluer honnêtement des distributions prédictives ; exemples : logarithmique, CRPS et scores pour quantiles. | Qu'optimiser un score probabiliste optimise le PnL net ou le risque accepté par l'utilisateur. |
| Guo et al., ICML 2017 | Des réseaux modernes peuvent être mal calibrés ; un ajustement de température est un outil simple dans leurs expériences de classification. | Que ce calibrage résiste à toutes les ruptures de marché, à la sélection des trades ou aux distributions continues. |
| Gibbs et Candès, NeurIPS 2021 | L'inférence conforme adaptative vise une fréquence de couverture sur le long terme malgré une distribution qui évolue. | Une protection conditionnelle pour chaque trade, chaque régime, chaque crise, ni un intervalle toujours étroit et exploitable. |
| Bailey et al., PBO, 2015/2017 ; Bailey et López de Prado, DSR, 2014 | La sélection parmi de nombreux backtests peut gonfler les performances ; des diagnostics et corrections sont proposés. | Une certification générale de stratégie, une suppression des fuites ou une garantie de stabilité future. |
| Meyer et al., prépublication v3, février 2026 | La contamination des modèles de fondation temporels inclut les échantillons recopiés et le chevauchement temporel de séries corrélées. | Que l'absence de doublons de fichiers suffise à rendre un test financier indépendant. |
| Noguer I Alonso et Franklin, prépublication, juin 2026 | Sur cinq actions américaines, plusieurs TSFM obtiennent de bons rangs mais les gains face à la marche aléatoire sont petits et peu nombreux. | Un résultat général sur tous les marchés, tous les horizons et les coûts de perpétuels. |
| Li et al., TSFMAudit, prépublication, mai 2026 | Propose un audit de contamination par dynamique d'adaptation, évalué sur six TSFM et 187 jeux de données. | Une preuve d'absence de contamination pour un checkpoint donné. |

Références directes : [Jiang–Kelly–Xiu, version publiée](https://economics.yale.edu/sites/default/files/2023-11/The%20Journal%20of%20Finance%20-%202023%20-%20JIANG%20-%20Re%25E2%2580%2590%20Imag%20in%20ing%20Price%20Trends_0.pdf), [DeepLOB](https://arxiv.org/abs/1808.03668), [Gneiting–Raftery](https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf), [Guo et al.](https://proceedings.mlr.press/v70/guo17a.html), [Gibbs–Candès](https://arxiv.org/abs/2106.00170), [PBO](https://escholarship.org/uc/item/4w1110bb), [DSR](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf), [Meyer et al., v3](https://arxiv.org/abs/2510.13654v3), [Noguer I Alonso–Franklin](https://arxiv.org/abs/2606.27100), [TSFMAudit](https://arxiv.org/abs/2605.26161).

### 2.1 Découvertes qui doivent influencer le projet

- **La lecture d'images de prix est déjà une vraie piste académique.** Le caractère innovant éventuel résiderait dans la combinaison précise de représentation, apprentissage probabiliste, transfert et validation sur la place ciblée ; pas dans l'idée générale de faire apprendre des graphiques à un réseau.
- **Une géométrie convaincante peut cacher une perte d'échelle économique.** La capacité à reconnaître une forme ne suffit pas à décider si son amplitude paiera le spread et les frais.
- **Un modèle peut être utile en prévoyant le risque sans prévoir la direction.** Filtrer des conditions défavorables ou améliorer un dimensionnement mérite un protocole séparé ; il ne faut pas rebaptiser ce résultat « prédiction du prix ».
- **Un actif jamais vu peut néanmoins être contaminé par le préentraînement.** Si des actifs corrélés à ce test ont été vus sur les mêmes dates futures, le modèle a pu apprendre le choc commun que le backtest lui demandera de prévoir.
- **Davantage de bougies n'équivaut pas à davantage d'expériences indépendantes.** Les fenêtres voisines, les actifs corrélés et les régimes communs réduisent la quantité d'information réellement disponible.
- **La principale rareté peut être la donnée d'exécution fiable.** Les API et archives officielles ne promettent pas un historique complet de tout ce qui serait nécessaire pour reproduire un marché.

La documentation officielle Hyperliquid indique que l'API de bougies ne donne accès qu'aux **5 000 bougies les plus récentes**. Elle avertit aussi que les archives peuvent comporter des manques et ne garantit pas la rapidité de leurs mises à jour. C'est une contrainte de provenance à auditer, pas une preuve que les données locales du projet sont insuffisantes : leur contenu doit être vérifié indépendamment. [Endpoint info](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint), [données historiques officielles](https://hyperliquid.gitbook.io/hyperliquid-docs/historical-data).

## 3. Panel critique simulé : dix points de vue explicitement fictifs

Ces profils sont des rôles d'analyse, pas des experts consultés. Leurs objections sont formulées ici par l'assistant. Ils ne doivent pas servir de caution sociale ou être comptés comme dix validations indépendantes.

| Profil fictif | Contexte d'usage et besoin concret | Angle mort qu'il combat | Question de contrôle | Condition de satisfaction |
|---|---|---|---|---|
| **Nadia, chercheuse en économétrie financière** | Examiner un modèle avant publication ; veut une conclusion réfutable et des intervalles d'incertitude. | Pseudo-réplication, scores choisis après résultat, multiples essais oubliés. | « Le gain subsiste-t-il avec dépendance temporelle, coûts et historique de sélection ? » | Plan préenregistré, comparaison appariée, chronologie, registre de toutes les variantes. |
| **Thomas, trader de perpétuels** | Décider si un signal mérite un ordre ; connaît les fills partiels et les retournements. | PnL au mid-price, maker supposé rempli, funding oublié. | « À quel prix, avec quelle probabilité et après quelle latence aurais-je réellement été exécuté ? » | PnL après coûts, modèle de fill prudent, passage en observation en direct. |
| **Inès, ingénieure données marché** | Produire un historique reconstructible pour des expériences répétables. | Bougies finales connues trop tôt, trous comblés avec le futur, mélange d'horloges. | « Prouve que cette valeur était reçue avant l'instant de décision. » | Temps d'événement et de réception, identifiants, contrôles de trous, provenance versionnée. |
| **Malik, chercheur en apprentissage automatique** | Comparer architectures à ressources comparables. | « Plus gros » pris pour « meilleur » ; codebook ayant appris sur le test. | « Le gain vient-il des tokens, du préentraînement, des données ou seulement de l'effort de réglage ? » | Ablations à information identique, budgets comparables, entraînement local de tous les prétraitements. |
| **Claire, responsable risque** | Tolérer seulement des comportements bornés et explicables. | Confusion entre bonne moyenne, rare catastrophe et calibration globale. | « Que fait le système quand il ne sait plus, ou quand son intervalle ne couvre plus ? » | Abstention, plafonds indépendants, critères de retrait, tests de dérive et scénario extrême. |
| **Hugo, ingénieur SRE sur serveur OVH** | Garder un service prévisible sous ressources finies. | Prototype GPU impossible à servir, interruptions de flux, états incohérents après redémarrage. | « Que se passe-t-il si les données arrivent en retard ou si le modèle prend dix fois plus de temps ? » | Budget de latence mesuré, données périmées détectées, mode sûr, reprise et retour arrière. |
| **Élodie, propriétaire du bot et utilisatrice non spécialiste** | Comprendre pourquoi le système agit et quand il faut lui faire confiance. | Une jolie trajectoire lue comme certitude ou une probabilité lue comme promesse de gain. | « Sur cent cas annoncés à 70 %, qu'ai-je réellement observé et combien m'ont-ils coûté ? » | Vue simple des scénarios, incertitude, coûts, nombre d'observations, abstention compréhensible. |
| **Jules, spécialiste microstructure et exécution** | Séparer un signal d'information d'un avantage d'accès à la liquidité. | Carnet agrégé utilisé pour inventer une position dans la file ; adverse selection ignorée. | « Les ordres sont-ils surtout exécutés lorsque la prévision se dégrade ? » | Mesures conditionnelles au fill, robustesse maker/taker, état du carnet au temps réalisable. |
| **Sara, responsable de reproductibilité** | Reproduire une conclusion six mois plus tard. | Checkpoints flottants, résultats impossibles à lier aux données et aux paramètres. | « Puis-je reconstituer chaque décision sans dépendre d'une API ayant changé ? » | Manifestes, empreintes des artefacts, versions, seeds, journal des exclusions et essais. |
| **Olivier, investisseur contradicteur** | Décider si les dépenses de R&D ont une justification. | Complexité séduisante, poursuite de dépenses malgré zéro avantage, benchmark artificiellement faible. | « Quel résultat ferait préférer une régression ou l'absence de trading ? » | Gates objectifs, comparaison au meilleur système simple, budget limité par étape, valeur alternative du modèle. |

### 3.1 Travail réellement effectué entre agents et limites de cette contradiction

Les personas du tableau sont fictifs. À côté de cette simulation, des échanges de travail ont réellement eu lieu entre l'agent chargé de cette contre-expertise et l'agent qui assemble le dossier. Ils ont porté notamment sur la contamination temporelle, les données historiques Hyperliquid, les prépublications de 2026, l'ouverture du projet à d'autres infrastructures et les représentations inhabituelles demandées par l'utilisateur.

Une relecture réelle du document scientifique 01 a également formulé trois demandes de précision : le sens d'intégration du flow matching ; la distinction entre horizon en événements et horizon calendaire ; la nécessité d'un état de marché assez riche pour simuler coûts et fills. Ces échanges sont des revues par agents logiciels, avec des hypothèses et potentiellement des angles morts communs. Ils ne sont ni dix avis humains indépendants, ni une revue par les pairs, ni des résultats d'expériences. Les cinq tours ci-dessous consignent l'évolution du raisonnement ; aucun vote fictif n'est utilisé comme preuve.

## 4. Journal de cinq itérations conceptuelles

### Itération 0 — Hypothèse initiale mise à l'épreuve

**Proposition initiale simulée :** convertir les figures chartistes en mots, entraîner un gros Transformer à prévoir le prochain mot, puis acheter ou vendre en fonction de la figure prédite.

| Objection issue du panel simulé | Révision retenue | Ce qui reste inconnu |
|---|---|---|
| Malik : les mots « triangle », « épaule » ou « support » imposent un vocabulaire humain subjectif. | Utiliser d'abord une représentation mesurable des OHLCV et des événements ; garder les noms chartistes comme annotations facultatives. | La meilleure représentation peut être continue, discrète ou hybride. |
| Inès : un sommet ou un zigzag confirmé exige parfois des observations futures. | Chaque événement porte un temps de détection ; un sommet confirmé n'est disponible qu'après confirmation. | L'intérêt du signal peut disparaître lorsque son vrai retard est pris en compte. |
| Nadia : une séquence cohérente n'est pas une preuve d'information sur les rendements. | Définir séparément qualité distributionnelle et résultat de décision. | L'une peut s'améliorer sans l'autre. |
| Olivier : aucune raison empirique ne justifie encore un grand modèle. | Commencer par les contrôles et des modèles modestes ; augmenter la taille uniquement si une courbe de gain le justifie. | La capacité optimale dépend de l'information effective et du budget. |

**Architecture révisée A :** petit prédicteur probabiliste causal sur données normalisées, baselines solides, sorties de rendement/volatilité, tokens chartistes facultatifs. **Verdict conceptuel :** hypothèse devenue testable ; aucune performance démontrée.

### Itération 1 — Le faux confort des formes et de la précision

| Objection issue du panel simulé | Révision retenue | Ce qui reste inconnu |
|---|---|---|
| Élodie : une unique courbe future semble être la prédiction certaine du modèle. | Afficher plusieurs scénarios, des quantiles et une probabilité d'événement ; préciser l'horizon et l'unité. | La présentation doit être évaluée avec de vrais utilisateurs plus tard. |
| Claire : un modèle sûr à 80 % globalement peut être dangereux dans les seuls cas où il trade. | Mesurer calibration globale, par régime et sur le sous-ensemble des décisions retenues. | Les sous-groupes peuvent manquer de puissance statistique. |
| Jules : supprimer l'échelle absolue masque des mouvements trop petits pour payer les coûts. | Préserver des variables d'échelle et coût ; fixer une règle d'abstention fondée sur une marge après coût. | Les coûts futurs ne sont pas connus exactement. |
| Malik : un gain image contre numérique peut venir d'un normalisateur différent. | Comparer les représentations avec même information historique, mêmes splits, même cible et effort de réglage déclaré. | Une égalisation parfaite des budgets reste difficile. |

**Architecture révisée B :** représentation numérique principale, branche image expérimentale seulement, têtes probabilistes, échelle et liquidité visibles, calibration passée uniquement. **Verdict conceptuel :** la génération devient une représentation de l'incertitude ; elle ne commande pas directement les ordres.

### Itération 2 — Le test historique « indépendant » qui ne l'était pas

| Objection issue du panel simulé | Révision retenue | Ce qui reste inconnu |
|---|---|---|
| Sara : un tokenizer entraîné sur toutes les dates a déjà vu le test. | Apprendre scaler, codebook, sélection de variables, calibration et politique sur les seules partitions autorisées. | Il faut disposer du détail d'entraînement des checkpoints importés. |
| Nadia : un test sur ETH peut être contaminé par BTC préentraîné aux mêmes dates futures. | Coupure temporelle globale de toutes les séries ; distinguer explicitement test de transfert entre actifs et véritable prédiction du futur. | Certains corpus de préentraînement restent opaques. |
| Inès : une bougie d'une heure jointe à une décision de 10 h 15 expose 45 minutes futures. | Jointures « as of » fondées sur disponibilité ; dernière bougie haute fréquence close ou agrégat partiel tel qu'observé alors. | Les historiques disponibles permettront-ils de reconstruire ces états ? |
| Olivier : choisir les meilleurs horizons et répéter le test final jusqu'au succès suffit à créer un vainqueur. | Registre des essais, sélection interne, test final scellé ; après consultation, ce test devient une donnée de développement. | La taille de l'historique vierge peut limiter la recherche. |

**Architecture révisée C :** laboratoire de comparaison avec chaîne de provenance, modèle de base entraîné sans futur, checkpoints préentraînés évalués avec statut de contamination explicite. **Verdict conceptuel :** une bonne architecture sans audit temporel reste non concluante.

### Itération 3 — La prévision arrive au marché réel

| Objection issue du panel simulé | Révision retenue | Ce qui reste inconnu |
|---|---|---|
| Thomas : toucher un prix dans une bougie ne signifie pas que mon ordre a été rempli. | Le POC suppose d'abord une exécution taker prudente ; le maker exige données de carnet, transactions et hypothèses de file documentées. | La profondeur agrégée peut ne pas suffire à identifier la file réelle. |
| Jules : les fills maker se produisent parfois surtout contre une information adverse. | Évaluer résultats conditionnels au fill et comparer une variante taker ; ne pas traiter l'absence de fill comme observation manquante aléatoire. | Le comportement dépendra de la latence et de la place. |
| Hugo : un modèle lent ou des données périmées peuvent invalider un signal bon en backtest. | Budget de décision complet et mode abstention sur données périmées ; validation d'abord en observation en direct. | Les latences et ressources exactes OVH restent à mesurer. |
| Claire : le modèle ne doit pas modifier ses propres limites de risque. | Limites de position, levier, pertes et exposition gérées par une couche indépendante ; modèle autorisé à suggérer, pas à outrepasser. | Les plafonds doivent être fixés avec le propriétaire avant tout capital réel. |
| Olivier : si seule la volatilité progresse, le projet ne doit pas être déclaré un succès directionnel. | Trois résultats possibles : moteur de signal, filtre de risque ou résultat négatif documenté. | La valeur d'un filtre doit elle aussi être mesurée hors échantillon. |

**Architecture révisée D :** moteur probabiliste sous contrôle, décision séparée, exécution et risque externes, baselines conservées, abstention explicite. **Verdict conceptuel :** c'est une voie de POC crédible ; la viabilité économique reste une hypothèse à expérimenter.

### Itération 4 — Hypothèses radicales, recherche fondation et infrastructure ouverte

Cette itération intègre la volonté d'explorer des représentations inhabituelles et de changer d'infrastructure si la recherche le justifie. Le bot Hyperliquid actuel est un terrain possible de comparaison ; il ne fixe pas la taille maximale, la fréquence ni les marchés de la recherche.

| Objection ou proposition issue du panel simulé | Révision retenue | Ce qui reste inconnu |
|---|---|---|
| Malik : prix absolus, écarts, pourcentages, paliers et directions portent des invariances différentes ; aucun ne doit être éliminé par goût. | Comparer ces langues sur la même période, les mêmes variables et le même budget ; mesurer d'abord information perdue et erreur de reconstruction. | Les meilleures invariances peuvent changer avec l'actif, le régime et la cible. |
| Nadia : un modèle fondation multiactif multiplie aussi les canaux possibles de contamination. | Coupure temporelle globale, tests de transfert explicitement séparés, actifs et périodes tenus à l'écart selon la question. | L'absence de contamination des corpus externes peut rester invérifiable. |
| Élodie : une langue de musique, de relief ou de motifs géométriques pourrait rendre le modèle plus intuitif. | Autoriser ces représentations comme hypothèses ; leur donner une traduction déterministe et un contrôle numérique à information égale. | L'intuition humaine ou les préentraînements correspondants peuvent aider, ou introduire des artefacts. |
| Inès : un palier ou événement n'est parfois complet qu'après une durée variable, avec des pointes au milieu. | Ajouter durée, état incomplet, seuil, overshoot et règles de disponibilité ; définir quel instant le token prédit représente. | Une quantification trop forte peut supprimer précisément les amplitudes et durées utiles. |
| Hugo : un GPU externe peut ouvrir une recherche impossible sur le VPS, mais impose un cycle d'artefacts maîtrisé. | Séparer entraînement, évaluation et service ; envisager distillation/quantification après preuve, avec validation du modèle effectivement servi. | La réduction de taille peut dégrader calibration et queues de distribution. |
| Olivier : un POC minuscule ne doit pas condamner à tort une hypothèse de transfert nécessitant de la diversité. | Définir un POC scientifique minimal et une expérience fondation conditionnelle avec plus de marchés, périodes et calcul. | Un échec à petite échelle n'invalide pas toute mise à l'échelle ; il ne justifie pas non plus une dépense illimitée. |

**Architecture révisée E :** programme à deux niveaux : une expérience contrôlée sur les représentations, puis une étude de transfert et d'échelle si les données et premiers résultats motivent son coût. La branche ambitieuse peut tester des corpus multi-marchés, plusieurs échelles temporelles, des tokens d'événements et de trajectoires et un entraînement GPU séparé. Les baselines et gates restent applicables à chaque niveau. **Verdict conceptuel :** aucune famille d'encodage n'est rejetée par analogie ; chaque famille doit annoncer l'information qu'elle conserve, les invariances qu'elle impose et les expériences qui pourraient la départager.

### Consensus obtenu et désaccords conservés

Le panel simulé converge sur le protocole à suivre, pas sur la rentabilité. Il reste divisé sur la valeur d'un vocabulaire discret, sur l'apport des images, sur le préentraînement multiactif, sur les horizons utiles et sur la quantité de données nécessaire. Ce sont précisément les questions des futures ablations. Les cinq itérations documentent des révisions de conception. Ajouter des tours identiques sans nouvelle hypothèse ni preuve aurait peu de valeur ; les itérations suivantes doivent être déclenchées par une représentation nouvelle suffisamment définie, une contrainte nouvelle ou des résultats expérimentaux.

## 5. Protocole d'expérience à préenregistrer avant développement

### 5.1 Questions et hypothèses falsifiables

Pour toute comparaison avec le bot Hyperliquid existant, le protocole LCM reste séparé des campagnes et holdouts déjà préinscrits. Leurs fenêtres ne doivent être ni consommées ni rebaptisées au bénéfice d'une nouvelle hypothèse. Aucun examen de leurs données réservées n'est requis par la présente étude. Les horizons d'une comparaison au bot seront alignés sur sa politique réelle ; une recherche fondation indépendante peut choisir d'autres horizons et marchés, avec son propre protocole.

**H1 — Représentation :** à information, cible et protocole comparables, une représentation en tokens améliore le score probabiliste hors échantillon par rapport à une représentation continue.

**H2 — Transfert :** le préentraînement sur un corpus dont toutes les observations sont antérieures au test améliore l'adaptation locale par rapport au même réseau entraîné de zéro.

**H3 — Image :** une image calculée sur le même OHLCV apporte un gain de représentation à budget déclaré ; elle ne bénéficie pas d'indicateurs absents du modèle numérique.

**H4 — Décision :** une politique figée exploitant le modèle apporte une valeur nette après coûts au-delà du meilleur benchmark simple retenu avant le test final.

**H5 — Risque :** si H4 échoue, un usage prédéfini de prévision du risque peut améliorer une métrique de risque à exposition ou rendement comparables. H5 doit avoir son propre test ; on ne choisit pas après coup la métrique sur laquelle le modèle semble gagner.

**H6 — Échelle :** augmenter paramètres ou corpus améliore suffisamment les résultats indépendants pour justifier le coût. Une baisse de loss d'entraînement ne valide pas H6.

On peut poursuivre certaines hypothèses en abandonnant une variante d'architecture. Un constat négatif bien identifié protège les étapes suivantes contre une prémisse erronée.

### 5.2 Définition d'une observation point-in-time

Pour une décision `i`, conserver conceptuellement :

- `t_event` : temps de l'événement de marché ;
- `t_receive` : temps auquel le collecteur l'a reçu ;
- `t_cut` : dernière information effectivement admissible pour cette décision ;
- `t_decision` : temps d'achèvement du calcul ;
- `t_arrival` : arrivée supposée ou observée de l'ordre ;
- `t_fill` et prix/volume exécutés ;
- `t_label_end` : instant où la cible devient entièrement connue ;
- versions du modèle, des transformations, de la politique et de la règle de coûts.

Les caractéristiques sont mesurables dans l'information disponible au temps de décision. Une donnée portant une date ancienne mais reçue tardivement n'était pas disponible plus tôt. Pour des historiques ne possédant pas `t_receive`, imposer un délai conservateur et marquer cette reconstruction comme une approximation. Un backtest peut être causal sur le temps d'événement tout en restant optimiste sur la disponibilité réseau.

**Exemple :** prédire une clôture à une heure à partir de bougies de cinq minutes. La dernière bougie utilisée doit être close et reçue. Le prix de la clôture utilisée comme entrée n'est pas automatiquement un prix d'exécution réalisable ; le premier ordre survient après réception, calcul et acheminement.

### 5.3 Splits chronologiques imbriqués

Séparer quatre fonctions, dans cet ordre temporel :

1. **Entraînement** des poids, du normalisateur et du tokenizer.
2. **Validation** pour choisir architecture, hyperparamètres, règle de décision et variables.
3. **Calibration** des probabilités ou intervalles, avec politique d'actualisation prédéfinie.
4. **Test extérieur** qui ne participe à aucun choix.

Répéter plusieurs fenêtres de type walk-forward : chaque modèle ne connaît que le passé de sa date de déploiement simulée. Une fenêtre glissante et une fenêtre croissante constituent deux variantes à sélectionner dans la validation, pas dans le test. Le calendrier de réentraînement et de recalibrage est fixé à l'avance. Un modèle actualisé pendant un test utilise exclusivement les cibles déjà arrivées à maturité ; son algorithme d'actualisation fait partie de la méthode évaluée.

Le nombre exact de mois par partition dépend de la couverture vérifiée et de l'horizon. Un découpage hypothétique tel que « 12 mois entraînement, 2 mois validation, 1 mois calibration, 1 mois test, avance mensuelle » sert à illustrer le mécanisme ; il n'est pas une recommandation aveugle pour l'historique actuellement disponible. Si plusieurs tests mensuels se chevauchent, ne pas compter plusieurs fois les mêmes décisions dans le portefeuille extérieur.

Conserver enfin une dernière période **scellée**, consultée une seule fois pour le candidat final. Un modèle préentraîné après cette période la rend potentiellement impropre à un backtest historique strict, même si aucun fine-tuning local n'a utilisé ses cibles.

### 5.4 Purge, horizon et embargo : des intervalles, pas un pourcentage magique

Pour chaque observation, définir l'intervalle de caractéristiques `[t_start, t_cut]` et l'intervalle cible `(t_cut, t_label_end]`. Les labels de train doivent être connus avant la date de gel de l'entraînement. Purger toute observation dont la cible empiète sur la période protégée, ainsi que toute observation dont le calcul utilise une information ultérieure à sa date admissible.

**Exemple :** décisions toutes les cinq minutes, cible à une heure. Une observation de train à 11 h 30 dont la cible finit à 12 h 30 ne peut appartenir au modèle gelé à 12 h pour un test commençant à 12 h. Selon la convention de frontière et le délai de publication, cela impose au minimum un retrait proche de l'horizon de douze pas à l'extrémité de train. Une cible à barrière variable se purge selon son vrai temps de fin, pas selon l'horizon moyen.

Un embargo est une distance supplémentaire empêchant la réutilisation trop proche d'observations après une partition test lorsque le schéma d'évaluation autorise des échantillons d'entraînement situés des deux côtés de celle-ci. Sa longueur découle du lookback, des horizons, des délais de publication et de la dépendance étudiée. Le walk-forward strict n'a pas de train futur à droite du test : il exige surtout la purge des labels non mûrs et des transformations causales ; ajouter mécaniquement un embargo des deux côtés ne remplace pas ces contrôles.

Le chevauchement de fenêtres de caractéristiques purement passées est courant en production et n'est pas automatiquement une fuite. Il crée cependant une forte dépendance des scores. Il faut traiter séparément causalité des données et incertitude statistique ; supprimer des lignes au hasard ne règle ni l'une ni l'autre.

### 5.5 Contamination du préentraînement

Le registre du modèle importé doit préciser checkpoint exact, date de publication, dates du corpus, actifs, sources, données synthétiques éventuelles et transformations. Quatre niveaux d'évidence sont utiles :

| Niveau | Situation | Interprétation permise |
|---|---|---|
| A | Corpus vérifié entièrement antérieur au test global | Backtest chronologique potentiellement propre, sous réserve des autres audits. |
| B | Séries exactes exclues, mais séries corrélées contemporaines présentes | Test de transfert possible ; pas preuve stricte de prévision de ce futur historique. |
| C | Dates ou contenu du corpus non vérifiables | Résultats exploratoires ; performance historique non certifiable comme indépendante. |
| D | Test prospectif postérieur au gel du checkpoint et du protocole | Preuve temporelle la plus solide disponible, à condition que la période ne serve pas à un réglage rétrospectif. |

Un détecteur de contamination peut enrichir l'audit, pas transformer l'absence de signal détecté en preuve d'innocence. Le modèle entraîné de zéro sur des données à coupure globale connue reste un contrôle essentiel. Les limites de contamination des TSFM sont documentées par [Meyer et al.](https://arxiv.org/abs/2510.13654v3) et l'audit récent [TSFMAudit](https://arxiv.org/abs/2605.26161).

### 5.6 Baselines obligatoires

| Famille | Baseline | Rôle |
|---|---|---|
| Absence de signal | Dernier prix / rendement moyen conditionnel nul ; distribution empirique glissante | Empêcher qu'une série de prix persistante fasse paraître une prévision triviale excellente. |
| Risque simple | Volatilité historique, EWMA, éventuellement GARCH | Identifier un gain essentiellement porté par la prévision de variance. |
| Linéaire | Régression régularisée ou logistique sur rendements, amplitude, volume et coûts | Tester si le signal nécessite un réseau complexe. |
| Non linéaire tabulaire | Arbres de gradient sur caractéristiques causales | Concurrent solide à coût d'entraînement limité. |
| Séquence continue | Petit TCN ou Transformer sur les mêmes entrées | Isoler la valeur du tokenizer. |
| Image | Petit CNN sur images construites à partir des mêmes entrées | Isoler la valeur de la géométrie visuelle. |
| Token simple | Quantification fixe et petit modèle autorégressif | Distinguer effet de discrétisation et effet d'un codebook appris complexe. |
| Politique | Aucun trade, stratégie simple de tendance et stratégie actuellement gelée du bot si reproductible | Mesurer la valeur économique incrémentale. |

Toutes les politiques reçoivent la même convention de coûts, la même information autorisée et le même budget de risque. « Aucun trade » est le plancher de décision, mais n'est pas à lui seul un benchmark scientifique suffisamment exigeant. Une exposition passive peut servir de référence de contexte sans être assimilée à une stratégie à risque identique.

### 5.7 Ablations destinées à comprendre, pas à collectionner des gagnants

Prévoir un petit jeu d'ablations motivées : OHLC seul versus OHLCV ; normalisation avec/sans canal d'échelle ; entrée numérique versus image à information égale ; tokens fixes versus appris ; même architecture entraînée de zéro versus préentraînée ; un horizon versus plusieurs ; prix seul versus prix avec liquidité ; un actif versus multiactif avec coupure globale ; poids gelés versus adaptation planifiée.

Chaque nouvelle ablation compte dans le registre des essais. Garder une matrice limitée, un budget par famille et un objectif principal. Un gain apparaissant seulement après des centaines de variantes doit être interprété avec une correction de sélection et une nouvelle vérification indépendante.

### 5.8 Contrôles négatifs et contrôles de validité

- **Cible permutée par blocs appropriés** : le modèle ne devrait plus prévoir la relation temporelle recherchée. La permutation brute n'est pas toujours un test nul valide sous dépendance ; la méthode de permutation doit être documentée.
- **Décalage temporel de la cible** : détruire la liaison locale par décalages hors de la portée plausible du signal, avec vigilance sur saisonnalité et frontières.
- **Prix simulés sans moyenne prévisible mais avec volatilité variable** : vérifier que l'évaluation distingue apprentissage du risque et alpha directionnel.
- **Métadonnées uniquement** : tester si heure, actif ou identifiant de fichier reproduisent anormalement le résultat ; un identifiant encodant le futur invalide l'expérience.
- **Images au style perturbé** : couleurs, épaisseur, marges et résolution changées sans modifier les valeurs ; une forte sensibilité révèle une fragilité de représentation.
- **Invariants OHLC** : vérifier `low ≤ min(open, close) ≤ max(open, close) ≤ high`, volume non négatif et timestamps cohérents. Une génération doit respecter ces contraintes par construction ou les violations doivent être mesurées.
- **Échantillon volontairement contaminé, réservé à l'audit** : un contrôle positif artificiel peut vérifier qu'un détecteur de fuite repère une anomalie évidente. Il ne doit jamais entrer dans le classement des méthodes.
- **Politique randomisée avec exposition et fréquence proches** : distinguer profit de signal, profit d'exposition et effet fortuit d'un régime haussier.

Un contrôle négatif qui réussit trop bien est une raison d'arrêter l'interprétation et d'auditer la chaîne. Un contrôle négatif qui échoue comme prévu ne prouve pas à lui seul que toute fuite a été éliminée.

### 5.9 Grille de contradiction pour les langues expérimentales

Cette grille est un complément au futur atlas de représentations. Elle autorise l'exploration créative tout en empêchant les analogies de remplacer une définition mathématique.

| Langue candidate | Question préalable | Contrôle qui la rend testable |
|---|---|---|
| Prix absolus | Le niveau est-il un signal, un identifiant d'actif ou un repère temporel mémorisable ? | Changer l'unité de cotation, tester de nouveaux niveaux de prix, comparer avec/sans identifiant d'actif et canal d'échelle. |
| Écarts arithmétiques | L'unité monétaire et la valeur du tick dominent-elles le vocabulaire ? | Déclarer l'unité, tester normalisation causale et prix de départ conservé pour reconstruction. |
| Pourcentages ou log-ratios | Quel dénominateur ? Que faire des valeurs nulles ou non positives des variables autres que le prix ? | Définir la transformation variable par variable, les cas limites, l'inverse et l'erreur ; ne pas appliquer aveuglément le logarithme au funding ou à un volume nul. |
| Paliers, seuils ou directional-change | Quand l'événement est-il confirmé et que perd-on entre deux seuils ? | Horodatage causal de confirmation, durée et dépassement, derniers états incomplets, ablation de l'information intrapalier. |
| Hausse/baisse uniquement | Une suite de signes oublie-t-elle toutes les amplitudes qui déterminent le gain net ? | Baseline sur signes, puis réintroduction progressive d'amplitude, durée, volatilité et coûts ; préciser ce qui n'est pas reconstructible. |
| Géométrie, contours ou relief | Les invariances imposées suppriment-elles la direction, l'échelle ou la temporalité utile ? | Transformations contrôlées, conservation des unités auxiliaires et comparaison aux valeurs numériques d'origine. |
| Musique, notes, rythme ou signal audio | Quelle relation déterministe lie notes, intensité et durée aux variables de marché ? | Même information et budget, ablation d'un préentraînement audio, contrôle sur transformations aléatoires de vocabulaire. La ressemblance musicale n'est pas une preuve de structure économique. |
| Spectre ou ondelettes | La transformation et le lissage utilisent-ils uniquement une fenêtre passée ? | Fenêtre achevée avant décision ; pas de filtrage symétrique sur toute la série ; comparaison conservant phase et localisation si nécessaires. |
| Topologie ou résumés de forme | Deux trajectoires économiquement différentes deviennent-elles identiques dans le résumé ? | Construire des paires de contre-exemples, mesurer information perdue, ajouter la temporalité et tester les invariances réellement utiles. |
| Figures chartistes nommées | Qui donne le label, avec quel accord entre annotateurs et quel retard ? | Détecteurs reproductibles, date de disponibilité explicite, figures reconnues sans voir leur dénouement ; labels humains comme supervision faillible. |
| Mélange de langues | Le gain vient-il de la représentation ou simplement d'entrées/capacité supplémentaires ? | Budget et information appariés, ablation de chaque langue, comparaison à une duplication neutre des mêmes données. |

Pour chaque langue, établir une fiche : variables sources, transformation, disponibilité, caractère réversible ou avec perte, fréquence/durée du token, entropie empirique, coût de calcul, erreurs de reconstruction dans les unités d'origine et domaine d'invariance. Une représentation irréversible n'est pas exclue : la compression peut régulariser. Elle doit simplement annoncer ce qu'elle abandonne et prouver que ce compromis sert la tâche.

Il n'existe pas d'unique « budget égal » parfait. Rapporter au minimum paramètres, tokens traités, durée, mémoire et effort de réglage. Une langue compacte peut traiter davantage de temps de marché avec le même contexte ; c'est un bénéfice potentiel légitime, à mesurer séparément d'un avantage de représentation à historique égal. Si l'on compare des modèles préentraînés sur texte, image ou audio, distinguer également l'information injectée et le coût historique de leur préentraînement.

### 5.10 Marchés réels, horloges variables et preuve finale

Le corpus empirique principal et toutes les preuves finales de prévision ou d'utilité économique doivent provenir de **données réelles de marché**, avec provenance et disponibilité vérifiées. Un contre-exemple mathématique ou une série artificielle sans signal sert uniquement à comprendre une propriété ou auditer une méthode. Il ne démontre ni la valeur d'un préentraînement sur marchés réels ni l'efficacité d'une stratégie. Aucun résultat synthétique ne doit se substituer au test réel protégé puis prospectif.

Pour des tokens à durée variable, prévoir le prochain événement n'est pas la même tâche que prévoir la prochaine heure. Une suite de dix franchissements de seuils peut durer quelques secondes ou plusieurs jours. Le modèle doit représenter conjointement la marque de l'événement, sa durée et l'état où aucun nouvel événement n'a encore été observé. Les fenêtres inachevées ne sont pas à supprimer en fonction de leur durée future : cela créerait un biais de sélection.

Comparer les langues sur des horizons calendaires communs et des coûts applicables au vrai temps écoulé. Publier aussi leurs métriques propres en temps événementiel. La conversion d'un processus d'événements en trajectoires horaires exige de modéliser les temps d'attente et la censure ; elle ne se résout pas en remplaçant mécaniquement un nombre de tokens par un nombre de minutes.

## 6. Évaluer distributions, décisions et incertitude

### 6.1 Tableau de mesures

| Objet | Mesures proposées | Précaution |
|---|---|---|
| Distribution continue du rendement | CRPS, log-score si densité comparable, pinball loss pour quantiles | Même cible et unités ; éviter les comparaisons de densités incohérentes après changement de transformation. |
| Événement tel que rendement net positif | Brier score, log-loss, diagrammes de fiabilité | Classe et coût définis avant test ; accuracy insuffisante. |
| Intervalles | Couverture et largeur à plusieurs niveaux | Couverture seule peut être obtenue avec des intervalles inutilisablement larges. |
| Trajectoires | Marginales par horizon, dépendances temporelles, probabilités de franchissement, scores multivariés adaptés | Un bon score marginal ne garantit pas une bonne probabilité de toucher un stop avant une cible. |
| Décision | PnL net, turnover, exposition, drawdown, pertes de queue, profit par unité de coût | Même capital, mêmes contraintes et conventions d'exécution. |
| Robustesse | Résultats par période, actif, volatilité, spread et disponibilité des données | Sous-groupes prévus ; ne pas chercher seulement ceux qui gagnent. |
| Opération | Latences, couverture des données, temps de reprise, fréquence d'abstention | Moyenne insuffisante : quantiles et cas dégradés. |

Les scores propres encouragent des probabilités honnêtes, mais leur pertinence pour la politique doit être vérifiée séparément. [Gneiting–Raftery](https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf).

### 6.2 Calibration et inférence conforme

Un « 70 % » crédible signifie que, sur une population comparable suffisamment grande, l'événement survient approximativement sept fois sur dix. Ce n'est ni 70 % de rendement ni une garantie sur une occurrence. La calibration doit être estimée sur des observations futures par rapport à l'ajustement du calibrateur. Une correction de température est une baseline pour des logits catégoriels, pas une solution universelle. [Guo et al.](https://proceedings.mlr.press/v70/guo17a.html).

La conformité adaptative peut être une enveloppe de prudence pour des intervalles. Il faut pourtant distinguer couverture marginale, couverture sur le long terme et couverture conditionnelle dans les cas où la stratégie agit. Les garanties standard sous échangeabilité ne s'appliquent pas automatiquement à une série dépendante et changeante. Une méthode adaptative peut maintenir une fréquence cible sur la durée tout en couvrant mal une crise ou en produisant des intervalles très larges. Ses mises à jour doivent attendre les labels mûrs et gérer explicitement les horizons retardés. [Gibbs–Candès](https://arxiv.org/abs/2106.00170).

La règle de trading sélectionne elle-même un sous-ensemble d'observations. Publier la calibration sur ce sous-ensemble, le nombre effectif de cas et la largeur des intervalles ; ne pas supposer qu'une calibration globale persiste après sélection. Il faut également examiner les erreurs conditionnelles aux fills, surtout pour des ordres maker.

### 6.3 Incertitude statistique sous dépendance

Les scores et rendements consécutifs ne sont pas indépendants. Utiliser des comparaisons appariées : à chaque date, comparer le modèle et son baseline sur la même décision. Estimer l'incertitude à l'aide de blocs temporels ou d'un bootstrap stationnaire adapté, en conservant ensemble les actifs d'une même période afin de préserver leurs chocs communs. Tester la sensibilité à plusieurs longueurs de blocs raisonnables, annoncées avant lecture du résultat final.

Le bootstrap stationnaire de Politis et Romano vise des observations stationnaires faiblement dépendantes ; un changement de régime structurel n'est pas neutralisé par ce rééchantillonnage. Il faut compléter les intervalles par la dispersion entre fenêtres et des scénarios de stress. [Politis–Romano, 1994](https://www.tandfonline.com/doi/abs/10.1080/01621459.1994.10476870).

Un intervalle calculé sur la politique finalement choisie, comme si elle n'avait jamais été sélectionnée, sous-estime le risque de recherche. Le registre des essais doit inclure architecture, horizon, codebook, normalisation, actifs, seeds, politique et conditions de coût. Des outils tels que DSR, PBO et les tests de type Reality Check / SPA sont des compléments pour la sélection multiple ; leurs hypothèses, leur mise en œuvre et le choix des candidats doivent être explicités. Ils ne remplacent pas un test prospectif. [DSR](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf), [PBO](https://escholarship.org/uc/item/4w1110bb), [White, 2000](https://users.ssc.wisc.edu/~behansen/718/White2000.pdf), [Hansen, 2005](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=264569).

Il n'existe pas de nombre universel de trades suffisant. La durée pertinente dépend de la variabilité, de la dépendance et du gain minimal recherché. À titre illustratif seulement, détecter une très petite différence moyenne standardisée `d = 0,05` avec un test indépendant unilatéral à 5 % et puissance 80 % exige approximativement `(1,645 + 0,842)^2 / 0,05^2 ≈ 2 474` observations indépendantes. Des milliers de bougies chevauchantes peuvent fournir beaucoup moins d'information. Ce calcul gaussien n'est pas une analyse de puissance adaptée au trading ; il montre pourquoi des résultats faibles demandent des historiques longs.

## 7. Simulation d'exécution et coûts Hyperliquid

### 7.1 Comptabilité minimale

Une politique doit être jugée sur une comptabilité cohérente des prix d'entrée et de sortie, des frais, du funding et de l'exposition. Schématiquement :

`PnL_net = PnL_aux_prix_exécutés − frais_explicitement_payés − funding_net − autres_coûts_non_inclus`.

Si spread et slippage sont déjà contenus dans les prix exécutés, ne pas les soustraire une seconde fois. Si le point de départ est un rendement au mid-price, il faut au contraire les ajouter comme coûts explicites. Cette convention doit être identique pour tous les modèles.

Au barème de base de niveau 0 consulté, les frais perpétuels affichés sont **0,045 % taker** et **0,015 % maker** par exécution, avant situations particulières, réductions ou paramètres applicables au compte et au marché. Un aller-retour taker à ce barème représente donc environ **9 points de base de frais explicites**, auxquels s'ajoutent les autres coûts. Ce calcul est un exemple ; un historique doit utiliser le barème connu et applicable à la date considérée, et non le barème actuel rétroactivement. [Frais Hyperliquid](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees).

Le funding des perpétuels Hyperliquid est payé chaque heure. Il faut imputer les flux effectifs de la position et ne pas donner au modèle, avant publication, le taux futur réalisé. [Funding Hyperliquid](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/funding).

### 7.2 Pourquoi commencer par une convention taker prudente

Une exécution taker à un instant réalisable, avec spread, profondeur et latence modélisés, est plus facile à rendre auditable qu'une exécution maker supposée parfaite. Cela n'en fait pas nécessairement la meilleure stratégie finale ; c'est un premier test sévère de la présence d'un avantage assez grand pour supporter les coûts.

Avec de simples bougies, les prix high/low ne disent ni dans quel ordre les événements ont eu lieu, ni quelle quantité était disponible, ni si un ordre particulier aurait été exécuté. Lorsque stop et objectif sont tous deux touchés dans la même bougie, l'ordre des événements est ambigu. Soit des données plus fines permettent de le résoudre, soit le scénario défavorable est retenu et la proportion de cas ambigus est publiée. Le prix de clôture d'une bougie ne peut simultanément servir d'entrée finale et de fill sans retard.

Pour des ordres maker, modéliser l'arrivée de l'ordre, son prix, sa taille, les annulations, les fills partiels, le temps d'attente et la sélection adverse. Des snapshots L2 agrégés ne révèlent généralement pas la position exacte d'un nouvel ordre dans une file. Définir une borne prudente de fill, puis la confronter à une observation future. « Le prix a touché ma limite » ne vaut pas confirmation de fill.

### 7.3 Stress proposés

Les valeurs ci-dessous sont des scénarios de protocole, pas des prévisions du marché :

- frais réels applicables, puis scénarios de spread/slippage dégradés de 1,5× et 2× ;
- latence nominale mesurée, puis latence haute mesurée et retard supplémentaire d'une décision ;
- réduction des fills maker et augmentation de leur sélection adverse ;
- funding défavorable, profondeur réduite, trous de données, volatilité forte ;
- retrait des meilleurs jours/trades pour mesurer la concentration des résultats, sans en faire une manipulation du test principal ;
- capacité : tailles d'ordre croissantes jusqu'à ce que profondeur, impact ou limites d'exposition rendent la politique non viable.

Les stress ne prédisent pas le pire cas absolu. Ils révèlent la fragilité à des erreurs de modèle d'exécution plausibles. Leur calibration doit ensuite être reliée aux données de la place et à la latence OVH réellement observée.

## 8. Critères de passage et d'arrêt à fixer avant le POC

Ces critères constituent une **proposition de gouvernance expérimentale**. Ils ne sont ni des résultats obtenus ni des garanties. Les seuils économiques et de risque exacts exigent le budget, le capital envisagé et les limites choisies par le propriétaire. Leur absence ne bloque pas la réflexion ; elle empêche de prétendre qu'un déploiement réel serait déjà justifié.

| Gate | Condition de passage proposée | Si elle échoue |
|---|---|---|
| G0 — Données | Provenance vérifiable, calendrier causal, couverture et trous quantifiés, cibles réellement disponibles. | Réparer la donnée ou restreindre la question ; aucune conclusion de performance. |
| G1 — Protocole | Baselines, cible principale, périodes, critères et budget d'essais figés ; contrôles de fuite satisfaisants. | Revoir le plan avant de comparer les modèles. |
| G2 — Prédiction | Gain sur le score principal face au meilleur baseline présélectionné ; incertitude compatible avec un effet utile ; aucun régime critique masqué. | Ne pas revendiquer d'avantage prédictif ; simplifier ou tester une hypothèse distincte. |
| G3 — Contribution LCM | Ablations indiquant que tokens, image ou préentraînement apportent quelque chose au-delà des données et de la complexité. | Conserver éventuellement le meilleur modèle simple ; le label LCM n'est pas un objectif en soi. |
| G4 — Économie historique | Valeur incrémentale nette à risque comparable ; résultat robuste aux coûts/latences plausibles ; incertitude et sélection multiple documentées. | Pas de passage au capital réel ; usage de recherche ou de risque seulement avec test dédié. |
| G5 — Observation prospective | Décisions horodatées avant observation des cibles, coût et comportement plausibles, aucune adaptation rétrospective cachée. | Réviser le modèle et ouvrir une nouvelle période prospective. |
| G6 — Exploitation | Retour arrière, limites indépendantes, gestion des données périmées et redémarrage testés ; budget de latence respecté. | Maintenir l'observation sans capital ou le modèle en simple conseil. |

Une version stricte et concrète de G2 peut demander un intervalle à 95 % du gain apparié sur le score principal entièrement favorable, après le mécanisme de sélection annoncé. Une version stricte de G4 peut demander une borne inférieure positive de valeur incrémentale nette après correction pertinente, ainsi que le respect des plafonds de risque dans les scénarios prévus. Si la puissance est insuffisante, le verdict est **indéterminé**, pas « rentable » ni « impossible ».

Ne pas choisir un seuil de Sharpe isolé comme passeport universel. Un Sharpe dépend de l'agrégation temporelle, de l'autocorrélation, des queues, des essais effectués et de la concentration de l'exposition. Ne pas fixer « quatre semaines de paper trading suffisent » sans analyser le nombre de régimes et de décisions informatives observés.

### 8.1 Arrêts immédiats de l'interprétation scientifique

Un résultat est déclaré non interprétable si une fuite de futur est constatée, si le coût de transaction est incomplet, si le baseline est lésé, si le modèle testé a été choisi après consultation de sa période présentée comme finale, ou si une précision de données/fills inconnue est présentée comme mesurée. Le travail peut reprendre après correction ; l'ancien résultat ne doit pas rester dans la conclusion comme preuve.

### 8.2 Trois issues positives distinctes, une issue négative recevable

1. **Signal directionnel confirmé dans son domaine mesuré** : poursuivre l'observation et un déploiement contrôlé à décider ensuite.
2. **Prévision du risque utile** : exploiter ce résultat via un protocole spécifique de filtrage ou de dimensionnement.
3. **Représentation transférable utile** : conserver l'encodeur pour d'autres tâches si elles sont évaluées proprement.
4. **Aucun gain détectable** : conserver données, pipeline et conclusion ; réviser la question plutôt que multiplier secrètement les essais.

## 9. Recommandations d'architecture issues de cette contre-expertise

La proposition de recherche la plus défendable est un **modèle probabiliste causal d'états de marché**, comparé à des modèles continus et aux benchmarks de risque. TRAME devient le nom de travail ; la question demeure celle initialement nommée LCM. Le besoin scientifique ne force ni une image, ni un tokenizer appris, ni un très grand nombre de paramètres. Une taille modeste facilite le premier concours contrôlé ; elle ne constitue pas un plafond imposé à la recherche fondation.

Le socle recommandé à tester comporte :

- une représentation des valeurs OHLCV dont les invariants et la causalité sont contrôlables ;
- une normalisation apprise sur train ou calculée sur passé connu, avec échelle utile conservée ;
- une sortie qui décrit plusieurs futurs possibles, évaluée en unités économiques ;
- une politique de décision séparée, simple et figée pendant chaque test ;
- une couche indépendante de risque et d'exécution ;
- une ablation systématique de l'image, des tokens, du préentraînement et des variables supplémentaires.

Une piste réellement intéressante à explorer est de comparer deux objectifs : un objectif génératif général sur les états futurs et un objectif probabiliste ciblé sur les événements utiles à la décision. Leur combinaison pourrait préserver une représentation transférable tout en consacrant de la capacité aux incertitudes qui affectent l'action. **Cette combinaison est ici une hypothèse de conception**, pas une innovation prouvée ni une promesse d'alpha. L'objectif auxiliaire, ses poids et ses effets doivent entrer dans le registre d'essais.

Le terme « intelligence émergente » n'est pas un critère de succès suffisamment opérationnel pour ce POC. Des capacités mesurables le remplacent : transfert vers un actif tenu à l'écart, résistance à un changement de style visuel, meilleure calibration dans un régime nouveau, reconnaissance d'une donnée aberrante et décision d'abstention. Même une réussite à ces tests ne démontrerait pas une compréhension causale du marché.

## 10. Documents de preuve à préparer au moment du futur POC

1. **Fiche de question scientifique** : hypothèses, variable cible, horizon, unité d'observation, gain minimal utile.
2. **Data card** : sources, droits d'usage, actifs, plages temporelles, trous, fuseaux, temps de disponibilité, qualité et limites.
3. **Model card** : représentation, préentraînement, dates de corpus, ressources, domaine validé, limites, version.
4. **Registre d'expériences** : tous les essais, y compris échecs et variantes abandonnées, et chaque consultation du test.
5. **Fiche de politique** : transformation des prévisions en exposition, coûts, contraintes, seuil d'abstention, calendrier de mise à jour.
6. **Rapport de validation** : scores, intervalles, résultats par période, contrôles négatifs, ablations, tests multiples et limites de puissance.
7. **Rapport d'exécution** : fills, spread, funding, latence, capacité, erreurs réseau et écarts avec simulation.
8. **Décision de passage** : gate atteint, preuves manquantes, responsabilité de validation, taille maximale et retour arrière éventuel.

**Limite de la présente étude :** aucune de ces preuves expérimentales n'a été produite ici. Le résultat est un protocole assez précis pour éviter qu'une expérience future soit séduisante mais non concluante. L'accès réel à l'historique GitHub/OVH, les ressources de calcul et les détails du bot doivent être documentés séparément à partir d'observations vérifiées ; ils ne sont pas inférés du seul thème du projet.
