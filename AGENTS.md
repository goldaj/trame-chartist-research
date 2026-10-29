> **Point de reprise unique au 29/10/2026 :** [PR #30](https://github.com/goldaj/trame-chartist-research/pull/30) et [docs/CONSOLIDATION_CODEX_20261029.md](docs/CONSOLIDATION_CODEX_20261029.md). Les pistes GPT6 A4/A5/A6/A8/P1-P4, CI initiale et S3.1A-G sont consolidées dans cette branche ; vérifier les CI du dernier SHA. Les archives des anciennes instructions conflictuelles sont dans `docs/merge-archive/`. Aucun modèle financier validé ni trading réel.

# ARRÊT VALIDÉ DU PROJET TRAME — 26/10/2026 : S3.1G TERMINÉE

**Point de reprise prioritaire pour Codex :** S3.1F terminée (PR #29 ; [run #40326818917](https://github.com/goldaj/trame-chartist-research/actions/runs/40326818917) 4/4 success). **S3.1G terminée scientifiquement** (PR #30 DRAFT ; [run #40329836255](https://github.com/goldaj/trame-chartist-research/actions/runs/40329836255) 4/4 success ; 9 modèles, 108 cellules de scores sur mêmes poids). L'issue #20 et `docs/CODEX_S3_1G_HANDOFF_20261026.md` sont à consulter AVANT tout changement.

**Rapport officiel ajouté :** `research/token_grammar/S3_1G_REAL_108_RESULTS_20261026.md`, avec tableau de justesse directionnelle + MAE prix et amplitude + persistance sur mêmes cas + source SHA, analyse et prochaine roadmap. Résultat NO-GO pour edge : les seuils q90 de magnitude prédite ne rendent pas le sens plus juste (BA D1 50,00%, H1 50,39%, M1 52,50%) malgré une couverture très faible 7,3/11,2/4,3%. SOFT peut diminuer MAE prix en contractant l'amplitude, mais ne prédit pas mieux le signe et dégrade la précision de magnitude.

**ARRÊT DEMANDÉ PAR LE PROPRIÉTAIRE** : achever documentation, lister suites, ne PAS relancer de campagne, ne PAS merger les PR draft, ne PAS ouvrir l'ancien dev 2022–25 ni holdout 2026. Les prochains jalons sont S3.1H audit calibration/robustesse, contrôle sampling M1, protocole confirmatoire figé, S3.2 nouvelles grammaires, S4 tailles × couches si justifié. Ne PAS agir sur Hyperliquid ni exposer secrets. Frais ignorés sur instruction, aucun PnL validé.

---

# TRAME S3.1G — sélection par grandeur prévue, PR #30 DRAFT (26/10/2026)

**Référence technique** :
`research/token_grammar/S3_1G_SELECTIVE_PROTOCOL_20261026.md`,
`research/token_grammar/selective_forecast.py`,
`research/token_grammar/selective_panel.py`,
`docs/CODEX_S3_1G_HANDOFF_20261026.md`.
[PR #30](https://github.com/goldaj/trame-chartist-research/pull/30)
enfant de #29 S3.1F. Aucune fusion automatique.

**S3.1F TERMINÉE** [Actions #40326818917](https://github.com/goldaj/trame-chartist-research/actions/runs/40326818917)
4/4 jobs, 9 vrais modèles BTC et 81
évaluations de règles sur mêmes poids ;
bilan/SHA dans `research/token_grammar/S3_1F_REAL_81_RESULTS_20261026.md`.
SOFT réduit très faiblement MAE du prix final
mais dégrade magnitude de 9,86–12,24%.
BA SOFT identique à HARD par construction.
Aucun edge ni profit prouvé.

**Question S3.1G** : à quelle fréquence
prédictions de forte amplitude sont-elles
mieux directionnellement et monétairement
calibrées ? Seuils 0/q50/q75/q90
estimés sur |prédiction HARD| TRAIN
seulement (retours labels connus avant
2020), puis appliqués MONITOR2020–21.
Score HARD/DIRECT/SOFT sur les MÊMES
cas sélectionnés ; couverture N
et classe vraie requises. Si N<30
ou classe manquante, BA=null.
Témoin persistance sur mêmes cases.
9 modèles réels D1/H1/M1×3 seeds
à 2000 updates, 4×3×9 =
108 cellules de mesure dépendantes,
pas 108 fits.

**Causalité** : ne pas réutiliser
ancien dev externe 2022–25 et
ne pas ouvrir test 2026 ; seuils
in-sample TRAIN (pas OOF) donc
toute conclusion exploratoire.
CI fixtures [vert #40329278603](https://github.com/goldaj/trame-chartist-research/actions/runs/40329278603),
smoke BTC [3/3 verts #40329375986](https://github.com/goldaj/trame-chartist-research/actions/runs/40329375986).
Campagne [#40329836255](https://github.com/goldaj/trame-chartist-research/actions/runs/40329836255)
en cours : NE PAS déclarer terminée
avant 4/4 jobs, panel, SHA archives.
Pas d'ordres Hyperliquid/PNL composé ;
frais ignorés par consigne utilisateur.
**Après S3.1G, arrêter de multiplier
les hypothèses sur MONITOR 2020–21.**

---

# DERNIER ÉTAT TRAME : S3.1F TERMINÉE, S3.1G PROCHAINE (26/10/2026)

**PR #29** `chatgpt/trame-s3-postprocess-ablation-20261026`
DRAFT fille de #28, pas de merge automatique.
[Actions #40326818917](https://github.com/goldaj/trame-chartist-research/actions/runs/40326818917)
**4/4 jobs SUCCESS**, 9 modèles BTC D1/H1/M1
réels à 2000 updates, 27 checkpoints,
**81 évaluations** de 3 règles de prix
sur les MÊMES poids. Code exécuté SHA
`58bc0f1e9425975a037ad2bf135943890a5b474b`.
Bilan scientifique complet et SHA des
rapports sources :
`research/token_grammar/S3_1F_REAL_81_RESULTS_20261026.md`.
Passation :
`docs/CODEX_S3_1F_HANDOFF_20261026.md`.
Archive des cinq JSON/MD + manifest
dans `trame_s3_1f_9_models_81_evaluations.zip`
disponible dans conversation.

**SOFT tanh** réduit MAE du prix
contre HARD (D1 282,704→280,707 ;
H1 54,611→54,511 ; M1 8,368→8,337 bps)
mais **aggrave l'erreur d'amplitude**
de 9,86–12,24%. La BA SOFT = HARD
PAR CONSTRUCTION, même signe logit.
Le retour mu direct n'améliore pas
le sens ni le prix. SOFT bat la
persistance de ~0,04–0,12% de MAE
mais sans test indépendant ni
robustesse temporelle. **NO-GO EDGE**.

**Nouvelle question S3.1G** :
l'utilisateur privilégie simultanément
justesse direction ET précision du
montant, et suppose qu'un trader
peut décider de ne pas agir si
l'amplitude prédite est trop faible.
Préenregistrer une étude **de
sélection d'observations par
magnitude prédite**, avec seuils
calculés sur TRAIN uniquement,
nombre/couverture, BA du sens,
MAE prix USD/bps, erreur amplitude,
Brier/monoclasse et persistance
sur mêmes cas. Ne jamais choisir
un seuil en fonction des résultats
MONITOR 2020–21. **2022–25 vieux
DEV déjà surexploré ; 2026 holdout
réservé**. Aucune preuve de profit,
pas d'ordres Hyperliquid, frais
ignorés conformément aux instructions.

---

# TRAME S3.1F EN COURS — PR #29, 26 OCTOBRE 2026

**Source de vérité** : [PR #29](https://github.com/goldaj/trame-chartist-research/pull/29)
`chatgpt/trame-s3-postprocess-ablation-20261026`
enfant de #28 S3.1E, pas de merge automatique.
`research/token_grammar/S3_1F_INFERENCE_PROTOCOL_20261026.md`
**PRÉENREGISTRÉ avant tout BTC réel**, et
`docs/CODEX_S3_1F_HANDOFF_20261026.md`.
Étude S3.1E précédente COMPLETÉE :
[27 fits et 81 observations, 4/4 jobs réussis](https://github.com/goldaj/trame-chartist-research/actions/runs/40318969005).
S3.1E avait révélé des désaccords entre les deux têtes
D1 7,9%, H1 19%, M1 26,7%, sans gain hard-price robuste.

**S3.1F isole le PRICING POST-PROCESSING**
sur un **SEUL modèle par seed/horizon** :
`joint_hard` (historique, signe logit×abs(mu)),
`signed_direct_mu`, `joint_soft_tanh`.
Nombre RÉEL d'entraînements **9** =
D1/H1/M1 ×3 seeds, checkpoints
200/800/2000 = **27 modèles-en-checkpoint**,
trois règles = **81 évaluations DÉPENDANTES**.
D1/H1/M1 spot Bitstamp public versionné ;
TRAIN labels avant 2020, MONITOR 2020–21,
ancien DEV 2022–25 et 2026 non consultés.
Même backbone, mêmes poids, G2 et loss legacy
que S3.1E ; tests exacts contre legacy et
`forecast_prices` historique.
BA direction ET MAE prix USD/bps ET amplitude
comme critères centraux, persistance témoin.
Brier est la qualité du logit, PAS la probabilité
de direction de la règle direct_mu.

**CI fixtures verte** [#40326446195](https://github.com/goldaj/trame-chartist-research/actions/runs/40326446195),
smoke réel [#40326446278](https://github.com/goldaj/trame-chartist-research/actions/runs/40326446278)
3/3 jobs verts.
Campagne complète [#40326818917](https://github.com/goldaj/trame-chartist-research/actions/runs/40326818917)
**lancée, pas encore vérifiée 4/4** au moment
de cette mise à jour ; ne déclarer résultat
qu'après panel final et SHA des artefacts.
Aucun ordre ou trading Hyperliquid, pas
de PnL inventé, frais ignorés selon user.

---

# ACTUALITÉ TRAME S3.1E TERMINÉE → S3.1F NEXT (26/10/2026)

**S3.1E complète** [Actions #40318969005](https://github.com/goldaj/trame-chartist-research/actions/runs/40318969005)
4/4 jobs SUCCESS, 27 vrais BTC fits /81
checkpoints, D1/H1/M1. Code SHA :
`73b56883dd09b3ad533aeeb4546eb1d402f2c003`.
Bilan scientifique et SHA256 des 5
fichiers de recherche :
`research/token_grammar/S3_1E_REAL_81_RESULTS_20261026.md`.
Passation `docs/CODEX_S3_1E_HANDOFF_20261026.md`.
**PR #28 DRAFT** fille de PR #27,
aucun merge automatique.

**La méthode SOFT ne prouve aucun gain
du cours HARD réellement servi.**
À 2000 updates legacy D1 BA52,24%
MAE prix282,704bps, H1 BA51,93%
MAE54,611bps, M1 BA53,02%
MAE8,368bps. Sur `reconciled_100`,
un petit gain BA/amplitude D1 est payé
par une hausse MAE prix à 285,563bps.
H1/M1 BA ou MAE prix se détériorent.
Désaccord entre signes des têtes
sur legacy D1 7,9%, H1 19% et M1 26,7%.

**Priorité S3.1F : isoler le postprocessing**
à poids exacts constants entre
`joint_hard`, `signed_direct_mu`,
`joint_soft_tanh` afin de savoir si
la combinaison des deux têtes est
la source du mauvais MAE final.
Préenregistrer avant les résultats,
ne pas choisir un « gagnant » sur
2020–21 comme confirmation indépendante.
BTC spot Bitstamp historique public
SHA contrôlé, TRAIN avant 2020,
MONITOR 2020–21, dev externe
2022–25 non consulté, 2026 gelé.
Tous tableaux sens ET montant et
amplitude ; aucune transaction,
aucun wallet, aucun PnL composé,
frais ignorés selon utilisateur.

---

# TRAME DERNIÈRE BRANCHE S3.1E : PR #28 DRAFT, 26/10/2026

**Précédent S3.1D TERMINÉ** [run #40313075915](https://github.com/goldaj/trame-chartist-research/actions/runs/40313075915)
4/4 jobs OK, 45 trajectoires /135 checkpoints
BTC spot D1/H1/M1. Bilan et SHA :
`research/token_grammar/S3_1D_REAL_135_RESULTS_20261026.md`.
L'erreur amplitude s'améliore si on renforce la
loss magnitude mais l'erreur **du prix réellement
prédit** et souvent la BA se détériorent.
Aucun edge direction/prix/AMP simultané.
Ne pas réexécuter S3.1D inutilement.

**NOUVELLE QUESTION S3.1E**, [PR #28](https://github.com/goldaj/trame-chartist-research/pull/28),
branche `chatgpt/trame-s3-reconciliation-loss-20261026`
empilée sur PR #27, pas de merge auto :
comparer sur backbone **identique 2418 params**
la loss S3.1D historique et 0,25/1,00
de Huber supplémentaire sur un surrogate
`tanh(logit/2)*sqrt(mu²+1e-12)`.
L'inférence conserve le HARD sign(logit)*abs(mu).
**Le SOFT est seulement différentiable et
n'est PAS le cours réellement prédit**.

**Protocole PRÉENREGISTRÉ** :
`research/token_grammar/S3_1E_RECONCILIATION_PROTOCOL_20261026.md`,
passation `docs/CODEX_S3_1E_HANDOFF_20261026.md`.
CI synthétique [run #40318703540](https://github.com/goldaj/trame-chartist-research/actions/runs/40318703540)
vert, pilote vrai 9 trajectoires
[run #40318703968](https://github.com/goldaj/trame-chartist-research/actions/runs/40318703968)
3/3 jobs verts. **Campagne complète**
[run #40318969005](https://github.com/goldaj/trame-chartist-research/actions/runs/40318969005),
27 véritables trajectoires/81 observations,
NE PAS déclarer réussie avant 4/4 jobs
et analyse des SHA/artefacts.

TRAIN BTC labels connus avant 2020,
MONITOR interne 2020–21, dev externe
2022–25 **interdit** pour tuning,
2026 holdout **fermé** ; pas d'ordres,
transactions, API Hyperliquid ni PnL
composé. L'utilisateur ignore les frais.
Toutes conclusions doivent fournir
BA sens, MAE USD/bps du prix HARD
réellement servi, erreur amplitude,
Brier, monoclasse, désaccord des têtes
et baseline persistance.

---

# TRAME S3.1D TERMINÉE / S3.1E PROCHAINE (26/10/2026)

Dernier état vérifié : **S3.1D 45 trajectoires
BTC RÉELLES / 135 checkpoints et 4/4 jobs
réussis**, [Actions #40313075915](https://github.com/goldaj/trame-chartist-research/actions/runs/40313075915),
Git SHA réel `5726cb99c0bcfef59509bf2b4884a7e1bf7036cc`.
**PR #27** draft fille de #26, aucun merge auto.

**Bilan scientifique complet, sources JSON et SHA256** :
`research/token_grammar/S3_1D_REAL_135_RESULTS_20261026.md`.
**Passation** :
`docs/CODEX_S3_1D_HANDOFF_20261026.md`.
**Historique échanges** :
`docs/CHATGPT_PROJECT_HISTORY.md`.
D1/H1/M1 ×5 losses ×3 seeds, modèle identique
width16/depth1 2418 params, G2 signée, 2000 updates,
checkpoints 200/800/2000. TRAIN labels <2020,
MONITOR 2020–21, **ne pas toucher le dev
externe 2022–25 ni le holdout 2026**.

Résultats à 2000 updates : référence BA
D1 52,24 / H1 51,93 / M1 53,02 % ;
`magnitude_100` réduit l'erreur
d'amplitude de 16–21% mais détériore le
MAE prix final 6–10% et le sens.
Aucun gain robuste conjoint, Brier
skill faible, même le MAE référence
moins bon que persistance simple à
2000 sur D1/H1/M1. **NO-GO trading**.

**Prochaine hypothèse : S3.1E cohérence des
deux sorties** : étudier le désaccord
direction de `mu` et `sigmoid(logit)`,
puis tester loss alignée sur le **prix
réellement reconstruit** sans modifier
architecture, G2, splits ni budgets.
Protocole préenregistré, tests d'abord
artificiels, pas d'accès 2022–25/2026.
Frais exclus par consigne, aucune
transaction, secret, wallet ou
modification du bot Hyperliquid.

---

# DERNIÈRE BRANCHE TRAME : S3.1D LOSS DIRECTION vs AMPLITUDE (26/10/2026)

**PR #27 DRAFT** `chatgpt/trame-s3-objective-ablation-20261026`,
enfant de PR #26 S3.1C **déjà terminée et documentée**.
Ne pas fusionner automatiquement.

**SOURCE DE VÉRITÉ** :
`research/token_grammar/S3_1D_LOSS_PROTOCOL_20261026.md`,
`docs/CODEX_S3_1D_HANDOFF_20261026.md`,
`research/token_grammar/loss_ablation.py`,
`research/token_grammar/loss_ablation_panel.py`,
tests `test_loss_ablation*.py`.

- S3.1C initialement « interrompue » était en fait
  **DÉJÀ TERMINÉE** :
  [Actions #40309653884](https://github.com/goldaj/trame-chartist-research/actions/runs/40309653884),
  4/4 jobs, 27 trajectoires, 81 mesures.
  Ne plus rouvrir ou dupliquer cette expérience.
  Les fichiers de duplication ont été supprimés.
- Le lecteur S3.1C emploie maintenant
  `stop_labels_before` pour **arrêter avant
  toute bougie de 2022**, au lieu d'ignorer
  simplement les labels, sans changement
  des anciennes sorties par défaut.
- S3.1D teste cinq coefficients de loss
  strictement **sur le même modèle/grammaire
  G2/20 retours passés, même SHA initial**
  sur D1/H1/M1. Labels TRAIN connus avant 2020,
  MONITOR seulement 2020–21. Ancien dev externe
  2022–25 **interdit** ; 2026 gelé.
- Matrice : 3 horizons ×5 losses ×3 seeds =
  **45 trajectoires**, mêmes optimisateurs
  continus jusqu'à 2000 updates, observés
  à 200/800/2000 = **135 checkpoints**.
  Direction BA, MAE prix USD/bps, erreur
  amplitude bps, Brier et monoclasse sont
  des critères SIMULTANÉS.
- Ancien smoke a échoué sur **argparse
  doublon --checkpoints** AVANT l'apprentissage.
  Bug corrigé, test CLI --help ajouté.
  Relance [smoke #40312924527](https://github.com/goldaj/trame-chartist-research/actions/runs/40312924527),
  complet [#40313075915](https://github.com/goldaj/trame-chartist-research/actions/runs/40313075915).
  **Vérifier leur succès effectif avant de
  prétendre disposer de résultats S3.1D**.
- Aucune validation indépendante ni
  stratégie profitable, aucun PnL composé
  et aucun ordre Hyperliquid. Frais
  volontairement ignorés sur instruction.
  BTC spot historiques publiables avec
  attribution et SHA ; aucun secret/compte.
- Historique des demandes du propriétaire
  et opérations réelles :
  `docs/CHATGPT_PROJECT_HISTORY.md`.

---

# S3.1C COMPLET — OBSERVER LA CONVERGENCE AVANT NOUVEAU SCALING

PR #26 `chatgpt/trame-s3-training-dynamics-20261026`,
base PR #25. Run officiel
[Actions #40309653884](https://github.com/goldaj/trame-chartist-research/actions/runs/40309653884)
**4/4 jobs réussis** : 27 trajectoires
réelles BTC D1/H1/M1, 3 checkpoints
200/800/2000 chacune = 81 évaluations
internes, et panel validé.

**SOURCE** :
`research/token_grammar/S3_1C_REAL_81_RESULTS_20261026.md`
contient les 27 groupes de scores direction,
MAE USD/bps, erreur amplitude, %UP,
monoclasse, Brier et provenance SHA des
JSON ; `docs/CODEX_S3_1C_HANDOFF_20261026.md`
contient le protocole/références.

**NOUVELLE RÈGLE DE RECHERCHE**
S3.1C évite le dev externe 2022–25
déjà surutilisé. Ajuster avec uniquement
TRAIN interne <2020 et monitor interne
2020–21, 2026 TOUJOURS gelé. Les
moniteurs ne participent JAMAIS aux
gradients, quantiles ou normalisateurs.

**OBSERVATION** : prolonger 200→2000
updates améliore H1/M1 sur certaines
métriques directionnelles, mais
dégrade D1 et/ou l'erreur d'amplitude
M1 ; random mono s'améliore H1/M1
mais reste 2/3 mono sur D1. Pas
de budget ni tokenizer gagnant
universel, pas d'edge financier.

**PROCHAINE ÉTAPE S3.1D (backlog #20)** :
étude indépendante préenregistrée de la
loss direction vs magnitude. Ne PAS
changer loss, taille, horizon et grammaire
simultanément. Toujours BA ET montant
USD/bps et Brier, pas de PnL cumulé.
Aucun merge auto, aucun secret/trading,
frais ignorés selon utilisateur.

---

# S3.1C CONVERGENCE INTERNE — PRIORITÉ ACTUELLE 26/10/2026

Branche `chatgpt/trame-s3-training-dynamics-20261026`,
**PR #26 DRAFT**, enfant de #25 (S3.1B 432 fits).
Avant modification lire
`docs/CODEX_S3_1C_HANDOFF_20261026.md`,
`research/token_grammar/S3_1C_CONVERGENCE_PROTOCOL_20261026.md`,
`research/token_grammar/S3_1B_REAL_432_RESULTS_20261026.md`
et issue GitHub #20. Aucune fusion automatique.

**Objectif scientifique** : comprendre les sorties
monoclasse et la convergence des prédictions de
direction ET amplitude avant d'investir dans
gros modèles/vector embeddings. L'ancien
DEV 2022–2025 a été sur-exploré :
**NE PAS le réutiliser pour choisir 200/800/2000 updates.**

S3.1C sépare le seul TRAIN PRÉ-2022 historique
en réservoirs indépendants :
- TRAIN label disponible <2020-01-01,
  seule source gradients, normalisation
  et quantiles signés G2, prior et baselines ;
- MONITOR label disponible 2020–21,
  aucune mise à jour ni fitting ;
- 2022–25 dev externe **non consulté** ;
  2026 holdout **jamais ouvert**.

Pour les trois horizons BTC Bitstamp public
D1/H1/M1, G2 quantiles signés,
3 bras decoded/embedding_ordered/random,
3 seeds, width16/depth1, loss Joint,
**27 vraies trajectoires** évaluées à
**200/800/2000 updates** = 81 observations.
Le même optimiseur continue après chaque
checkpoint ; ne pas prétendre 81 entraînements
indépendants. Instrumenter gradients préclip,
loss TRAIN/monitor, BA accuracy direction,
%UP et monoclasse, MAE USD/bps, erreur
amplitude bps, Brier vs prior train-only.
+11 paramètres pour learned vs decoded,
ordered-v-random égalité de capacité.

Code `research/token_grammar/convergence.py`,
`convergence_panel.py`, tests adversariaux.
CI synthétique verte et run réel
[Actions #40309653884](https://github.com/goldaj/trame-chartist-research/actions/runs/40309653884).
**Vérifier les 3 jobs et l'agrégateur**
avant de déclarer le travail fini. Les
résultats D1/H1 en interne 2020–21
montrent déjà que prolonger l'entraînement
n'a pas d'effet uniforme ; rien de
confirmatoire sur 2026 ni d'edge financier.

Les historiques BTC spot sont publics
avec attribution source; aucune clé,
wallet ou compte. Frais ignorés par
l'utilisateur ; aucun trade ni PnL
cumulé validé, aucun bot Hyperliquid touché.

---

# S3.1B RÉSULTATS OFFICIELS — 26/10/2026

PR **#25** `chatgpt/trame-s3-learned-embeddings-20261026`,
sur PR #24 S3.1A. **432 vrais fits
D1/H1/M1 TERMINÉS** [Actions #40306642813](https://github.com/goldaj/trame-chartist-research/actions/runs/40306642813),
**4/4 jobs verts**, modèle Git SHA
`5ac86805aceec952d92424fb1cf679355773de99`.
**Rapport complet direction + précision montants
USD/bps + amplitude + biais monoclasse**
dans `research/token_grammar/S3_1B_REAL_432_RESULTS_20261026.md`
avec hashes des 5 fichiers JSON/MD.

Protocole préenregistré `S3_1B_PROTOCOL_20261026.md`.
Les embeddings **scalar trainables** 11 catégories
G1/G2 ajoutent +11 paramètres vs decoded :
capacité NON égalisée sur learned-v-numeric ;
ordered-v-random strictement mêmes paramètres.
**Conclusion NO-GO** sur supériorité nette.
Random init donne souvent monoclasse H1 G2
joint 11/12 vs ordered/decoded 0/12,
la BA reste ~50%, erreurs prix/amplitude
donnent compromis, pas de gain de trading.

**Prochaine étape S3.1C** (issue #20) :
préenregistrer tests de convergence
200/800/2000 updates, gradient/loss
sur mêmes cohortes, trois horizons,
stabilité du sens et de l'amplitude,
sans ouvrir 2026. Ne pas lancer de grands
embeddings avant de diagnostiquer la
dynamique d'entraînement.
Lire `docs/CODEX_S3_1B_HANDOFF_20261026.md`,
`docs/CHATGPT_PROJECT_HISTORY.md`,
`research/data/PUBLIC_DATA_README_20261026.md`.
Pas de merge automatique, pas de clé/compte,
aucun ordre Hyperliquid, frais ignorés.

---

# S3.1A CONFIRMÉE (26/10/2026) — 288 FITS TERMINÉS

Le [run #40300156418](https://github.com/goldaj/trame-chartist-research/actions/runs/40300156418)
a officiellement **réussi 4/4 jobs** :
3 ×96 vrais entraînements BTC Bitstamp
D1/H1/M1 (3 graines, 200 steps) et panneau
comparatif complet (**288 fits, 72 groupes
appariés, 24 lignes de synthèse**).

**RECHERCHE** : pas de gain directionnel
et d'amplitude robuste simultané,
beaucoup de modèles monoclasse ;
H1 Joint G2 51.40% BA / 34.154 bps
MAE vs continu 51.14% /34.490,
mais amplitude absolue G2 30.136
vs continu 28.753. Aucun edge prouvé.

**Passation S3.1A** :
`research/token_grammar/S3_1A_REAL_288_RESULTS_20261026.md`,
`docs/CODEX_S3_1_HANDOFF_20261026.md` ;
PR #24 draft. Le prochain travail S3.1B
doit évaluer de **vrais embeddings appris**
avec budget modèle apparié, protocole
nouveau préenregistré, CI et 2026 gelé.
Aucun frais selon consigne, pas de
transactions live ni Hyperliquid.

---

# DERNIÈRE ÉTAPE : S3.1A GRAMMAIRES SUR BTC RÉEL (26/10/2026)

**PR #24** `chatgpt/trame-s3-predictive-grammars-20261026`,
base PR #23 source BTC publique. Voir
`docs/CODEX_S3_1_HANDOFF_20261026.md`,
`research/token_grammar/PREDICTIVE_PROTOCOL_20261026.md`
et [issue #20](https://github.com/goldaj/trame-chartist-research/issues/20).

- **S3.1A déjà testée sur cours réels** :
  D1/H1/M1, 4 grammaires ×2 objectifs = **24 fits**
  avec une graine, width16/depth1, 40 updates.
  [Workflow #40299287171](https://github.com/goldaj/trame-chartist-research/actions/runs/40299287171),
  3/3 jobs verts et SHA JSON dans
  `research/token_grammar/S3_1_REAL_PILOT_RESULTS_20261026.md`.
- **Campagne complète mathématiquement correcte :
  288 fits, PAS 192** = 3 résolutions ×4 grammaires
  ×2 losses ×2 widths ×2 depths ×3 seeds
  = 96 / horizon. Workflow
  `.github/workflows/trame-s3-predictive-288.yml`,
  [run #40300156418](https://github.com/goldaj/trame-chartist-research/actions/runs/40300156418).
  **NE PAS prétendre à la réussite tant que les 3 jobs
  ET l'agrégateur final ne sont pas terminés.**
  Ancien workflow mal dimensionné 192 retiré,
  résultat inutilisable.
- Code `research/token_grammar/predictive.py` :
  G0b continu, G0a arrondi, G1 bins fixes signés,
  G2 bacs quantiles fit sur TRAIN uniquement.
  Les tokens G1/G2 sont **DÉCODÉS en scalar bps**
  pour le même backbone S2b ; ceci **n'évalue PAS**
  un embedding de token appris (S3.1B future).
- Même seed, init SHA256, 20 pas passés, cible,
  loss, mini-batches, échelles d'entrée et cible
  TRAIN continu ; le tableau `predictive_panel.py`
  rejette groupes incomplets/décalés.
  Balanced direction accuracy, taux UP,
  MAE USD et bps, erreur d'amplitude bps,
  Brier skill des vrais logits entraînés,
  monoclasse ≥99%, pas de PnL cumulé.
- Les pilotes restent dominés par scores ~50%
  et sorties monoclasse, notamment H1.
  D1 G1 joint a BA 52.83% mais se dégrade
  sur erreur de magnitude absolue vs continu ;
  pas d'edge prouvé, encore moins de généralisation.
- Source BTC Bitstamp spot publique versionnée/vérifiée
  par SHA, 2026 GELÉ pour train/dev, D1 public 2012+,
  aucune clé/compte/wallet. Frais ignorés selon
  consigne, aucun ordre ni bot Hyperliquid modifié.
- Prochaine étape S3.1B : véritables token embeddings
  et décompositions signe/magnitude, après rapport
  288 fits, **préenregistrer avant expérimentation**.
- Tracer l'historique brut des demandes disponibles
  dans `docs/CHATGPT_PROJECT_HISTORY.md`.
  Pas de fusion automatique des PR empilées.

---

# DERNIÈRE PREUVE TRAME, 26/10/2026 : 144 ESSAIS PUBLICS RÉELS FINIS

**Contrôle réussi :** [GitHub Actions #40296933559](https://github.com/goldaj/trame-chartist-research/actions/runs/40296933559)
a exécuté **144 entraînements S2b réels** sur les
cours BTC/USD SPOT publics D1/H1/M1
(3 résolutions × 2 encodages × 2 objectifs
× 2 largeurs × 2 profondeurs × 3 seeds).
**Trois jobs sur trois réussis**, 200
mises à jour chacun ; modèle public SHA
`2c9a3bab9d274852564abe6c70042a1145e6193c`.

Détails scientifiques et SHA des JSON dans
`research/data/S2B_REAL_PUBLIC_144_RESULTS_20261026.md`.
**NO-GO** sur toute affirmation « l'encodage
continu prédit mieux » : aucune supériorité
constante, énormes biais de classe, environ
50% balanced accuracy. Les pertes de signe
D1/H1/M1 de G0a dans l'historique passé
(2.86% / 13.74% / 64.26%) sont réelles
mais ne prouvent aucun avantage de prévision.

**NOUVELLE PRIORITÉ** : S3.1 issue #20,
comparaison *prédictive* des grammaires G1/G2
avec le retour continu G0b comme référence
à protocole, architecture, loss, seed
et fenêtre historique appariés.
Préenregistrer AVANT tout résultat. Travail
sur branche/PR distincte **sans merge automatique**.
Pas d'utilisation de 2026 pour entraîner,
tuner ou choisir un modèle. Pas de PnL
composé, pas de frais selon propriétaire,
aucune action Hyperliquid.

---

# AUTORISATION PUBLIC BTC / PR #23 — 26 OCTOBRE 2026

**Nouvelle décision utilisateur, PRIORITAIRE sur les anciennes notes
« pas de données BTC brutes dans TRAME » :** publier/intégrer les
**seules données historiques de prix Bitcoin** dans le dépôt TRAME
est autorisé. Citation utilisateur :
« si si tu peux les considérer publics, si tu prends les données
historiques btc c'est rien de grave ». Cette permission
**n'inclut aucun secret, portefeuille, clé, identifiant**
ou autre historique sensible ; respecter les
licences des tiers (voir `research/data/PUBLIC_DATA_README_20261026.md`).

**Preuve réelle :** D1 Bitstamp 2012–2026H1
(372096 octets, SHA Git identique) effectivement
committé sous `research/data/reference/`.
H1/M1 original gzip téléchargeable SANS jeton privé
depuis le GitHub amont public, SHA Git blob
vérifié par `python -m research.data.public_data`,
dans cache local (110+ Mo, non commit pour
éviter le gonflement du dépôt Git).

Les vrais workflows publics D1/H1/M1 ont
réussi [D1 #40295846917](https://github.com/goldaj/trame-chartist-research/actions/runs/40295846917)
et [H1/M1 #40296158821](https://github.com/goldaj/trame-chartist-research/actions/runs/40296158821).
Il existe **12 bras réels** (4 par horizon,
40 steps, 1 seed) de S2b et trois audits de
grammaires réels, aucun test de prédiction
indépendant, 2026 gelé. Voir
`research/data/REAL_PUBLIC_BTC_RESULTS_20261026.md`.
Un nouveau protocole 144 fits, 3 seeds, 200
updates est lancé (run #40296933559), vérifier
sa conclusion avant de déclarer terminé.

**Branche/PR :** `chatgpt/trame-public-btc-data-import-20261026`,
PR #23 basée sur PR #22 S3 → #21 S2b →
#19 S2 → #18 D1 → #17 S1. Aucune fusion
automatique. Anciennes limitations d'une
action GitHub privée ne sont **pas** une
interdiction scientifique de lire des
cours publics ; ne pas déduire l'absence
de résultats des restrictions de transport.

Limites : D1 2010–2011 indicatif et Bitstamp
2011H2 restent non committés pour licence
de redistribution insuffisamment établie ;
ils sont disponibles dans l'ancien cache
privé mais ne doivent pas être fabricés en
OHLCV. Comparer D1 2012+ vs ancien
D1 2011H2+ avec prudence (cohortes distinctes).
Aucun ordre Hyperliquid, frais de simulation
toujours ignorés sur décision utilisateur,
aucun score de portefeuille composé
présenté comme validé, année 2026
strictement hors sélection des modèles.

Codex doit commencer par
`docs/CODEX_PUBLIC_BTC_IMPORT_20261026.md`,
puis lire `research/data/REAL_PUBLIC_BTC_RESULTS_20261026.md`,
`research/representation_ablation/PROTOCOL_20261026.md`
et [issue #20](https://github.com/goldaj/trame-chartist-research/issues/20)
pour la future étude des grammaires, avant nouveau
gros scaling.

---

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
