# Codex — S3.1B embeddings de tokens BTC (26 octobre 2026)

## Origine et état vérifié
Reprise utilisateur verbatim : « t'as crash, continue »,
après S3.1A 288 fits réels achevés et documentés sur
[PR #24](https://github.com/goldaj/trame-chartist-research/pull/24).
Cette branche **PR #25 DRAFT** `chatgpt/trame-s3-learned-embeddings-20261026`
est **enfant de PR #24** (puis #23 BTC source publique,
#22 diagnostic, #21 S2b, #19 S2). Aucune fusion automatique.

S3.1A source scientifique :
`research/token_grammar/S3_1A_REAL_288_RESULTS_20261026.md`,
[Actions #40300156418](https://github.com/goldaj/trame-chartist-research/actions/runs/40300156418)
(4 jobs OK) :
**aucune preuve** d'amélioration conjointe du sens et
du montant, mais la quantification signée G2 réduit le
collapse monoclasse H1 Joint, **0/12 vs 6/12**,
pour une dégradation d'erreur amplitude.

## Nouveau protocole enregistré AVANT tout BTC S3.1B
`research/token_grammar/S3_1B_PROTOCOL_20261026.md`.
Deux grammaires avec 11 tokens signés : G1 fixe
ou G2 seuils magnitude fit sur TRAIN seulement ;
chaque grammaire reçoit TROIS bras :
- `decoded` : token ID décodé au centre bps,
  `ContinuousDirectionModel` S3.1A exact.
- `embedding_ordered` : vraie table
  `nn.Embedding(11,1)` **trainable**, initialisée
  au centre bps normalisé.
- `embedding_random` : même embedding et
  nombre de paramètres, mais initialisé
  aléatoirement (écart-type 0.25).

***Limite causale capitale*** : arms appris ont
**11 paramètres entraînables de PLUS** que
`decoded`. Le contraste `ordered` vs `random`
est exactement à capacité identique ; celui
learned vs decoded ne l'est PAS. Ces 11
paramètres sont signalés dans chaque run.
L'embedding est **scalaire** et non une grande
matrice d'embeddings vectoriels. Les
embeddings vectoriels/PatchTST restent
une expérimentation distincte ultérieure.

## Code et vérifications
- `research/token_grammar/learned_embeddings.py` :
  mapping ID 0 FLAT, 1..5 DOWN0..4,
  6..10 UP0..4; quantiles G2 fit TRAIN
  exclusivement, comparaisons via modèle
  S2b partagé, mêmes vrais labels futurs
  CONTINUS, même séquence mini-batches
  et même init des paramètres backbone
  SHA256, même std input/target calculée
  sur continu TRAIN, 20 retours historiques.
- `research/token_grammar/test_learned_embeddings.py` :
  l'ordered à l'instant initial est
  **numériquement identique** à la branche
  `decoded`; le bras `decoded` après
  entraînement reproduit exactement la
  sortie S3.1A de même config/seed/steps.
  Refuse labels 2026, IDs inconnus,
  changement des quantiles via dev.
- `research/token_grammar/learned_embeddings_panel.py`
  et `test_learned_embeddings_panel.py` :
  groupes de trois appariés, SHA backbone
  et scale obligatoirement identiques,
  capacités 0/11/11 supplémentaires
  **strictement vérifiées**, délégation
  métriques direction, montant USD/bps,
  amplitude, Brier et monoclasse.
- `.github/workflows/trame-s3-learned-embeddings-fixtures.yml`
  CI tests synthétiques verts; vérifier
  la dernière CI au SHA du code courant.
- `.github/workflows/trame-s3-embedding-real-pilot.yml`
  : **36 fits D1/H1/M1**, 40 steps, 1 seed,
  width16/depth1 ; [run #40305840861](https://github.com/goldaj/trame-chartist-research/actions/runs/40305840861)
  lancé, vérifier les trois jobs avant
  de déclarer pilote complet et d'en
  tirer tout chiffre. D1/H1 d'abord verts,
  M1 en cours à la rédaction initiale.

## Prochaines sous-étapes exactes
1. **Contrôler le run pilote 36** : trois
   jobs et rapport valide. Revoir l'échelle
   du signe et du montant, taux UP, Brier,
   distribution des 11 identités de tokens.
   Les scores sont développement seulement.
2. Après les trois canaries verts,
   créer et exécuter le workflow **432 fits**
   = D1/H1/M1 × G1/G2 × 3 bras ×2 losses
   ×2 widths ×2 depths ×3 seeds, 200 updates.
   Conserver source SHA, rapports et
   strict panel collectif.
3. Documenter scores BADIRECTION ET AMPLITUDE,
   monoclasse, coût et +11 paramètres des
   bras learned ; ne pas déclarer de gain
   robuste sans validation indépendante.
4. Sur base de ces chiffres, sélectionner
   questions *scientifiques*, PAS modèles
   gagnants par sur-ajustement 2022–25.
5. Suite, protocole d'embeddings vectoriels
   avec nombre paramètres/FLOPs appariés,
   puis patches/multi-résolution.
6. Mettre à jour `AGENTS.md`,
   `docs/CHATGPT_PROJECT_HISTORY.md`,
   [issue #20](https://github.com/goldaj/trame-chartist-research/issues/20),
   PR #25 avant de clôturer.

## Frontières
La donnée BTC historique SPOT publique a
été autorisée explicitement par l'utilisateur
et est vérifiée par SHA Bitstamp amont.
Toutefois **aucun secret, portefeuille,
clé API, compte** ne doit être publié.
D1 public = depuis 2012 ; 2026 holdout
jamais utilisé pour train/dev/selection.
L'utilisateur ignore les frais de simulation,
mais aucune simulation PnL cumulée
n'est un résultat scientifique établi.
Pas d'ordre live et aucun changement du bot
Hyperliquid. Ne pas inférer un edge
à partir d'une balanced accuracy ~50%.
