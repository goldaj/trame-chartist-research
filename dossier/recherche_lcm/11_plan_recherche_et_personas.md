# TRAME : plan de recherche et premières décisions

## 1. Objectif et ordre des preuves

**15 octobre 2026, édition 2.3. Plan engagé à la demande du porteur.** Le programme vise un modèle GPT apprenant un langage des courbes sur plusieurs marchés réels. La première question n'est pas combien de paramètres acheter, mais quelles expériences permettront d'attribuer une amélioration au langage, à l'information, à l'apprentissage ou à leur interaction.

Le travail reste une conception scientifique, accompagnée d'audits documentaires et arithmétiques. La demande de commencer le plan est exécutée dans ce périmètre : aucun modèle construit ou entraîné, aucune dépense engagée. Les étapes de développement apparaissent pour rendre le chemin complet, pas comme des opérations déjà effectuées.

| Étape | Livrable et condition de passage |
|---|---|
| 1. Fermer P1-A | Contrastes de représentation, témoins numériques sérieux, initialisations et budgets documentés. Tout gain doit avoir une interprétation précise. |
| 2. Définir P1-B | État causal, token futur, loi normalisée, génération et décodage ; distinguer la vraisemblance d'un code du score sur le prix. |
| 3. Étendre le corpus | Matrice familles × époques × résolutions, petits échantillons réels vérifiés, disponibilité et versions explicites. |
| 4. Geler l'évaluation | Test indépendant identifié, règles de sélection et de poursuite arrêtées, protocole versionné avant les nouveaux scores. |
| 5. Réaliser le POC | Lors de la phase de développement : tests d'information, témoins, petits GPT, calcul mesuré et résultats reproductibles. |
| 6. Étudier l'échelle | Courbes capacité/données/diversité/contexte/précision, transferts entre familles, réplications ; limites du système mesurées. |

Les étapes 1 et 2 peuvent avancer en parallèle de la qualification des données. Le gel définitif dépend des trois. Le développement ne doit pas masquer les ambiguïtés de conception ; réciproquement, nous ne chercherons pas à résoudre tout problème théorique imaginable avant une expérience utile.

Le résultat attendu du premier POC sera une réponse locale et interprétable. Une mauvaise prévision par un petit réseau ne condamnera pas la langue. Une bonne prévision sur un corpus déjà exploré ne suffira pas à revendiquer une structure universelle du Marché.

<!-- pagebreak -->

## 2. Personas : rôles, objections et décisions

Les profils ci-dessous prolongent le panel existant. **Ils sont simulés par l'agent principal.** Les agents auxiliaires restent indisponibles sur une limite de service constatée ; aucune relecture indépendante n'est revendiquée. Les rôles servent à produire des objections différentes, pas à multiplier artificiellement les validations.

| Persona et responsabilité | Objection prioritaire | Décision de cette session |
|---|---|---|
| Léa, théorie de l'information | Une écriture plus élaborée ne crée pas d'information. | Garder une entrée numérique commune et distinguer précision, représentation et fonction apprise. |
| Malik, architecture GPT | P1-A ne réalise pas encore le prochain token. | Formaliser dès maintenant un premier générateur conditionnel de vingt codes futurs. |
| Nadia, statistique expérimentale | Le réglage des concurrents peut décider du classement. | Même grille, mêmes budgets d'exposition et seeds appariées ; sélection sur développement seulement. |
| Camille, calcul numérique | Le témoin affine est faible et les queues peuvent casser les scores. | Définir des témoins résiduels non linéaire/périodique ; analyser les moments des prix générés. |
| Inès, données de marché | Une fréquence annoncée ne garantit pas une observation indépendante. | Contrat de données par source et fréquence réellement observée ; pas de secondes interpolées. |
| Sara, reproductibilité | Modifier le protocole sans conserver l'ancien empêche l'audit. | Archiver le candidat 0.3, créer 0.4 et séparer P1-B de P1-A. |
| Élodie, lecture et finalité | La théorie peut devenir une suite de reports sans preuve. | Associer à chaque étape un livrable, une limite et une décision vérifiable. |

### Deux cycles de contradiction effectivement menés

**Cycle 10 : témoins et ressources.** Proposition initiale : comparer l'hybride au seul numérique affine. Objection de Camille : un avantage pourrait venir d'une non-linéarité disponible seulement d'un côté. Révision : ajouter une petite correction MLP et une correction périodique à C et Q. Nadia demande alors de compter leur réglage et leur calcul : mêmes essais de taux d'apprentissage, comparaisons appariées et paramètres explicités. Ce n'est pas une égalité de FLOPs.

**Cycle 11 : futur et valeurs rares.** Proposition initiale : prévoir les codes et ajouter une tête spécifique pour les extrêmes. Sara rappelle qu'une tête ne recevant aucun exemple peut rester sans apprentissage. Révision : étudier une distribution numérique définie sur tous les entiers, modifiée par des corrections de probabilité dans le dictionnaire. Camille ajoute une objection : une distribution raisonnable en logarithmes peut avoir une espérance de prix infinie. La note technique donne une condition suffisante pour éviter cette difficulté ; elle ne prétend pas avoir entraîné ce modèle.

<!-- pagebreak -->

## 3. Ce qui est commencé, et ce qui suit

**Étape 1, engagée.** Le candidat P1-D passe en 0.4. Deux témoins numériques sont définis par leurs opérations et paramètres. La proposition d'optimisation, la séparation des seeds de réglage et de répétition, le budget initial et son comptage sont explicités. Les hypothèses et chiffres sont des choix de protocole, pas des réglages validés par résultats.

**Étape 2, engagée.** Un candidat P1-B0 formalise la génération conditionnelle de vingt codes de prix, avec une ancre et une échelle figées à l'origine. La récurrence est causale ; la loi sur les codes est normalisée. Les conditions suffisantes de moments finis en prix sont dérivées. Architecture complète de la tête, constantes de bornage, stabilité numérique et calibration restent à préciser.

**Étape 3, à poursuivre ensuite.** Constituer une matrice de couverture réelle : matières premières, actions/indices, devises, taux, puis autres familles pertinentes. Conserver deux axes complémentaires : histoire longue et détail récent. Choisir les échantillons par disponibilité documentée, pas par succès observé. Auditer prix de transaction, référence, moyenne ou règlement ; calendriers, changements de définition, instruments disparus et observations manquantes. Les données déjà reçues servent au développement, pas à fabriquer un test intact.

**Étape 4, avant toute prétention de confirmation.** Distinguer un test de nouvelles dates, de nouveaux instruments et d'une nouvelle famille. Fixer leur priorité, leur accès et les règles de dévoilement. Un historique révisé n'est pas une reconstitution certifiée des premières publications. La taille et le seuil de gain pertinent doivent être justifiés ; le nombre de courbes ne remplace pas l'estimation de leur dépendance.

**Étape 5, lors du futur POC.** Commencer par les témoins et les tests de causalité. Mesurer temps, mémoire et calcul d'une exécution courte avant le budget complet. Entraîner ensuite les variantes selon le protocole retenu, publier aussi les échecs numériques et les essais non sélectionnés. Comparer les prix et distributions, pas seulement une courbe visuellement plausible.

**Étape 6, après qualification du POC.** Augmenter séparément les axes d'échelle, puis tester leurs interactions. Vérifier si une langue rattrape les autres avec la capacité, si la diversité aide un actif peu documenté, et si les autres actifs apportent une information contemporaine supplémentaire. Un système scientifiquement fiable exige aussi stabilité, calibration et détection de situations éloignées de l'ajustement.

<!-- pagebreak -->

## 4. Décisions et livrables attendus

| Situation observée à l'avenir | Réponse de recherche |
|---|---|
| Une fuite d'information ou un canal auxiliaire non déclaré | Corriger avant d'interpréter les performances ; conserver la trace et réviser les résultats concernés. |
| Le petit GPT n'apprend pas correctement l'ajustement | Diagnostiquer optimisation et capacité ; ne pas conclure contre la langue. |
| Gain seulement face au numérique affine | Limiter la conclusion à ce témoin ; examiner les contrôles numériques plus expressifs. |
| Gain qui change avec budget ou initialisation | Étudier l'interaction ; ne pas publier uniquement la configuration favorable. |
| Gain sur données déjà explorées | Le traiter comme exploratoire ; préparer sa reproduction indépendante. |
| Absence de gain dans une expérience bien exécutée | Décrire précisément les conditions négatives et choisir une nouvelle hypothèse identifiable. |

### Livrables produits dans cette session

Le présent plan, la note technique 12, le candidat P1-D 0.4, le candidat théorique P1-B0 0.1 et un rapport arithmétique. Ce dernier vérifie comptes de paramètres, budgets et exemples de récurrence ; il ne lit aucun prix et ne calcule aucun score de prévision. Les nouvelles lectures primaires sont consignées avec leurs limites.

### Prochaine tâche précise

Qualifier les bornes et la tête de probabilité P1-B0, puis arrêter un inventaire de tests indépendants multi-marchés. En parallèle, confronter la proposition d'optimisation à une revue technique avant son gel. Les règles de calcul proposées ne sont pas une garantie de convergence ; leur coût réel attend une future mesure.

Nous ne fixons pas une date fictive de modèle fiable. La durée dépendra de l'accès aux données, des ressources mesurées et de ce que révéleront les expériences. En revanche, chaque prochaine session doit fermer une décision ou produire une preuve identifiable, pas simplement reformuler le dossier.
