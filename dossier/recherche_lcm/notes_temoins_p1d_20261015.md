# Témoins P1-D : définitions exactes avant une expérience prédictive

Révision documentaire 0.2, 15 octobre 2026. Aucun des prédicteurs ci-dessous n'a été implémenté, ajusté ou évalué. Cette note ferme les ambiguïtés de formule du candidat 0.1 ; elle ne constitue pas un nouveau tableau de résultats.

Mise à jour documentaire 0.3 après l'audit de 14:38 UTC : les formules demeurent celles de 0.2 ; les blocs annuels ont désormais été comptés sur le calendrier réel. Ils fournissent par actif 1 255 origines de résidus potentiels à h=1, 1 239 à h=5 et 1 179 à h=20, avec toutes les cibles d'ajustement antérieures à leur année de calibration. Aucun résidu n'a été calculé. Voir le [rapport descriptif et ses limites](notes_audit_reel_et_langage_hybride_20261015.md).

## 1. Information, cible et précision

À l'origine i, les témoins utilisent les 256 références positives `P_(i-255), ..., P_i` et le calendrier passé. Ils prévoient les mêmes prix que les futurs GPT, aux horizons de 1, 5 et 20 publications, sur les origines communes déjà comptées. Les observations postérieures à l'origine sont interdites en entrée. Le statut de l'historique reste celui d'une version révisée acquise en 2026, non d'une reconstitution certifiée des premières publications.

Les témoins sur prix non quantifiés disposent de l'information continue de C. Ils évaluent le niveau de difficulté de la tâche et la valeur du dispositif complet. Ils ne constituent pas des témoins « à information identique » de Q/H ; cette qualification est réservée aux contrastes de représentation spécifiés ailleurs. Aucun témoin ne reçoit un actif supplémentaire dans la première comparaison qui limite les GPT à l'histoire de l'actif cible.

La volatilité s_i est l'écart-type de population des 64 incréments logarithmiques terminant en i, centré par leur moyenne, avec plancher 10^-6. Les incréments correspondent à des publications successives ; la multiplication par sqrt(h) est une hypothèse du témoin, pas une mesure du temps physique ni une loi certifiée des prix.

## 2. Trois témoins sans paramètre appris

**B0, persistance.** Tous les quantiles annoncés valent P_i, pour chacun des horizons. C'est une distribution dégénérée et un repère utile pour la médiane ; elle sera normalement peu adaptée à la couverture d'intervalles non dégénérés. Aucun résultat de couverture n'est présumé.

**B1, marche aléatoire en logarithme.** Pour un niveau tau, `q_(i,h,tau) = P_i exp(s_i sqrt(h) Phi^-1(tau))`, où Phi est la fonction de répartition normale standard. Le drift logarithmique est nul. La médiane vaut P_i, mais l'espérance de cette loi lognormale vaut `P_i exp(h s_i²/2)`. On ne décrira donc pas B1 comme une martingale du prix.

Une sensibilité B1m impose une espérance du prix égale à P_i : `q = P_i exp(-h s_i²/2 + s_i sqrt(h) Phi^-1(tau))`. Cette égalité est celle de la distribution supposée, pas une assertion sur le marché. L'évaluation quantile ne récompense pas la même fonctionnelle qu'une erreur quadratique sur la moyenne ; la distinction empêche d'attribuer un simple changement de cible à la langue.

**B2, distribution empirique locale.** Pour chaque h, construire les `n=256-h` incréments `r_(j,h)=log(P_j/P_(j-h))`, pour `j=i-255+h, ..., i`. Les valeurs terminales candidates sont `V_j=P_i exp(r_(j,h))`. Trier ces n prix, puis calculer les quantiles par interpolation linéaire dans **l'espace des prix** : avec `a=(n-1) tau`, `ell=floor(a)` et `g=a-ell`, `q=(1-g)V_(ell)+g V_(ell+1)`, indices commençant à zéro, avec la convention habituelle au dernier indice. Pour les sept niveaux retenus, ils restent intérieurs lorsque n>1.

Cette définition correspond à `method="linear"` dans la [documentation officielle de NumPy](https://numpy.org/doc/2.3/reference/generated/numpy.quantile.html). Calculer d'abord un quantile interpolé en logarithme puis l'exponentier donnerait en général une autre valeur ; on ne mélangera pas ces deux versions. Les incréments se chevauchent, particulièrement à h=20 : ils ne sont pas autant de tirages indépendants, et leur nombre n'implique aucune précision statistique garantie.

Les témoins B0/B1/B1m/B2 actualisent leur contexte déterministe à chaque origine ; ils ne réajustent pas de poids sur les cibles du développement ou du pseudo-test. Leurs sorties sont évaluées avec exactement les sept quantiles et les mêmes pertes natives/normalisées que les candidats neuronaux.

## 3. Témoin linéaire avec information propre ou croisée

Le témoin B3 vise à distinguer un gain de contexte croisé d'une dépendance linéaire simple. Deux variantes séparées sont prévues : B3-propre pour les comparaisons de langue utilisant seulement l'actif cible ; B3-croisé pour la comparaison H2 avec six histoires disponibles. Elles ne constituent pas une reproduction d'un article particulier.

À chaque origine et pour chaque actif disponible b, inclure les 20 derniers incréments logarithmiques divisés par s_(b,i), puis log(s_(b,i)). Cela donne 21 caractéristiques dans B3-propre et 126 dans B3-croisé. Pour chaque actif cible a et horizon h, la cible de régression est `z = log(P_(a,i+h)/P_(a,i)) / (s_(a,i) sqrt(h))`. Les coefficients sont propres à chaque actif et horizon. Le partage de paramètres entre actifs n'est pas testé par ce témoin.

Chaque colonne est centrée et réduite sur les origines d'ajustement de la régression concernée, sans utiliser développement ni pseudo-test. Une variance nulle donne une colonne nulle et une échelle conventionnelle égale à 1. L'interception est libre. La régression minimise `(1/n) somme (z-beta0-X beta)^2 + alpha ||beta||²`, sans pénalité sur beta0. La grille alpha proposée est `{0,0001 ; 0,01 ; 1 ; 100}`. Ce sont des constantes de conception, pas des valeurs sélectionnées après observation de scores.

Pour convertir la position prévue en quantiles, on emploie des résidus obtenus hors ajustement dans cinq blocs annuels 2005–2009. Pour chaque année y et chaque alpha, ajuster sur les origines dont la cible à horizon h est publiée strictement avant le 1er janvier y. Prédire ensuite les origines de l'année y appartenant au cohort commun et dont la cible demeure dans y. Les caractéristiques et leur standardisation sont recalculées avec le seul ajustement de ce bloc. Aucun résidu d'ajustement direct ne remplace ces résidus chronologiques.

On regroupe ces résidus z moins prévision, séparément par actif, horizon, alpha et variante propre/croisée. Leurs sept quantiles c_tau sont obtenus par la même interpolation linéaire, cette fois dans l'espace des résidus standardisés. La prévision terminale est `q = P_i exp(s_i sqrt(h) (z_hat + c_tau))`. Il s'agit d'un modèle de décalage de résidus supposé transférable. L'hétéroscédasticité résiduelle et les ruptures peuvent invalider sa calibration ; aucune couverture théorique uniforme n'est promise.

Pour chaque alpha, la régression finale est ajustée sur toutes les origines admissibles 1999–2009. Les résidus restent ceux des cinq blocs historiques, pas les résidus de cet ajustement final. Le choix d'alpha utilise le score primaire moyen à horizon 1 sur le développement 2010–2014, avec poids égal aux six actifs ; un alpha commun est retenu pour les six actifs et les trois horizons, séparément pour B3-propre et B3-croisé. En cas d'égalité numérique stricte, le plus grand alpha est retenu. Les coefficients, échelles et quantiles résiduels sont ensuite gelés pour le pseudo-test 2015–2020. Aucun réajustement sur ses cibles.

Le développement sert donc explicitement à un choix ; il ne sera pas rapporté comme confirmation indépendante. Le pseudo-test est déjà exploratoire par provenance. Les effectifs exacts des cinq blocs ont été vérifiés et aucun n'est vide. Le conditionnement numérique et la suffisance statistique des résidus futurs restent à examiner. Si une sortie devient non finie, on interrompt et documente l'amendement ; on n'invente pas un remplacement favorable.

## 4. Ce qui reste à fermer

Les définitions ci-dessus sont suffisantes pour demander ultérieurement une implémentation sans laisser choisir discrètement le drift, l'espace d'interpolation, les résidus ou le numéraire. Il reste à arrêter les budgets de réglage et d'optimisation des GPT, leurs diagnostics de convergence et les sensibilités des encodeurs numériques. Les comptes de paramètres de la note sur l'alphabet ne représentent ni mémoire réelle mesurée, ni durée de calcul.

La question de recherche demeure : à information déclarée et coût documenté, quel système apprend le mieux la distribution de prix ? Un échec à battre B1 sur ce corpus limiterait le résultat de cette expérience. Il ne réfuterait ni tout langage possible, ni l'effet d'une nouvelle famille d'actifs, ni la possibilité d'une meilleure architecture à une autre échelle.
