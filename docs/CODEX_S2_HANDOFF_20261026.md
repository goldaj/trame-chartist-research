# Codex handoff : S2 direction continue, 26/10/2026

## D'abord : statut des preuves
- L'utilisateur a demandé D1 **avant toute suite**. C'est achevé
  en PR #18 (dépendance de cette PR #19), avec D1/H1/M1 réels
  depuis la release privée approuvée, aucun label 2026 ouvert.
- S1 a désormais trois séries réelles vérifiables :
  1. A7 D1 et H1/M1 direction harmonisée :
     privé [#40280347574](https://github.com/goldaj/btc-historical-data/actions/runs/40280347574)
     et [#40280464439](https://github.com/goldaj/btc-historical-data/actions/runs/40280464439).
  2. 135 fits de faisabilité 5 tailles×3 profondeurs×3 familles×3 horizons :
     privé [#40281223578](https://github.com/goldaj/btc-historical-data/actions/runs/40281223578),
     6/6 jobs **réussis**.
  3. 243 fits 3 tailles×3 profondeurs×3 familles×3 seeds×3 horizons,
     200 updates :
     privé [#40281657954](https://github.com/goldaj/btc-historical-data/actions/runs/40281657954),
     3/3 jobs **réussis**. Lire
     `research/scaling_study/S1_REAL_200UPDATES_20261026.md`.
- Aucun avantage directionnel validé malgré ces 378 entraînements.
  D1 reste très fortement biaisé « toujours hausse », et des modèles
  200 updates montrent balanced accuracy à 50 %.
  Le codec quantifié peut expliquer une part de la perte de sens
  mais ce n'est PAS encore prouvé causalement.

## S2 prêt côté code, non exécuté sur cours réels
- PR #19 : `chatgpt/trame-continuous-direction-20261026`,
  base **PR #18**, puis #17/#14. Pas de fusion automatique.
- **S2.1** protocole de recherche gelé :
  `research/continuous_direction/PROTOCOL_20261026.md`.
- **S2.2** `Case.continuous_past_bps` est rempli en parallèle
  des anciens codes (ces derniers restent inchangés).
- **S2.3** 2 modes même modèle causal GPT-style :
  Huber sur return continu vs Huber + 0.5 BCE direction ; signe du
  forecast joint = tête classification, amplitude = abs retour
  prédit. Contrôle de cohérence ex ante.
- **S2.4** runner avec normalisation **strictement train-only**,
  mêmes splits et cas, métriques direction, balanced, amplitude,
  Brier et comparaison aux témoins toujours-up/down.
- **S2.5** tests adversariaux et CI publique verts sur
  [GitHub Actions #40283099756](https://github.com/goldaj/trame-chartist-research/actions/runs/40283099756)
  (code au SHA `72ca8fdbcc3270c364429029fd68bceb92c99376`).
- **S2.6 NON EFFECTUÉ** : tentative de créer le workflow réel privé
  dans `goldaj/btc-historical-data` sur la branche vide
  `chatgpt/trame-private-s2-continuous-20261026` **bloquée
  par l'outil avec un message de sécurité**. Aucun workflow
  effectif ni run S2 réel, ne pas inférer de scores ou dire
  « en cours d'entraînement ». Ne pas contourner ce blocage
  par une écriture déguisée du même workflow.

## Mode de reprise explicitement documenté
Sur un environnement disposant **déjà** d'un accès autorisé
au dépôt de données privé et suivant les politiques applicables :
~~~bash
python -m unittest research.continuous_direction.test_continuous -v
python -m research.btc_h1_m1.release_store --resolution D1 --download
python -m research.btc_h1_m1.release_store --resolution H1 --download
python -m research.btc_h1_m1.release_store --resolution M1 --download
python -m research.continuous_direction.runner --interval D1 --steps 200 --output /tmp/s2_d1_real.json
python -m research.continuous_direction.runner --interval H1 --steps 200 --output /tmp/s2_h1_real.json
python -m research.continuous_direction.runner --interval M1 --steps 200 --output /tmp/s2_m1_real.json
~~~
Ne pas exposer ces sorties ou les données brutes si elles deviennent
sensibles ; les seuls artefacts publics admissibles sont des métriques
agrégées accompagnées de code hash, source et limites.
Le workflow et les politiques d'accès privé doivent être revus avant
création. L'utilisateur a demandé **aucun frais** dans les simulations,
mais les calculs bruts par bougie ne valent pas un PnL composé.

## Hypothèse scientifique et No-Go
Risque fort : direction = classe majoritaire et amplitude = faible,
même avec meilleur score MAE. Les variantes S2 ne sont pas
équivalentes en distribution de sortie ni en FLOPs à la vieille
NLL ; ne pas comparer les scores Huber/BCE à NLL ou déclarer
« plus gros = mieux ». D1 2010–2011 est close indicatif seulement,
jamais une fausse bougie OHLCV. 2026 reste hors entraînement/dev.
