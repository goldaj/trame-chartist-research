# Codex — TRAME S3.1D ablation pertes direction et amplitude
26 octobre 2026. **PR #27 DRAFT**, branche
`chatgpt/trame-s3-objective-ablation-20261026`
basée sur [PR #26 S3.1C](https://github.com/goldaj/trame-chartist-research/pull/26).
Ne pas fusionner automatiquement. Historique complet dans
`docs/CHATGPT_PROJECT_HISTORY.md`.

## Point exact de la reprise
Le propriétaire a dit « t'as crash, reprends ».
À la reprise, S3.1C était **DÉJÀ finie** :
[GitHub Actions #40309653884](https://github.com/goldaj/trame-chartist-research/actions/runs/40309653884)
**4/4 jobs verts**, 27 vrais modèles entraînés jusqu'à
2000 updates et 81 checkpoints, train interne <2020,
monitor 2020–21, dev externe 2022–25 et test 2026
non exploités, conclusions/empreintes dans
`research/token_grammar/S3_1C_REAL_81_RESULTS_20261026.md`.
D1 se dégrade avec prolongement, H1/M1 parfois
s'améliorent mais l'erreur d'amplitude ne suit
pas systématiquement. Aucun edge de trading.

Un début de réimplémentation redondante
`internal_cohorts.py/training_dynamics.py` a été
**supprimé**, sans produire d'expérience rivalisant
avec le run #40309653884. Une seule source
de vérité S3.1C reste `convergence.py`
et `convergence_panel.py`.
La correction additive `stream.py` supporte
maintenant un `stop_labels_before`
qui stoppe explicitement le lecteur avant toute
bougie 2022+, plutôt que de la parcourir
puis ignorer ses labels ; `convergence.py`
l'utilise. Les précédents chiffres ont été calculés
sur l'ancien code mais les exemples pré2022
ne changent pas : la nouvelle preuve correspond
au hardening, pas à un nouvel essai identique.
Test régression dans `test_convergence.py`.

## S3.1D préenregistrée AVANT toute mesure BTC réelle
**Source méthodologique** :
`research/token_grammar/S3_1D_LOSS_PROTOCOL_20261026.md`.
Changer seulement le poids des composantes
de loss, pas architecture/tokenisation/graines.
`research/token_grammar/loss_ablation.py` :
- `reference` : Huber(retour)+0.50 BCE(sens)
- `direction_025` : Huber+0.25 BCE
- `direction_100` : Huber+1.00 BCE
- `magnitude_025` : Huber+0.50 BCE+0.25 Huber(|retour|)
- `magnitude_100` : Huber+0.50 BCE+1.00 Huber(|retour|)

Toutes 5 variantes : `ContinuousDirectionModel`
width16/depth1 JOINT avec **exact même nombre de
paramètres**, même Git/SHA init, G2 signed quantiles
fit TRAIN interne uniquement puis décodés en
bps, même réconciliation direction × amplitude,
même mini-batches et l'optimiseur AdamW.
Le test de parité compare `reference` à
`ContinuousDirectionModel.loss()`
numériquement, y compris cible plate.
Même train<2020, monitor2020–21, embargo
2022–25 ET 2026.

## Tests, bugs et corrections honnêtes
- `test_loss_ablation.py` et
  `test_loss_ablation_panel.py` sur retours
  artificiels, contrôle anti-fuite temporelle,
  capacités/SHA, math exactes de BCE, panel
  complet et fraude de paramètres.
- `.github/workflows/trame-s3-1d-loss-fixtures.yml`
  CI verte.
- Premier smoke réel [run #40312632612](https://github.com/goldaj/trame-chartist-research/actions/runs/40312632612)
  **ÉCHOUÉ AVANT TRAINING** : l'option argparse
  `--checkpoints` était enregistrée deux fois ;
  corrigé en commit ultérieur.
  Ne pas rapporter cet échec comme
  résultat de modèle.
- Relance pilote ingénierie
  [run #40312924527](https://github.com/goldaj/trame-chartist-research/actions/runs/40312924527) :
  5 loss arms ×3 horizons ×1 seed,
  checkpoints courts 10/20/40, flag
  `engineering_canary_not_scientific_selection=true`.
  La CLl est d'abord contrôlée par `--help`.
- Campagne SCIENTIFIQUE complète,
  [run #40313075915](https://github.com/goldaj/trame-chartist-research/actions/runs/40313075915)
  : 3 horizons ×5 loss arms ×3 seeds =
  **45 trajectoires distinctes**,
  2000 updates chacune ; 3 checkpoints
  200/800/2000 = **135 évaluations**.
  Aucun résultat S3.1D ne doit être annoncé
  avant vérification officielle des **3 jobs
  et de l'agrégateur** et de leurs artefacts.
- `loss_ablation_panel.py` vérifie les
  5 bras à chaque seed/checkpoint, même SHA,
  paramètres/normaliseur, coefficient de loss
  EXACT, année 2022–25 non accédée.
  Report direction BA/accuracy, % UP,
  sorties monoclasse, MAE prix **USD/bps**,
  erreur de montant absolu **bps**, Brier
  vs prior TRAIN, losses et gradients.
  Ne pas mélanger D1/H1/M1.

## Suite chercheur × ingénieur
1. Vérifier les CI dernier SHA, les
   trois jobs du run 45 et agrégateur.
2. Contrôler SHA des JSON agrégés et
   score par seed, année, régimes internes ;
   éviter une p-value abusive sur 3 graines.
3. Analyser les compromis BA vs
   MAE prix vs magnitude, effondrement
   monoclasse/Brier; aucune victoire
   proclamée sans amélioration conjointe.
4. Documenter conclusions et prochaines
   hypothèses Codex/AGENTS/issue #20.
5. Décider seulement ensuite de nouveaux
   embeddings vectoriels, patchs causaux
   ou scaling. Ne PAS ouvrir 2026 et
   ne pas retourner à dev 2022–25 comme
   test indépendant.
6. Frais ignorés sur instruction utilisateur,
   aucun ordre réel, PnL portefeuille,
   compte, secret ou wallet Hyperliquid.
