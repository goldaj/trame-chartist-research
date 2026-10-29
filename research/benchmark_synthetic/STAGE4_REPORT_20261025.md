# Étape 4 TRAME : évaluation appariée synthétique et conditions de gel

**25 octobre 2026.** Instruments de mesure testés sur données
artificielles. **Aucune comparaison financière réelle exécutée** :
l'étape 3 bloque toujours l'ingestion des sources non qualifiées.

## Question

Comment comparer une prévision P1-B0 à un témoin simple sans
inflation par fenêtres recouvrantes, fusion abusive des monnaies
ou fausse précision des statistiques ?

## Bilan des sous-étapes

| Sous-étape | Réalisé | Limitation |
| --- | --- | --- |
| 4.1 Contrat apparié | \`bootstrap.validate_records\` adopte les 7 colonnes de la PR #1, avec actif, horizon et indices origine/cible | Les prédictions entrantes doivent en plus prouver leur provenance via le contrat étape 3 |
| 4.2 Persistance | Erreur absolue de \`anchor\` sur chaque cible, sans apprentissage | Aucun score commercial inférable des fixtures |
| 4.3 Modèle numérique fort | Régression linéaire et oracle **train-only/development** de l'étape 2 conservés | Pas encore d'AR/Ridge temporel multiactif calibré de manière complète |
| 4.4 Scores | MAE natives de chaque bras et gain apparié, séparés actif/horizon ; CRPS, quantiles et couverture du laboratoire étape 1 | Une NLL de codes ne se compare pas directement à une densité de prix |
| 4.5 Audits | Rejet colonnes inattendues, doublons origine/actif/horizon, prix non finis, indices et horizons contradictoires | Aucun validateur ne peut détecter une fuite de features non consignée en amont |
| 4.6 Dépendances | \`moving_block_interval\` : bootstrap par blocs d'origines, déterministe à graine fixée | Sensibilité de taille des blocs, non-stationnarité et comparaisons multiples encore ouverts |
| 4.7 Gel confirmatoire | **No-Go**, absence de marché point-in-time qualifié et d'holdout réservé ; design ouvert | Ne pas présenter le percentile bootstrap comme p-value de découverte |

## Résultats techniques démontrés

Tests artificiels qui forcent un gain connu de 0,8 unité de prix
pour un actif et 120 pour un autre. Les résultats doivent
rester **distincts**, avec une amélioration relative de 80 %
pour chaque actif. Le code refuse une ligne dupliquée
plutôt que de compter deux fois la même origine.
Les fenêtres dont les cibles se recouvrent sont marquées.

Un intervalle bootstrap par blocs répète des tirages de séquences
contiguës, et non des points supposés indépendants. Les tests
dérivent un intervalle dégénéré sur un gain artificiel constant :
c'est une preuve d'implémentation, **pas** une preuve de robustesse
aux changements de régime.

## Reproduction

~~~bash
python -m pip install 'numpy==2.3.5'
python -m unittest discover -s research/benchmark_synthetic -p 'test_*.py' -v
~~~

Lire \`.github/workflows/trame-benchmark.yml\` pour la CI.

## No-Go scientifique : étapes 5 à 7

**Étape 5, entraînement financier réel**, reste bloquée :
- Sélection de sources et droits approuvés (étape 3.6).
- Partition train/développement légalement et temporellement justifiée.
- Budgets et témoins numériques comparables, choix de seeds et arrêt.
- Audit de causalité sur tous les prétraitements et features.

**Étape 6, généralisation**, attend d'abord un modèle financier
effectivement entraîné sur des corpus admissibles, puis des
régimes distincts et marchés nouveaux prédéclarés.
Une expérience synthétique AR(1) ne permet pas de tester
la généralisation sur crise bancaire, crypto ou inflation.

**Étape 7, test indépendant**, attend un registre de holdout
inviolé, règles de décision, métriques et seuils figés,
budget d'incertitude et audit externe. Aucune des observations
déjà explorées ou des fixtures répétées ne peut en tenir lieu.

Tenter malgré tout de livrer un moteur de prévision « prouvé »
violerait le programme scientifique.

## Produit alternatif licite et utile pendant ces blocages

Poursuivre en parallèle **l'étape 8 limitée à TRAME Research Lab
v0.1**, un atelier offline d'expériences synthétiques et de rapport
reproductible. Il ne doit **pas** être présenté comme
« TRAME Predictive v1 », ni accéder à API de négociation ni détenir
des fonds. Il peut être livrable **comme outil de recherche** avec
les méthodes et limites affichées en clair.

## Passage pour Codex

Branche \`chatgpt/paired-benchmark-sandbox-20261025\` empilée
sur la PR #5 de qualité des données. L'outil \`bootstrap.py\`
est autonome pour les fixtures et réutilise volontairement le
schéma de la PR #1. Ne pas merger en éclasant cette PR historique.
