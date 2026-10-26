# ÉTAPE S3.0c : GRAMMAIRES, DIAGNOSTIC UNIQUEMENT (26/10/2026)

Le propriétaire a demandé de poursuivre TRAME et de préparer
différentes « grammaires de courbes », manière de convertir
des mouvements BTC en tokens. La priorité de cette branche
**S3.0c** est l'information **perdue avant tout entraînement**,
et non la prédiction elle-même.

- PR **#22** branche `chatgpt/trame-grammar-audit-20261026`,
  **sur PR #21** S2b, elle-même sur PR #19 S2.
- [Issue #20](https://github.com/goldaj/trame-chartist-research/issues/20)
  = backlog complet G0a/G0b/G1/G2/G3–G8.
- `research/token_grammar/ROADMAP_20261026.md`
  = calendrier. S3.0 maintenant, **S3.1 prédictif réel
  seulement APRÈS la première ablation S2/S2b réelle
  autorisée**, AVANT gros scaling.
- `research/token_grammar/audit.py` et `test_audit.py`
  : diagnostics d'encodage sur 20 rendements passés
  d'une Case, vocabulaire quantiles TRAIN-ONLY,
  **aucun modèle entraîné**. Test CI synthétique
  `.github/workflows/trame-s3-grammar-audit.yml`.
- `docs/CODEX_S3_HANDOFF_20261026.md` est la passation
  actuelle. Les stats de tokens sont fortement
  **recouvrantes** ; les traiter comme 80k bougies
  indépendantes serait une erreur méthodologique.
- Aucun chiffre BTC réel S3 prétendu ; ancien blocage
  de sécurité de workflow privé S2 **toujours appliqué**,
  aucune tentative de contournement.
- D1/H1/M1, train <2022, dev 2022–25,
  2026 gelé, pas de fausses bougies OHLCV pour le
  D1 indicatif, pas de données privées dans ce repo.
  Les frais ne sont pas intégrés ; aucune simulation
  de PnL validé ni transaction ou bot Hyperliquid.
- Ne pas fusionner automatiquement les PR.

---

# S2b EN COURS — INSTRUCTION DU 26 OCTOBRE 2026

Le propriétaire demande de **continuer** le travail TRAME ;
la voie d'exécution privée S2 demeure non disponible après un
refus de sécurité. Continuer scientifiquement sans contournement :
**S2b ablation isolée de l'encodage d'entrée** compare
`continuous_bps` à `legacy_quantized_bps` en gardant
**cibles continues, loss, architecture, origine, graines,
batches et normalisation des ENTRÉES ET CIBLES communes,
fit sur les seuls retours continus du TRAIN**.

- PR #21, branche `chatgpt/trame-representation-ablation-20261026`,
  **basée sur PR #19 S2** ; pas de fusion automatique.
- Référence scientifique : `research/representation_ablation/PROTOCOL_20261026.md`.
- Code/tests : `runner.py`, `panel.py`,
  `test_ablation.py`, `test_panel.py`, `README.md`.
- Consignes Codex : `docs/CODEX_S2B_HANDOFF_20261026.md`.
- S3 grammaires toujours en
  [issue #20](https://github.com/goldaj/trame-chartist-research/issues/20) ;
  les résultats S2b doivent précéder le choix des grammaires
  réelles, avant un nouveau scaling coûteux.
- **144 fit BTC S2b ne sont PAS exécutés** ; les tests
  synthétiques n'indiquent ni puissance prédictive ni PnL.
  Le workflow privé S2 précédent a été bloqué par les
  contrôles de sécurité ; ne pas détourner ce refus.
- D1/H1/M1, train <2022, dev 2022–2025,
  test 2026 strictement gelé. D1 indicatif ne fournit
  aucune OHLCV fictive. Aucun accès/trade Hyperliquid.
  Les frais restent ignorés selon la demande.
- Vérifier CI au SHA courant AVANT de déclarer S2b
  qualifié, puis observer uniquement les résultats
  réellement disponibles.

---

# ROADMAP S3 / GRAMMAIRES — DEMANDE UTILISATEUR 26/10/2026

L'utilisateur confirme **continuer S2** et ajoute une hypothèse
d'importance élevée : réétudier la transformation des courbes BTC
en **tokens/grammaires**. Cette hypothèse est désormais suivie
par [l'issue #20](https://github.com/goldaj/trame-chartist-research/issues/20)
et documentée dans
`research/token_grammar/ROADMAP_20261026.md`.

**ORDRE FIXÉ** : S3.0 revue + diagnostic/reconstruction sur
fixtures synthétiques **maintenant**, S3.1 benchmark causal
des grammaires **après l'exécution réelle autorisée S2**
sur D1/H1/M1, **avant** de recommencer le gros scaling
ou d'autres architectures. Si S2 réel est bloqué par
sécurité, seules S3.0/docs/fixtures peuvent progresser ;
ne pas contourner un refus de sécurité, ni inventer
des mesures financières. S3.2–S3.3 grammaires
patch/OHLCV/événements/VQ/multirésolution seulement
si l'ablation initiale le justifie.

Le laboratoire `research/token_grammar/diagnostics.py`
et `test_diagnostics.py` mesurent uniquement pertes
de direction/magnitude et entropie de tokens sur nombres
**inventés** ; jamais la performance de prévision BTC.
Ne pas modifier le codec historique S1 ni remplacer les
retours continus S2 clandestinement.

Frais toujours ignorés sur décision utilisateur ;
direction ET précision du montant sont deux dimensions
obligatoires. Labels 2026 gelés, données privées séparées,
aucune exécution d'ordres ou modification Hyperliquid.
Codex doit consulter `docs/CODEX_S2_HANDOFF_20261026.md`
et l'issue #20 avant de modifier une architecture.

---

# PRIORITÉ DE REPRISE S2 — APRÈS INTERRUPTION (26/10/2026)

Consulter maintenant `docs/CODEX_S2_HANDOFF_20261026.md`
et `research/continuous_direction/PROTOCOL_20261026.md`
avec leurs addenda S2.1b/c. Le code a été renforcé :
témoin de probabilité train-only, Brier skill,
témoin d'amplitude drift train-only, empreintes des
origines ex ante, identification fiable du commit TRAME,
refus des sorties excessives, générateur de tableau
apparié `continuous_direction/panel.py`.
Les tests synthétiques sont vérifiés par
`.github/workflows/trame-s2-continuous.yml` ; vérifier
la **dernière** CI de PR #19 avant toute suite.

Toujours respecter D1/H1/M1, le gel 2026, les
frais ignorés sur demande, les résultats S1 archivés et
l'absence de commande de trading. S2 sur BTC réel
**n'a pas encore été exécuté** : ancien essai de
workflow privé refusé par contrôle de sécurité,
ne pas contourner ce refus. Les sorties S2
synthétiques ne valent pas des scores financiers.

---

# S2 ACTIF / ÉTAT EXACT — 26 OCTOBRE 2026

Après restauration et exécution vérifiée de D1/H1/M1, l'expérimentation
S1 a effectué 135 fits de scaling à une graine + 243 fits
à 200 updates/trois graines. Les résultats NE prouvent PAS de
gain directionnel : voir `research/scaling_study/S1_REAL_200UPDATES_20261026.md`.
L'absence de qualité n'autorise pas l'ouverture de 2026.

Branche S2 `chatgpt/trame-continuous-direction-20261026` (PR #19)
basée sur D1 PR #18. Objectif : distinguer l'effet d'un retour
d'entrée CONTINU de l'encodeur historique quantifié, avec régression
Huber seule contre régression Huber+BCE du sens. Lire obligatoirement
`research/continuous_direction/PROTOCOL_20261026.md`,
`research/continuous_direction/README.md`, et
`docs/CODEX_S2_HANDOFF_20261026.md`.

S2 **tests synthétiques verts**, mais **AUCUNE campagne réelle S2**
n'est encore exécutée. La création d'un workflow GitHub Actions
privé a été BLOQUÉE par des contrôles de sécurité. Ne jamais annoncer
de performances S2 réelles, contourner un blocage, copier des
cours privés dans TRAME ou intervenir sur Hyperliquid.
Frais de trading ignorés explicitement par l'utilisateur ;
aucune simulation de PnL de portefeuille ou passage d'ordre.
Aucun merge automatique des PR, et les labels 2026 restent exclus.

---

# URGENCE REPRISE D1 — NOUVELLE CONSIGNE UTILISATEUR (26/10/2026)

**Cette instruction supersède la priorité S1 qui suit** jusqu'à
complétion des étapes D1.1–D1.7 : inclure **D1** dans toute la recherche
basée sur la nouvelle release BTC, y compris les témoins Ridge/persistance,
trois architectures, régimes, justesse directionnelle/amplitude et matrice
S1 5 tailles×3 profondeurs. Conserver H1/M1 et les comparer à D1
à horizons explicites ; ne PAS comparer leurs NLL entre horizons.
Branche `chatgpt/trame-d1-parity-20261026` et PR #18 basée sur #17 ;
base initiale A7 #14 inchangée, pas de merge automatique.
Lire `research/btc_h1_m1/D1_RECOVERY_PLAN_20261026.md` et
`docs/CODEX_D1_HANDOFF_20261026.md`.

Le D1 2010–2011 est **indicatif close-only** ; ne jamais inventer de
bougies, de volume ou d'ordres. La cohorte OHLCV utilise le vrai
Bitstamp D1, le cut-off 2026 et train/dev historiques inchangés.
**Frais ignorés** sur décision du propriétaire ; direction et
ampleur restent métriques de premier plan. Ne jamais baptiser « edge
directionnel » le fait de toujours prédire la classe majoritaire.

---

# REPRISE AUTORISÉE S1 — NOUVELLE CONSIGNE UTILISATEUR 26/10/2026

**La pause/arrêt propre ci-dessous reste une archive de la session A7.**
Nouvelle instruction expresse : reprendre, documenter puis préparer et exécuter
un protocole **scaling × profondeur × direction/amplitude** en baby steps ;
continuer automatiquement après chaque sous-étape, annoncer chaque achèvement.
Expériences 5 tailles × 3 profondeurs (1/2/4) × 3 familles, H1/M1,
3 seeds minimum. Voir obligatoirement
[`research/scaling_study/PROTOCOL_20261026.md`](research/scaling_study/PROTOCOL_20261026.md)
et [`research/scaling_study/README.md`](research/scaling_study/README.md).
**Consigne additionnelle du 26/10 : ignorer TOUS les frais dans les
simulations ; importance majeure de la justesse directionnelle ET
du montant/amplitude prévu(e). Le trader décide seul de l'intérêt d'acheter.**
Ne pas présenter l'illustration brute par bougie comme PnL cumulé.
Les résultats de synthèse doivent conserver une précision directionnelle avec
couverture et erreurs d'amplitude en bps/dollars.

Branche de travail `chatgpt/trame-scaling-depth-direction-20261026`
**basée sur PR #14**. L'ancienne série #8/#9/#10/#14 et les branches
sœurs #11–#16 restent distinctes. 2026 est gelé. Aucun merge automatique,
aucun bot ni exécution live, aucun historique brut public.
Sur CI publique, utiliser uniquement des **fixtures fabriquées**.
Voir aussi `docs/CODEX_SCALING_HANDOFF_20261026.md`.
Ne pas interpréter la reprise S1 comme autorisant d'autres chantiers.

---

# TRAME — périmètre indépendant

Cette recherche est séparée du bot Hyperliquid. Travailler ici pour les prochaines évolutions TRAME. Ne pas modifier, démarrer ni déployer le bot. Préserver protocoles gelés, versions et frontières train/validation/test. Aucun résultat prédictif ou modèle entraîné ne peut être déduit de la validation du codec. Ne pas ajouter de données brutes ou d'archives sans vérifier les droits de redistribution. Aucun secret ou journal de compte dans Git.


## ARRÊT PROPRE DE SESSION — DERNIÈRE CONSIGNE (26/10/2026)

**Ordre utilisateur le plus récent : terminer l'analyse H1 des régimes,
mettre la recherche et la passation à jour, puis S'ARRÊTER.**
La session est clôturée après ces opérations ; l'ancien ordre général
de continuation permanente ne constitue **plus** une autorisation
de lancer des étapes supplémentaires sans nouvelle sollicitation.

L'état scientifique actuel est documenté dans
[`docs/CODEX_EXECUTION_BOARD_20261025.md`](docs/CODEX_EXECUTION_BOARD_20261025.md)
et dans
[`research/btc_h1_m1/A7_STATUS_20261025.md`](research/btc_h1_m1/A7_STATUS_20261025.md).
La [PR #14](https://github.com/goldaj/trame-chartist-research/pull/14)
porte les résultats réels exploratoires H1/M1 et les découpes
H1 par régime (développement 2022–2025 ; labels 2026 non ouverts).
Ne pas confondre ces runs avec une validation indépendante, des
FLOPs alignés ou une rentabilité financière ; ne pas modifier le
bot Hyperliquid.

**Règles Codex** : PR #8/#9/#10 forment la chaîne principale ;
#11 à #16 sont des branches sœurs empilées sur #10, et leurs
fichiers ne coexistent pas automatiquement. Deux PR privées
et une branche de régimes séparée contiennent les workflows
d'exécution sur les données privées. Ne jamais fusionner les
branches ou exposer les cours privés implicitement.

## REPRISE AUTORISÉE — consigne historique utilisateur (25/10/2026)

L'utilisateur a **levé la pause précédente** et demandé la reprise autonome
de TRAME comme programme de recherche et d'ingénierie, sous-tâche
par sous-tâche, avec information à chaque livraison. Le bloc
de pause historique du 25/10 est **supersédé** sur cette branche.

**Lire en premier [le tableau de bord actif](docs/CODEX_EXECUTION_BOARD_20261025.md)**
et [le protocole A3c](research/architecture_comparison/A3C_PROTOCOL_20261025.md).
Le document `docs/CODEX_REPRISE_TRAME_PAUSE_20261025.md` est conservé pour
l'historique, **pas** comme ordre d'arrêt actuel.

Première phase : A3c.1 à A3c.5, puis A4 Mamba-2/Mamba-3 ; feuille
de route A5–A8 et P1–P4 dans le tableau actif. Chaque sous-étape doit
avoir hypothèse, code, tests, preuves et limites. Ne jamais
déclarer « tout fini » lorsque des campagnes matérielles ou financières
n'ont pas réellement été exécutées. Pas de merge automatique,
pas d'ordre, pas d'accès aux secrets ni de modification du bot.

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


## BTC historique : source privée UNIQUE, versionnée (25/10/2026)

**Dernière décision de l'utilisateur : elle remplace les précédentes.**

Le référentiel commun à TRAME et au bot est désormais le dépôt PRIVÉ
goldaj/btc-historical-data, release tag exactement
btcusd-bitstamp-2010-2026-reference-v1 :
https://github.com/goldaj/btc-historical-data/releases/tag/btcusd-bitstamp-2010-2026-reference-v1

Contenu : 3 D1 (2010–2026), 1 H1 et 15 M1 (2012–2026),
MANIFEST.json et SHA256SUMS.txt, 21 release assets.
Les précédentes copies à partir du dépôt du bot Hyperliquid,
ou des deux artefacts temporaires GitHub Actions, sont abandonnées.
**Ne jamais committer les historiques de prix dans TRAME public.**
Il n'y a aucun accès automatique privé depuis la CI publique.

Lire research/btc_h1_m1/README.md puis release_store.py.
Utiliser l'authentification gh existante et l'acquisition explicite,
à la demande, de la release depuis le dépôt privé :
python -m research.btc_h1_m1.release_store --resolution H1 --download
(également M1, D1 ou ALL). Le cache versionné par tag se trouve
hors du clone Git, dans le dossier personnel/.cache/trame/bitcoin/.
Les octets téléchargés restent identiques aux assets de la release.
En présence d'un cache complet, ne PAS retélécharger à chaque lecture.
Éviter l'utilisation de jetons privés dans le dépôt, les logs ou les
GitHub Actions publics.

L'utilisateur a demandé de faire confiance aux données en l'état :
**pas de nouvelle vérification de provenance**. On conserve les
seules règles techniques nécessaires aux expériences : chronologie
causale, ruptures temporelles, bougies à volume nul, splits et gel.
Les résolutions D1/H1/M1 doivent être distinguées, et les premiers
prix indicatifs D1 ne sont pas de fausses bougies OHLCV.
Les données de marché BTC spot ne reproduisent pas les conditions
historiques d'exécution Hyperliquid.

Les trois backbones de TRAME restent des candidats de recherche et non
des gagnants démontrés. Mamba/SSM/fondations chronologiques doivent
être évalués selon le protocole multibras à terme. Aucune métrique
sur cours réel n'est déclarée tant qu'un run de recherche réel
n'est pas effectivement exécuté. Aucun ordre/live/trading.

La branche chatgpt/btc-h1-m1-20261025 succède à la branche D1
chatgpt/btc-history-bridge-20261025 abandonnée ; elle est empilée
sur la PR #8 multi-architectures. Ne pas merger aveuglément
les branches des expérimentations historiques.
