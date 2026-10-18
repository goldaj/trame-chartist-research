# Faisabilité scientifique et technique de TRAME

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
