# S3.0c — audit d'information des grammaires (sans modèle prédictif)

Ce module est une **préparation**, pas une expérience de prévision
du Bitcoin. Lire d'abord [la roadmap S3](ROADMAP_20261026.md)
et le protocole S2b `research/representation_ablation/PROTOCOL_20261026.md`.

## Objectif
Mesurer sur **les mêmes 20 retours passés disponibles à
la décision** quelles informations sont conservées par :
- `legacy_g0a` : code entier `round(log-return×1000)`;
- `continuous_g0b` : bps continus ;
- `signed_uniform_g1` : signe explicite, bacs de magnitude fixes ;
- `signed_quantile_g2` : signe explicite, seuils bps fit **train-only**.

`audit.py` produit un JSON agrégé avec, pour chaque
encodage, taux de signes effacés, erreur d'amplitude
à la reconstruction en bps, distribution/entropie du
vocabulaire, dépassement du dernier seuil quantile.
**Aucune précision directionnelle prédictive** ou PnL
n'est mesurée ici : reconstruire un mouvement déjà
connu n'est pas anticiper le mouvement futur.

## Tests entièrement synthétiques
~~~bash
python -m unittest research.token_grammar.test_diagnostics research.token_grammar.test_audit -v
~~~
`.github/workflows/trame-s3-grammar-audit.yml` ne
télécharge pas de données privées.

## Usage futur dans un environnement privé déjà autorisé
La campagne S2/S2b réelle attend encore la revue de
l'accès privé. Ce code ne constitue pas un contournement.
Une fois les archives de la release BTC approuvée
disponibles localement de manière autorisée :

~~~bash
python -m research.token_grammar.audit --interval D1 --output /tmp/s3_info_D1.json
python -m research.token_grammar.audit --interval H1 --output /tmp/s3_info_H1.json
python -m research.token_grammar.audit --interval M1 --output /tmp/s3_info_M1.json
~~~

Les sorties contiennent des statistiques et **des
seuils de quantiles**, pas de cours bruts, mais doivent
rester dans la zone de travail privée jusqu'à revue.
Les runs D1/H1/M1 utiliseront 4096 train (moins pour
D1) et 1024 dev sélectionnés comme dans A7/S2,
M1 stride60. Les origines 2026 sont exclues ;
D1 indicatif 2010–2011 n'est pas de l'OHLCV.

## Limites (essentielles)
- Les 20 context returns se **chevauchent**.
  Les dizaines de milliers de « positions de tokens »
  ne sont pas des dizaines de milliers de bougies
  indépendantes. Le rapport indique explicitement
  `context_token_observations_overlapping=true`.
- Les quantiles sont calculés uniquement sur les
  fenêtres de **train échantillonnées**, dont le
  recouvrement pondère certains retours plusieurs fois.
  C'est une loi de représentation d'entraînement,
  **pas** la distribution indépendante des rendements
  historiques. Toute comparaison doit en tenir compte.
- `signed_uniform` préserve le sens d'une variation
  non nulle, mais peut déformer fortement les très
  petites amplitudes (surreprésentation du 1er centre).
- `legacy` efface les retours sous l'équivalent
  de 5bps environ, avec une asymétrie d'arrondi aux
  points exactement aux bornes.
- Si les quantiles ont des bornes non distinctes,
  le code doit échouer explicitement plutôt que
  prétendre avoir un vocabulaire de taille fixée.
- Une meilleure reconstruction de l'historique **ne
  prouve pas** une meilleure prévision BTC. S3.1 reste
  une expérience future *après* premier S2/S2b réel
  autorisé et avant tout nouveau gros scaling.
- Aucune donnée brute/trading, aucun frais dans des
  simulations, pas de sélection de modèle sur 2026.

## Codex
Issue [#20](https://github.com/goldaj/trame-chartist-research/issues/20),
PR #22 S3.0c **sur PR #21 S2b, elle-même sur PR #19 S2**.
Voir `AGENTS.md`, `docs/CODEX_S3_HANDOFF_20261026.md`,
`docs/CODEX_S2B_HANDOFF_20261026.md`.
Ne pas fusionner automatiquement.
