# Codex — S3.0c grammaires / audits informatifs D1-H1-M1
Date : 26 octobre 2026. **État de recherche synthétique/logiciel uniquement.**

## Contexte utilisateur et priorité
L'utilisateur a demandé une réflexion sur les « différentes
grammaires » utilisées pour convertir les courbes en tokens,
à programmer après les études sur les représentations
actuelles, sans perdre la rigueur chercheur+ingénieur.
La demande est tracée verbatim dans
`docs/CHATGPT_PROJECT_HISTORY.md` et l'issue
[#20](https://github.com/goldaj/trame-chartist-research/issues/20).

Ordre de recherche :
1. S2/S2b : mêmes données D1/H1/M1, vraie direction et
   véritable amplitude, isoler entrée arrondie de retour continu.
2. **S3.0c** : perte d'information *sans modèle* par horizon,
   avec grammaires G0a/G0b/G1/G2. Les tests sur fixtures
   peuvent se faire sans autorisation d'archives privées.
3. **S3.1 réel**, seulement après S2/S2b réel autorisé :
   deux grammaires sont comparées dans une même IA,
   mêmes graines/budget/objectif et cohorte.
4. S3.2/3 patches/OHLCV/événement/VQ/multi-échelle,
   après justifications, **avant** nouveau scaling lourd.

## Développements réalisés
- PR **#22** `chatgpt/trame-grammar-audit-20261026`
  **basée sur PR #21** (S2b) → #19 (S2) → #18 (D1) → #17 (S1).
  Aucune fusion automatique.
- `research/token_grammar/audit.py` : utilise les
  mêmes cohorte/cas A7 `collect` que S2b,
  20 retours **passés** par origine, quatre grammaires
  via `diagnostics.py`, quantiles G2 calculés exclusivement
  sur retours du TRAIN, puis **appliqués tels quels** sur dev.
  Refuse 2026 via `_validate_chronology`.
- `test_audit.py` : fixtures falsifiées, vérifie
  que des dev outliers ne déplacent pas les seuils train,
  continuous conserve le signe, legacy efface certains
  mouvements, scores déclarés explicitement **non prédictifs**
  et 2026 refusé.
- `.github/workflows/trame-s3-grammar-audit.yml` :
  CI artificielle / aucune release privée requise.
  Vérifier la CI au dernier SHA avant de dire verte.
- `research/token_grammar/AUDIT_README_20261026.md` :
  runbook et précautions.

## Limites scientifiques NON négociables
- Chaque `Case` répète 20 rendements précédents.
  Les ~80 000 positions de tokens ne sont PAS autant
  de bougies indépendantes. L'audit émet
  `context_token_observations_overlapping=true`,
  `estimated_unique_candle_count=null`.
- La distribution de tokenisation est pondérée par la
  sélection A7 (jusqu'à 4096 train/1024 dev,
  M1 stride60). Ce n'est pas une distribution
  exhaustive des cours BTC à pas constant.
- Amélioration de l'information reconstruite ≠ capacité
  à prédire un rendement futur. Les sorties rapportent
  `model_trained=false`, `price_prediction_performed=false`.
  Aucun PnL, aucun ordre, frais volontairement ignorés.
- Les 2010–2011 D1 sont prix indicatifs sans OHLCV :
  seules les vraies bougies Bitstamp entrent dans
  le pipeline causal A7 ; pas de volume inventé.
- Aucun seuil de quantile/VQ n'est estimé depuis 2022–25
  ou depuis 2026 ; le dev ne peut choisir ni le vocabulaire
  ni son ordre des bacs.
- **2026 gelé**. Ne pas inférer de retours
  réels d'après la CI synthétique.
- Si le vocabulaire G2 devient non identifiable,
  le code échoue au lieu d'inventer des quantiles.
- Les briques S2/S2b sur cours réels ne sont PAS lancées,
  car la création préalable d'un workflow privé
  a été refusée par les contrôles de sécurité.
  **Ne pas contourner le refus**, inventer un nom de
  workflow différent, ou supposer que les chiffres existent.
  La création d'une CLI offline réutilisable ne constitue
  pas l'autorisation de publier ou récupérer des prix privés.

## Prochaine passation
1. Vérifier CI PR #22, corriger sans modifier les splits.
2. Audit de causalité anti-lookahead et diagnostics
   statistiques sur données artificielles.
3. Quand autorisation effective de traitement du corpus :
   calculer des rapports agrégés réels par horizon,
   garder les artefacts dans dépôt/espace privé,
   enregistrer SHA code/horaires et qualité des données.
4. S3.1 après S2/S2b : aligner **même quantité d'histoire**,
   même loss, même nombre réel de paramètres et graines.
   Balanced accuracy, couverture, erreur amplitude
   en bps/USD, Brier skill et prévisions monoclasse
   sont les métriques prioritaires.
