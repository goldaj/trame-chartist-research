# CODEX — S2b représentation seule (passation 26 octobre 2026)

## Priorité et raison
Après 378 entraînements réels S1, l'IA prédit très souvent
**toujours le même sens**, même en augmentant profondeur
et paramètres. S2 testait à la fois rendements continus
et modification de l'objectif d'entraînement.
Pour isoler **le véritable impact du codec historique**,
S2b a été préenregistré **avant tout run BTC réel S2b**
dans `research/representation_ablation/PROTOCOL_20261026.md`.
User brief le plus récent : « continue ». L'hypothèse
explicite sur « différentes grammaires » demeure dans
`research/token_grammar/ROADMAP_20261026.md`
et l'issue [#20](https://github.com/goldaj/trame-chartist-research/issues/20).

## État des branches
- PR #21 : `chatgpt/trame-representation-ablation-20261026`
  (draft, **base PR #19**).
- #19 S2 `chatgpt/trame-continuous-direction-20261026`
  (base PR #18 D1 puis #17 S1 et #14 A7).
- Ne pas intégrer implicitement PR #11–#16 ou les branches
  privées des workflows précédents ; aucun merge automatique.
- Aucun code de trading ni repo Hyperliquid modifié.

## Livrables réels S2b (code seulement, jusqu'à nouvelle preuve)
1. `research/representation_ablation/PROTOCOL_20261026.md` :
   facteur 2×2 (input quantifié/continu × loss Huber/Huber+BCE),
   2 largeurs 16/32, 2 couches 1/2, trois horizons
   D1/H1/M1, trois seeds = **144 entraînements prévus**.
2. `runner.py` : `features` accepte soit les vrais
   log-returns ex-ante en bps, soit les codes EXACTS
   `case.encoded_past * 10` bps ; mêmes **vraies**
   étiquettes cible continues entre bras.
   **Entrées ET cibles normalisées par le MÊME écart-type**
   calculé sur train des entrées continues (train-only).
   L'écart-type de l'entrée quantifiée est calculé pour
   DIAGNOSTIC seulement et ne modifie pas son échelle. Même suite d'indices
   de mini-batches et même graine avant construction du
   modèle ; `initial_state_sha256` prouve le même point
   de départ entre représentations.
3. `test_ablation.py` : tests fixtures de retour
   minuscule codé zéro, label-invariance des features,
   poids initiaux équivalents, dev 2026 rejeté,
   normalisation indépendante des labels dev.
4. `panel.py`, `test_panel.py` : agrégation
   quantifié vs continu, `delta_continuous_minus_quantized`,
   strictement par horizon, mode, width, depth, nombre
   d'updates et seed. Un couple absent ou des SHA
   initiaux différents produisent une erreur.
5. CI publique `.github/workflows/trame-s2b-representation.yml`
   **sur fixtures inventées**. Vérifier son dernier SHA
   et ses logs avant de marquer ce palier qualifié.

## Risques scientifiques à expliquer, non à masquer
- S1 vs S2 était confondu : nouveau label, loss,
  mode d'encodage. S2b isole l'**entrée** sans modifier
  la fonction de perte au sein d'une même paire.
- Les deux encodages partagent l'échelle d'entrée
  **et** de cible `std(continuous_train_past_bps)`, fit
  sur train seulement. Seul l'input arrondi change ;
  cela renforce l'identification scientifique.
  Les écarts-types natives distincts des inputs restent
  disponibles en diagnostics de quantité d'information.
- Si les codes quantifiés M1 sont presque tous à zéro,
  l'écart-type des inputs arrondis peut être nul :
  `std_degenerate_fallback=true` et scale 1,
  sans prétendre qu'une telle entrée contient du signal.
- Reconstruction fidèle / maintien du signe sur le
  passé ne démontre pas une amélioration de **prévision
  du futur**. Balanced accuracy, distribution des signes,
  MAE USD et bps, erreur d'amplitude, Brier skill
  sur joint et tests par régimes doivent être rapportés
  ensemble. Aucun classement inter-horizons par MAE USD.
- D1 indicatif 2010–2011 conserve seulement sa
  clôture, aucune OHLCV artificielle ni volume inventé.
  Train avant 2022, dev 2022–25, **2026 gelé**.
- **Frais ignorés** à la demande du propriétaire ;
  aucun rendement capitalisé validé ni ordre de trading.

## S2b.5 / VÉRITABLE EXÉCUTION BTC
**NON EXÉCUTÉE à la date de rédaction.** Le workflow
privé S2 avait été refusé par contrôle de sécurité de
l'outil. Ne pas recréer le même workflow en le déguisant
en autre écriture, ne pas contourner les politiques.
Dans un environnement disposant d'un accès privé
**déjà autorisé**, suivre le runbook des commandes
directes dans `research/representation_ablation/README.md`.
Ne jamais publier les prix bruts ni les secrets.

## Prochaine décision
1. CI dernière SHA verte S2b et documentation consolidée.
2. Assurer provenance du modèle/selection temporelle.
3. Après accès autorisé au train BTC, canary D1 puis H1/M1,
   conserver JSON agrégé privé, jamais ouvrir 2026.
4. Analyser si continu > quantifié **à même loss**,
   puis déterminer S3.1 « grammaires » (issue #20)
   **avant** nouvelle grosse campagne de scaling.
5. Si aucune exécution privée permise, maintenir
   le statut S2/S2b « résultats réels non disponibles »
   et ne poursuivre que tests artificiels et recherche.

## Convention d'historique
Comme demandé par le propriétaire, garder le texte
utilisateur exact disponible et distinguer les réponses
résumées du verbatim. Mise à jour :
`docs/CHATGPT_PROJECT_HISTORY.md`.
