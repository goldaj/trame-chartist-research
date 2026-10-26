# TRAME S3.1 — ÉTUDE PRÉENREGISTRÉE DES GRAMMAIRES PREDICTIVES
Date : 26 octobre 2026, **avant tout résultat S3.1 sur BTC réel**.

## Décision chercheur × ingénieur
S2b réel est terminé : 144 fits (3 horizons D1/H1/M1,
3 seeds, 200 updates) ont échoué à montrer une supériorité
cohérente du rendement continu contre le token entier
historique, bien que l'arrondi efface une part significative
du signe des rendements historiques, surtout M1.
Preuve : `research/data/S2B_REAL_PUBLIC_144_RESULTS_20261026.md`.

**Question primaire** : à modèle, cible, entraînement,
histoire physique et loss identiques, une grammaire qui
sépare le signe de l'amplitude est-elle plus utile que
le rendement continu pour prédire **à la fois la direction
de la bougie future et le montant en bps/USD** ?

Il faut séparer deux effets :
1. **S3.1A (maintenant)** : codecs avec aller-retour
   `returns -> tokens -> décodage numérique`, même
   modèle `ContinuousDirectionModel` scalaire. Ce
   protocole teste l'effet de l'information conservée
   / quantifiée, pas la capacité propre d'un modèle à
   exploiter des embeddings discrets appris.
2. **S3.1B (suivant, distinct)** : vrais embeddings
   catégoriels `embedding(token_id)`, multi-canaux
   signe × amplitude ou patches, et réconciliation
   en prix. Cet essai nécessitera un protocole séparé
   pour contrôler le nombre de paramètres/FLOPs.
   Ne pas appeler S3.1A « benchmark de tokens appris ».

## Quatre entrées comparées (exactement 20 bougies passées)
- **G0b** `continuous_bps` : chaque log-return continu
  `10000 × ln(P[t]/P[t-1])` en bps. Référence identique
  au modèle S2b vérifié.
- **G0a** `legacy_quantized_bps` : code historique natif
  `floor(1000 × ln(P[t]/P[t-1]) + 0.5) × 10 bps`.
  Valeur zéro perd le signe ; données exactes
  `Case.encoded_past`, pas recréées par approximation.
- **G1** `signed_uniform_g1` : FLAT uniquement si retour
  vrai = 0 ; sinon préfixe UP/DOWN et magnitude dans
  5 bins à frontières **fixes** 1, 5, 20, 100 bps,
  centres numériques **fixes** 0.5, 3, 12.5, 60, 150 bps.
  Les outliers sont saturés sur le dernier centre :
  cette perte est comptée et déclarée.
- **G2** `signed_quantile_g2` : même signe explicite,
  5 bacs de magnitude dont 4 seuils à quantiles 20/40/
  60/80 % calculés sur les **retours PASSÉS du TRAIN
  seulement**, et centres déterministes définis
  dans `research/token_grammar/diagnostics.py`.
  Aucun ajustement à dev 2022–25 ni à test 2026.

Le token est **toujours reconstruit comme scalaire bps
avant le réseau** à cette étape A. Les quatre bras ont
donc précisément le même nombre de paramètres.

## Conditions fixes
- **D1 / H1 / M1** Bitstamp BTC/USD SPOT source
  publique épinglée et contrôlée SHA1/taille ;
  D1 depuis **2012** (2011H2 omis), distinct de
  l'ancienne cohorte complète. Train labels <2022,
  dev labels 2022–2025, 2026 gelé.
- Cas prélevés via `collect` et mêmes strides : M1
  stride 60, D1/H1 stride 1. Jusqu'à 4096 train
  (D1 3608) / 1024 dev.
- 20 rendements **passés et disponibles au moment de
  la décision**, même ancre USD et même cible continue
  vraie pour chaque grammaire.
- **Normalisation commune** entrée + sortie
  `std(continuous TRAIN historical past returns)`,
  estimée une fois sur TRAIN, identique à S2b.
- `ContinuousDirectionModel` inchangé, 2 objectifs :
  Huber ou Huber + 0.5 BCE direction.
- Mêmes seeds 20261025/26/27, même suite de mini-lots,
  même initialisation des poids et empreinte SHA256,
  même ordre des exemples, mêmes 200 updates,
  AdamW lr0.003 weight decay0.001. Le temps CPU sera
  *mesuré*, FLOPs non équivalents garantis.
- **Campagne** 3 horizons × 4 grammaires × 2 objectifs ×
  2 largeurs (16/32) × 2 profondeurs (1/2) × 3 seeds
  = **192 fits**. Pré-campagne smoke sur D1/H1/M1
  avec 1 width, 1 depth, 1 seed, 40 updates = 24 fits.
- Pour une comparaison en table, séparer horizons :
  MAE USD et distribution volatilité non comparables
  entre D1, H1 et M1.

## Critères de sortie et refus de sur-interprétation
Prioritaires **simultanément** :
1. **Balanced accuracy** direction hausse/baisse
   (au-delà du hasard et des biais monoclasse),
   accuracy brute, couverture et % de sorties UP/DOWN.
2. MAE de prix **USD** et **bps** rapportée à l'ancre,
   **erreur absolue d'amplitude** en bps.
3. Pour le mode avec tête BCE entraînée seulement :
   Brier/CE, Brier Skill vs P(hausse) **train-only**.
4. Baselines persistence, toujours UP/DOWN,
   Ridge, drift train-only, prior directionnel.
5. Comparaisons **appariées par horizon/width/depth/
   loss/seed**, `G1 - G0b`, `G2 - G0b`,
   `G0a - G0b`. Rapporter moyenne/écart-type entre
   seeds, aucune p-value abusive sur 3 graines.
6. Taux de pertes de signe/reconstruction/entropie
   et saturation par grammaire **train vs dev**.
   Meilleure reconstruction ne prouve pas prédiction.
7. Signaler sorties monoclasse ≥99% d'un sens et
   avertir qu'un score directionnel en développement
   peut provenir du choix multiple de variantes.
8. Éviter **tout** PnL cumulé ou extrapolation
   de rendement investisseur : les bougies de
   développement sont échantillonnées et imbriquées.
   Frais ignorés à la demande utilisateur.
9. **2026 jamais utilisé**, pas de test indépendant
   dans cette campagne : aucune revendication edge
   durable/validation finale, aucun ordre Hyperliquid.

## Ordre des sous-étapes
- **S3.1A.1** préenregistrement, contrat de cohorte,
  taxonomie et risques -> présent document.
- **S3.1A.2** implémentation d'une feature-provider pure
  depuis G0a/G0b/G1/G2, fit G2 TRAIN ONLY. Réutiliser
  le **runner S2b** et le même réseau, pas re-coder
  15k caractères de boucle de train.
- **S3.1A.3** tests artificiels d'invariance
  des labels/dev, empreintes poids, reproduction
  exacte des bras G0a/G0b de S2b.
- **S3.1A.4** CI publique, vrai **pilote 24 fits**
  sur D1/H1/M1, puis examen de provenance.
- **S3.1A.5** vrai benchmark **192 fits**, rapport
  agrégé et tableau apparié ; critiquer ce qui
  est démontré et non démontré.
- **S3.1B.0** préenregistrer tokens appris et
  architecture à embeddings, coûts/paramètres
  appariés ; seulement ensuite implémenter/
  tester autre grammaire ou patches.
- **S3.2** patches 4/8/16 avec égalité en TEMPS
  physique d'information, puis OHLCV, événements
  et représentations hiérarchiques causales.

## Passation
PR nouvelle **enfant de #23** (source BTC publique) ;
issue [#20](https://github.com/goldaj/trame-chartist-research/issues/20).
Garder les expériences antérieures intactes, mise à jour
`AGENTS.md` et `docs/CHATGPT_PROJECT_HISTORY.md`,
pas de merge automatique. Ne pas ajouter secrets/identifiants
à la data librement publiable.
