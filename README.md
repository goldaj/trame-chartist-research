# TRAME — recherche sur un modèle chartiste génératif

Projet scientifique indépendant du bot BTC-PERP Hyperliquid. TRAME étudie comment représenter des courbes de marché comme un langage causal, puis comparer des architectures génératives de type GPT sur la prédiction de prix bruts. L'étude concerne plusieurs marchés et ne constitue pas une stratégie de trading déployée.

## Reprise scientifique du 25 octobre 2026

**Exécution reprise sur instruction explicite de l'utilisateur.**
[Tableau de bord actif pour Codex](docs/CODEX_EXECUTION_BOARD_20261025.md),
[protocole A3c](research/architecture_comparison/A3C_PROTOCOL_20261025.md),
[PR #10](https://github.com/goldaj/trame-chartist-research/pull/10).

Priorité A3c : mesurer les coûts, étendre les contextes et comparer des
budgets *sans prétendre que les FLOPs partiels couvrent toutes les
opérations*. Puis A4 Mamba-2/Mamba-3, A5 hybrides, A6 modèles
temporels, A7 essais BTC, A8 Research Lab et phases produit P1–P4.
Aucune preuve financière ni produit Predictive v1 n'est encore livrée.
Le document de pause d'origine est conservé comme archive
chronologique et n'est plus l'instruction active.

## État réel au 16 octobre 2026

Édition 2.4 : quatorze documents et un dossier consolidé de 102 pages. La conception du langage et les audits de données réelles sont engagés. Aucun modèle génératif n'a été entraîné et aucun avantage prédictif n'est démontré. Les tests synthétiques vérifient les outils de mesure ; ils ne sont pas des observations de marché.

## Parcours de lecture

- [Index scientifique et état courant](dossier/recherche_lcm/LIRE_EN_PREMIER.md)
- [Synthèse accessible](dossier/recherche_lcm/00_synthese_accessible.md)
- [Dossier PDF consolidé](output/pdf/TRAME_Dossier_complet.pdf)
- [Bibliographie](dossier/recherche_lcm/BIBLIOGRAPHIE_LIENS.md)
- [Journal des versions](dossier/recherche_lcm/JOURNAL_DES_VERSIONS.md)
- `research/` : protocoles, scripts d'acquisition, audits et rapports de qualification.
- `tools/pdf/` : générateurs historiques des documents, avec conventions de chemins à adapter avant réutilisation.

## Données et reproduction

Les données brutes téléchargées et archives complètes restent sur le poste local et sont exclues de Git dans l'attente d'une revue des droits de redistribution de chaque fournisseur. Les scripts, URLs de provenance et empreintes permettent d'en retrouver l'origine. Les liens vers les archives ZIP dans les documents historiques ne sont donc utilisables que dans la copie locale complète. Cette séparation ne modifie ni les documents scellés ni leurs conclusions.

Tests du premier appareil de mesure : depuis `research/trame_poc0`, exécuter `python -m unittest test_research` avec NumPy installé. Les contrôles datés ont leurs propres instructions ; ne pas ouvrir des partitions de test pour une simple vérification de dépôt.

## Relation au bot

[hyperliquid-btc-pilot](https://github.com/goldaj/hyperliquid-btc-pilot) reste un projet distinct. Aucune intégration au bot, aucun déploiement ni aucune transaction ne découle de cette publication.

Les fichiers d'origine sont conservés dans leur ancien dossier pour préserver les liens des conversations existantes. Pour la suite, utiliser ce dépôt comme source de vérité TRAME ; ne pas développer les deux copies en parallèle.

## P1-B0 : premiers développements scientifiques, 25 octobre 2026

La branche expérimentale `chatgpt/p1b0-numerical-lab-20261025`
contient un [véritable laboratoire numérique](research/p1b0_numerics/README.md)
reproductible : probabilités de cellules gaussiennes en **log-espace**,
normalisateur BASE/FLAT/HIER sur 4096 codes, dérivées des corrections,
échantillonnage et garde-fous de valeurs extrêmes.

**Résultats observés uniquement sur objets mathématiques construits :**
15 cas de stress normalisés (erreur max 3,33 × 10^-16), 15 tests,
entraînement de corrections sur mélange artificiel et simulation causale
de 20 pas avec CRPS en prix fictifs. Le laboratoire a aussi mis en
évidence une limite réelle de float64 : une probabilité de queue
non nulle en log-espace peut devenir nulle lors du tirage.

Ceci **n'entraîne pas de GPT sur un marché**, ne valide aucune prévision
boursière et ne déverrouille aucun jeu de test. Les documents scellés
des éditions précédentes sont inchangés. Voir le README du laboratoire
pour les commandes, chiffres, hypothèses et limites.

## Étape 1 P1-B0 : qualification de la différentiabilité

La branche `chatgpt/p1b0-stage1-validation-20261025` (superposée à
la PR #2) ajoute les gradients complets de la tête en PyTorch, les
stress tests de queues, les métriques de calibration et les mesures de
CPU. Lire [l'avis Go/No-Go et les sous-étapes 2.1–2.7](research/p1b0_numerics/STAGE1_DECISION_20261025.md).
**Go limité : premier mini-modèle sur données artificielles seulement**.

## Étape 2 : mini-Transformer expérimental

La branche `chatgpt/mini-transformer-synthetic-20261025` contient
[le premier entraînement autoregressif synthétique](research/mini_gpt_synthetic/README.md)
avec oracle exact, témoin linéaire entraîné sur train seulement,
masque causal et ablations initiales BASE/HIER/FLAT.
**Aucune prévision de marché ni classement de modèles financier.**

## Étape 3 : contrat de données historiques

Le [rapport de l'étape 3](research/market_data_contract/STAGE3_REPORT_20261025.md)
contient un modèle `as-of` et un encodage P1-D causal testés sur
fixtures artificielles. **Toutes les sources réelles restent bloquées**
faute de garanties vérifiées pour les droits et millésimes : pas de
rétroqualification artificielle d'un ancien CSV en test indépendant.

## Étape 4 : comparaison appariée et bootstrap

La [note étape 4](research/benchmark_synthetic/STAGE4_REPORT_20261025.md)
décrit les comparaisons de prix natifs **sur fixtures synthétiques**,
avec bootstrap par blocs et séparation stricte actif/horizon.
**Go** pour un atelier de recherche offline ; **No-Go** pour
les étapes financières réelles 5–7 sans source, benchmark et holdout qualifiés.


## Décision du 25 octobre 2026 — TRAME multi-architectures

Ne pas présupposer que le Transformer original est le meilleur pour
la prévision de prix : tous les futurs travaux doivent suivre
[le protocole multi-architectures](research/architecture_comparison/README.md).
Première étude de câblage : Transformer causal, GPT-style miniature,
GRU, mêmes données synthétiques et mêmes mini-lots ; **aucun bras
Mamba/LLM pré-entraîné** encore exécuté. Les conclusions restent
strictement exploratoires et hors finance réelle.


## Référentiel de données financières (25 octobre 2026)

TRAME utilise désormais comme source Bitcoin de référence la
[release versionnée du dépôt privé btc-historical-data](https://github.com/goldaj/btc-historical-data/releases/tag/btcusd-bitstamp-2010-2026-reference-v1),
avec D1 dès juillet 2010, H1 et M1 à partir de 2012.

Le code ne recopie pas les prix dans ce dépôt public. Le composant
[BTC Release Store](research/btc_h1_m1/README.md) télécharge
uniquement les assets nécessaires vers le cache local de
l'utilisateur authentifié via GitHub CLI, puis les relit en streaming.
La CI publique ne touche jamais au dépôt privé.

Cette source remplace les snapshots du bot Hyperliquid et ses
artéfacts temporaires. Les données sont acceptées en l'état par
le propriétaire : pas de nouvel audit de provenance. Les
résultats exploratoires ne valent pas validation de trading.
