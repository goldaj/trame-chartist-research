# TRAME : une sortie générative définie et des cibles réelles auditées

Édition 2.4 - 16 octobre 2026. Complément au plan 11 et à la proposition 12. P1-D reste en révision 0.4 ; le candidat génératif séparé P1-B0 passe de 0.1 à 0.2. Ce document précise la conception et présente un audit de reconstruction. Aucun GPT, aucune tête prédictive et aucun entraînement ne sont implémentés. Les anciennes éditions restent archivées.

## 1. Ce qui change, en langage courant

Nous avons maintenant une définition plus concrète de ce que le GPT pourrait produire : un nombre entier décrivant le déplacement depuis le dernier prix reconstruit, puis un autre entier, et ainsi de suite. Le modèle aurait accès au passé connu et à ses propres codes précédents. Il produirait des probabilités sur les prochaines possibilités, pas une unique courbe présentée comme certaine.

Trois sorties sont proposées : une loi numérique simple, une correction par case du dictionnaire, et une correction qui partage des composantes entre cases. Les trois lisent exactement le même passé dans cette première comparaison. L'objectif est de savoir ce qu'apporte la structure du langage de sortie avant de modifier simultanément toutes les entrées.

Le codage a été vérifié sur six séries réelles de devises, dans leur seule partition d'ajustement 1999-2009. Les 304 920 présentations de cibles proviennent de 15 360 cotations distinctes ; leurs fenêtres se recouvrent. La reconstruction respecte sa borne numérique dans tous les cas testés. Cela démontre une cohérence du codage sur cet échantillon, aucune capacité de prévision.

Deux réserves modifient la conception. Seuls 156 codes centraux apparaissent parmi 4 096 possibles. Et une distribution peut autoriser mathématiquement tous les extrêmes tout en leur donnant une probabilité presque nulle par construction. La prochaine étape doit donc qualifier la distribution et son évaluation, plutôt que supposer que le mot « génératif » résout ces difficultés.

## 2. Un invariant simplifie le langage

À une origine i, on connaît le prix P_i et l'échelle s_i : écart-type population des 64 derniers incréments logarithmiques, avec plancher 10^-6. On fixe delta=s_i/8 pour les vingt publications futures. On définit u_h=log(P_(i+h)), u_0=log(P_i), et R(x)=floor(x+1/2), avec demi-entiers vers +inf.

La proposition 0.1 utilisait la récurrence suivante, en notant uhat le prix logarithmique reconstruit :

`k_h = R((u_h - uhat_(h-1))/delta)`

`uhat_h = uhat_(h-1) + delta*k_h`.

Or, si n_(h-1) est entier et uhat_(h-1)=u_0+delta*n_(h-1), l'identité R(x-n)=R(x)-n donne :

`n_h = R((u_h-u_0)/delta) ; k_h = n_h-n_(h-1)`

`uhat_h = u_0+delta*n_h ; n_0=0`.

C'est exactement le même codec en arithmétique réelle. Il est donc possible de conserver un état entier cumulé et d'éviter de faire dépendre la définition canonique de l'accumulation des arrondis flottants. Cette formulation 0.2 a été consignée avant le nouvel audit. La récurrence flottante antérieure a été comparée, sans correction silencieuse des écarts éventuels.

La borne reste |uhat_h-u_h| <= delta/2 pour les vrais codes, sans accumulation. Elle ne borne pas l'erreur d'une suite de codes prédits. Les 3 609 transitions rationnelles construites vérifient l'identité et la borne, y compris pour des niveaux négatifs ; elles ne constituent pas des données de marché.

Un code delta n'apporte donc pas plus d'information qu'un niveau quantifié cumulé, lorsque l'ancre et le pas sont connus. Le choix peut néanmoins changer la difficulté statistique de la prédiction : modéliser un petit déplacement et modéliser un niveau cumulé ne sont pas les mêmes biais d'architecture.

## 3. Attention aux motifs créés par le codec

Écrivons e_h=uhat_h-u_h. L'incrément reconstruit satisfait exactement :

`delta*k_h = (u_h-u_(h-1)) + e_h-e_(h-1)`.

Le signal codé contient donc des différences d'erreurs de quantification. Sous une approximation supplémentaire d'erreurs indépendantes, centrées et uniformes sur [-delta/2,delta/2], le bruit ajouté a une variance delta²/6 et une covariance à un retard de -delta²/12. Cette approximation n'a pas été testée sur le corpus et n'est pas une propriété universelle des erreurs de quantification ; elle illustre un mécanisme possible de dépendance artificielle.

Un GPT peut apprendre des régularités de codage sans améliorer la prévision des prix. Un gain de compression des codes devra être confronté aux scores en prix natifs et aux témoins numériques. L'état initial exact e_0=0 rend également le premier pas particulier. Ni une entropie de codes plus faible ni une autocorrélation des codes ne suffiraient à conclure à un motif économique découvert.

## 4. Architecture proposée : un GPT, trois sorties

Le cœur reprend le Transformer causal documenté dans P1-D : L blocs, largeur d, attention multi-têtes, MLP de largeur 4d, normalisations avant blocs et positions sinusoïdales fixes. Le passé contient 256 observations Q, chacune issue du même quantificateur et de la même projection affine. Le contexte est causal à l'origine de prévision ; aucune perte next-token n'est appliquée à ses anciennes positions recentrées sur cette origine.

En teacher forcing, la séquence possède 276 positions : 256 observations historiques, un BOS, puis 19 états futurs déjà codés. BOS prédit k_1 ; l'état n_h/8 prédit k_(h+1), pour h de 1 à 19. Le masque interdit de regarder les codes ultérieurs. En génération, les états proviennent uniquement des codes tirés par le modèle. La vingtième cible n'est jamais un input nécessaire à sa propre prédiction.

Une projection numérique N(v)=a*v+b est commune aux types de positions dans chaque modèle. Le passé utilise les milieux Q, le BOS utilise zéro, les positions futures utilisent n_h/8. Ce changement de convention est explicite : Q emploie des cellules par floor pour le passé, les cibles futures un arrondi au plus proche. Toutes les sorties comparées partagent ces conventions.

Les métadonnées sont quatre scalaires projetés par une transformation affine : log(P_i), log(s_i), log1p du délai calendaire, indicateur de sortie du dictionnaire. Les délais futurs inconnus sont remplacés par une sentinelle zéro, identifiée par le type FUTURE. Pour ces positions, l'indicateur est calculé depuis n_h, pas depuis un prix futur inconnu. Trois embeddings de type HISTORY/BOS/FUTURE s'ajoutent aux six embeddings de devise. Il n'y a aucune date future réalisée introduite comme information.

| Sortie | Valeurs affines produites à chaque pas | Rôle |
|---|---:|---|
| BASE | 2 | Moyenne et écart-type de la normale arrondie |
| FLAT | 4 098 | BASE et une correction par code central |
| HIER | 520 | BASE, 512 composantes grossières et trois paires binaires |

Pour k central, écrire q=floor(k/8), puis décomposer le reste de 0 à 7 en trois bits. HIER forme g_k=g_q+g_bit2+g_bit1+g_bit0. FLAT apprend g_k directement. HIER impose une classe de fonctions plus restreinte ; l'égalité de données conditionnantes ne signifie pas égalité d'expressivité. Les composantes additives ont aussi des redondances de paramétrage : déplacer une constante d'une composante vers une autre peut laisser leur somme inchangée.

La sortie utilise a_k=A*tanh(g_k/A), un choix résiduel dont la dérivée en zéro vaut un. Les sorties BASE, FLAT et HIER constituent un nouveau contraste sur la génération ; ce ne sont pas les encodeurs d'entrée Q, F+ et H+ déjà décrits dans P1-D.

## 5. Probabilités normalisées et bornes proposées

Sur tous les entiers, la base est la normale arrondie :

`q(k)=Phi((k+1/2-mu)/sigma)-Phi((k-1/2-mu)/sigma)`.

Sur I=[-2048,2047], w(k)=exp(a_k) ; ailleurs w(k)=1. La loi finale vaut p(k)=q(k)w(k)/Z, avec Z=q(hors I)+somme_I q(k)exp(a_k). Les deux queues commencent aux limites continues -2048.5 et 2047.5. BASE utilise simplement q, avec Z=1.

La masse par différence de CDF a des antécédents dans les modèles génératifs. PixelCNN++ l'utilise pour des pixels et des mélanges logistiques ; cela ne valide ni une base gaussienne ni les hypothèses financières proposées ici. [Source primaire, section 2.1](https://arxiv.org/pdf/1701.05517).

La révision 0.2 propose M=256, S=64, sigma_min=0.25 et A=4. On pose `mu=M*tanh(g_mu/M)`, et `sigma=sigma_min+(S-sigma_min)*sigmoid(g_sigma)`. Une sensibilité S=256 est inscrite avant l'audit. Ces valeurs sont des choix de conception non ajustés : une unité k représente s_i/8, donc les bornes centrales correspondent à 32 échelles s_i pour la moyenne et huit pour l'écart-type. Elles ne plafonnent pas le support des codes.

À l'initialisation proposée, les matrices de sortie sont nulles ; mu=0, sigma=8, a_k=0. Le biais de g_sigma est log((8-.25)/(64-8)). La sensibilité S=256 doit adapter ce biais pour conserver sigma initial égal à huit. L'initialisation identique en distribution permet de comparer le départ ; elle ne prouve pas que l'optimisation soit équitable ou convergente. Les gradients du cœur sont retardés au premier pas par les matrices de sortie nulles, comme signalé pour P1-D.

Sous des bornes uniformes M,S,A à tous les états générés, la preuve de 12 reste valable, conditionnellement à l'origine et à son delta fixe : `E[P_hat_h | H_i] <= P_i*C^h`, avec `C=exp(2A+delta/2+delta*M+delta²*S²/2)`. Cette borne peut être extrêmement large. Finitude mathématique des moments et précision d'une estimation Monte-Carlo sont deux sujets différents.

### Une limite substantielle : support infini ne signifie pas extrêmes bien représentés

À l'extérieur du dictionnaire, w=1 et Z>=exp(-A). Donc p(hors I)<=exp(A)*q(hors I). On peut borner chaque queue gaussienne uniformément sur |mu|<=M et sigma<=S, puis additionner ces deux bornes conservatrices.

| Configuration proposée | Borne supérieure de p(hors I), par état |
|---|---:|
| M=256, S=64, A=4 | 9.0844 × 10^-171 |
| M=256, S=256, A=4 | 1.3977 × 10^-10 |

Ce sont des conséquences des hypothèses, pas des probabilités mesurées sur les marchés. La loi admet tous les entiers mais impose des queues très faibles au-delà du dictionnaire. Même la sensibilité plus large ne constitue pas une garantie de calibration extrême. Le statut de cette tête reste **candidat de comparaison**, et non solution universelle aux changements de régime. Des mélanges gaussiens à paramètres bornés ou une autre loi à moments exponentiels contrôlés restent des pistes distinctes à spécifier ; elles ne sont pas réputées supérieures sans test.

## 6. Un symbole absent n'est pas une ligne de sortie sans gradient

Pour une correction indépendante a_j centrale et la perte -log p(k), la dérivée vaut p(j)-1(k=j), à base q fixée. Un code jamais observé comme cible positive peut donc recevoir un gradient par le normalisateur. En calcul machine, une masse sous-fluée ou une saturation peut néanmoins annuler ce signal numérique.

Cela diffère des tables d'entrée : une ligne jamais consultée peut rester sans gradient de tâche. La règle P1-D qui garde nulles les lignes d'entrée jamais visitées ne doit pas être transférée à la tête de sortie. HIER redistribue les gradients par ses composantes partagées.

Un gradient ne remplace pas une observation. Pour un symbole jamais réalisé, il s'agit surtout d'ajuster la masse concurrente des cibles vues. Cela ne démontre ni estimation fiable de sa probabilité ni généralisation à une crise absente. La base mu/sigma participe à toutes les masses et peut apprendre sur les cibles ordinaires ; cela ne résout pas les compensations possibles avec les corrections centrales.

## 7. Taille et coût : compter deux choses différentes

Le commun, hors tête de sortie, compte 12Ld²+13Ld+18d paramètres. Les 18d rassemblent projection numérique 2d, devises 6d, projection des métadonnées 5d, normalisation finale 2d et types 3d. Une tête à r sorties ajoute r(d+1). Les comptes ont été recoupés par un inventaire séparé des modules, sans instancier de réseau.

| L, d | BASE | HIER | FLAT |
|---|---:|---:|---:|
| 4, 128 | 795 650 | 862 472 | 1 324 034 |
| 6, 256 | 4 743 682 | 4 876 808 | 5 796 354 |
| 8, 512 | 25 229 314 | 25 495 048 | 27 330 562 |

HIER utilise moins de poids de sortie. Cependant sa somme de normalisation comporte encore 4 096 masses centrales par pas, soit 81 920 contributions pour les vingt positions cibles d'une origine. La dépendance de q(k) à k et la correction bornée empêchent de remplacer directement cette somme par 518 termes indépendants. BASE n'a pas cette somme centrale.

Pour une attention dense sur n=276 positions, les principales multiplications du cœur valent approximativement L*(24nd²+4n²d) opérations flottantes en forward, en comptant multiplication et addition séparément. Cela donne environ 0.590, 3.073 et 15.140 milliards d'opérations pour les trois tailles. Ces estimations excluent rétropropagation, normalisations, softmax et fonctions spéciales.

À petite taille, les matrices de sortie ajoutent respectivement 10 240, 2 662 400 et 20 981 760 opérations pour BASE, HIER et FLAT. Le coût des CDF, de leurs dérivées et des réductions vient en plus ; aucun temps GPU, débit, mémoire ou budget monétaire n'a été mesuré. Les 88 exécutions proposées pour P1-D ne doivent pas être attribuées automatiquement à P1-B0.

## 8. Audit réel : déclaration et résultats

Le protocole, le candidat 0.2 et le script ont été scellés localement le 16 octobre à 02:59:37 UTC, avant de calculer les nouveaux codes cibles. Ce gel d'intégrité n'est pas une préinscription externe, et le corpus avait déjà été exploré pour d'autres représentations. La source reste le fichier BCE de SHA-256 b8a684b6331d3cf0310a1838efdce806495906ead99d672671642c3bf24130de, reçu en 2026, sans certification des versions historiques initiales.

Le filtre 1999-2009 est appliqué avant conversion des prix en nombres. Les 16 950 lignes hors période sont ignorées pour les valeurs ; le calcul de l'empreinte lit seulement leurs octets. Aucun nouveau prix de développement ou pseudo-test n'a été analysé dans cette opération. Les 16 896 prix numériques admis représentent 2 816 dates par devise.

Avec 256 observations historiques et vingt publications futures entièrement contenues dans la partition, on retrouve 2 541 origines par devise, du 27 décembre 1999 au 2 décembre 2009. Les cibles correspondent à 2 560 dates distinctes par devise. Leur réutilisation sur vingt horizons explique les 304 920 présentations ; ce ne sont pas 304 920 observations indépendantes.

| Devise par EUR | Code minimal | Code maximal | Codes distincts | Maximum absolu de n |
|---|---:|---:|---:|---:|
| USD | -38 | 44 | 81 | 152 |
| JPY | -59 | 56 | 102 | 227 |
| GBP | -35 | 67 | 91 | 158 |
| CHF | -82 | 58 | 122 | 217 |
| CAD | -32 | 47 | 78 | 190 |
| AUD | -80 | 101 | 131 | 247 |

L'union comprend 156 codes, de -82 à 101, sans sortie de [-2048,2047]. La valeur absolue a pour quantiles 50 %, 90 %, 99 % et 99.9 % les valeurs 5, 14, 25 et 45. Il y a 18 155 codes nuls, soit 5.954 %. Ces fréquences sont celles de présentations recouvrantes, conditionnées par l'origine et son échelle.

Zéro divergence de codes a été trouvé entre la définition canonique et la récurrence flottante. Zéro dépassement de borne avec la tolérance déclarée, et aucune activation du plancher d'échelle. L'erreur maximale observée est 0.499992732*delta. La tolérance prévue est un diagnostic d'ingénierie fondé sur l'epsilon float64, pas une preuve générale d'erreur flottante. Ces succès ne couvrent pas tous les niveaux, toutes les devises ni les futurs états générés.

Le plus grand code absolu est +101 pour AUD/EUR, cible du 16 août 2007, depuis une origine du 24 juillet, à l'horizon 17. Son échelle s_i vaut environ 0.00325958. Ce code représente un incrément par rapport au dernier état reconstruit, avec échelle fixée à l'origine ; ce n'est pas le rendement cumulé de dix-sept jours. Le rapport conserve les prix et les états nécessaires à l'interprétation. Aucune causalité événementielle n'en est inférée.

Le support des cibles n'est pas celui des contextes P1-D : l'ancien cas de grand déplacement historique divisé par une petite volatilité récente concernait des niveaux passés. On ne peut ni transférer ses nombres aux nouveaux incréments cibles ni conclure que les extrêmes ont disparu du problème scientifique. Réduire le dictionnaire d'après cette seule partition compromettrait une comparaison multi-marchés non encore réalisée.

## 9. Stabilité : une spécification, pas encore une qualification complète

Soustraire deux CDF proches de un est dangereux. Sur l'intervalle normal standard [10,11], le calcul direct en float64 avec erf donne zéro dans l'illustration exécutée ; une différence de fonctions de survie calculées par erfc donne environ 7.61966*10^-24, de logarithme -53.23131. Ce sont des arguments construits pour l'analyse numérique, pas des données de marché.

La documentation SciPy explique l'intérêt d'un calcul direct de log-CDF et montre des pertes de précision dans l'approche naïve. [Documentation officielle log_ndtr](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.log_ndtr.html).

Pour a=(k-.5-mu)/sigma et b=(k+.5-mu)/sigma, la spécification proposée utilise logPhi(b)+log1mexp(logPhi(a)-logPhi(b)) si b<=0, et la symétrie des fonctions de survie si a>=0. Quand l'intervalle traverse zéro, une somme d'erf peut éviter la soustraction de valeurs voisines de un. Pour d<=0, log1mexp(d) se calcule avec log1p(-exp(d)) loin de zéro, et log(-expm1(d)) près de zéro.

La normalisation utilise ensuite une réduction logsumexp des masses centrales corrigées et des deux queues. [Documentation officielle logsumexp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.logsumexp.html). Ces primitives et leur composition doivent encore être vérifiées dans le futur moteur différentiable.

SciPy et mpmath n'étaient pas installés dans le runtime utilisé. Aucune comparaison haute précision ni vérification de gradients n'a donc été effectuée. Quatre illustrations ont employé la bibliothèque standard math ; elles ne remplacent pas un audit des fonctions spéciales. erfc sous-flue aussi pour des arguments suffisamment grands. Des limites de cellules distinctes en arithmétique réelle peuvent se confondre en machine ; l'exponentielle du log-prix peut déborder. Un échec doit être signalé, pas transformé en écrêtage invisible du support.

## 10. Quel succès pourrait réellement être revendiqué ?

La perte proposée est la moyenne des vingt -log p(k_h | passé,codes précédents). Elle évalue une loi de trajectoire quantifiée fixée. Elle ne constitue pas une densité de prix continus. Comparer directement cette NLL entre pas delta différents favoriserait ou pénaliserait aussi la résolution du langage ; il faut une mesure commune.

Pour rester fidèle à l'objectif de prix brut, la future évaluation devra aussi porter sur les prix natifs aux horizons 1, 5 et 20 : pinball, quantiles, couverture et largeur. Les prix reconstruits forment une loi sur une grille ; aucune distribution intra-cellule n'est ajoutée implicitement. Une éventuelle interpolation ou désquantification serait une nouvelle hypothèse à déclarer.

La génération libre doit être évaluée en plus de la vraisemblance sous vrais préfixes. Le nombre de trajectoires Monte-Carlo et sa précision ne sont pas fixés ; les erreurs de simulation doivent être suffisamment faibles pour distinguer les modèles. La condition de moments ne remplace pas ce contrôle. Il n'y a encore aucun score de prévision ou vainqueur.

## 11. Cycle 12 du panel simulé

| Persona fictif | Objection | Décision prise |
|---|---|---|
| Léa, information | Le résidu semble annoncé comme une information nouvelle | Dériver l'équivalence à la grille de niveaux ; distinguer représentation et information |
| Malik, GPT | Des cibles pourraient entrer dans leur propre contexte | Écrire les 276 positions, les vingt sorties et le décalage causal |
| Nadia, statistiques | Le codec peut créer des dépendances et la NLL changer avec la résolution | Ajouter le mécanisme de bruit différencié et l'évaluation en prix natifs |
| Camille, calcul numérique | Support infini, queues négligeables et CDF instables sont confondus | Dériver la borne de queue ; garder le statut de candidat non qualifié |
| Inès, données | Les cibles recouvrantes gonflent artificiellement la taille du corpus | Rapporter présentations et 15 360 cotations distinctes séparément |
| Sara, reproductibilité | Les choix risquent de suivre les résultats | Sceller candidat, métriques et script avant l'audit ; préserver 0.1 |
| Élodie, lecture du projet | « Audit réussi » pourrait faire croire à une prédiction réussie | Résumé initial et résultats explicitement limités à la reconstruction |

Ces personas sont des perspectives simulées par l'agent principal, pas des personnes consultées ni une validation indépendante. Les auxiliaires connus étaient indisponibles pour limite de service ; aucun avis supplémentaire d'un agent n'est inventé.

## 12. Livrables et travail restant

Les fichiers de cette étape se trouvent dans research/trame_research_plan/20261016 : p1b0_candidate.json, audit_protocol.json, freeze.json, audit_targets.py, target_audit_report.json, check_design.py et design_report.json. Les sources et choix sont qualifiés dans source_audit.json. Les fichiers 20261015 et leurs rapports restent inchangés.

Le prochain bloc doit fermer le contrat de scores en prix et la précision de simulation, puis qualifier numériquement les fonctions de probabilité et leurs gradients lors de la future phase technique. Le choix des bornes doit être challengé sur une matrice de corpus et de régimes déclarée, sans utiliser les tests finaux pour le régler. Les témoins à calcul comparable, le protocole d'optimisation de P1-B0 et une évaluation indépendante restent ouverts.

La grammaire partagée entre actifs et le Marché latent commun restent les hypothèses générales. Cette étape vérifie une brique univariée partagée ; elle n'a pas testé l'information croisée entre actifs, l'or, un indice actions, les observations à la seconde ni un effet d'échelle. Aucun résultat local n'est extrapolé à ces questions.
