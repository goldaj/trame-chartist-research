# TRAME : apprendre les structures du Marché

## La recherche en trois pages

**Édition scientifique 2.2, 15 octobre 2026. Les versions précédentes sont archivées ; les conclusions restent révisables. Aucun modèle prédictif n'a été construit ou entraîné.**

Votre demande est de construire une théorie puis un programme expérimental pour apprendre les courbes comme un modèle GPT apprend des séquences. Il faut trouver le langage numérique, les données et l'architecture permettant d'anticiper la suite des prix. L'objet est scientifique : quelles structures existent, lesquelles sont apprenables et comment les mesurer sur des observations nouvelles ?

**TRAME** reste un nom de travail. Il évoque les relations entre actifs, époques et échelles de temps. Le projet doit pouvoir porter sur l'or, les indices, les actions, les devises et d'autres marchés suffisamment documentés. Les choix du premier petit échantillon ne fixent pas sa destination.

### Deux intuitions deviennent deux expériences

Première possibilité : chaque actif parle sa langue. Un modèle commun apprend plusieurs langues, mais utilise surtout le passé de l'actif qu'il doit prévoir. Cette mise en commun peut aider un instrument peu documenté grâce aux motifs appris ailleurs.

Deuxième possibilité : les actifs sont des observations différentes d'un état de marché partagé. Ils ne racontent pas exactement la même chose : certains réagissent à la monnaie, d'autres à la croissance, à une entreprise ou à une offre physique. Le modèle chercherait ce qu'ils partagent tout en conservant leurs particularités.

Nous comparerons donc un modèle par actif, un modèle partagé sans information croisée, puis un modèle qui observe plusieurs actifs simultanément. Cette distinction est essentielle : bénéficier de beaucoup de courbes pendant l'entraînement ne prouve pas que leurs mouvements simultanés aident à prédire.

### À quoi ressemble le langage ?

Une bougie peut devenir un objet structuré : ouverture relative au dernier prix, corps signé, mèches, activité, durée et disponibilité. Une simple référence quotidienne ne contient pas tous ces éléments : nous ne les inventons pas. Les nombres peuvent être continus, découpés en paliers ou écrits avec un vocabulaire ; les unités accompagnent le contenu.

Une image, des pourcentages et une suite de signes mettent en valeur des propriétés différentes. **Changer l'écriture peut faciliter l'apprentissage sans ajouter d'information ; réduire une amplitude à son signe en efface.** Le protocole sépare ces effets. Une représentation détaillée peut préserver un signal qu'une écriture simple perd ; cette dernière peut aussi mieux généraliser avec peu de données.

<!-- pagebreak -->

## Pourquoi privilégier un GPT et beaucoup de données ?

Un Transformer peut apprendre des dépendances entre des événements éloignés et entre plusieurs séries. Nous le retenons comme architecture principale à étudier. L'idée proposée est un GPT hiérarchique : détails récents à la seconde si disponibles, passé plus ancien regroupé en minutes, heures et journées, puis échanges d'information entre actifs. Les fenêtres ne contiennent que ce qui était observable à leur date.

Il ne faut pas confondre le principe GPT avec l'obligation de transformer chaque nombre en mot ou de générer un symbole à la fois. Des sorties continues et des prévisions par blocs restent possibles. Des architectures récurrentes et des modèles simples serviront de comparaisons, sans devenir le centre du projet.

**Votre objection au petit POC est retenue : une mauvaise prévision avec un petit réseau ne condamne pas son langage.** Il faut varier séparément taille du réseau, quantité de données, diversité des actifs, longueur du passé et précision de l'encodage. Nous chercherons des courbes de progression, pas un verdict après un seul essai.

La littérature observe déjà des effets d'échelle sur des séries temporelles, mais pas une garantie universelle sur les prix financiers. Plus de calcul peut aider à exploiter une information difficile ; il ne suffit pas à recréer une amplitude effacée par un encodage, ni une nouvelle extérieure jamais observée. Les documents 01, 05 et 08 développent cette distinction.

### Plusieurs histoires et plusieurs vitesses

Les épisodes de 2000, de 2008 et de la pandémie sont des contextes utiles. Nous voulons aussi des périodes ordinaires : un modèle entraîné presque uniquement sur les crises apprendrait une fréquence de crise artificielle. Les événements servent à vérifier la robustesse ; leurs noms attribués après coup ne deviennent pas des informations disponibles avant qu'ils surviennent.

Une longue histoire quotidienne et une histoire plus récente à la seconde sont complémentaires. Transformer artificiellement une observation quotidienne en milliers de secondes n'ajoute rien. À une seconde, les pauses de cotation, les observations inchangées et les différences de calendrier doivent être représentées explicitement.

<!-- pagebreak -->

## Ce que les données ont déjà changé

Trois sources réelles ont été auditées : 58 240 bougies horaires complètes pour une étude de reconstruction, 33 792 références quotidiennes de six devises, et six histoires mensuelles de matières premières avec 732 valeurs chacune de 1960 à 2020, dont l'or. Aucun score de prévision n'a encore été calculé.

L'audit récent a révélé que le traitement prévu pour les valeurs hors dictionnaire n'aurait reçu aucun exemple à l'ajustement, tout en étant sollicité dans 40 contextes du franc suisse au développement. Nous proposons donc une **base numérique utilisée partout, complétée par des corrections symboliques**. Ce langage est explicitement hybride ; la correction ne démontre pas encore une meilleure prévision.

Le cas extrême venait d'un ancien cours exprimé dans l'unité d'une période récente très calme. Il motive l'étude de plusieurs échelles, sans constituer une découverte de signal. Autre distinction : plus de huit millions de valeurs présentées dans les fenêtres répétaient seulement 33 672 prix distincts. Les répétitions ne créent pas l'histoire manquante.

### Ce qui reste à prouver

P1-A comparera les écritures du passé avec une sortie commune de quantiles du prix. P1-B étudiera ensuite la génération des prochains symboles. Un masque causal ne suffit pas : la normalisation et les états de génération doivent aussi respecter l'information disponible. Budgets, réglages, diagnostics de convergence et évaluation indépendante restent à arrêter.

Pour la mise à jour technique, lire **10, Du langage à l'expérience contrôlée**, qui amende les propositions antérieures lorsqu'elles diffèrent. Lire ensuite 08 pour le Marché latent et le GPT, 02 pour les langages, 09 pour les observations et le corpus. Le papier 01, la faisabilité 03, le tutoriel 04, la validation 05 et l'état de l'art 06 complètent le dossier.

Le panel est simulé ; il ne remplace pas une validation indépendante. La prochaine preuve recherchée reste une amélioration reproductible sur de nouveaux prix, attribuable à un dispositif précis. Un résultat négatif sera conservé avec sa portée exacte ; il ne condamnera pas automatiquement tout un langage.
