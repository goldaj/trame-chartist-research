# TRAME — hypothèse d’un marché latent et prédiction scientifique des prix

Document de conception du 14 octobre 2026. Périmètre : prix observés multi-actifs, représentation, prévision et généralisation. Six travaux scientifiques et une annonce technique primaire vérifiés ; propositions de recherche distinguées des résultats publiés. Aucune expérience prédictive n’a été réalisée pour ce document. Le premier banc de reconstruction mesure un encodage ; ses résultats ne constituent pas une validation de prévision.

## 1. Reformulation de l’hypothèse

L’or, un indice, une action et une paire de devises pourraient être différentes expressions d’une dynamique partiellement commune. Leur histoire serait comparable à plusieurs langues : certaines structures se partagent, d’autres restent propres à chaque langue. Un modèle de type GPT pourrait apprendre cette structure par préentraînement sur une grande collection de séquences réelles, puis estimer la distribution des prochains prix.

Cette hypothèse est scientifiquement cohérente et testable. Sa forme la plus défendable est **« une dynamique commune partielle, complétée par des dynamiques propres aux actifs »**. Elle n’exige ni une variable unique qui expliquerait tout, ni que chaque marché soit traduisible sans perte dans chaque autre. « Marché latent » désigne un état mathématique appris, dont la dimension et les composantes sont à déterminer.

Il faut séparer deux mécanismes : **partager une grammaire**, grâce à des paramètres appris sur des historiques différents ; **observer plusieurs vues simultanées**, grâce aux informations disponibles sur d’autres actifs au même moment. Le premier peut améliorer un modèle même lorsque les historiques ne se chevauchent pas. Le second exige un alignement temporel rigoureux. Les confondre ferait attribuer à un « marché commun » un gain provenant seulement de davantage de données d’entraînement.

## 2. Six travaux et une évolution de 2026, avec leur portée exacte

| Source | Résultat ou mécanisme pertinent | Portée pour TRAME |
|---|---|---|
| **Vaswani et al., 2017 — Attention Is All You Need** | Architecture fondée sur l’attention ; traitement parallèle à l’entraînement et représentation de relations dans une séquence. Les expériences initiales concernent notamment la traduction. | Justifie l’étude d’une architecture Transformer ; ne démontre aucune propriété particulière des marchés. Notice et résumé consultés. [Source primaire](https://arxiv.org/abs/1706.03762). |
| **Woo et al., 2024 — Moirai** | Patches de plusieurs tailles, attention acceptant un nombre variable de séries et sorties probabilistes ; préentraînement sur des domaines hétérogènes. Les auteurs précisent qu’un gain faible avec la taille à corpus fixe ne constitue pas une réfutation solide du scaling. | Appui direct à un modèle partagé entre fréquences et variables ; les performances décrites n’établissent pas notre hypothèse financière. Méthode et analyse du scaling consultées. [Méthode et section 4.2](https://arxiv.org/html/2402.02592v1). |
| **Liu et al., 2023/2024 — iTransformer** | Chaque historique de variable devient un token ; l’attention porte sur les relations entre variables. L’article examine le risque de mélanger trop tôt des mesures de sens différent ou des événements décalés. | Montre que le choix de l’axe des tokens est une variable scientifique majeure. Ce modèle supervisé ne constitue pas à lui seul une preuve de modèle fondation universel. Méthode et introduction consultées. [Version du 14 mars 2024](https://arxiv.org/html/2310.06625v4). |
| **Ansari et al., 2025 — Chronos-2** | Alternance d’attention temporelle et d’attention entre séries d’un groupe, patches, masques et covariables connues. Prévision universelle étudiée sur plusieurs benchmarks ; certaines dépendances multivariées de préentraînement sont synthétiques. | Source de conception pour le partage entre actifs et la gestion des données manquantes. Le corpus réel voulu pour TRAME reste une décision propre au projet. Méthode consultée. [Rapport primaire](https://arxiv.org/html/2510.15821v1). |
| **Jain et Sen, Google Research, 31 août 2026 — TimesFM-3** | Modèle de 330 M paramètres, patches de 32 points et alternance d’attention temporelle causale et d’attention entre séries. L’horizon masqué est décodé en une passe. | Exemple récent montrant qu’un décodeur Transformer peut utiliser une sortie non autorégressive. Les neuf quantiles annoncés par cible et horizon décrivent des marges ; ils ne spécifient pas une loi jointe complète. Annonce technique des auteurs consultée, sans reproduction. [Source primaire](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/). |
| **Yao et al., ICLR 2025 — Towards Neural Scaling Laws for Time Series Foundation Models** | Étudie paramètres, données et calcul sur un corpus non financier filtré à SNR supérieur à 20 dB. | Motive le programme, sans établir une loi pour les prix à la seconde. La version 3 du 18 mars 2025 confirme ce filtre ; les ressources y sont étudiées séparément. [Texte primaire](https://arxiv.org/html/2410.12360v3). |
| **Locatello et al., ICML 2019 — Challenging Common Assumptions in the Unsupervised Learning of Disentangled Representations** | Montre, dans son cadre théorique, la non-identifiabilité du désentrelacement non supervisé sans hypothèses inductives sur modèle et données. | Une représentation efficace ne révèle pas automatiquement les « vrais facteurs » économiques. Cela ne démontre pas l’impossibilité de prévoir ni l’impossibilité d’identifier des modèles temporels sous hypothèses supplémentaires. Notice PMLR et résumé consultés. [Publication primaire](https://proceedings.mlr.press/v97/locatello19a.html). |

Ces références étayent des composants et des méthodes. Aucun résultat cité ici ne prouve une intelligence générale du modèle, une prédictibilité universelle des prix ou un seuil magique de paramètres.

## 3. Modèle formel : des vues communes et des dynamiques propres

Notons `a` un instrument réel, `t` un instant physique et `P_a(t)` son prix observé selon une définition documentée. Un modèle conceptuel possible est :

`P[a,t] = G[a](z[t], u[a,t], m[a,t]) + epsilon[a,t]`.

`z_t` représente les composantes partagées ; `u_a,t` les composantes propres à l’actif ; `m_a,t` les métadonnées observables, dont unité, calendrier et type de mesure ; `epsilon` la part d’erreur ou d’aléa du modèle. Cette équation est une hypothèse de conception, pas une découverte empirique. `G_a` peut partager une grande partie de ses paramètres avec les autres actifs, avec une adaptation limitée par famille.

L’objectif principal est une distribution conditionnelle :

`p_theta({P[a,t+h]} pour a et h | F[t])`, où F[t] contient les observations effectivement disponibles au plus tard à t.

Cette formulation distingue prix futur, horizon physique et information disponible. Un modèle qui prédit chaque actif séparément n’est pas nécessairement un modèle de distribution jointe. Les dépendances entre futurs des actifs et entre horizons doivent être évaluées explicitement si le modèle les revendique.

**Multivarié et joint ne sont pas synonymes.** L’information d’autres actifs peut améliorer les quantiles marginaux d’une cible sans que le modèle décrive la dépendance entre tous les futurs. Deux processus peuvent avoir les mêmes marges et des corrélations très différentes. Les références à quantiles servent donc au comparatif marginal ; une ambition de trajectoires conjointes exige un générateur ou une structure de dépendance supplémentaire et des évaluations distinctes.

### Trois hypothèses concurrentes

**H0 — langues principalement distinctes.** Le partage n’améliore pas suffisamment les prévisions hors échantillon à ressources comparables. Des modèles par famille ou par actif restent meilleurs.

**H1 — grammaire partagée.** Un préentraînement commun améliore les prévisions d’actifs réservés ou disposant de peu d’historique, même lorsque l’inférence utilise uniquement leur propre passé. Le gain provient d’une représentation transférable.

**H2 — état partagé informatif.** En plus de H1, des observations alignées d’autres actifs améliorent la prévision de la cible. Le gain diminue lorsqu’on détruit spécifiquement l’alignement entre actifs en conservant leurs historiques marginaux.

H1 peut être vraie sans H2. H2 peut concerner certaines familles ou certains régimes sans être universelle. Une combinaison de composantes communes et spécialisées est un résultat possible, et ne représente pas un échec du projet.

### Identifiabilité : ce que signifie « découvrir le marché »

Si une transformation inversible `T` remplace `z` par `z'=T(z)` et les décodeurs par `G'_a=G_a∘T⁻¹`, les prix décrits peuvent rester identiques. Les observations seules ne choisissent donc pas forcément une unique orientation ou signification des coordonnées latentes. Cette ambiguïté simple est compatible avec une bonne prévision.

Le critère primaire doit être l’information prédictive transférable. Pour interpréter ensuite une coordonnée comme « facteur commun », il faut des tests additionnels : stabilité entre initialisations, transfert vers des actifs absents de l’apprentissage, relation à des variables externes réservées et robustesse aux changements de régime. Des cartes d’attention ou des groupes visuellement séduisants ne suffisent pas. Les hypothèses temporelles, les vues multiples et des contraintes de structure peuvent aider l’identification ; leur efficacité doit être mesurée et leur rôle déclaré.

## 4. Une famille GPT comme axe principal de recherche

Le choix principal proposé est un **Transformer causal préentraîné sur séquences de marché**. « GPT » décrit ici une famille architecturale et un objectif autorégressif ; les tokens peuvent être numériques appris et n’ont pas besoin d’être des mots humains. Un vocabulaire appris conjoint et une sortie continue restent deux variantes comparables de cette même ambition.

La conversion peut suivre quatre niveaux : observation réelle → petit patch local → token ou vecteur appris → séquence du modèle. Les champs de contexte conservent l’actif ou ses métadonnées, la durée couverte, la disponibilité et les paramètres de normalisation causale. Un actif inconnu ne doit pas rendre le système inutilisable faute d’un identifiant appris : tester des métadonnées et une représentation calculée sur son contexte disponible.

Une architecture ambitieuse à tester comporte :

1. un encodeur local des prix ou patches de chaque actif ;
2. une attention temporelle causale dans chaque série ;
3. une attention entre vues déjà observées, avec masque d’âge et de disponibilité ;
4. une mémoire lente des sessions et régimes, pour les horizons longs ;
5. un décodeur génératif de distributions ou trajectoires, restituées dans les unités des instruments.

Le découpage factorisé est un choix de calcul à évaluer. Avec `A` actifs et `T` patches, une attention dense sur tous les couples actif–temps coûte schématiquement `O(A²T²)` en interactions ; des blocs temporels et transversaux séparés donnent `O(AT²+TA²)`, hors dimensions cachées et autres couches. Un ensemble de latents partagés plus petit peut réduire encore le coût, au risque de supprimer des relations. Cela justifie une comparaison de représentations, pas l’empilement automatique de toutes les techniques.

Une variante Transformer à futur masqué peut servir de comparaison pour distinguer bénéfice du préentraînement, bénéfice de l’attention et bénéfice de l’autorégression. Cette comparaison ne nécessite pas de faire d’un modèle récurrent la voie principale. Les échecs d’un petit modèle d’une autre famille ne peuvent pas trancher la capacité du système proposé.

### Prévoir le prix brut en conservant une représentation adaptée

La cible reste le prix dans son unité originale. Cela n’interdit pas une transformation interne inversible : par exemple `y=(P−P_ancre)/s`, où l’ancre et l’échelle `s>0` ne dépendent que du passé disponible. Le décodeur restitue `P=P_ancre+s·y`. Pour les séries strictement positives, une variante logarithmique peut être comparée ; la version affine reste définie lorsque le domaine inclut zéro ou des valeurs négatives.

Conserver l’ancre et l’échelle évite de supprimer toute information de niveau. À l’inverse, utiliser directement tous les prix avec la même erreur quadratique donnerait une importance arbitraire aux unités les plus grandes. Si l’on compare des densités après transformation, inclure le jacobien : pour la transformation affine, `log p_P(P)=log p_y(y)−log(s)`. La métrique doit correspondre à la variable réellement revendiquée.

« Prix » nécessite un contrat de données : dernier prix observé, référence quotidienne, milieu de cotation ou autre mesure. Un indice, une action et une série de contrats raccordés ne possèdent pas le même mécanisme de construction. Conserver ces différences comme métadonnées ; ne pas les effacer en les renommant toutes « close ».

## 5. Asynchronisme et plusieurs échelles

Un événement possède au moins une heure d’observation et, lorsque disponible, une heure de réception ou publication. L’attention à l’instant `t` n’accède qu’aux données connues à cet instant. Une observation de date civile identique peut avoir été publiée plus tard sur un autre marché. Une normalisation commune calculée sur la journée entière peut également introduire du futur.

Trois représentations temporelles sont à comparer : grille physique commune avec masques ; flux d’événements irréguliers avec délais ; structure hybride où les événements deviennent des résumés à plusieurs échelles. Le forward fill est admissible comme état « dernière observation connue » uniquement si l’âge et l’absence d’une nouvelle observation sont conservés. Il ne doit pas produire une fausse transaction ni une fausse bougie observée.

Le modèle peut utiliser des reconstructions multi-vues pendant le préentraînement, mais il faut séparer deux tâches. Compléter une vue manquante à une date historique en utilisant d’autres vues contemporaines est une tâche de représentation. Prévoir au-delà de l’instant courant doit masquer **tous** les futurs inconnus, y compris ceux des autres actifs. Sinon le résultat mesure la reconstruction d’un futur partiellement fourni.

## 6. Des décennies et la seconde : deux dimensions complémentaires

Des données fines peuvent révéler des structures supprimées par l’agrégation. Des décennies peuvent fournir des régimes absents d’une courte fenêtre. Collecter uniquement l’un des deux ne remplace pas l’autre. Le corpus doit donc être organisé suivant les axes **profondeur historique, granularité, familles d’actifs, diversité des régimes et qualité de mesure**.

Les épisodes autour de 2000, 2008 et 2020 peuvent constituer des domaines historiques utiles, mais leur rôle expérimental doit être fixé avant d’observer les scores. Pour une simulation de prévision historique de 2008, l’entraînement doit se terminer avant la période évaluée. Un modèle entraîné sur 2009–2026 puis évalué sur 2008 réalise une autre expérience de transfert rétrospectif, à nommer explicitement. Le fait de retirer les lignes de 2008 ne suffit pas à transformer cette seconde expérience en prévision prospective.

Une série à la seconde ne peut pas être reconstruite à partir de données horaires réelles sans inventer les variations intermédiaires. Le corpus doit accepter des résolutions et profondeurs hétérogènes avec masques. Les actifs qui n’existaient pas pendant un épisode ne reçoivent pas d’histoire artificielle. Un échantillon défini uniquement par les actifs survivants aujourd’hui doit être déclaré comme tel et complété lorsque les sources le permettent.

Calcul d’ordre de grandeur, indépendant de toute disponibilité : 30 ans continus à une observation par seconde représentent environ **947 millions de points par actif**, soit **947 milliards pour 1 000 actifs**, avant champs supplémentaires. Les calendriers de cotation réduisent certains volumes. Ce calcul ne prouve pas qu’un tel corpus existe ou soit uniforme ; il montre l’intérêt de stockage hiérarchique, patching et échantillonnage.

La densité n’est pas l’indépendance. Multiplier les observations voisines pendant une même crise ne crée pas de nouvelles crises. Conserver des statistiques par blocs de temps, familles et régimes ; comparer de l’historique supplémentaire à un suréchantillonnage des mêmes journées. Un corpus plus grand doit être décrit par sa couverture autant que par son nombre de tokens.

## 7. Plan expérimental qui départage réellement les hypothèses

| Question | Comparaison proposée | Observation qui soutiendrait l’hypothèse |
|---|---|---|
| Existe-t-il une grammaire transférable ? | Transformer par famille ; Transformer partagé recevant une seule série à la fois. Corpus et budgets de comparaison explicités. | Le partagé améliore les actifs réservés, à plusieurs horizons, sans dégrader systématiquement une famille. |
| Les autres vues contiennent-elles une information utile ? | Modèle partagé univarié ; modèle multivarié aligné ; version où l’alignement entre actifs est perturbé par blocs. | L’aligné améliore les prévisions ; la perturbation retire une partie du gain sans modifier le passé propre de la cible. |
| Le marché commun est-il seulement local à des familles ? | Paramètres totalement partagés ; tronc commun et adaptations par famille ; modèles séparés. | Des adaptations limitées améliorent le transfert tout en conservant le bénéfice du tronc commun. |
| La résolution fine apporte-t-elle de l’information ? | Même période et mêmes actifs en données fines, agrégées et patches multi-échelles ; comparaison à calcul fixé puis à information fixée. | Le gain persiste sur un futur réservé et n’est pas seulement lié à davantage d’étapes d’apprentissage. |
| Les décennies ajoutent-elles une diversité utile ? | Historique récent ; ancien+récent ; répétition du récent à nombre de tokens similaire. | L’ancien+récent améliore les régimes réservés davantage que la répétition. |
| Le tokenizer est-il le goulet d’étranglement ? | Quantification simple ; codes appris ; patches continus, avec architectures de taille et budgets documentés. | Les gains de représentation persistent quand la capacité augmente et se traduisent en meilleure prévision. |
| Les capacités sont-elles limitées par l’échelle ? | Grille de tailles, volumes de données et longueurs de contexte ; plusieurs initialisations aux points clés. | Courbes reproductibles où certaines erreurs diminuent avec capacité ou diversité, et extrapolations confirmées sur une échelle non utilisée pour les ajuster. |

Le contrôle d’alignement doit préserver autant que possible saisonnalité, qualité des données et régimes marginaux ; une permutation arbitraire peut créer un problème trop artificiel. Le gain d’un modèle partagé doit être confronté à deux budgets : nombre de paramètres comparable et calcul total comparable. Un ensemble de petits modèles peut avoir davantage de paramètres cumulés qu’un seul modèle partagé.

Réserver séparément : une période future commune à tous les actifs ; des instruments ; une famille entière ; éventuellement une place et un épisode historique. Pour mesurer le transfert vers une classe absente, la classe doit aussi être absente de l’ajustement du tokenizer, du choix des normalisations globales et de la sélection des hyperparamètres.

Les métriques centrales sont prévision en unités d’origine par actif, erreur normalisée par une échelle calculée sur entraînement, score probabiliste approprié, couverture des intervalles et dépendance des chemins lorsque modélisée. Rapporter horizons et familles séparément, puis une agrégation équilibrée. La persistance du dernier prix constitue un repère indispensable : reproduire un niveau presque constant à horizon très court ne suffit pas à établir l’apprentissage des variations.

Pour les distributions marginales, employer par exemple CRPS ou des scores de quantiles comparables. Pour un générateur joint, ajouter score d’énergie, score de variogramme ou diagnostics ciblés de dépendance et de chemins, avec leur propre incertitude. Une victoire sur les marges ne sera pas présentée comme une victoire sur la distribution jointe.

## 8. Scaling : préserver l’ambition et diagnostiquer les échecs

Une campagne peut explorer, à titre de grille conceptuelle, 10 M, 40 M, 160 M, 640 M puis 1 B+ paramètres. Ces nombres sont des niveaux d’expérience possibles, pas des besoins démontrés ni un engagement d’exécution. À chaque niveau, faire varier les données et le contexte ; augmenter seulement les paramètres à corpus et optimisation insuffisants ne teste pas correctement le potentiel de la représentation.

Une loi exploratoire telle que `L(N,D)=L_inf+a·N^(−alpha)+b·D^(−beta)` peut aider à résumer les mesures. Elle doit comporter une incertitude, des contrôles de résidus et une validation sur un niveau non utilisé pour l’ajustement. Le plan doit suivre volume nominal, diversité par blocs et calcul dépensé. `L_inf` est un paramètre ajusté dans un domaine expérimental limité, pas une connaissance du plafond physique de prédictibilité.

Un petit échec peut venir d’un tokenizer trop destructeur, d’un contexte trop court, d’une optimisation inadéquate, d’un manque d’exemples rares ou d’un modèle incapable d’exploiter des dépendances pourtant présentes. Il ne réfute pas à lui seul H1 ou H2. Symétriquement, remettre tout résultat négatif au compte d’une taille encore insuffisante rendrait l’hypothèse impossible à tester. Chaque étape doit préciser ce qu’elle met à l’épreuve, l’incertitude restante et l’expérience suivante capable de la réduire.

Une erreur irréversible du tokenizer sur un attribut observé ne sera pas réparée exactement par davantage de paramètres ; le modèle pourrait néanmoins prévoir correctement une cible qui n’exige pas cet attribut. Une bonne reconstruction est donc une propriété utile, mais ni nécessaire dans tous ses détails ni suffisante pour une bonne prévision. Le POC de reconstruction existant mesure l’instrument de représentation ; il ne tranche pas encore la possibilité d’un marché latent partagé.

Le résultat recherché est une preuve graduelle : structure transférable, information croisée exploitable, puis progression mesurée avec données et capacité. Une amélioration démontrée sur ces dimensions constituerait un résultat scientifique fort, même sans attribuer une « intelligence » au réseau. Les sorties resteraient des distributions conditionnelles soumises à l’information observée et aux limites de généralisation établies par les expériences.

## 9. Une objection spécifique au Marché unique : le numéraire

L'acquisition réelle de six devises contre EUR rend une difficulté immédiatement concrète. Toutes les séries partagent une unité de référence. Une partie de leur mouvement commun peut donc provenir du dénominateur, même si les dynamiques propres des devises ne se sont pas rapprochées. Un latent très commun n'est pas automatiquement une découverte sur un mécanisme mondial.

Notons Q[a/EUR] le nombre d'unités de la devise a pour un euro, et Q[b/EUR] celui de b. La conversion dérivée donne Q[a/b] = Q[a/EUR] / Q[b/EUR]. Pour les variations logarithmiques entre les mêmes dates, on obtient exactement :

`r[a/b] = r[a/EUR] - r[b/EUR]`.

Cette relation est une identité algébrique sous conventions cohérentes, pas un résultat statistique nouveau. Construire toutes les paires croisées peut multiplier le nombre de séries, mais ne crée pas autant de nouvelles observations indépendantes. Une approximation due aux arrondis ou à des heures de mesure différentes ne doit pas être interprétée sans contrôle comme un nouveau facteur.

Trois expériences sont proposées. D'abord, changer le numéraire en conservant exactement les mêmes observations et mesurer la stabilité des prévisions ramenées à une cible commune. Ensuite, comparer un modèle qui reçoit explicitement la référence monétaire à un modèle qui doit l'inférer. Enfin, comparer la structure latente à des identités de conversion et à des facteurs linéaires simples ajustés sur le passé. Une amélioration résiduelle, reproduite ailleurs, serait plus informative qu'une visualisation de six séries qui bougent ensemble.

Ce contrôle n'exige pas l'invariance de toutes les coordonnées latentes : leur géométrie peut changer sous une transformation inversible. Il demande que les affirmations prédictives survivent au retour vers les mêmes prix et dates. Une conversion d'unités connue peut être traitée comme une symétrie ; la dynamique propre d'une devise de référence reste une information à modéliser.

La même précaution s'étend aux indices et produits apparentés, sans leur appliquer abusivement la formule des devises. Un indice, ses composants et un produit qui le suit possèdent des dépendances de construction. Ils ne doivent pas être répartis naïvement entre apprentissage et test comme des langues totalement nouvelles. La composition historique, les règles d'indice et les dates de disponibilité définissent le degré de séparation réellement obtenu.

## 10. Une grammaire cohérente entre résolutions

Une autre proposition est d'exiger que les prévisions fines et grossières décrivent le même futur possible. Soit A_h l'opérateur qui agrège une trajectoire fine en observation sur h secondes, minutes ou heures. La loi grossière devrait être compatible avec la loi obtenue en agrégeant les trajectoires fines :

`Loi_grossiere(. | F[t]) ≈ image_par_A_h(Loi_fine(. | F[t]))`.

Pour des bougies, A_h conserve la première ouverture, le dernier cours, le maximum des hauts, le minimum des bas et la somme des volumes compatibles. Il doit aussi conserver les intervalles incomplets et la définition du volume. Pour des références quotidiennes sans chemin intrajournalier, cet opérateur n'existe pas sous cette forme ; la branche ne reçoit pas une trajectoire fine inventée.

La cohérence s'évalue sur des distributions ou des trajectoires échantillonnées. Agréger des prédictions moyennes ne suffit pas : l'espérance d'un maximum n'est pas en général le maximum des espérances. Des marges bien calibrées peuvent ainsi produire un ensemble de résolutions incompatibles.

Le projet pourrait apprendre un vocabulaire local fin et une grammaire lente avec un objectif auxiliaire de cohérence. Le contraste scientifique serait le même GPT avec et sans ce terme, à calcul documenté, puis la vérification sur des fréquences et actifs réservés. Trop de contrainte peut dégrader les prévisions si l'agrégation, les observations ou le modèle sont mal spécifiés ; la cohérence ne devient donc pas un dogme.

Ces deux axes, symétries d'unité et cohérence d'agrégation, donnent un sens technique à l'idée de plusieurs langues décrivant un même Marché. Ils ajoutent des relations vérifiables entre représentations. Leur nouveauté et leur bénéfice devront être évalués par rapport aux travaux existants ; aucune expérience prédictive ne les a encore départagés dans TRAME.
