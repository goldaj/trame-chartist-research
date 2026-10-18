# Ancres, causalité et langue différentielle : trois contrôles avant le GPT

Note de travail du 15 octobre 2026. Déductions mathématiques et propositions expérimentales. Aucun modèle implémenté, aucune performance nouvelle mesurée. Ce texte complète les sections 5 et 6 du document 09 ; il ne remplace pas l'étude de reconstruction 07, dont la portée descriptive était explicite.

## 1. Le canal auxiliaire peut annuler la perte du tokenizer

Considérons un passé `P_0, ..., P_T`. Si l'on quantifie ses variations mais que l'on transmet aussi l'ancre exacte `P_(t-1)` pour chaque observation t, le canal des ancres révèle presque tous les prix. Si le dernier prix P_T est également fourni, les données entières sont connues indépendamment des tokens. La comparaison peut alors mesurer l'aptitude du réseau à lire des doublons plutôt que l'effet de la langue.

Le problème est distinct d'une fuite du futur : toutes ces ancres peuvent appartenir au passé autorisé. C'est une confusion sur **quelle information la représentation élimine réellement**. Si S contient tout X, `I(Y;X | Z,S)=0` pour toutes les langues Z ; on ne peut plus interpréter la différence comme la perte d'information de Z seul.

Le POC0 mesurait la reconstruction conditionnelle avec des ancres et échelles connues, et ne prétendait pas tester un prédicteur. Ses erreurs restent valides pour cette tâche. Elles ne suffisent pas à prédire le comportement d'une séquence autonome de tokens. Le candidat P1-A limite donc S à un prix courant et une échelle par origine, avec des métadonnées communes clairement listées. Une expérience de compression autonome devra plutôt compter une ancre initiale et les éventuels rafraîchissements explicites.

Des échelles locales continues, des durées codées avec une précision arbitraire ou des longueurs de code peuvent également transmettre de l'information. Cela n'est pas interdit, mais doit être mesuré comme un canal à part entière. Un tokenizer « à seulement trois symboles » ne constitue pas une compression à trois états si ses métadonnées restituent les amplitudes.

## 2. Masque causal et prétraitement causal ne sont pas équivalents

Normaliser toute une fenêtre par son prix final P_T est autorisé pour prévoir après T. Mais cela fournit P_T au calcul des tokens des positions antérieures. Si l'on entraîne ensuite une perte de prochain prix à chaque position t<T, le masque d'attention ne retire pas l'information future déjà contenue dans ces tokens.

Deux contrats sont valides, à condition de ne pas les mélanger. Le contrat par origine traite toute la fenêtre comme contexte connu et évalue seulement les cibles après son dernier point. Le contrat en flux exige que le token t, l'état du codeur et ses échelles ne dépendent que du préfixe jusqu'à t. Le premier ne prouve pas que le tokenizer du second est causal.

Contrôle proposé pour un codeur en flux : modifier un suffixe de données sans changer le préfixe ne doit modifier aucun token ni état de normalisation du préfixe. Pour un codeur par origine, le contrôle porte sur toutes les valeurs postérieures à l'origine ; modifier un prix à l'intérieur du contexte peut légitimement changer son encodage. Le choix du test suit le contrat, pas seulement la présence d'un masque triangulaire dans le GPT.

Dans P1-B, une génération future peut conditionner le raffinement d'un token sur sa partie grossière déjà produite. Elle ne peut recevoir la partie grossière réelle du futur. La différence entre apprentissage de la factorisation et génération effective doit être vérifiée au point d'évaluation.

## 3. Une piste de langue en flux : encoder l'écart au prix reconstruit

La méthode suivante est une adaptation conceptuelle du codage prédictif différentiel, avec des antériorités anciennes. Les mécanismes de prédiction à partir de valeurs reconstruites sont décrits notamment dans le [manuscrit de Robert Gray, chapitre 10](https://ee.stanford.edu/~gray/lpcip.pdf). TRAME ne revendique pas l'invention de DPCM.

Pour simplifier, écrivons `u_t = log(P_t)` quand les prix sont strictement positifs. Le codeur et le décodeur partagent une première ancre u_0. Ils conservent ensuite le même état reconstruit `u_hat_(t-1)`. Le codeur forme `e_t = u_t - u_hat_(t-1)`, le quantifie en q_t, puis les deux côtés mettent à jour `u_hat_t = u_hat_(t-1) + q_t`.

Avec une grille de pas delta et arrondi au plus proche sans saturation, `|q_t-e_t| <= delta/2`. Par substitution, `u_hat_t-u_t = q_t-e_t`. L'erreur de reconstruction du niveau courant reste donc bornée par delta/2, sans addition de toutes les anciennes erreurs. Cette propriété suppose un état identique, un code transmis correctement et aucune saturation. Elle ne couvre pas une perte de token ou une différence d'initialisation.

En comparaison, si l'on quantifie les vraies variations `u_t-u_(t-1)` puis qu'on les additionne à la reconstruction précédente, l'erreur de niveau est une somme des erreurs de quantification. Son pire cas peut croître avec le nombre de pas. Cette différence motive un témoin distinct de la quantification des variations véritables déjà étudiée.

La borne sur les logarithmes implique une borne de facteur multiplicatif : le rapport reconstruit/vrai se situe entre `exp(-delta/2)` et `exp(delta/2)`. Pour des prix non positifs, une formulation affine remplace le logarithme. Un pas adaptatif peut être calculé à partir du passé reconstruit partagé ou transmis explicitement ; le coût et le contenu informatif de sa transmission doivent être comptés.

Une version progressive décompose q_t en plusieurs niveaux. **Le flux grossier doit posséder son propre état grossier.** Si les tokens grossiers suivants sont encodés relativement à un état fin mais que leur lecteur a supprimé les raffinements, codeur et décodeur ne partagent plus la même prédiction. La propriété de reconstruction peut disparaître. Deux pistes sont admissibles : des niveaux ayant chacun leur état reproductible, ou des corrections fines indépendantes qui ne modifient jamais l'état utilisé par le flux grossier suivant. Leur débit et leur avantage d'apprentissage restent à étudier.

Ce détail rapproche la question de langue de celle d'un protocole : un préfixe de bits doit non seulement décrire le point courant, mais aussi permettre d'interpréter correctement les points suivants. Un alphabet hiérarchique local ne garantit pas à lui seul un flux hiérarchique cohérent.

## 4. La borne de reconstruction ne prédit pas le futur

Lorsque u_t est déjà observé, le codeur calcule e_t exactement à partir du vrai prix. Lors d'une prévision, u_t est inconnu et le GPT doit produire une distribution de q_t, éventuellement complétée par un résidu. La borne de quantification ne borne pas son erreur prédictive : elle compare la vraie valeur à son code, pas à un code deviné.

Le codage différentiel peut même modifier la difficulté statistique : les erreurs de reconstruction passées entrent dans le prochain résidu. Une structure apparente dans les tokens peut provenir du codeur. Le témoin doit être soumis au même codeur ; un gain sur les tokens ne suffit pas si les prix décodés n'en bénéficient pas. Une meilleure reconstruction et une meilleure modélisation du prochain résidu sont deux objectifs distincts.

Il faudra également séparer le cas où une prévision à un pas est réinitialisée à chaque vrai prix nouvellement observé du cas où une trajectoire entière est générée sans observation intermédiaire. Le second accumule des erreurs de modèle même si le codec, appliqué aux observations, possède une borne sans dérive.

## 5. Expérience documentaire proposée avant tout réseau

Une comparaison future de codecs pourrait appliquer aux mêmes observations réelles : variations véritables quantifiées, résidus relativement à l'état reconstruit, et quantification des niveaux avec une ancre. On fixerait au préalable le pas, la précision des ancres, les règles de rafraîchissement, les états grossiers/fins et les échappements.

Les mesures porteraient sur erreur de niveau, erreurs locales, débit réel complet, fréquence des échappements, délai de décodage et conservation de la causalité. Les mêmes données déjà explorées peuvent servir à cette analyse descriptive, sans prétention de test final. Aucun modèle prédictif n'est nécessaire à ce stade ; aucune expérience de ce type n'a été exécutée pendant cette itération.

Les preuves et les contre-exemples ci-dessus servent à corriger le plan, pas à choisir dès maintenant un vainqueur. Ils constituent des critères précis pour éliminer une implémentation incohérente sans éliminer prématurément une famille de langages.
