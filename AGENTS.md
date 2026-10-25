# TRAME — périmètre indépendant

Cette recherche est séparée du bot Hyperliquid. Travailler ici pour les prochaines évolutions TRAME. Ne pas modifier, démarrer ni déployer le bot. Préserver protocoles gelés, versions et frontières train/validation/test. Aucun résultat prédictif ou modèle entraîné ne peut être déduit de la validation du codec. Ne pas ajouter de données brutes ou d'archives sans vérifier les droits de redistribution. Aucun secret ou journal de compte dans Git.


## Contexte conversationnel ChatGPT / passation Codex

Lire aussi **`docs/CHATGPT_PROJECT_HISTORY.md`** pour les échanges et décisions retrouvés. Ce journal est explicitement partiel ; ne jamais présenter un résumé comme un verbatim. À chaque changement de projet, ajouter les nouveaux échanges pertinents avec rôles Utilisateur/Assistant, texte exact et horodatages uniquement lorsqu'ils sont disponibles ; sinon noter la lacune. Préserver l'ensemble des règles et documents existants de ce dépôt et ne publier aucun secret.

## Travail expérimental parallèle du 25 octobre 2026

Lire `research/p1b0_numerics/README.md` avant de modifier la branche
`chatgpt/p1b0-numerical-lab-20261025`. Il s'agit de nouvelles
expériences **uniquement synthétiques**, non scellées : **ne pas**
déplacer les résultats de cette branche dans les audits historiques,
retoucher les calculs figés de 2026-10-14/16, ouvrir les holdouts
ou les présenter comme mesures prédictives. Le score CRPS fourni
porte sur des **prix fictifs** ; la tête numérique n'est pas un GPT
entraîné et la précision des queues sous-fluées reste une limite.

## Branche de qualification P1-B0 2026-10-25

Travail expérimental dépendant de la branche de PR #2 :
`chatgpt/p1b0-stage1-validation-20261025`.
La décision, les tests et les limitations sont dans
`research/p1b0_numerics/STAGE1_DECISION_20261025.md`.
En particulier, les tirages extrêmes **conditionnels** ne constituent
pas une preuve d'un sampler inconditionnel fidèle et le gradient nul
près d'une saturation de bornes est connu. **Ne pas fusionner cette PR
avant sa base**, réécrire des protocoles gelés, ou vendre des gains de
prévision avec les exemples artificiels.

## Etape 2 : mini-GPT synthétique (25 octobre 2026)

Lire `research/mini_gpt_synthetic/README.md`,
`research/mini_gpt_synthetic/data.py` et
`research/mini_gpt_synthetic/experiment.py` avant de modifier.
Branche dépendante `chatgpt/mini-transformer-synthetic-20261025`
reposant sur `chatgpt/p1b0-stage1-validation-20261025`.
Préserver la séparation stricte train/dev/test réservé. Ne **jamais**
ouvrir `reserved_synthetic_test` pour régler l'architecture. Ne
pas annoncer un gain de prédiction financière à partir de cette
expérience. La comparaison BASE/HIER/FLAT n'est **pas** égalisée
en capacité ou FLOPs ; mesurer avant d'en tirer une conclusion.

## Contrat de sources/versions historiques TRAME

Lire `research/market_data_contract/STAGE3_REPORT_20261025.md`.
La branche `chatgpt/point-in-time-data-contract-20261025` est
une étape de contrôle *avant* ingestion de marchés. Toutes les
sources réelles candidates sont volontairement `unverified` ; ne
pas changer cet état sans preuve d'utilisation/licence, d'horodatage
point-in-time et de provenance de téléchargement. Les fixtures
sont 100 % construites, sans prix réel. Ne pas confondre
`observed_at` et `available_at`.

## Etape 4 : pas de réinterprétation des pseudo-performances

Branche `chatgpt/paired-benchmark-sandbox-20261025` basée sur
`chatgpt/point-in-time-data-contract-20261025`. Lire
`research/benchmark_synthetic/STAGE4_REPORT_20261025.md`.
Un gain apparié synthétique ou son intervalle bootstrap
**n'est pas** un p-value confirmatoire et ne permet ni
fusionner des prix en devises différentes ni choisir un modèle
après consultation d'un holdout. Conserver le projet comme
laboratoire d'études tant que sources réelles non approuvées.

## Reprise TRAME Research Lab hardening (25 octobre 2026)

Branche `chatgpt/trame-lab-hardening-20261025` empilée sur
`chatgpt/trame-research-lab-v01-20261025` ; lire
`research/trame_lab/HARDENING_NOTE_20261025.md` et
`research/trame_lab/test_cli.py`. Les scores NLL sont également
affichés dans un tableau sémantique ; tests statiques seulement,
pas de validation lecteur d'écran ni de certification WCAG.
Contrôler 1 <= train_steps <= 200 et les métriques finies sans
changer les expériences synthétiques. Deux sorties HTML/JSON ne
sont pas encore garanties atomiques. Ne pas fusionner les branches
sans relire leurs bases, ne pas déverrouiller les sources réelles.
