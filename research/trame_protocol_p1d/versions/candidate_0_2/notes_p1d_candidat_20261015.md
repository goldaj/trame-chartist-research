# P1-D : fiche de conception du premier test de langage

Travail intermédiaire du 15 octobre 2026, postérieur au complément 2.1. Candidat 0.2, ni gelé ni enregistré, aucun modèle développé ou entraîné. Cette note prépare une décision expérimentale ; elle ne constitue pas une nouvelle preuve prédictive ni une nouvelle édition PDF du dossier. La révision 0.1 est conservée dans research/trame_protocol_p1d/versions/candidate_0_1.

La révision 0.2 précise [l'alphabet, l'information et les encodeurs](notes_alphabet_information_egale_20261015.md) ainsi que [les témoins sans réseau et linéaires](notes_temoins_p1d_20261015.md). Ces deux notes font partie du candidat courant. Elles fixent les conventions numériques et les comptes de paramètres d'un gabarit minimal ; elles ne rendent pas le protocole gelé tant que les budgets et contrôles restants ne sont pas arrêtés.

## 1. La question délibérément restreinte

À contenu quantifié exactement identique, une présentation hiérarchique aide-t-elle un GPT à prévoir la prochaine référence quotidienne mieux qu'une présentation numérique ou qu'un vocabulaire plat, sous contraintes de capacité et de calcul déclarées ?

Cette question est plus précise que « les tokens sont-ils meilleurs que les nombres ? ». Elle sépare la perte d'information due à la quantification de la façon de présenter cette information au réseau. Le résultat resterait local à six devises et à une résolution quotidienne. Il ne peut ni valider ni réfuter un modèle universel de marchés à la seconde. P1-D sert notamment à déboguer le raisonnement expérimental avant le corpus massif.

La source existante est le fichier BCE déjà audité, SHA-256 b8a684b6331d3cf0310a1838efdce806495906ead99d672671642c3bf24130de. On ne télécharge pas une nouvelle version. Les six séries portent sur des unités USD, JPY, GBP, CHF, CAD et AUD par EUR, aux mêmes 5 632 dates de 1999 à 2020.

## 2. Trois horloges et une limite de version

La date de référence, l'heure à laquelle le taux représente le marché et l'heure de publication sont distinctes. Le communiqué BCE de 2015 mentionne 14:15 pour la mesure et un changement de publication de 14:30 vers 16:00 au 1er juillet 2016. Le cadre actuel du 23 juin 2026 mentionne environ 14:10 pour la mesure, avec des validations et plusieurs sources possibles. Il autorise des republications jusqu'à la publication suivante, sous ses règles. Ces documents ne justifient pas de rétroprojeter la méthode de 2026 sur 1999-2020. [Communiqué historique](https://www.ecb.europa.eu/press/pr/date/2015/html/pr151207.en.html), [cadre 2026, sections 2 et 6](https://www.ecb.europa.eu/stats/pdf/exchange/Frameworkfortheeuroforeignexchangereferencerates.en.pdf).

Le candidat utilise donc un ordre de publications, sans inventer d'heure historique exacte. Son énoncé sera « prévision rétrospective conditionnelle à l'historique révisé reçu », tant que les versions d'origine ne sont pas qualifiées. Retarder l'entrée d'une publication peut devenir une sensibilité sous hypothèse explicite ; cela ne prouve pas automatiquement l'absence de révisions antérieures. Le cadre actuel donne une piste de vérification, pas une garantie rétroactive.

## 3. Échantillonnage vérifié sur les dates réelles

Proposition : 256 prix observés de contexte, horizons 1, 5 et 20 publications. Les mêmes origines sont conservées pour tous les horizons. La dernière cible reste dans sa partition ; les prix de contexte peuvent venir de la partition précédente puisqu'ils étaient antérieurs à l'origine. Les mois ou jours sans référence ne reçoivent aucun prix inventé.

| Partition proposée | Dates de source | Origines admissibles | Première / dernière origine | Couples actif-origine |
|---|---:|---:|---|---:|
| Ajustement 1999-2009 | 2 816 | 2 541 | 27/12/1999 - 02/12/2009 | 15 246 |
| Développement 2010-2014 | 1 281 | 1 261 | 04/01/2010 - 01/12/2014 | 7 566 |
| Pseudo-test rétrospectif 2015-2020 | 1 535 | 1 515 | 02/01/2015 - 02/12/2020 | 9 090 |

Le premier ensemble retire 255 dates de chauffe et 20 origines de fin ; les deux autres retirent 20 origines chacune. Le nombre de cellules cibles à trois horizons vaut respectivement 45 738, 22 698 et 27 270. Ce sont des comptes déterministes du calendrier déjà reçu, pas des observations indépendantes ni des résultats de modèle. Le script `research/trame_protocol_p1d/count_calendar.py` ne calcule aucune statistique des prix et n'ajuste aucun paramètre.

Le pseudo-test appartient à un fichier déjà acquis et audité. Il ne sera jamais décrit comme un test final inédit. Une nouvelle tranche ou famille réservée, et un inventaire de l'exposition préalable des modèles, seront nécessaires à une étude confirmatoire ultérieure.

La date effective de la future publication définit l'horizon évalué, mais son écart calendaire réalisé ne sera pas communiqué en entrée : une absence future imprévue ne doit pas annoncer la cible. Les écarts passés sont disponibles. Si l'on ajoute plus tard des variables de calendrier futur, elles devront être des calendriers connus à l'origine, pas les absences constatées après coup.

## 4. Contrat d'information avant le choix du vocabulaire

Pour l'origine i, le passé contient `P_(i-255), ..., P_i`. Soit `s_i` l'écart-type de population des 64 derniers incréments logarithmiques terminant en i, avec plancher 10^-6. Les coordonnées historiques proposées sont `x_(j;i) = log(P_j/P_i) / s_i`.

L'information auxiliaire commune est **un seul prix courant exact P_i et une seule échelle s_i par actif et par origine**, plus identité, unité, type d'observation et dates passées. Les niveaux de chaque ancien prix ne sont pas ajoutés comme « ancres » individuelles. L'information portée par s_i est reconnue : ce test compare les détails historiques conditionnellement à une volatilité récente commune, pas des langues totalement isolées.

Cette normalisation est causale pour prévoir après i, mais elle n'est pas causale à chaque position j du contexte. Le prix P_i et s_i peuvent contenir le futur de j. Le candidat P1-A calcule donc sa perte exclusivement sur les cibles postérieures à i. Appliquer un objectif de prochain token à toutes les positions de ce contexte recentré créerait une fuite, même avec un masque d'attention triangulaire. Cette distinction est une condition obligatoire d'implémentation ultérieure.

Un entraînement en flux sur toutes les positions demandera une représentation qui se construit à partir des seuls préfixes. Il s'agit d'un autre contrat, présenté dans la note sur les ancres et le codage différentiel. Un Transformer causal ne rend pas causal un prétraitement qui a déjà lu la fin de la séquence.

## 5. Quatre représentations, trois contrastes

On fixe provisoirement une grille de largeur 1/8 : `k = floor(8 x)`. La normalisation est calculée en float64, puis x est converti en float32 pour C et pour le calcul de toutes les cellules. L'intervalle représente `[k/8, (k+1)/8)` et son milieu vaut `(k+0,5)/8`. Les sorties du modèle restent des prix physiques ; ces cellules décrivent ici le passé. Calculer les cellules depuis un x plus précis que celui reçu par C pourrait invalider la relation de perte d'information C vers Q : la révision 0.2 l'interdit explicitement.

| Variante | Contenu proposé | Question |
|---|---|---|
| C | Coordonnées x en float32 | Référence continue de précision finie |
| Q | Milieux des cellules, donnés numériquement | Quel est l'effet de la perte de précision ? |
| F | Indices k sous forme de symboles plats | Quel est l'effet d'une entrée symbolique ? |
| H | Même k décomposé en entier grossier et trois bits de détail | Quel est l'effet d'une hiérarchie à contenu identique ? |

Dans H, `q0 = floor(k/8)` et `r = k - 8 q0`, avec r dans 0...7 ; les trois bits codent r. Q, F et H sont mathématiquement en bijection pour cette grille. Le calcul flottant, les valeurs extrêmes, les codes d'échappement et la sérialisation devront préserver cette équivalence. On ne déclarera pas « mêmes informations » après avoir tronqué une seule des variantes.

Le contraste primaire candidat est Q contre H ; C contre Q et F contre H sont secondaires. La plage principale est k de -2048 à 2047 ; H utilise q0 de -256 à 255 et trois bits. Hors plage, la sérialisation entière canonique ESC/signe/chiffres/END est décodée localement vers un module numérique commun à Q/F/H, sans écrêtage. Ce contraste est donc hybride sur les grandes amplitudes, pas un test de leur génération symbolique. La note sur l'alphabet fixe une borne suffisante de précision float32 ; sa conformité sur les fenêtres réelles reste à vérifier. Aucune valeur future n'est utilisée pour choisir un nombre de bits ou pour compléter un résidu en entrée.

Pour P1-A, une même observation produit un vecteur local fusionné avant l'attention temporelle. La fenêtre physique reste de 256 observations. Le nombre de symboles internes et le coût de leur encodeur sont néanmoins comptés. P1-B évaluera séparément les séquences de tokens générées, pour éviter de confondre la hiérarchie des entrées avec une simple réduction de l'horizon couvert par un nombre fixe de tokens.

## 6. Sorties, scores et témoins

Les sept quantiles candidats sont 0,05 ; 0,10 ; 0,25 ; 0,50 ; 0,75 ; 0,90 ; 0,95, avec une tête commune qui produit des prix positifs et ordonnés. La médiane est évaluée en erreur absolue native. La perte primaire candidate est la moyenne des pertes quantiles à horizon 1, divisée par l'échelle connue `P_i s_i`, puis moyennée à poids égal entre les six actifs. Cette division positive dépend du passé et ne réécrit pas la cible ; les pertes natives sont toujours rapportées.

Pour un quantile q au niveau tau, `rho_tau(y-q) = (tau - 1[y<q]) (y-q)`. Une grille finie évalue les quantiles annoncés, pas toute une distribution continue de façon strictement propre. Ses intervalles ne constituent pas une loi jointe des trajectoires. Les horizons 5 et 20, les couvertures 50/80/90 % et les largeurs sont secondaires. La distinction entre fonctionnelle et loi complète suit la théorie des [scores propres de Gneiting et Raftery](https://doi.org/10.1198/016214506000001437).

L'objectif d'ajustement proposé moyenne les sept pertes quantiles sur les trois horizons avec division par `P_i s_i sqrt(h)`. Le critère primaire de comparaison reste h=1. La tête de quantiles est définie par des accroissements softplus en coordonnées logarithmiques, puis retour en prix positifs. Cette séparation entre objectif d'ajustement et critère primaire est explicite depuis la révision 0.2.

Les témoins sont désormais définis dans la note associée : persistance, marche aléatoire logarithmique à drift nul et sa sensibilité à espérance de prix constante, quantiles empiriques de prix terminaux, régression ridge avec contexte propre ou croisé et résidus chronologiques hors ajustement. L'espace d'interpolation, la grille de régularisation, la sélection sur développement et le gel avant pseudo-test y sont spécifiés. Aucun témoin n'est implémenté. Les témoins non quantifiés possèdent le passé continu ; ils ne sont pas décrits comme des contrastes à information égale avec Q/H.

## 7. Capacité et comparaisons entre actifs

Les candidats de dimensionnement du cœur Transformer sont : quatre couches de largeur 128 et quatre têtes ; six couches de largeur 256 et huit têtes ; huit couches de largeur 512 et huit têtes. Le terme approximatif `12 L d²` vaut 786 432, 4 718 592 et 25 165 824 paramètres. Il exclut embeddings, normalisations, biais, encodeurs et têtes de sortie. La note sur l'alphabet donne désormais les opérations et totaux complets d'un gabarit minimal. Pour le plus petit candidat, C/Q comptent 797 717 paramètres, H additif 864 021 et F plat 1 322 005. Ces valeurs sont algébriques, sans réseau instancié ni devis de calcul.

Le contraste conserve le cœur L/d et la fenêtre physique ; il n'est pas à nombre total de paramètres égal. Une sensibilité à budget comparable devra déplacer de la capacité utile et compter le coût des encodeurs. Les alternatives numériques non linéaires/périodiques restent à définir avant toute conclusion qui dépasserait le témoin affine.

Le premier contraste de langage utilise des paramètres partagés et uniquement l'histoire de l'actif cible à l'inférence. Les effets de partage et de contexte croisé viennent dans des blocs distincts. Pour l'effet croisé, un modèle de même architecture est entraîné avec les autres actifs masqués, puis comparé à celui entraîné avec leurs observations disponibles. Masquer seulement au test serait une autre question.

Cinq initialisations sont proposées par configuration retenue. La répétition des fenêtres ne compte pas comme données nouvelles. L'égalisation du calcul total et celle de l'exposition de l'actif cible sont rapportées séparément : elles ne sont pas simultanément garanties. Les budgets de réglage, règles d'arrêt et critères d'extension aux capacités suivantes restent à définir avant toute exécution.

## 8. Incertitude, numéraire et résultat négatif

L'unité d'incertitude est le vecteur de pertes appariées d'une origine sur les six actifs, pas chaque cellule. Proposition : blocs temporels communs, longueur centrale de 60 publications, sensibilités 20 et 120, 2 000 rééchantillonnages. La longueur ne supprime pas automatiquement toute dépendance ni les ruptures ; les périodes et actifs seront aussi présentés séparément. Les initialisations mesurent une variabilité d'apprentissage, pas de nouvelles histoires de marché.

Un changement de numéraire réexprime les mêmes observations et ne multiplie pas les données. On évaluera toujours les prévisions reconverties vers la cible physique initiale. Les références BCE peuvent en outre être construites à partir de cotations et de taux croisés selon leur méthodologie ; leur dépendance observée n'est pas automatiquement une interaction économique nouvelle.

Un gain stable Q-H est compatible avec un biais d'apprentissage favorable à la présentation hiérarchique sous ces conditions. Un gain C-Q concerne aussi la précision conservée. Un échec de H à une petite capacité ne réfute pas le codage hiérarchique en général. Une absence de convergence, une incertitude élevée ou une limite de corpus sont des diagnostics à conserver. Aucun p-value confirmatoire n'est revendiqué sur ce pseudo-test exploratoire.

## 9. Points à fermer avant le gel

Les encodeurs minimaux, échappements, comptes de paramètres et témoins ont une définition documentaire précise en révision 0.2. Il reste à auditer les domaines numériques et les blocs de résidus sur les fenêtres réelles, fixer les sensibilités numériques, le budget de réglage et d'arrêt, les règles de poursuite à plus grande capacité, le test indépendant et les conventions historiques de la source. Les détails d'optimisation, d'initialisation et de calcul restent ouverts. Cette liste est un travail de conception restant, pas une demande d'autorisation d'entraînement. Le fichier JSON candidat garde explicitement `implemented=false`, `trained=false` et aucune performance.

Les comptes de calendrier ont été vérifiés lors de la révision 0.1. La révision 0.2 vérifie seulement l'arithmétique des comptes de paramètres et de petits exemples de représentation construits à cette fin. Aucune nouvelle mesure sur les prix, aucune corrélation, aucun score prédictif, aucun modèle ni tokenizer appris. Les fichiers du POC0 gelé et les données réservées n'ont pas été modifiés.
