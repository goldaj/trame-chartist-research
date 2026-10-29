# TRAME / Codex — passation S1 scaling × depth × direction
26 octobre 2026. Cette note est une passation **de recherche en cours**, pas un rapport de résultats BTC.

## Source de vérité / décisions utilisateur
- Reprendre après la clôture A7.5-H1 du 26/10 (l'arrêt ancien reste historique).
- Chercheur **et** ingénieur ; annoncer chaque sous-étape terminée et poursuivre sans validations intermédiaires.
- Décliner cinq tailles cibles (2.4k, 37k, 148k, 592k, 2.36M) avec trois profondeurs **1, 2 et 4 couches chacune**.
- Étudier le sens **et** le montant prévu. **Ne pas tenir compte des frais**. Le trader humain décidera de l'usage ; scores bruts par bougie échantillonnée ne sont pas un portefeuille.
- Garder le split A7 (train avant 2022 ; dev 2022–25 ; 2026 non ouvert), la release BTC privée et les branches existantes intactes.
- Aucun ordonnancement de trading, aucun transfert de prix privés dans TRAME, aucune PR fusionnée automatiquement.

## Statut au dernier commit de la branche
- S1.1 audit du code A7 et limites de l'encodeur : fait.
- S1.2 protocole S1 : `research/scaling_study/PROTOCOL_20261026.md`.
- S1.3 trois backbones multicouches : `models.py` avec formule `expected_parameters`, grille `capacity_grid`. Qualification synthétique à confirmer via CI.
- S1.4 direction+amplitude, classes flat comprises, strates train-only, deux témoins sans modèle et Ridge train-only : `metrics.py`. Qualification synthétique à confirmer via CI.
- S1.5 orchestrateur `runner.py` : origine explicite `ARTIFICIAL_FIXTURE` par défaut et `BTC_PRIVATE_REAL` exclusivement via `run_history`; même échantillon/batches/seeds ; pas d'ouverture 2026.
- S1.6 `test_scaling.py` / `trame-s1-scaling.yml` : contrôle de tests adversariaux et grille, **aucun cours réel dans la CI publique**.
- S1.7 campagne réelle : **non encore lancée** tant que la branche n'est pas qualifiée et qu'un runner privé n'exécute pas le script.
- S1.8 tableau résultat BTC : **non disponible**, ne pas inventer chiffres de sens ou de rentabilité.
- S1.9 validation indépendante et étude des régimes : non réalisées.

## Pièges identifiés
1. Le flux historique A7 quantifie les rendements log en entiers (échelle 1000). De minuscules variations M1 deviennent code 0. La direction cible est calculée sur **les vrais prix**, pas sur le code arrondi ; documenter cette limite.
2. La persistance a une MAE USD souvent très forte, mais direction « flat » toujours : ne jamais donner un « 50 % de justesse » inventé. La couverture directionnelle doit figurer à côté de l'accuracy conditionnelle.
3. Les seuils faible/moyenne/forte amplitude sont appris sur train, **sur la magnitude de prévision** sur dev ; ne pas utiliser ex post la taille du mouvement réel pour simuler un signal.
4. Les 270 entraînements sous 40 pas sont des pilotes de faisabilité **sous-entraînés**, pas une loi d'échelle. Poursuivre avec courbes d'apprentissage, budget total et comparaison hardware avant tout jugement.
5. `gross_signal_return_mean_bps_per_sample` **n'est pas** un rendement de portefeuille (observations échantillonnées, sans exposition temporelle continue, sans frais, sans rebalancing).
6. `compute_matched=False` partout ; comparaison à paramètres proches ne signifie pas coût/latence égaux.
7. GRU est un témoin récurrent, **pas Mamba**. Les PR #11–#16 sont parallèles, elles ne sont pas dans cette branche.

## Reprise technique ordonnée
1. Vérifier CI sur SHA de tête de PR S1 ; lire les logs et corriger tout échec réel.
2. Sur runner autorisé, commencer par `--plan-only`, puis canary H1 minimal ; enregistrer SHA du code, runner, env, source release, sortie JSON hash ; si échec, documenter et arrêter avant campagne.
3. Lancer matrice paramétrée H1, ensuite M1, sur le dépôt **privé** (workflow isolé, jeton temporaire seulement au téléchargement) ; conserver seulement données agrégées publiques.
4. Produire tableau : architecture, cible, largeur, profondeur, paramètres, seeds, train wall time, NLL, USD MAE, bps MAE, magnitude MAE, accuracy total / actif, couverture, balanced recall, strates de magnitude, témoin momentum et persistance, signaux bruts moyens sans frais.
5. Analyse par année/régime et dispersion, éventuellement protocole de signaux continus ; puis décider s'il faut une nouvelle campagne de convergence / scaling plus lourde.
6. Préserver le gel 2026 et l'ancien journal `docs/CHATGPT_PROJECT_HISTORY.md`, sans substituer un résumé à une transcription intégrale.

## Graphe de dépendances
- [PR #14 A7](https://github.com/goldaj/trame-chartist-research/pull/14) = base de cette branche.
- #14 basée sur #10, puis #9, #8. Les PR #11–#16 sont sœurs de #14 et **non** parties de la présente intégration.
- Source historique : dépôt **privé** `goldaj/btc-historical-data` release `btcusd-bitstamp-2010-2026-reference-v1`; ne pas refaire l'audit de provenance déjà accepté.
