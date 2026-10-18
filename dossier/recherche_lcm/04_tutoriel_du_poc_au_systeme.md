# Construire TRAME comme programme scientifique

## Tutoriel du premier appareil de mesure au modèle reproductible

**Version 2, 14 octobre 2026. La cible est la prévision des prix sur plusieurs marchés. Les étapes prédictives ci-dessous restent à réaliser ; l'étude de reconstruction du document 07 est la seule expérience quantitative achevée à ce stade.**

## Étape 1 Écrire une question qui puisse recevoir une réponse

Nous commençons par deux questions distinctes. Le partage d'un modèle entre actifs améliore-t-il les prévisions ? L'observation simultanée des autres actifs apporte-t-elle ensuite une information supplémentaire ? La première teste le transfert de grammaire ; la seconde teste une représentation commune de l'état de marché.

La fiche de chaque expérience précise variable de prix, horizon, dates d'information, représentation, architecture, budget, métrique principale et comparaisons. Une hypothèse plus ambitieuse peut rester ouverte après un échec local ; la fiche doit annoncer exactement ce qui est testé pour ne pas lui attribuer une portée universelle.

**Livrable :** fiche d'expérience versionnée avec date de gel. **État :** protocole de reconstruction gelé puis amendé de façon tracée ; fiche de prévision multi-marchés encore à figer.

## Étape 2 Définir les instruments et trois profondeurs historiques

Construire un registre d'actions, d'indices, d'or ou autres matières, de devises et éventuellement d'autres actifs. Pour chacun : type exact de prix, calendrier, devise, unité, durée de disponibilité, champs et droits de recherche. Le choix n'est pas fondé sur le résultat d'un modèle.

Prévoir une couche historique longue, une couche intrajournalière intermédiaire et une couche récente fine. Réserver des familles entières et des dates futures avant d'optimiser les langages. Les épisodes historiques servent à analyser les différences de comportement ; ils ne remplacent pas les périodes ordinaires.

**Livrable :** matrice instruments × périodes × résolutions, où disponible, acquis et validé sont trois états différents. **État :** petit corpus témoin réel vérifié ; corpus scientifique général incomplet.

## Étape 3 Rendre chaque observation traçable

Conserver les fichiers bruts avec URL, date, taille et empreinte ; enregistrer les versions et les corrections. Le schéma normalisé distingue date du phénomène, fin de bougie et première disponibilité connue. Une donnée historique sans heure de publication attestée reste marquée comme telle.

Contrôler doublons, valeurs non finies, unités, ordre temporel, cohérence OHLC, heures absentes et intervalles incomplets. Une fermeture du marché n'est pas une panne de collecte. Les changements de contrat, de symbole et d'indice ont leurs propres métadonnées.

Le premier appareil de mesure a rencontré des bougies qui se terminent avant leur heure attendue. Elles ont été conservées dans le brut, exclues de la comparaison à durée fixe et consignées avant le calcul des métriques. Cet exemple montre pourquoi un checksum ne certifie pas la cohérence temporelle.

**Livrable :** manifeste et rapport de qualité. **État :** réalisés pour le témoin décrit dans le document 07 ; à étendre aux autres familles.

## Étape 4 Tester les langues sans encore confondre avec prévision

Encoder et reconstruire les mêmes observations avec une branche continue, des quantifications fixes ou adaptées, un vocabulaire empirique et un contrôle volontairement pauvre comme les signes. Mesurer la distorsion, en particulier dans les queues, le nombre de symboles et les informations latérales nécessaires.

L'appareil POC0 et ses tests se trouvent dans research/trame_poc0. Le protocole, les empreintes et les résultats JSON permettent de vérifier le document 07. Les données synthétiques présentes dans les tests servent uniquement à contrôler les calculs ; les résultats scientifiques descriptifs utilisent des observations réelles.

Les prochaines variantes de langage ne seront pas ajustées discrètement sur la même validation. Un protocole suivant pourra ajouter un symbole hors plage, une quantification logarithmique des extrêmes et un résidu continu. Il conservera une référence de débit pour inclure l'ancre, les échelles et le codebook.

**Livrable :** atlas expérimental des pertes et invariances. **État :** première comparaison réalisée ; aucun vocabulaire déclaré gagnant pour prévoir.

## Étape 5 Préparer des cibles identiques pour tous les modèles

Séparer input et cible future avec une convention explicite de disponibilité. À la seconde, une cotation arrivée plus tard que la date de prédiction est interdite même si son timestamp d'événement est antérieur. À l'heure, une bougie partiellement observée ne peut être remplacée par sa valeur finale.

Choisir une première cible principale et quelques diagnostics. Les candidats doivent prévoir les mêmes prix ou accroissements aux mêmes horizons. Les losses internes par token restent des diagnostics propres à chaque langage ; le score commun porte sur les valeurs physiques décodées.

**Livrable :** constructeur de cibles audité, inventaire des fenêtres et contrôle des dates. **État :** spécification ; aucun label prédictif n'a été calculé pour les mesures du document 07.

## Étape 6 Construire les références et le premier GPT

Entraîner des références simples puis un premier Transformer de taille modeste. Le choix d'une taille initiale vise à vérifier l'expérience et l'optimisation. Il ne vise pas à prouver qu'un langage échouera à grande échelle.

Comparer A, modèles par actif ; B, paramètres partagés sans contexte d'autres actifs ; C, paramètres partagés avec contexte inter-actifs ; D, facteurs communs et états spécifiques explicites. Conserver les entrées physiques et rendre visibles les différences de budget. Le document 08 fournit les masques, les mécanismes et les ablations proposées.

**Livrable :** prévisions sauvegardées, checkpoints, courbes d'apprentissage et scores. **État :** futur. Aucun réseau n'est encore développé ou entraîné dans cette phase.

## Étape 7 Mesurer le passage à l'échelle

Prendre plusieurs tailles de GPT, plusieurs volumes d'observations originales et plusieurs niveaux de diversité. Mesurer leur interaction au lieu d'augmenter toutes les dimensions à la fois. Conserver une précision d'encodage suffisante ou la faire varier comme un facteur expérimental séparé.

La première grille complète peut coûter cher ; un plan partiel équilibré sert à estimer les tendances, avec répétitions et points de confirmation. Réserver des configurations pour vérifier l'extrapolation. Les exposants d'une loi de puissance resteront empiriques, limités à la plage observée. Ne pas leur faire prédire mécaniquement une capacité future à une taille mille fois supérieure.

**Livrable :** courbes loss/capacité/données/diversité et diagnostic d'optimisation. **État :** programme proposé, développé au document 05.

## Étape 8 Tester le transfert et les événements rares

Évaluer des actifs et familles réservés, puis des périodes non utilisées. Les observations d'une même crise sur cent actifs partagent un contexte ; elles ne donnent pas cent crises indépendantes. Les intervalles d'incertitude doivent respecter la dépendance en blocs temporels et entre actifs.

Tester la calibration, les queues et les dépendances de trajectoire séparément. Une moyenne favorable peut cacher un échec sur une famille. Une mauvaise moyenne sur un régime nouveau ne dit pas automatiquement si le langage est mauvais : étudier l'information manquante, la représentation et l'adaptation autorisée.

**Livrable :** rapport de transfert et de robustesse, y compris résultats négatifs. **État :** futur.

## Étape 9 Confirmer avec des observations futures

Enregistrer les distributions avant que leurs cibles ne soient observées. Geler les versions, la fréquence des rapports et les critères d'analyse. Une prévision postérieurement reconstruite à partir d'une archive actuelle ne remplace pas cette étape.

**Livrable :** expérience prospective de prévision, reproductible et datée. **État :** futur. Son rôle est scientifique : mesurer hors des choix rétrospectifs de la recherche.

## Étape 10 Mettre à jour les documents après chaque expérience

Pour chaque itération, conserver la version précédente puis mettre à jour la synthèse, le papier, l'atlas, la faisabilité, le tutoriel, le panel et les sources. Ajouter un rapport distinguant prévu, exécuté, observé et interprété. Tout amendement indique son motif et ce qui avait déjà été vu au moment du changement.

Le journal d'expérience doit permettre de répondre à trois questions : quelle observation a fait changer d'avis ; quelle explication concurrente reste possible ; quelle expérience pourrait la départager ? Cette pratique rend les documents révisables et utiles, au lieu de les transformer en conclusions figées.
