# TRAME, étape 1 : qualification de la tête P1-B0

*Session du 25 octobre 2026. Document de recherche révisable, non gelé.
Ne jamais le confondre avec un rapport de validation financière.*

## Portée et décision

On peut passer à un **mini-modèle sur séries artificielles**, à condition
de conserver le statut expérimental et les garde-fous ci-dessous.
**No-Go** pour un entraînement de marché présenté comme probant, la
génération fiable d'événements extrêmes, le temps réel de trading et le
produit de prévision commercial : les données, les témoins et la
validation externe n'ont pas été qualifiés.

Cette branche dépend de \`chatgpt/p1b0-numerical-lab-20261025\`, PR #2 ;
ne pas y écraser la PR #1 de métriques. Aucune partition réservée n'a
été consultée, aucune transaction n'a été faite.

## Matrice des sept sous-étapes

| Sous-étape | État technique | Preuve reproductible | Limite résiduelle |
| --- | --- | --- | --- |
| 1.1 mu/sigma | Implémentation PyTorch double précision, comparaison indépendante SciPy | \`test_torch_head.py\` | Autodiff PyTorch évaluée sur matrice construite ; gradients de backbone absent |
| 1.2 bornes | Mapping candidat tanh/sigmoid, initialisation et saturation testées | \`torch_head.bounds_transform\` + tests | La saturation donne des gradients quasi nuls, à contrôler pendant un vrai fit |
| 1.3 queues | Évaluation log-space, audit de sous-flux, échantillonnage conditionnel via \`ndtri_exp\` | \`tails.py\`, \`test_stage1.py\` | Le tirage **conditionnel** n'est pas un tirage *inconditionnel* des événements rares |
| 1.4 causalité | Tests de 20 pas avec état entier, répétabilité et teacher forcing | \`rollout.py\`, \`test_stage1.py\` | Tête fictive plutôt qu'un Transformer entraîné ; tests de très grands chemins non exhaustifs |
| 1.5 prix/MC | Quantiles, couverture 50/80/90 %, largeurs, CRPS empirique, MC répété | \`calibration.py\`, \`test_calibration.py\` | L'écart-type MC ne représente pas l'incertitude des régimes de marché |
| 1.6 coût | Benchmark CPU reproductible du normalisateur 4096 termes et backward PyTorch | \`benchmark_stage1.py\` + artefact CI | Mesures propres à un runner CPU partagé ; pas de profil GPU ni de comparaison des modèles complets |
| 1.7 revue | Limites, décisions et escalade vers l'étape 2 consignées | Ce document, Git history, \`AGENTS.md\` | Revue indépendante externe toujours absente |

## Notes de chercheur

### Dérivées et valeur probante

\`torch_head.py\` reproduit
\`q(k)=Phi((k+.5-mu)/sigma)-Phi((k-.5-mu)/sigma)\`
sans soustraire de CDF proches de 1, et inclut **les deux queues**
dans le normalisateur. La fonction de perte accepte des cibles hors
[-2048, 2047] sans écrêtage.
Les dérivées par autodiff de mu et sigma sont croisées avec des
différences finies de la tête SciPy d'origine et les gradients des
logits avec le calcul analytique de la PR #2. Cela qualifie la
tête isolée, **pas** l'optimisation d'un modèle de langage complet.

### Événements extrêmes

Le test de stress peut *forcer* un tirage conditionnel dans les queues,
y compris si leur probabilité inconditionnelle n'est pas représentable
en double. Ce tirage ne peut donc pas servir à estimer leur fréquence
réelle ; il ne démontre pas non plus que leur impact financier
serait négligeable. Une politique de risque extrême fiable reste un
verrou produit et l'implémentation refuse de prétendre le contraire.

### Scores

\`score_ensemble\` ne mélange jamais les unités de différents actifs
et horizons, accepte les prix strictement positifs finis uniquement,
calcule les quantiles, la couverture et le CRPS d'ensemble.
\`mc_replicate_crps\` estime uniquement la variation du score due à
des **simulations répétées indépendantes** : ne pas utiliser l'écart
type comme intervalle de confiance sur le pouvoir prédictif.
Pour des prévisions à fenêtres historiques recouvrantes, utiliser
les procédures de dépendance temporelle déclarées au protocole séparé.

### Coûts

Le programme \`benchmark_stage1.py\` mesure des temps de création
complets (incluant 4096 masses et normalisateur) et de dérivées
CPU avec \`torch.set_num_threads(1)\`. Les statistiques doivent
être lues avec la configuration de machine jointe ; ne pas inventer
un nombre de FLOPs ou une comparaison GPU équivalente.
Le calcul scientifique force float64 dans la qualification ; aucune
prétention de stabilité en float32 n'est autorisée.

## Reproduction

À partir de cette branche :

~~~bash
python -m pip install 'numpy==2.3.5' 'scipy==1.17.0'
python -m pip install 'torch==2.10.0' --index-url https://download.pytorch.org/whl/cpu
python -m unittest discover -s research/p1b0_numerics -p 'test_*.py' -v
python research/p1b0_numerics/preflight.py
python research/p1b0_numerics/benchmark_stage1.py
~~~

Voir \`.github/workflows/p1b0-stage1.yml\` pour le run attesté et ses
rapports machine. Préserver les fichiers bruts en artefacts Actions
et les logs d'échec. Aucun script ne télécharge le marché.

## Critère de Go/No-Go

**Go limité pour l'étape 2 :** développer un petit Transformer
*exclusivement sur lois synthétiques*, comparaison au modèle oracle
et au témoin de persistance, avec tests de fuite et budgets modestes.

**No-Go** sur entraînement réel confirmatoire tant que les étapes
sur corpus, modèles témoins et holdout n'ont pas été remplies.
**No-Go** sur usage de trading automatique, API privées, effet de
levier ou communication de performance financière.

### Audit pour Codex

- Base de PR : \`chatgpt/p1b0-numerical-lab-20261025\`, pas \`main\`.
- Commits sur branche \`chatgpt/p1b0-stage1-validation-20261025\`.
- Référence théorique \`research/trame_research_plan/20261016/p1b0_candidate.json\`
  conservée en l'état.
- Toute réparation doit garder l'évidence d'échec et l'amendement ;
  ne pas réécrire les audits historiques des éditions précédentes.

## Préparation de l'étape 2 : sous-étapes détaillées

2.1. Contrat synthétique *train / validation / test* et source oracle
   scellée, avec générateurs reproductibles et séparation stricte
   des graines. Préférer des distributions causales connues
   plutôt que fabriquer des données qui avantagent TRAME.

2.2. Backbone Transformer minimal autoregressif, petit CPU, avec
   BOS, masque causal et entrée des codes précédents seulement.
   Préserver la tête P1-B0 et l'état entier cumulatif ; simplifier
   explicitement si l'on change de protocole.

2.3. Faire fonctionner une passe avant et arrière sur un batch
   artificiel et prouver l'absence de fuite du futur.

2.4. Entrainer un modèle miniature avec budgets et graines
   déclarés. Conserver tous les runs et échecs, ne pas sélectionner
   sur les exemples de test.

2.5. Témoin oracle/base indépendant et comparaison hors
   entraînement : NLL de codes, CRPS en prix fictifs, erreurs,
   couverture et intervalles MC.

2.6. Ablations BASE / HIER / FLAT et témoins non Transformer,
   **uniquement** après égalisation ou mesure explicite des budgets.
   Publier les différences de capacités et de calcul.

2.7. Rapport et décision Go/No-Go vers la préparation du corpus
   réel ; si échec, le publier sans réinterpréter l'expérience.
