# Le langage à information égale : ce que le GPT doit réellement apprendre

Note scientifique de travail, 15 octobre 2026. Complément au candidat P1-D, révision 0.2. Démonstrations et spécifications documentaires ; aucun réseau construit, aucun entraînement et aucun score de prévision. Les exemples numériques sont construits pour expliquer les codes, pas présentés comme des cours observés. Les résultats descriptifs sur données réelles restent ceux des documents 07 et 09.

## L'idée en une page

L'intuition du projet se précise : une « langue de marché » doit rendre les relations entre observations plus faciles à apprendre. Remplacer un nombre par un mot ne crée pas, à lui seul, d'information sur son avenir. En revanche, montrer au modèle que deux amplitudes sont voisines, qu'une précision fine complète une précision grossière, ou qu'un déplacement s'exprime relativement à un état connu peut changer fortement le nombre d'exemples et le calcul nécessaires.

Nous pouvons isoler cette question. Un même passé quantifié possède trois écritures : nombres, symboles plats ou unités grossières accompagnées de trois bits. Les trois écritures conservent exactement les mêmes cellules. Elles diffèrent par les relations que l'encodeur apprend ou impose. Le premier test doit donc porter sur l'efficacité de cet apprentissage à information constante. La meilleure écriture éventuelle ne sera pas automatiquement la meilleure compression, ni une preuve de la prévisibilité d'un marché universel.

Une conséquence pratique apparaît : compter uniquement les paramètres du Transformer est insuffisant. Dans le plus petit gabarit proposé, le dictionnaire plat ajoute environ un demi-million de paramètres. Cette différence est du même ordre que le cœur du réseau. Une comparaison présentée comme « même taille de modèle » aurait été inexacte. La révision donne désormais les formules complètes pour un candidat minimal, sans prétendre qu'il est optimal.

Trois antériorités renforcent la nécessité de cet examen : xVal pour des nombres continus dans une architecture de langage, les embeddings numériques de Gorishniy et ses coauteurs, et Number Cookbook pour l'interaction entre écriture des nombres et capacité. Leurs expériences ne prouvent rien sur la prévision financière de TRAME ; elles empêchent de confondre Transformer, texte et vocabulaire discret.

## 1. Proposition : trois alphabets, un même contenu

On conserve la grille de la révision 0.1 : `k = floor(8 x)` et `m = (k+0,5)/8 = (2k+1)/16`. La cellule est `[k/8, (k+1)/8)`. Dans la révision 0.2, x désigne précisément la coordonnée déjà convertie en float32, commune à C et à la quantification. Q transmet m numériquement ; F transmet k comme symbole ; H transmet `q = floor(k/8)` et les trois bits de `r = k-8q`, dans l'ordre du poids fort au poids faible. Le décodage est `k = 8q + 4b2 + 2b1 + b0`.

| Coordonnée explicative x | k | Milieu m | H : q ; b2 b1 b0 |
|---:|---:|---:|---|
| -0,01 | -1 | -0,0625 | -1 ; 1 1 1 |
| 0 | 0 | 0,0625 | 0 ; 0 0 0 |
| 1,23 | 9 | 1,1875 | 1 ; 0 0 1 |

La division entière des négatifs est une division vers moins l'infini, pas une troncature vers zéro. L'origine x=0 ne se reconstruit pas en zéro dans cette grille à milieux : c'est la convention déjà proposée, pas une anomalie cachée. Le prix courant exact est connu par le canal auxiliaire commun. Une future grille centrée sur zéro serait une autre expérience et devrait recevoir un amendement explicite ; on ne change pas maintenant les frontières pour améliorer un résultat inexistant.

Soit K la séquence de cellules, S les informations communes déclarées et Y la cible. Si Q, F et H sont des transformations bijectives de K, leurs informations conditionnelles sont les mêmes : `sigma(Q,S) = sigma(F,S) = sigma(H,S)`. Pour toute perte et une classe non restreinte de prédicteurs mesurables, les infimums de risque de Bayes sont donc égaux. La preuve est constructive : tout prédicteur d'une écriture peut être composé avec le décodage bijectif d'une autre. Les conditions d'existence/intégrabilité de la perte restent nécessaires.

Cette égalité ne dit pas qu'un Transformer fini retrouvera ces compositions à coût nul. Ses paramètres, sa géométrie d'entrée, ses initialisations et son optimisation peuvent rendre certaines fonctions plus faciles à apprendre. Le contraste Q-H mesure ce système complet sous un budget donné. Il ne mesure pas une information prédictive supplémentaire créée par H. Le contraste C-Q, lui, change également la précision conservée.

Contrôle futur proposé : décoder Q/F/H vers exactement les mêmes milieux, puis appliquer un encodeur et des poids communs. Les sorties doivent être identiques à la tolérance numérique déclarée. Ce contrôle ne sera pas un quatrième concurrent ; il détectera une erreur de sérialisation, de masque ou de métadonnées. Il n'a pas été exécuté ici sur un modèle.

## 2. Domaine fini, extrêmes et précision effective

Pour rendre le candidat minimal explicite, le dictionnaire principal couvre `-2048 <= k <= 2047`, soit 4 096 cellules. Le dictionnaire grossier de H couvre alors `-256 <= q <= 255`, soit 512 entrées. Ces limites sont des choix de conception, pas des quantiles ajustés aux performances. Tout autre k emprunte une voie d'échappement commune aux variantes Q/F/H, sans écrêtage du prix.

La sérialisation documentaire d'un entier hors dictionnaire est `ESC`, signe obligatoire, chiffres décimaux de sa valeur absolue sans zéro initial, puis `END`. Les zéros négatifs, chaînes vides et variantes non canoniques sont refusés. Ce choix donne une grammaire décodable avec un alphabet fini. Il ne garantit ni une longueur bornée ni un décodeur numérique de précision infinie.

Dans **P1-A**, cette séquence n'est pas donnée au Transformer temporel comme une longue suite. Elle est décodée localement en m ; le même module affine numérique traite les échappements de Q/F/H. Un indicateur d'échappement, déterministe à partir de x, appartient aux métadonnées communes, y compris pour C. Le candidat est donc hybride hors dictionnaire. Il teste les présentations symboliques sur leur domaine principal ; il ne permet pas d'attribuer aux bits un avantage de généralisation sur les échappements, où le traitement est commun.

La bijection mathématique ne suffit pas en float32. Une condition suffisante pour représenter exactement le milieu m est `-2^23 <= k <= 2^23-1` : le numérateur impair `2k+1` tient dans les 24 bits significatifs, et la division par 16 est dyadique. Au-delà, F/H pourraient préserver une différence que Q efface. Le candidat impose donc un contrôle préalable de tous les contextes utilisés. Un dépassement arrête la comparaison et entraîne un amendement de précision avant mesure ; il n'autorise ni suppression silencieuse d'origines ni saturation. La conformité des fenêtres BCE à cette borne **n'a pas encore été mesurée**.

La normalisation et s sont calculées en float64 ; la coordonnée obtenue est ensuite convertie une seule fois en float32, pour donner x. C reçoit x. Pour Q/F/H, x est remonté exactement en float64 avant le calcul de `floor(8 x)` ; Q convertit m en float32 sous le contrôle ci-dessus. Ainsi, la quantification est bien une fonction de ce que C reçoit. Calculer k depuis la valeur float64 initiale aurait pu séparer deux valeurs devenues égales dans C près d'une frontière, et rendre inexact l'énoncé « Q ne fait que perdre de la précision par rapport à C ». Cette convention définit les cellules à partir du résultat numérique calculé, pas d'un logarithme mathématique exact inaccessible. Les valeurs non finies sont des erreurs explicites. Une normalisation glissante par origine reste autorisée uniquement pour les cibles postérieures à cette origine.

Le débit de fichier, le nombre de symboles locaux et le nombre de vecteurs temporels seront rapportés séparément. Un « token » dans une table de vocabulaire n'est pas une unité physique de stockage comparable à un float32. Les fréquences d'échappement et de cellules jamais vues à l'ajustement devront aussi être publiées. Un code admissible mais jamais appris constitue une question de généralisation distincte d'une erreur de décodage.

## 3. L'encodeur impose une hypothèse avant même l'attention

Voici un candidat minimal entièrement spécifié au niveau des opérations et des paramètres. Il sert à borner les confusions de la comparaison, pas à désigner l'architecture finale.

Pour une largeur d, C et Q utilisent un module affine scalaire `a v + b`, soit 2d paramètres, avec v=x pour C et v=m pour Q. F utilise une table de 4 096 vecteurs de largeur d, et son module numérique d'échappement de 2d paramètres. H utilise une table de 512 vecteurs grossiers, trois tables de deux vecteurs pour les bits, puis additionne les quatre vecteurs ; son module d'échappement compte encore 2d paramètres.

Ainsi, `E_H(k) = A[q] + B2[b2] + B1[b1] + B0[b0]` dans le dictionnaire. H utilise 520d paramètres d'entrée, F 4 098d et C/Q 2d. Les tables sont partagées entre actifs. L'addition de H n'est pas équivalente à une table arbitraire : changer b0 produit toujours le même déplacement de vecteur, quel que soit q. Cette restriction peut favoriser un transfert entre amplitudes, ou empêcher une interaction utile. Le Transformer peut construire ensuite des interactions ; elles ne sont pas déjà offertes gratuitement par l'encodeur.

La somme de vecteurs appris n'est pas garantie injective pour tous les poids possibles. L'équivalence d'information démontrée plus haut porte sur les codes **avant** cet encodeur. L'apprentissage peut ensuite en perdre, volontairement ou non. Il faut donc éviter l'énoncé plus fort et faux « les représentations internes du réseau ont toujours la même information ».

Deux sensibilités documentaires évitent un témoin numérique trop faible : un module numérique non linéaire, et un module numérique comportant des fonctions sinusoïdales à plusieurs fréquences avec conservation de la coordonnée scalaire. Les paramètres et la recherche d'hyperparamètres supplémentaires seront comptés. Des sinusoïdes seules peuvent créer des alias ; conserver v laisse une coordonnée injective en arithmétique exacte. Une amélioration de H face au seul affine Q ne suffirait pas à éliminer ces alternatives. Les fréquences et tailles de ces sensibilités restent à fixer avant gel.

Cette précaution est motivée par [Gorishniy, Rubachev et Babenko, NeurIPS 2022, sections 3–4](https://papers.nips.cc/paper/2022/file/9e9f0ffc3d836836ca96cbf8fe14b105-Paper-Conference.pdf) : les auteurs étudient des encodages linéaires par morceaux et des activations périodiques sur des tâches tabulaires. Le bénéfice observé concerne plusieurs architectures. Nous en retenons la nécessité d'un témoin numérique sérieux ; nous ne transposons ni leurs scores ni leurs classements aux prix.

Une variante H avec fusion non linéaire des unités grossières et fines sera une ablation distincte. Elle changera l'hypothèse additive et le coût. Ajouter des paramètres inutilisés à H pour afficher le même total que F ne constitue pas un contrôle scientifique de capacité.

## 4. Compte complet d'un candidat GPT minimal

À chaque position du contexte de 256 observations, le vecteur d'entrée additionne l'encodage de valeur, un embedding d'actif à six entrées, une position sinusoïdale fixe, et une projection affine de quatre nombres connus : log(P_i), log(s_i), log(1+écart calendaire passé), indicateur d'échappement. La dernière composante est redondante avec x ; elle n'apporte pas de donnée externe. Pour le premier point de fenêtre, l'écart est calculé depuis la publication précédente, quand elle existe, selon le calendrier connu. Au tout premier point de l'historique, la sentinelle 0 signifie « prédécesseur absent » ; deux dates de publication valides ne partagent pas une date, donc ce code ne représente aucun intervalle observé. L'identité fixe ici unité et type de référence ; cette simplification ne s'étend pas automatiquement à un corpus hétérogène.

Le cœur est un décodeur causal à L blocs, attention dense standard avec matrices Q/K/V et projection de sortie munies de biais, MLP `d -> 4d -> d` avec GELU et biais, deux LayerNorm affines par bloc, normalisation finale affine. Positions fixes, aucune table de positions entraînable. Pas d'embedding de vocabulaire en sortie, pas de tête de classification des tokens. Aucun partage de matrices entre attention et sortie.

Un bloc compte `12d² + 13d` paramètres : 4d²+4d pour l'attention, 8d²+5d pour le MLP et 4d pour les deux normalisations. L'embedding d'actif compte 6d, la projection des quatre métadonnées 5d, la normalisation finale 2d et la tête affine 21d+21. Cette tête traite le dernier état du contexte et produit sept valeurs pour chacun des trois horizons.

Le total commun hors encodage de valeur est donc `12Ld² + 13Ld + 34d + 21`.

| Candidat | C ou Q | H additif | F plat | Excédent F sur H |
|---|---:|---:|---:|---:|
| L=4, d=128, 4 têtes | 797 717 | 864 021 | 1 322 005 | 457 984 |
| L=6, d=256, 8 têtes | 4 747 797 | 4 880 405 | 5 796 373 | 915 968 |
| L=8, d=512, 8 têtes | 25 237 525 | 25 502 741 | 27 334 677 | 1 831 936 |

Ces nombres sont des comptes algébriques du candidat décrit, vérifiés arithmétiquement ; ils ne proviennent pas d'un modèle instancié. Une modification d'encodeur, de normalisation, de tête ou de métadonnées invalidera ces totaux. Les statistiques de l'optimiseur, les gradients et les activations ne sont pas des paramètres supplémentaires ; ils contribuent néanmoins à la mémoire.

Le contraste principal conserve L, d, les 256 observations et la tête physique. Il n'est donc **pas à nombre total de paramètres identique**. On publiera séparément l'exposition aux exemples, le calcul réellement consommé et les paramètres entraînables. Une sensibilité à budget total comparable devra déplacer effectivement de la capacité et documenter cette modification. Égaliser à la fois tous ces axes n'est pas une propriété automatique de l'expérience.

Pour chaque horizon h, la première sortie z est libre et les suivantes ajoutent successivement un softplus positif. Les quantiles de prix sont `P_i exp(s_i sqrt(h) z_tau)`, donc positifs et ordonnés. Ils restent des quantiles marginaux, pas une trajectoire jointe. Aucun plafond de sortie statistique n'est introduit pour dissimuler un débordement numérique ; la gestion numérique sera vérifiée avant entraînement.

La révision distingue enfin deux objets : l'objectif d'ajustement proposé moyenne les sept pinball losses sur les trois horizons, en divisant chaque terme par `P_i s_i sqrt(h)` ; le critère primaire de comparaison reste l'horizon 1. Les horizons 5 et 20 ne sont pas des têtes laissées sans entraînement. Cette précision ferme une ambiguïté du candidat 0.1 ; elle n'est motivée par aucun score observé.

## 5. Ce qui est transposable de la littérature

[xVal, version 2 du 15 décembre 2024, sections 2–3](https://arxiv.org/html/2310.02989v2) associe un symbole numérique à une valeur continue et modifie la sortie numérique. Ses expériences comprennent température et orbites simulées ; certaines utilisent du masquage plutôt qu'une génération autorégressive. C'est une antériorité directe pour l'option continue dans une architecture de langage. Elle ne démontre pas une efficacité financière, et un symbole NUM portant un réel n'est pas une compression de toute l'amplitude en un bit. Les résultats ne sont pas reproduits ici.

[Number Cookbook, version 2, section 3.1 et annexe A.4.2](https://arxiv.org/html/2411.03766v2) compare plusieurs découpages de nombres et tailles de modèles sur des tâches arithmétiques. L'étude rapporte des interactions entre taille, segmentation et généralisation en longueur. Elle justifie de tester ces axes ensemble, sans conclure qu'un alphabet arithmétique sera supérieur pour une série stochastique. Les affirmations de l'article sur les modèles « actuels » restent datées de son étude.

Ces travaux rendent plausible un changement d'efficacité dû à la représentation. Ils ne fournissent ni garantie d'émergence, ni preuve d'un signal ignoré par tous les modèles existants. La contribution à rechercher pour TRAME reste une combinaison vérifiée de sémantique d'observation, grammaire numérique, apprentissage commun et évaluation sur plusieurs marchés réels.

## 6. Deux nouvelles pistes audacieuses mais falsifiables

**Plusieurs écritures comme plusieurs langues du même passé.** Un même réseau pourrait recevoir aléatoirement Q, F ou H et apprendre une distribution de prix cohérente entre ces présentations. Une perte de cohérence utiliserait uniquement le passé autorisé et les sorties du modèle. Les variantes ne constituent pas de nouvelles observations indépendantes. La cohérence pourrait régulariser, mais pourrait aussi conduire les prédicteurs à partager la même erreur. À comparer à un simple accroissement du nombre de présentations de Q sous le même calcul ; aucun gain n'est acquis.

**Une grammaire qui apprend d'abord des relations certaines.** Une étape auxiliaire pourrait demander ordre des niveaux, conversion entre échelles connues, décodage des raffinements ou identité des ratios sur les contextes observés. Elle pourrait aider le modèle à apprendre l'arithmétique de sa langue avant les régularités incertaines du futur. Les réponses sont dérivées de données déjà connues ; elles n'ajoutent pas d'information de marché. Le témoin doit recevoir autant de calcul et les mêmes exemples. Si l'auxiliaire améliore seulement la reconstruction, on ne le présentera pas comme un progrès de prévision. Les données de marché de l'expérience restent réelles ; les relations auxiliaires sont des cibles dérivées, clairement étiquetées.

Ces pistes restent hors du contraste primaire pour ne pas changer simultanément écriture, objectif et budget. Le passage ultérieur à P1-B devra préciser la probabilité des codes d'échappement, leur longueur et leur arrêt ; la présente tête de quantiles ne répond pas à ces questions.

## 7. Huitième passage du panel : objections consignées

Panel fictif, raisonnement du principal ; aucune consultation de personnes ni relecture indépendante réussie pendant cette itération. Les agents auxiliaires restent indisponibles après leurs erreurs de limite de service.

| Point de vue simulé | Objection | Modification ou limite conservée |
|---|---|---|
| Théoricien de l'information | H ne crée aucune information si le code est bijectif. | Preuve explicite ; bénéfice recherché dans l'apprentissage fini. |
| Chercheuse en calcul numérique | Une bijection sur les réels peut disparaître en float32. | Borne suffisante, arrêt sur dépassement, pas de troncature cachée. |
| Architecte Transformer | Le dictionnaire change beaucoup la taille du petit modèle. | Comptes complets ; aucune revendication de taille totale identique. |
| Spécialiste des nombres | Le témoin affine peut être artificiellement faible. | Sensibilités numériques non linéaires et périodiques requises avant conclusion. |
| Statisticien | Une bonne reconstruction n'est pas un résultat prédictif. | Aucun classement de langues annoncé ; objectif et score primaire séparés. |
| Porteur explorateur | Un test quotidien étroit ne doit pas abandonner les langues ambitieuses. | Deux extensions identifiées ; résultats futurs explicitement locaux au corpus testé. |

Prochaine étape documentaire : articuler ces encodeurs avec les témoins définis dans la note associée, fermer optimisation et budgets, puis auditer les conditions numériques sur les fenêtres réelles déjà explorées. Ce travail prépare une expérience ; il ne l'autorise pas implicitement à être développée ou exécutée.
