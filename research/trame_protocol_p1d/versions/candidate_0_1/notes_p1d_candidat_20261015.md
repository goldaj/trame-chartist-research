# P1-D : fiche de conception du premier test de langage

Travail intermédiaire du 15 octobre 2026, postérieur au complément 2.1. Candidat 0.1, ni gelé ni enregistré, aucun modèle développé ou entraîné. Cette note prépare une décision expérimentale ; elle ne constitue pas une nouvelle preuve prédictive ni une nouvelle édition PDF du dossier.

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

On fixe provisoirement une grille de largeur 1/8 : `k = floor(8 x)`. L'intervalle représente `[k/8, (k+1)/8)` et son milieu vaut `(k+0,5)/8`. Les sorties du modèle restent des prix physiques ; ces cellules décrivent ici le passé.

| Variante | Contenu proposé | Question |
|---|---|---|
| C | Coordonnées x en float32 | Référence continue de précision finie |
| Q | Milieux des cellules, donnés numériquement | Quel est l'effet de la perte de précision ? |
| F | Indices k sous forme de symboles plats | Quel est l'effet d'une entrée symbolique ? |
| H | Même k décomposé en entier grossier et trois bits de détail | Quel est l'effet d'une hiérarchie à contenu identique ? |

Dans H, `q0 = floor(k/8)` et `r = k - 8 q0`, avec r dans 0...7 ; les trois bits codent r. Q, F et H sont mathématiquement en bijection pour cette grille. Le calcul flottant, les valeurs extrêmes, les codes d'échappement et la sérialisation devront préserver cette équivalence. On ne déclarera pas « mêmes informations » après avoir tronqué une seule des variantes.

Le contraste primaire candidat est Q contre H ; C contre Q et F contre H sont secondaires. Les grandes amplitudes possèdent une voie d'échappement sans écrêtage. La plage du dictionnaire et son codage entier doivent encore être arrêtés. Aucune valeur future n'est utilisée pour choisir un nombre de bits ou pour compléter un résidu en entrée.

Pour P1-A, une même observation produit un vecteur local fusionné avant l'attention temporelle. La fenêtre physique reste de 256 observations. Le nombre de symboles internes et le coût de leur encodeur sont néanmoins comptés. P1-B évaluera séparément les séquences de tokens générées, pour éviter de confondre la hiérarchie des entrées avec une simple réduction de l'horizon couvert par un nombre fixe de tokens.

## 6. Sorties, scores et témoins

Les sept quantiles candidats sont 0,05 ; 0,10 ; 0,25 ; 0,50 ; 0,75 ; 0,90 ; 0,95, avec une tête commune qui produit des prix positifs et ordonnés. La médiane est évaluée en erreur absolue native. La perte primaire candidate est la moyenne des pertes quantiles à horizon 1, divisée par l'échelle connue `P_i s_i`, puis moyennée à poids égal entre les six actifs. Cette division positive dépend du passé et ne réécrit pas la cible ; les pertes natives sont toujours rapportées.

Pour un quantile q au niveau tau, `rho_tau(y-q) = (tau - 1[y<q]) (y-q)`. Une grille finie évalue les quantiles annoncés, pas toute une distribution continue de façon strictement propre. Ses intervalles ne constituent pas une loi jointe des trajectoires. Les horizons 5 et 20, les couvertures 50/80/90 % et les largeurs sont secondaires. La distinction entre fonctionnelle et loi complète suit la théorie des [scores propres de Gneiting et Raftery](https://doi.org/10.1198/016214506000001437).

Les témoins prévus comprennent la persistance du prix, une marche aléatoire en logarithme à volatilité estimée sur le passé et une distribution empirique d'incréments historiques au même horizon. Leurs formules, interpolations de quantiles et éventuels réglages doivent être fixés avant gel. Un témoin linéaire utilisant le contexte croisé est nécessaire pour attribuer au GPT un gain au-delà d'une dépendance linéaire simple ; son choix précis reste ouvert.

## 7. Capacité et comparaisons entre actifs

Les candidats de dimensionnement du cœur Transformer sont : quatre couches de largeur 128 et quatre têtes ; six couches de largeur 256 et huit têtes ; huit couches de largeur 512 et huit têtes. Le terme approximatif `12 L d²` vaut 786 432, 4 718 592 et 25 165 824 paramètres. Il exclut embeddings, normalisations, biais, encodeurs et têtes de sortie. Ce sont des gabarits documentaires, pas des architectures construites ni un devis de calcul.

Le premier contraste de langage utilise des paramètres partagés et uniquement l'histoire de l'actif cible à l'inférence. Les effets de partage et de contexte croisé viennent dans des blocs distincts. Pour l'effet croisé, un modèle de même architecture est entraîné avec les autres actifs masqués, puis comparé à celui entraîné avec leurs observations disponibles. Masquer seulement au test serait une autre question.

Cinq initialisations sont proposées par configuration retenue. La répétition des fenêtres ne compte pas comme données nouvelles. L'égalisation du calcul total et celle de l'exposition de l'actif cible sont rapportées séparément : elles ne sont pas simultanément garanties. Les budgets de réglage, règles d'arrêt et critères d'extension aux capacités suivantes restent à définir avant toute exécution.

## 8. Incertitude, numéraire et résultat négatif

L'unité d'incertitude est le vecteur de pertes appariées d'une origine sur les six actifs, pas chaque cellule. Proposition : blocs temporels communs, longueur centrale de 60 publications, sensibilités 20 et 120, 2 000 rééchantillonnages. La longueur ne supprime pas automatiquement toute dépendance ni les ruptures ; les périodes et actifs seront aussi présentés séparément. Les initialisations mesurent une variabilité d'apprentissage, pas de nouvelles histoires de marché.

Un changement de numéraire réexprime les mêmes observations et ne multiplie pas les données. On évaluera toujours les prévisions reconverties vers la cible physique initiale. Les références BCE peuvent en outre être construites à partir de cotations et de taux croisés selon leur méthodologie ; leur dépendance observée n'est pas automatiquement une interaction économique nouvelle.

Un gain stable Q-H est compatible avec un biais d'apprentissage favorable à la présentation hiérarchique sous ces conditions. Un gain C-Q concerne aussi la précision conservée. Un échec de H à une petite capacité ne réfute pas le codage hiérarchique en général. Une absence de convergence, une incertitude élevée ou une limite de corpus sont des diagnostics à conserver. Aucun p-value confirmatoire n'est revendiqué sur ce pseudo-test exploratoire.

## 9. Points à fermer avant le gel

Il reste à définir exactement l'encodeur local et les échappements, les comptes de paramètres complets, les témoins, le budget de réglage et d'arrêt, les règles de poursuite à plus grande capacité, le test indépendant et les conventions historiques de la source. Cette liste est un travail de conception restant, pas une demande d'autorisation d'entraînement. Le fichier JSON candidat garde explicitement `implemented=false`, `trained=false` et aucune performance.

Les comptes de calendrier ont été vérifiés dans cette itération. Aucune corrélation, aucun score prédictif, aucun modèle ni tokenizer appris n'ont été calculés. Les fichiers du POC0 gelé et les données réservées n'ont pas été modifiés.
