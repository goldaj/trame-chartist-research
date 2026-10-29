# BILAN FINAL IMPORT PUBLIC ET PREMIÈRE EXPÉRIENCE COMPLETE

Le workflow [public 144-fit #40296933559](https://github.com/goldaj/trame-chartist-research/actions/runs/40296933559)
est **TERMINÉ avec succès (3/3 jobs)**.
Ne plus le présenter comme « en cours ».
Les trois fichiers JSON authentiques archivés
sur Actions sont identifiés par SHA-256 dans
`research/data/S2B_REAL_PUBLIC_144_RESULTS_20261026.md`.
Train D1 3608, H1/M1 4096 ; dev 1024
par résolution ; 2026 gelé, et aucune
preuve d'edge directionnel. L'ancien
blocage technique de la release privée
a été contourné **non par un accès secret**,
mais par usage de la source BTC publique
d'origine **avec autorisation expresse
de l'utilisateur**, téléchargement H1/M1
vérifié et code public de TRAME.

Le comparatif apparié à 200 updates
n'identifie aucune victoire générale du
retour continu sur l'arrondi. Les
séries M1 restent extrêmement sensibles
à l'arrondi historique, mais préserver
le signe des mouvements passés n'a pas
automatiquement amélioré la prévision
future. La première question de S2b est
donc TRAITÉE exploratoirement, mais
pas confirmée sur test temporel
indépendant.

**Reprise Codex :** S3.1 de l'issue
[#20](https://github.com/goldaj/trame-chartist-research/issues/20),
changer la grammaire/tokenisation à
backbone/loss/seeds/amount d'historique
et budget appariés, et analyser par
année/régime. N'ouvrir 2026 ni pour
choisir les tokenizers, ni pour évaluer
des variantes en boucle. D1 indicatif
2010–2011 reste *close-only*, hors OHLCV
Bitstamp public 2012+.

---

# Codex — BTC public : transfert effectif et exécution sans repo privé
Date 26 octobre 2026 ; instruction utilisateur expresse.

## Demandes exactes de la séance (verbatim)
> et qu'est-ce qui te bloque pour accéder aux données du repo privé ? Tu peux juste les dl et les intégrer dans ton repo en fait

Puis :
> si si tu peux les considérer publics, si tu prends les données historiques btc c'est rien de grave

## Correction factuelle essentielle
L'accès **lecture** à `goldaj/btc-historical-data` a été confirmé.
Le blocage antérieur de S2 concernait **la création d'un
workflow Actions privé**, pas l'inaccessibilité intellectuelle
des cours ni le manque de permissions sur GitHub.
Les releases contiennent 16 gzip H1/M1 et trois CSV D1 ;
les gzip proviennent d'un dépôt amont lui-même PUBLIC.
Le connecteur GitHub lit les CSV en UTF-8, mais ne
transfère pas directement de gzip de ~113 Mo vers le
runtime local de l'assistant. Il ne fallait pas déduire
« impossible d'utiliser les cours réels » de ce seul
problème de transport.

## Action effectivement réalisée sur PR #23
- Branche `chatgpt/trame-public-btc-data-import-20261026`,
  basée sur PR #22 S3 (elle-même #21 S2b → #19 S2
  → #18 D1 → #17 S1, PR #14 A7). **Aucune fusion automatique**.
- Import public RÉEL
  `research/data/reference/btcusd-bitstamp-d1-2012-2026H1.csv`,
  372096 octets, Git blob SHA-1
  `a8f2da91cb00fce75117ba5bf000384f240abd56`
  **strictement identique** au fichier du dépôt privé.
  5 295 jours, 2012-01-01 à 2026-06-30.
- `research/data/reference/bitstamp_source_manifest.json`
  : 16 fichiers H1/M1 compressés de la source PUBLIQUE
  `alessiostomeo/btc-cycle-data` revision figée
  `b57f460fab1afb82705eb813cee2ef4afb1f6848`.
- `research/data/public_data.py` : télécharge par
  `urllib` et stocke dans le cache `TRAME_BTC_CACHE_DIR`
  en respectant longueur ET Git blob SHA1 + SHA256
  (identité réelle, pas de token GitHub ni de workflow
  privé). Les archives gzip restent dans cache local
  pour éviter des blobs gigantesques dans Git.
- `research/btc_h1_m1/daily.py` supporte
  D1 **2012+ seul** OU le D1 2010–2026 à 3 fichiers,
  sans inventer OHLCV indicatif, et conserve le gel 2026.
  La cohorte D1 « 2012+ seulement » n'est PAS identique
  à l'ancienne cohorte D1, qui incluait 2011H2 :
  comparer sans harmoniser est un biais.
- `research/representation_ablation/runner.py`,
  `panel.py`, `research/token_grammar/audit.py`
  acceptent le nouveau label `BTC_PUBLIC_REAL`
  et exigent un SHA de code Git traçable.
- Test CI `.github/workflows/trame-public-btc-data.yml`
  vert sur la vraie référence D1 et faux gzip adversariaux.
- **PREMIER essai D1 réel réussi**
  [GitHub Actions #40295846917](https://github.com/goldaj/trame-chartist-research/actions/runs/40295846917) :
  S2b 4 bras 1 graine, 40 steps, width16/depth1,
  train **3608**, dev **1024**, 2026 exclus.
  Rendement continu/régression balanced direction
  ≈53.41%, arrondi/régression ≈53.40%.
  Les bras joint sont ≈51.14/51.04%.
  **Pas de significativité**, ni conclusion « continu meilleur ».
  Le diagnostic S3 informe qu'environ **2.86%**
  des retours historiques non plats des contextes
  D1 dev deviennent token de signe nul avec
  `round(log_return*1000)`. L'erreur de
  reconstruction G0a ≈2.51 bps dans ces contextes.
- Workflows publics autonomes `trame-public-d1-canary.yml`
  et `trame-public-h1m1-canary.yml`, uniquement
  données publiquement autorisées/sources publiques :
  **ne pas annoncer la réussite H1/M1 sans vérifier
  les deux jobs et analyser leurs JSON**.

## Attribution / limites
Voir `research/data/PUBLIC_DATA_README_20261026.md`.
Origines Bitstamp Kaggle (Zielak/mczielinski),
ff137/bitstamp-btcusd-minute-data,
alessiostomeo/btc-cycle-data.
Licences annoncées CC BY-SA 4.0 et CC BY 4.0 selon
cohortes. La permission du propriétaire de TRAME ne
remplace pas les conditions des sources tierces.
D1 2010–2011 (close-only indicatif source CoinGecko)
et D1 Bitstamp 2011H2 (licence de redistribution
non confirmée) **ne sont pas committés publiquement**.
Le pipeline privé historique à 3 CSV reste fonctionnel.

Données BTC SPOT, non perp Hyperliquid. Pas de frais
dans simulations (consigne utilisateur), pas de PnL
composé validé, aucun ordre, clé, jeton ni wallet publié.
2026 test demeure gelé pour la recherche : les
archives sources peuvent inclure 2026, mais aucune
**cible 2026** n'est utilisée en apprentissage/dev.

## Commandes pour relancer après checkout PR #23
~~~bash
python -m research.data.public_data --resolution D1 --check-only
python -m research.data.public_data --resolution H1
python -m research.data.public_data --resolution M1
python -m research.data.public_data --resolution ALL --check-only

# 4 bras pilotes à comparer sur le même échantillonnage
python -m research.representation_ablation.runner --interval D1 \
  --directory research/data/reference --data-origin BTC_PUBLIC_REAL \
  --widths 16 --depths 1 --steps 40 --seeds 20261026 \
  --output /tmp/d1_public_s2b.json

# H1/M1 : fichiers dans DEFAULT_CACHE après installation publique
python -m research.representation_ablation.runner --interval H1 \
  --data-origin BTC_PUBLIC_REAL --widths 16 --depths 1 \
  --steps 40 --seeds 20261026 --output /tmp/h1_public_s2b.json
python -m research.representation_ablation.runner --interval M1 \
  --data-origin BTC_PUBLIC_REAL --widths 16 --depths 1 \
  --steps 40 --seeds 20261026 --output /tmp/m1_public_s2b.json

# Comparaisons d'amplitude et de justesse appariées
python -m research.representation_ablation.panel \
  --inputs /tmp/d1_public_s2b.json /tmp/h1_public_s2b.json /tmp/m1_public_s2b.json \
  --output /tmp/public_s2b_panel.json --markdown /tmp/public_s2b_panel.md
~~~

Attention : si ces chemins existent déjà, les runners
refusent de les écraser. Les mêmes sorties doivent
être conservées avec commit Git, origine, cohorte
et graines. Comparer D1/H1/M1 **par horizon**.

## Prochaines étapes scientifiques
1. Vérifier et consolider H1/M1 depuis le runner
   **public**, contrôler les checksums des 16 gzip.
2. Mettre les tableaux S2b direction + amplitude sur
   trois horizons, sans choisir un gagnant sur
   1 graine / 40 updates.
3. Étendre à 3 graines et 200 updates pour
   S2b, puis recherche S3 grammaires (issue #20).
4. Enregistrer les exceptions licence et différences
   de cohorte ; ne pas confondre un test « source
   réelle » et une validation indépendante.
