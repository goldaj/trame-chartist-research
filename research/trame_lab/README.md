# TRAME Research Lab v0.1 : livrable offline expérimental

**25 octobre 2026 | version de recherche, non financière.**

La commande livre immédiatement **deux fichiers locaux** :
un rapport HTML autonome et un rapport JSON chiffré.
Elle exécute de vraies expériences sur un **marché entièrement inventé**
et peut servir de démonstration reproductible à un chercheur ou
à Codex, sans télécharger de données ni accéder à un portefeuille.

**Elle n'est pas TRAME Predictive v1.**
Aucune validation de capacité prédictive sur cours réels n'existe.

## Installation (Windows / PyCharm / PowerShell ou Linux)

Python 3.12 et dépôt cloné :

~~~powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install numpy==2.3.5 scipy==1.17.0
python -m pip install torch==2.10.0 --index-url https://download.pytorch.org/whl/cpu
python -m research.trame_lab.cli --output trame_research_lab.html
~~~

Depuis Linux/macOS, activer \`.venv/bin/activate\` à la place.
Pour expérimenter rapidement sans prétendre mesurer une convergence :

~~~powershell
python -m research.trame_lab.cli --steps 5 --output essai.html
~~~

Le résultat contient \`essai.html\` et \`essai.json\`.
Ouvrir \`essai.html\` dans un navigateur sans serveur HTTP.
Pour éviter l'écrasement accidentel, un résultat préexistant
provoque une erreur ; ajouter \`--overwrite\` pour remplacer.

Pour tester uniquement le logiciel (sans entraîner 40 fois) :

~~~powershell
python -m unittest discover -s research/trame_lab -p "test_*.py" -v
~~~

## Ce que montre le rapport

1. NLL de **développement synthétique** pour le mini-Transformer,
   l'oracle exact de la loi artificielle, la régression
   train-only et le témoin gaussien constant.
2. Quantiles et CRPS de trajectoires de **prix fictifs**
   engendrées sur 20 pas (aucune origine réelle).
3. Scoring apparié avec gain **fabriqué intentionnellement**,
   pour démontrer le bootstrap, et non pour affirmer que
   le modèle est meilleur.
4. Liste permanente des blocages de la recherche financière :
   licences et millésimes, baselines réelles, tests indépendants,
   risques extrêmes.

Le JSON reprend les mesures, graines, tailles, contrôles
et limites. Les durées CPU de calcul varient entre machines
même si les seeds et l'environnement numérique sont fixés.

## Contrats de sécurité et d'honnêteté

- Aucun import de \`requests\`, client exchange, wallet, clé,
  connexion API ou mécanisme d'ordres n'est effectué par le labo.
- \`--output\` nomme les fichiers écrits. Rien n'est écrasé
  silencieusement, même si le HTML est présent sans son JSON.
- Toute figure porte la mention claire *données artificielles*.
- Aucune métrique ne représente un backtest ou une performance
  de trading. Le rendu n'affiche jamais de recommandation d'achat.
- La connaissance de l'oracle artificiel ne se transfère pas
  aux vrais marchés. Les partitions financières vierges
  ne sont ni ouvertes ni fabriquées ici.

## Vérification CI et paquet livrable

Le workflow \`.github/workflows/trame-research-lab.yml\`
exécute les tests, génère le rapport et publie l'artéfact
\`trame-research-lab-0_1-synthetic\`, contenant HTML + JSON.
Les fichiers sont archivés avec le commit qui les a produits
et ne nécessitent pas un serveur.

## Position dans les huit étapes

- Étape 1 : qualification de la tête, terminée pour fixtures.
- Étape 2 : mini-modèle et comparateurs synthétiques, terminée
  pour ses expériences exploratoires.
- Étape 3 : règles de données, code validé ; **source réelle bloquée**.
- Étape 4 : outillage de benchmark, code validé ;
  **benchmark financier et gel bloqués**.
- Étapes 5, 6 et 7 : **non entamables honnêtement** sans données
  et tests indépendants approuvés.
- Étape 8 : **livrable Research Lab v0.1 livré ici** ;
  pas de maturité Predictive v1 tant que 5–7 restent No-Go.

## Prochaines sous-étapes produit, lorsqu'on peut avancer

8.1. CLI reproductible HTML + JSON et tests (ce dépôt).
8.2. Audit d'interface et d'accessibilité locale sur navigateur
     réel, non encore réalisé.
8.3. Import de séries via le contrat point-in-time étape 3,
     **uniquement** quand licence et source qualifiées.
8.4. Graphiques conditionnels par actif et horizon avec
     quantiles, scores et intervalles correctement calibrés.
8.5. Checkpoints de modèles réels, versionnement, fiches
     d'entraînement et détecteurs de distribution hors domaine.
8.6. Packaging, tests Windows/PyCharm et
     répétabilité inter-machines.
8.7. Revue indépendante et livraison de Predictive v1
     **seulement si** étapes 5–7 concluent Go.

## À faire par Codex

Lire les fichiers dans cet ordre :
\`AGENTS.md\`,
\`docs/CHATGPT_PROJECT_HISTORY.md\`,
\`research/p1b0_numerics/STAGE1_DECISION_20261025.md\`,
\`research/mini_gpt_synthetic/README.md\`,
\`research/market_data_contract/STAGE3_REPORT_20261025.md\`,
\`research/benchmark_synthetic/STAGE4_REPORT_20261025.md\`,
puis ce document et \`cli.py\`.

Branche \`chatgpt/trame-research-lab-v01-20261025\`,
empilée sur la branche de benchmark de la PR #6 :
pas de fusion indépendante des bases sans revue.

## Consolidation expérimentale du 25 octobre 2026

La branche dépendante `chatgpt/trame-lab-hardening-20261025`
introduit les sous-étapes **8.2a** (tableau NLL accessible aux
technologies d'assistance, lien clavier) et **8.6a** (contrôles
de paramètres et métriques avant publication).
Consulter [la note d'audit, ses tests et ses limites](HARDENING_NOTE_20261025.md).
**Le contrôle navigateur réel 8.2b et l'atomicité de la paire de
fichiers restent ouverts**, et les étapes prédictives 5–7 sont toujours
bloquées. Aucune conclusion financière supplémentaire.


## Politique multi-architectures désormais obligatoire

TRAME n'est plus gouverné par l'hypothèse que le Transformer de l'étape 2
serait l'architecture finale. Le [registre et protocole de comparaison](../architecture_comparison/README.md)
définit des bras causaux identiques en cibles et données, leurs statuts,
les contrôles statistiques et les familles futures (SSM, hybride,
modèles de séries temporelles). La première comparaison automatique
entre ancien Transformer, mini décodeur GPT-style et GRU est
**purement synthétique, de développement et non compute-fair**.
Elle ne fournit aucun résultat de marché ni classement final.


### Sortie multi-architectures incluse dans le rapport

La commande existante `python -m research.trame_lab.cli --steps 20
--output trame_research_lab.html` produit aussi une section
**3 architectures × 3 graines**, reproductible dans le JSON
sous `architecture_comparison`. Ces nombres sont uniquement
des NLL de développement d'un processus AR(1) fabriqué ;
l'écart de taille/compute est signalé dans le rapport.


### Vérification de capacité A3a (exploratoire)

Un nouveau choix de largeurs minimise l'écart de nombres de paramètres
autour du Transformer largeur 16, et rapproche le total à moins de
10 % par architecture sur la grille proposée. Le rapport affiche
explicitement le nombre de paramètres et la largeur de chaque bras.
**Le coût réel d'entraînement, le budget de recherche et les FLOPs
restent différents ; aucun classement compute-fair n'est revendiqué.**
