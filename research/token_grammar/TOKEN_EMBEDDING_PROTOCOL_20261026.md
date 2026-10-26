# TRAME S3.1B — Tokens catégoriels à embeddings réellement appris
26 octobre 2026. **PRÉENREGISTREMENT AVANT TOUT ESSAI BTC S3.1B**.

## Motivation factuelle
S3.1A [288 fits réels](https://github.com/goldaj/trame-chartist-research/actions/runs/40300156418)
a montré que G2 (quantiles signés train-only) réduit le
collapse monoclasse en H1 joint (0/12 vs continu 6/12)
et améliore légèrement BA/MAE prix, tout en dégradant
l'erreur d'AMPLITUDE. Mais S3.1A décodait les catégories
en un rendement scalaire : aucun réseau n'apprenait
des embeddings propres à des symboles. S3.1B teste
exactement CETTE hypothèse distincte.

## Contrat d'entrée et d'architecture
Tous les modèles utilisent la même nouvelle
`TokenHybridDirectionModel`, dérivée de la même
architecture `ContinuousDirectionModel` S2b :
- Chaque pas passé a deux canaux séparés :
  `(return_scalar_normalized, token_id)`.
  Le canal retour contient soit le rendement
  passé bps / std(TRAIN continu), soit 0
  pour les bras purement catégoriels.
- Le token id entier est compris entre 0 et 10 :
  **0 = neutral/no-token/FLAT**, UP0..UP4 =1..5,
  DOWN0..DOWN4 =6..10 ; **aucune OOV silencieuse**.
  Les grammaires G1/G2 sont fixées/fittées sur
  les contextes TRAIN passés uniquement, jamais
  sur les prix du DEV ou du holdout 2026.
- Représentation cachée identique :
  `Linear(1,width)(return_scalar) +
    Embedding(11,width)(token_id)`,
  puis EXACTS blocs CausalGQABlock, norm,
  return_head et direction_head déjà présents.
  Les embeddings sont des paramètres vraiment
  entraînés par backprop. Dtype float64 comme S2.
- Toutes les variantes incluent les **deux**
  canaux, l'intégralité de l'embedding 11×width,
  même nombre TOTAL de paramètres, même
  graph/backbone, même graine et SHA poids initial.
  Attention : nombre de paramètres **actifs** et
  gradients reçus par catégorie peuvent différer ;
  FLOPs et vitesse mesurés, pas garantis identiques.

## Cinq bras, CHOISIS AVANT résultats
- `continuous_scalar` : vrai retour CONTINU
  normalisé comme scalaire, token_id=0 toujours.
- `g1_decoded_scalar` : G1 fixe signée,
  retour après décodage centre de bin comme
  scalaire, token_id=0.
- `g1_learned_token` : G1 fixe signée,
  retour scalaire=0, token_id=UP/DOWN/FLAT.
- `g2_decoded_scalar` : G2 quantiles
  magnitude TRAIN-only, retour après
  décodage comme scalaire, token_id=0.
- `g2_learned_token` : G2 TRAIN-only, retour
  scalaire=0, token_id=UP/DOWN/FLAT.

Les comparaisons **catégorie apprise contre
la catégorie décodée** G1cat vs G1scalar et
G2cat vs G2scalar sont plus pertinentes
pour isoler l'interface embedding. Le
témoin `continuous_scalar` permet
de déceler un écart absolu. Ne PAS comparer
directement les scores de S3.1A comme si
le réseau était identique : S3.1B contient
un embedding additionnel pour TOUS les bras.

## Matrice et pilotage
- D1/H1/M1 Bitstamp BTC/USD SPOT publics,
  mêmes 20 rendements complets de chaque
  origine que S2b/S3.1A. D1 public = 2012+,
  ancien 2011H2 exclu faute de droits.
- Train labels avant 2022, dev 2022–25,
  **2026 jamais ouvert**, même split causal
  `collect`, train 3608/4096,
  dev 1024 par horizon, M1 stride60.
- Même cible retour log CONTINU normalisée
  `std(continuous_past_bps TRAIN)` et
  dénormalisée en prix par ancre.
- Deux objectifs Huber et Huber+0.5 BCE
  direction nonflat, identiques S2b.
  Deux widths 16/32, depths 1/2,
  seeds 20261025/26/27 et 200 mises
  à jour, batchsize16 et optimizer AdamW
  lr0.003, wd0.001.
- **Matrice complète = 3×5×2×2×2×3 =
  360 FITS**, soit 120 par horizon,
  12 fits par (horizon, loss, grammaire).
  **Pilote** : 3×5×2 =30 fits, 40
  updates, width16/depth1, seed 20261026.
- Les sorties enregistrent SHA modèle,
  SHA des 20 rendements temporels
  originaux, SHA poids initial,
  statistiques token train-only et
  provenance Bitstamp, aucune donnée
  de portefeuille et aucun ordre.

## Métriques primaires et prudence
Direction **balanced accuracy** (prioritaire),
accuracy brute, % UP, couverture et
effondrement monoclasse ≥99%.
Erreurs de prix en USD et bps, erreur
d'amplitude absolue bps (aussi prioritaire),
Brier/CE vs prior train-only (seulement
tête joint réellement entraînée),
baselines persistance/toujours up/down/
drift/Ridge, temps CPU et nb params.

Chaque delta apparié = différence entre
G1cat et G1scalar, G2cat et G2scalar
à **même horizon, width/depth, mode,
graine, labels, normalisation, initial weights**
+ comparaison descriptive à `continuous_scalar`.
Exiger mean et dispersion sur 3 graines
mais les 1024 fenêtres DEV sont recouvrantes :
ce ne sont PAS des échantillons indépendants.
Aucune p-value sur 3 graines, aucun
rendement financier composé inféré, frais
ignorés (utilisateur), aucun ordre Hyperliquid.

### Décisions GO/NO-GO
- **GO technique** si les embeddings sont
  effectivement mis à jour par gradients,
  token IDs restent entiers in-range, G2
  ne consulte pas DEV, cohorte appariée
  sans 2026, CI synthétique et pilotes réels.
- **GO recherche** si categorical G1/G2
  améliore le compromis BA+MAE+amplitude
  et réduit monoclasse de façon cohérente
  sur plusieurs seeds/horizons/régimes.
- **NO-GO conclusion prédictive** si
  BA reste ~50%, Brier near0 ou
  amélioration prix détruit précision du montant.
  Ne pas choisir « la meilleure » graine.
- **Épreuve indépendante** seulement
  après gel de l'hypothèse, évaluation
  strictement hors dev ; 2026 réservé
  jusqu'au protocole final.

## Sous-étapes S3.1B
1. **B.1** présent protocole, hypothèses
   et 5 bras; aucune modification S3.1A.
2. **B.2** implémenter `TokenHybridDirectionModel`
   et la préparation tensorielle
   `(float normalisé, int token)`.
3. **B.3** tests sur cours INVENTÉS :
   token IDs, gradient embedding, même SHA,
   quantiles train-only et gel 2026.
4. **B.4** pilote réel 30 fits D1/H1/M1
   avec provenances et 40 updates.
5. **B.5** campagne 360 fits / 200 updates,
   tableau apparié, Brier et amplitude,
   dispersion/monoclasse, source SHA.
6. **B.6** décisions sur patches 4/8/16,
   grammaires événementielles, et
   généralisation hors développement,
   AVANT de grossir arbitrairement les IA.

## Pour Codex
Branch distincte basée sur PR #24 S3.1A,
doc de référence `docs/CODEX_S3_1_HANDOFF_20261026.md`
et `AGENTS.md`; issue
[#20](https://github.com/goldaj/trame-chartist-research/issues/20).
Toujours consigner user et assistant (citations
textuelles seulement quand réellement connues),
ne pas fusionner PR sans demande explicite.
