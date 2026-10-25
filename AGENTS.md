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


## Nouvelle règle permanente : comparaison multi-architectures (2026-10-25)

L'utilisateur a explicitement demandé que **toutes les évolutions à venir**
de TRAME comparent aussi les architectures des LLM récents et d'autres
familles pertinentes, plutôt que d'assumer que le Transformer est optimal.
Lire obligatoirement `research/architecture_comparison/README.md`
et son registre avant chaque choix d'architecture, acquisition,
entraînement, validation, benchmark ou présentation de résultat.
Tout travail futur doit nommer ses bras inclus, les bras différés,
les contrôles et le statut de leur équité. Les comparaisons
inégales en FLOPs/capacité demeurent exploratoires. Mamba-2, Mamba-3,
hybrides, TimesFM-3, Chronos-2, Moirai-2 sont des candidats,
**non implémentés** dans le premier laboratoire. Ne jamais confondre
GRU avec Mamba ni une miniature GPT-style aléatoirement initialisée
avec un LLM actuel pré-entraîné. Préserver le holdout synthétique
et toutes les limites point-in-time du projet. Branche de travail :
`chatgpt/trame-multi-architecture-20261025`.


## A3a — nuance capacité vs coût

`research/architecture_comparison/experiment.py::choose_widths`
rapproche les comptes de paramètres de la référence, mais n'égalise
pas les FLOPs, les opérations GPU ni la latence. Les comparaisons
restent développement **artificiel**. Avant publication d'une
conclusion comparative, achever A3b (budget computationnel),
examiner plusieurs graines et valider sur des marchés admis
avec évaluation indépendante.


## A3b — audit CPU multi-tailles

Consulter `research/architecture_comparison/cost_audit.py`
et `test_cost_audit.py`. Les durées sur un CPU et petit corpus
synthétique ne sont **pas** des FLOPs, des latences trading,
ni des métriques de performance financière. L'étude de coût
inférence longue séquence, mémoire et égalité de FLOPs
reste à développer.


## Qualification externe obligatoire

Consulter `research/architecture_comparison/EXTERNAL_MODELS_ADMISSIBILITY_20261025.md`
avant d'installer un nouveau backbone ou des poids externes.
Mamba-3 (2026) rejoint Mamba-2. Les poids TimesFM 3.0 sont
**non commerciaux et non production** selon les conditions
vérifiées le 25/10/2026, distinctes de la licence du code.
Pas de package GPU dans la CI CPU commune et pas de sélection
d'un modèle zero-shot comme s'il avait été entraîné from scratch.


## BTC H1/M1 : nouvelle référence imposée par l'utilisateur (25/10/2026)

Lire research/btc_h1_m1/README.md avant tout travail de données BTC.
Le corpus de référence est désormais Bitstamp BTC/USD H1 et M1
(2012–juin2026), sous deux artefacts du run GitHub Actions
40208291215 du bot Hyperliquid. Il remplace le projet d'adaptateur
D1 précédent, branche chatgpt/btc-history-bridge-20261025, qui
n'est PAS à fusionner ici. Aucune série réelle n'est encore
transférée dans TRAME : seule l'interface offline a été codée.

L'utilisateur accepte les archives telles quelles pour ses travaux
et ne demande pas un nouvel audit de provenance. Conserver leurs
octets, leurs noms et leurs attributions existantes. La plateforme
a bloqué les tentatives de copie directe d'un dépôt privé vers un
dépôt public. L'utilisateur peut copier les deux artefacts
manuellement, sans modifier les .csv.gz.

La nouvelle expérimentation utilise les données en streaming,
ignore les bougies à volume nul et les ruptures temporelles,
préserve la quarantaine 2026 et compare exactement les mêmes cas
pour Transformer causal, mini-GPT-style et GRU. Il faut toujours
bien distinguer le forecast à une minute du forecast à une heure.
Ne pas entraîner une seule architecture puis prétendre que la
comparaison multi-modèles demandée est faite. Mamba-2/Mamba-3
et fondations chronologiques restent prévus mais non implémentés.

Le CSV synthétique de CI ne compte pas comme une vraie donnée.
Ne pas annoncer des scores financiers réels avant la copie
effective et une campagne exécutée sur les archives. Aucun
déploiement ni lien au moteur de trading Hyperliquid.
