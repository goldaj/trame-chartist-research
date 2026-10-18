# Ce que les données réelles changent dans notre langage

15 octobre 2026, après l'audit de 14:38 UTC. Résultat descriptif et amendement du candidat P1-D vers 0.3. Aucun modèle prédictif construit, ajusté ou évalué. Cette note amende les encodeurs minimaux de la révision 0.2 ; leurs versions exactes restent archivées. Les PDFs publiés demeurent l'édition 2.1.

## À retenir avant les détails

Le vocabulaire précédent sait représenter les observations, mais une partie de son apprentissage aurait été mal définie : sa branche numérique, réservée aux valeurs hors dictionnaire, ne reçoit **aucun exemple** dans le passé destiné à l'ajustement. Elle serait néanmoins utilisée 195 fois dans 40 contextes de développement. Ce défaut a été trouvé sur les références réelles du franc suisse, avant de construire le réseau.

La correction proposée consiste à donner à chaque valeur quantifiée une base numérique utilisée dans tous les contextes, puis à laisser les symboles apprendre une correction. Les paramètres de la base seront donc exposés à la tâche d'apprentissage, même si aucune valeur hors dictionnaire n'apparaît. Cela corrige un chemin non entraîné ; cela ne garantit ni extrapolation correcte ni meilleure prévision.

Le cas extrême n'est pas un nouveau choc de prix. Il vient d'un ancien cours exprimé dans les unités d'une volatilité récente devenue beaucoup plus faible. La langue doit donc conserver la signification de son échelle et être examinée sur plusieurs régimes, y compris les périodes calmes après une rupture. Nous n'avons pas modifié la normalisation pour faire disparaître ce cas.

## 1. Expérience descriptive et provenance

L'audit porte sur le fichier BCE déjà reçu et exploré : six devises contre EUR, 5 632 dates communes, 33 792 références numériques entre 1999 et 2020. Empreinte SHA-256 : `b8a684b6331d3cf0310a1838efdce806495906ead99d672671642c3bf24130de`. Aucune nouvelle cotation n'a été téléchargée ; le fichier est inchangé. Il reste une version historique révisée reçue en 2026, sans certification des publications initiales.

Le protocole descriptif et son script ont été figés à **14:38:46 UTC avant leur exécution**. Ce gel local rend l'analyse traçable ; il ne constitue ni un préenregistrement externe ni le gel du futur protocole prédictif P1-D. Ils vérifient exactement le candidat 0.2, avec sa grille, ses contextes de 256 prix et ses horizons 1/5/20. Le pseudo-test déjà exploratoire est inclus dans cet audit de représentation ; il ne pourra pas être présenté ensuite comme un jeu totalement intact.

Les artefacts sont dans [l'audit descriptif](../../research/trame_protocol_p1d/audits/preflight_01/protocol.json), [le gel et ses empreintes](../../research/trame_protocol_p1d/audits/preflight_01/freeze.json) et [le rapport intégral](../../research/trame_protocol_p1d/audits/preflight_01/report.json). Le script utilise Python 3.12.14 et NumPy 2.3.5. Il calcule des propriétés du contexte passé, sans score de prévision ni ajustement d'un prédicteur. Aucun prix postérieur à une origine n'entre dans ses caractéristiques ; un prix devenu passé peut naturellement entrer dans le contexte d'une origine plus tardive.

| Partition | Couples actif-origine | Valeurs présentées dans les fenêtres | Prix sources distincts utilisés dans cette partition | Valeurs hors dictionnaire | Contextes concernés |
|---|---:|---:|---:|---:|---:|
| Ajustement 1999–2009 | 15 246 | 3 902 976 | 16 776 | 0 | 0 |
| Développement 2010–2014 | 7 566 | 1 936 896 | 9 096 | 195 | 40 |
| Pseudo-test 2015–2020 | 9 090 | 2 327 040 | 10 620 | 0 | 0 |

Au total, 8 166 912 présentations de valeurs proviennent de **33 672 prix sources distincts** dans l'union des contextes. La répétition d'un prix dans de nombreuses fenêtres ne crée pas autant d'observations indépendantes. Les contextes de développement peuvent utiliser un passé de la partition précédente ; la somme des prix distincts par partition n'est donc pas le total distinct global.

Toutes les valeurs respectent la borne suffisante permettant de conserver exactement les milieux de cellule en float32. Aucun milieu n'a été altéré par sa conversion, aucune décomposition hiérarchique n'a échoué, et le plancher de volatilité de 10^-6 n'a été activé sur aucune origine. La correction d'ordre d'arrondi de la révision 0.2 change effectivement **24 cellules** par rapport à une quantification directe en float64 : 10 à l'ajustement, 7 au développement et 7 au pseudo-test. Ce faible nombre ne permet pas de présumer un effet prédictif mesurable ; il justifie néanmoins la convention exacte.

## 2. Un alphabet peut être décodable sans être appris

Dans l'ajustement, le dictionnaire plat voit 735 de ses 4 096 cellules principales. La partie grossière de H voit 96 de ses 512 entrées ; les deux états de chacun des trois bits sont observés. Les tables sont partagées entre actifs : ces nombres utilisent l'union de leurs contextes d'ajustement, sans lire les périodes suivantes pour construire le support appris.

| Partition ultérieure | Présentations d'une cellule plate jamais vue à l'ajustement | Présentations comportant une unité grossière jamais vue | Couples actif-origine comportant une cellule plate jamais vue |
|---|---:|---:|---:|
| Développement | 9 514 | 8 202 | 338 |
| Pseudo-test | 69 | 0 | 15 |

Ces comptes concernent seulement les valeurs **dans** le dictionnaire, donc excluent les 195 échappements. Ils indiquent où des lignes de tables n'auraient reçu aucun gradient lié aux données. Ils ne mesurent ni entropie prédictive, ni généralisation, ni erreur future. H peut recombiner des composants déjà vus pour former une cellule nouvelle ; il reste à vérifier si ses paramètres appris rendent cette composition utile.

Le défaut plus net concerne les échappements. Dans le candidat 0.2, F et H appellent un module affine distinct uniquement hors de leur dictionnaire. Comme aucun échappement n'apparaît à l'ajustement, ce module ne reçoit aucun gradient provenant de la tâche. Une éventuelle régularisation ne lui enseignerait pas la relation entre nombres et prévisions. Avoir le même type de module que Q ne suffit pas : Q utilise le sien sur toutes les valeurs, alors que F/H n'utiliseraient pas le leur. Les poids de modèles distincts ne se transmettent pas leur apprentissage automatiquement.

Ce constat ne signifie pas qu'un modèle a échoué : aucun n'a été entraîné. Il signifie que le protocole aurait confondu l'effet de la langue avec l'absence d'exemples pour une branche de l'encodeur. Il doit être corrigé avant toute comparaison.

## 3. Le cas réel : une unité qui devient très petite

Après avoir observé les agrégats, nous avons déclaré un diagnostic ciblé, explicitement **exploratoire et postérieur à l'audit initial**. Il cherche le contexte CHF le plus extrême, vérifie sa normalisation par un calcul scalaire indépendant et compare deux échelles sur ce même passé. Il ne sélectionne aucun hyperparamètre ni nouveau prédicteur. [Plan et statut](../../research/trame_protocol_p1d/audits/preflight_01/followup_plan.json), [résultats et vérification](../../research/trame_protocol_p1d/audits/preflight_01/followup_scale_report.json).

Les 40 origines avec échappement se situent entre le 15 juin et le 9 août 2012. Le minimum de coordonnée normalisée apparaît à l'origine **1er août 2012**, en regardant le prix historique du **10 août 2011** :

| Élément | Valeur |
|---|---:|
| Référence historique | 1,0451 CHF par EUR |
| Référence à l'origine | 1,2013 CHF par EUR |
| Logarithme du ratio historique/courant | -0,1392917291 |
| Écart-type des 64 derniers incréments | 0,0003005311 |
| Coordonnée après division, en float64 | -463,4853067 |
| Indice quantifié k | -3 708 |
| Écart-type des 255 incréments du contexte | 0,0075289986 |
| Rapport échelle longue/échelle courte | 25,0523 |

La valeur -463 ne désigne **pas** une variation sur une publication de 463 écarts-types. Elle désigne un écart entre deux niveaux éloignés dans le contexte, mesuré avec l'unité des seules 64 publications récentes. L'échelle longue est ici environ 25 fois plus grande. Le calcul scalaire de l'échelle et de la coordonnée concorde avec le calcul vectorisé dans les tolérances déclarées.

La BNS a instauré un cours minimum de 1,20 CHF par EUR le 6 septembre 2011, et confirmait son maintien en 2012. Cela documente le régime institutionnel entre les deux dates observées. L'association avec la faible volatilité récente est une interprétation compatible avec ces éléments ; notre audit n'est pas une estimation causale de l'effet de cette politique. [Annonce officielle du 6 septembre 2011](https://www.snb.ch/en/publications/communication/press-releases/2011/pre_20110906), [déclaration officielle du 7 février 2012](https://www.snb.ch/en/publications/communication/speeches/2012/ref_20120207_tjn).

La normalisation a donc une sémantique propre. Pour `x=log(P_j/P_i)/s_i`, un passé de variation finie peut produire un x très grand lorsque s_i devient petit. Ajouter des paramètres au GPT ne change pas cette identité. Cela peut rendre utile une représentation à plusieurs échelles, mais il faut distinguer cette hypothèse d'une correction de code ou d'une preuve de signal financier.

## 4. Amendement 0.3 : base numérique et corrections symboliques

La révision garde les mêmes données, cellules, métadonnées, horizons et sorties. Elle modifie les encodeurs F/H et leurs initialisations proposées. Notons `m=(2k+1)/16`, et `N(m)=a m+b`, un module affine de largeur d. Pour toutes les valeurs admissibles :

- Q reçoit `N(m)`.
- F+ reçoit `N(m) + T[k]` si k appartient au dictionnaire ; hors dictionnaire, il reçoit `N(m)`.
- H+ reçoit `N(m) + A[q] + B2[b2] + B1[b1] + B0[b0]` dans le dictionnaire ; hors dictionnaire, il reçoit `N(m)`.

Chaque modèle possède ses propres paramètres ; N est partagé entre les domaines ordinaire et hors dictionnaire **à l'intérieur du modèle**. Il n'est pas préentraîné dans Q puis transféré discrètement ailleurs. Le module numérique est désormais utilisé sur toutes les observations. Les tables T/A/B sont initialisées à zéro et proposent des corrections de vecteurs, pas des prédictions d'erreur future. Les entrées de table jamais visitées doivent conserver ce zéro sous l'optimiseur futur ; ce sera un contrôle explicite d'implémentation.

À initialisation commune du cœur et de N, Q, F+ et H+ ont mathématiquement les mêmes vecteurs d'entrée puisque les corrections sont nulles. Aucun réseau n'a été instancié pour tester cette égalité. Au cours de l'apprentissage, les écritures symboliques pourront diverger par leurs corrections : table libre pour F+, partage entre composants pour H+. Les gradients sont possibles sur les tables nulles parce qu'elles sont additionnées directement, sans produit par une seconde porte également nulle.

Une cellule plate jamais vue reçoit la base numérique sans correction. Pour H+, une composante grossière jamais vue reste nulle, mais les bits déjà appris peuvent contribuer. Ce comportement évite une correction aléatoire attachée à une ligne jamais entraînée ; il n'assure pas que la correction recombinée soit juste. Le module numérique lui-même n'est pas garanti de bien extrapoler : il est exposé à l'ajustement, ce qui est une condition utile, pas une preuve suffisante.

F+/H+ sont **des encodeurs hybrides**. La valeur m est une fonction exacte des mêmes codes, donc n'ajoute aucune information au passé quantifié ; elle fournit directement au réseau une relation numérique qu'un alphabet purement symbolique lui demandait d'apprendre. Le contraste primaire devient Q contre H+ ; C contre Q et F+ contre H+ restent secondaires. Il pose une question précise : les corrections hiérarchiques améliorent-elles l'apprentissage au-delà d'une base numérique disponible à tous ? Il ne répond pas à la question de la supériorité d'un langage purement discret.

Les nombres de paramètres sont inchangés : 2d pour C/Q, 4 098d pour F+ et 520d pour H+. Le module auparavant réservé aux échappements est réutilisé partout, sans ajout de module. Les gabarits minimaux restent à 797 717 / 864 021 / 1 322 005 paramètres pour C/Q, H+ et F+ à L4d128. Le nombre d'opérations change : la base numérique est maintenant évaluée aussi dans le dictionnaire pour F+/H+. L'ancien coût ne doit pas être repris sans mesure.

Les encodeurs purs 0.2 restent une variante historique à revoir si nous voulons étudier séparément l'apprentissage de l'arithmétique depuis les symboles. Ils ne sont pas éliminés universellement. Un véritable témoin symbolique ouvert pourrait employer des chiffres partagés partout ; il changerait toutefois l'expérience et devrait compter son coût local et son entraînement de tous les composants.

## 5. Calendrier des témoins et limites restantes

L'audit a aussi vérifié les cinq blocs chronologiques de résidus de B3, sans ajuster de régression ni calculer de résidu. Les nombres de prévisions de calibration possibles par actif sont :

| Année | Horizon 1 | Horizon 5 | Horizon 20 |
|---|---:|---:|---:|
| 2005 | 256 | 252 | 237 |
| 2006 | 254 | 250 | 235 |
| 2007 | 254 | 250 | 235 |
| 2008 | 255 | 251 | 236 |
| 2009 | 236 | 236 | 236 |
| Total | 1 255 | 1 239 | 1 179 |

La réduction de fin 2009 vient du cohort commun global à horizon 20, conservé dans tous les calculs. Chaque ajustement de bloc utilise uniquement des cibles datées avant l'année concernée. Les blocs sont non vides, mais leurs tailles ne garantissent ni indépendance des résidus, ni stabilité de leurs quantiles, ni bon conditionnement d'une régression future.

Une piste distincte reste à tester : représenter simultanément une échelle courte et une échelle longue, ou utiliser des coordonnées différentes selon l'âge du segment. Cela fournirait de nouvelles statistiques du passé ou une autre précision ; ce n'est plus le même contraste à information égale. Le résultat CHF motive cette piste sans choisir son poids ni son seuil. Le candidat 0.3 conserve s64 et son plancher, ainsi que toutes les dates : aucune observation gênante n'a été supprimée.

## 6. Neuvième passage du panel simulé

Panel fictif, conduit par le principal. Aucun expert humain consulté ni relecture indépendante nouvelle. Les agents auxiliaires précédemment tentés restent indisponibles à cause d'une limite de service ; leur absence ne vaut pas approbation.

| Objection | Réponse dans cette révision |
|---|---|
| « Une voie d'échappement décodable suffit. » | Non : il faut vérifier que les paramètres qu'elle utilise ont reçu des exemples de la tâche. |
| « Plus de 8 millions de valeurs constituent déjà un grand corpus. » | Ce sont des présentations recouvrantes de 33 672 prix distincts ; leur répétition ne crée pas l'histoire manquante. |
| « L'extrême prouve un crash inconnu. » | Il s'agit d'un ancien niveau exprimé dans une petite unité récente ; aucune anomalie prédictive n'est découverte. |
| « La correction hybride donnera nécessairement de meilleurs résultats. » | Elle retire une confusion expérimentale ; son effet prédictif reste à mesurer. |
| « On a changé la langue après avoir vu des données. » | Oui, après un audit descriptif déclaré sur un corpus exploratoire. La révision, sa motivation et l'exposition au pseudo-test sont conservées. Aucun score n'a guidé ce choix. |
| « Il suffit alors de réduire la fenêtre ou d'élargir le dictionnaire. » | Cela déplacerait le problème et changerait contexte ou coût. Ces options ne sont pas choisies pour faire disparaître le cas observé. |

Le travail restant concerne les encodeurs numériques plus expressifs, les budgets et diagnostics de convergence, les nouvelles familles de marchés et l'évaluation indépendante. Les résultats présents améliorent la validité de la future expérience ; ils n'établissent pas encore la prévisibilité d'un prochain prix.
