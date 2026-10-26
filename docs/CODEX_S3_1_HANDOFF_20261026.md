# Passation Codex TRAME S3.1A : quatre grammaires prédictives
Date : 26 octobre 2026. Branch
`chatgpt/trame-s3-predictive-grammars-20261026`,
**PR #24 DRAFT**, empilée sur #23 BTC PUBLIC,
#22 S3 diagnostic, #21 S2b, #19 S2, #18 D1.
Jamais de merge automatique.

## Requête à reprendre
L'utilisateur a demandé « continue, t'as crash »,
après confirmation d'une campagne S2b **réelle**
de 144 entraînements terminée le 26/10/2026,
et d'un backlog de grammaires d'encodage des
courbes. Le texte utilisateur exact et son
historique sont dans `docs/CHATGPT_PROJECT_HISTORY.md`.

## Ce qui est prouvé avant S3.1
- D1 CSV public réellement versionné ;
  H1/M1 reconstruits de 16 gzip amont PUBLICS,
  identité Git SHA vérifiée. Voir
  `research/data/PUBLIC_DATA_README_20261026.md`.
- S2b [run #40296933559](https://github.com/goldaj/trame-chartist-research/actions/runs/40296933559),
  3/3 jobs réussis, 144 fits (3 horizons ×2 codecs
  ×2 losses ×2 widths ×2 depths ×3 graines).
- Résultats et limites :
  `research/data/S2B_REAL_PUBLIC_144_RESULTS_20261026.md`.
  Continu n'est pas supérieur de façon constante ;
  équilibrée ~50%; nombreux modèles monoclasse.
- Grammaire historique G0a efface environ
  2.86% des signes non plats D1, 13.74% H1,
  64.26% M1 dans les contextes de dev.
  Ne pas confondre perte d'information connue
  et capacité prédictive de la future bougie.

## S3.1A préenregistrée avant résultats réels
Document :
`research/token_grammar/PREDICTIVE_PROTOCOL_20261026.md`.
G0b continu, G0a arrondi, G1 signe + bins fixes
et G2 signe + quantiles MAGNITUDE du TRAIN
uniquement. **Les tokens sont DÉCODÉS en
valeurs numériques avant l'input du backbone**.
Les embeddings appris relèvent de S3.1B
distinct ; aucune conclusion sur leur utilité
ne peut être tirée de S3.1A.

`research/token_grammar/predictive.py` utilise
`TrainOnlyGrammarFeatures` et réutilise
**sans modification de l'objectif** le
`run_cases` S2b via `feature_provider`
optionnel (S2b traditionnel identique sinon).
Mêmes cibles continues, mêmes 20 bougies
terminées, même mini-batches, seed,
initial weights SHA, même échelle input +
target calculée UNIQUEMENT sur TRAIN continu.
Test 2026 exclu, dev 2022–2025.

`test_predictive.py` teste invariance des
targets, indépendance des quantiles envers
dev, séquence exact G0a/G0b identique à S2b
et stabilité des poids initiaux.
`predictive_panel.py` et `test_predictive_panel.py`
rejettent un groupe incomplet, un SHA ou
scale de départ décalé, un doublon et
le label 2026. Compare direction accuracy,
balanced accuracy, MAE USD et bps, précision
d'amplitude absolue bps, proportion de
hausses prédites, têtes joint Brier skill
vs prior train-only, nombre de sorties
monoclasse ≥99%. Résumé inter-fits
exploratoire, PAS d'intervalle de confiance
sur observations temporelles indépendantes.

## Exécutions et statut (À VÉRIFIER)
- Fixtures CI :
  `.github/workflows/trame-s3-predictive-fixtures.yml`,
  lancer sous Python 3.12 + torch 2.10 CPU.
- Vrai pilote :
  `.github/workflows/trame-s3-predictive-canary.yml`,
  3×8=24 fits, 40 updates, width16/depth1
  et graine 20261026.
  Le **premier lancement a entraîné
  correctement mais un ASSERTION CI était
  incorrect** : il exigeait deux SHA initiaux
  alors que toutes les variantes de même
  width/depth/seed démarrent volontairement
  du même SHA. Assertion corrigée avant
  le second lancement. **Vérifier le run
  courant, ne PAS déclarer « succès » avant
  conclusion officielle des 3 jobs**.
- Campagne visée :
  **288 fits** (96 par horizon) D1/H1/M1×4 grammaires×2
  objectifs×2 largeurs×2 profondeurs×3 seeds,
  200 updates. Ne pas prétendre exécutée
  sans preuve des trois jobs et de leurs
  artefacts. Résultats uniquement sur
  développement, 2026 réservé.

## Commandes de reproduction
Depuis la branche #24 avec données installées
via `python -m research.data.public_data` :
~~~bash
python -m unittest research.token_grammar.test_predictive research.token_grammar.test_predictive_panel -v

python -m research.token_grammar.predictive \
  --interval D1 --directory research/data/reference \
  --data-origin BTC_PUBLIC_REAL \
  --steps 200 --seeds 20261025 20261026 20261027 \
  --widths 16 32 --depths 1 2 \
  --output /tmp/S3_1_D1.json
# Pour H1/M1, lire le cache public vérifié ;
# utiliser --interval H1 puis M1.
python -m research.token_grammar.predictive_panel \
  --inputs /tmp/S3_1_D1.json /tmp/S3_1_H1.json /tmp/S3_1_M1.json \
  --output /tmp/S3_1_PANEL.json --markdown /tmp/S3_1_PANEL.md
~~~

## Limites non négociables
- La priorité directionnelle du propriétaire
  inclut la **justesse en montant USD/bps** :
  ne jamais communiquer seulement la BA.
- Le pipeline ignore volontairement frais,
  aucun ordre de bourse ou modification
  du bot Hyperliquid, aucun PnL cumulé validé.
- **2026 gelé**. Ne pas exploiter
  les cibles/valeurs de 2026 pour calibrer
  les quantiles, choisir un tokenizer ou
  annoncer un succès indépendant.
- D1 public démarre 2012, pas 2011H2 ;
  garder provenance des cohortes distinctes.
- Ne pas appeler l'expérience embeddings
  de tokens : G1/G2 sont décodés en float
  pour que les paramètres soient IDENTIQUES.
- Faire S3.1B (embeddings réels + budget
  de paramètres apparié) seulement après
  analyse des résultats de S3.1A.
- Garder documents `AGENTS.md` et historique
  de la conversation à jour à chaque pas.
