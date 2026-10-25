> **ARCHIVE HISTORIQUE : PAUSE LEVÉE LE 25 OCTOBRE 2026.**
> L'ordre utilisateur ultérieur demande de **reprendre** TRAME et
> d'avancer sous-tâche par sous-tâche. L'instruction active figure dans
> [`CODEX_EXECUTION_BOARD_20261025.md`](CODEX_EXECUTION_BOARD_20261025.md)
> et `AGENTS.md` sur la branche de PR #10. Les mentions d'arrêt
> ci-dessous sont conservées comme preuve historique, non comme
> consigne en vigueur.

# TRAME — point d'arrêt et feuille de route pour Codex

**Décision utilisateur du 25 octobre 2026 : EXÉCUTION EN PAUSE.**  
**Statut de ce document : passation documentaire seulement.**
Ne pas reprendre les expériences, entraîner, télécharger de modèles/données, ouvrir les jeux réservés, fusionner des PR ou démarrer un déploiement au seul motif que ce document existe. **Attendre une nouvelle instruction explicite de reprise.**

## 1. Résumé exécutable en une minute

La parenthèse sur les données BTC est terminée : une release versionnée dans le dépôt privé
`goldaj/btc-historical-data` fournit les sources D1/H1/M1. TRAME public possède un
adaptateur/cache, **aucune copie des archives de prix**. La prochaine tâche scientifique
à reprendre est **A3c : achever une comparaison de coûts/compute réellement équitable**
entre les trois premières familles déjà câblées, puis **A4 : intégrer de véritables
Mamba-2 et Mamba-3**.

Ce travail vise à comparer les modèles selon des preuves, **pas à démontrer qu'un
Transformer ou un LLM moderne est forcément supérieur**. La validation sur de
vrais cours, la robustesse et la valeur économique viendront après, avec témoins et
partitions contrôlées. Aucun modèle gagnant financier ni bot de production n'existe.

**Sources à lire dans cet ordre** :
1. `AGENTS.md` (règles permanentes) ;
2. **ce document** (pause, état, ordre de reprise, critères de sortie) ;
3. `docs/CHATGPT_PROJECT_HISTORY.md` (décisions utilisateur et historique partiel) ;
4. `research/architecture_comparison/README.md` et
   `EXTERNAL_MODELS_ADMISSIBILITY_20261025.md` (protocole et candidats) ;
5. `research/btc_h1_m1/README.md` (release privée, cache et précautions) ;
6. `research/market_data_contract/STAGE3_REPORT_20261025.md`,
   `research/benchmark_synthetic/STAGE4_REPORT_20261025.md` et
   `research/trame_lab/README.md` (portes scientifiques/produit).

## 2. État observé au point d'arrêt

| Chantier | État au 25/10/2026 | Preuve / limitation |
| --- | --- | --- |
| A1 : registre multibras, invariants causaux | Fait pour le laboratoire synthétique | `research/architecture_comparison/README.md` |
| A2 : comparateur Transformer / GPT-style / GRU | Fait pour données fabriquées | `experiment.py`, tests, 3 seeds, tableau Research Lab ; pas de marché |
| A3a : alignement approximatif des paramètres | Fait, diagnostic limité | ~2 610 / 2 418 / 2 602 paramètres ; pas de FLOPs alignés |
| A3b : profils de coûts CPU | Premier diagnostic fait | `cost_audit.py`, largeurs 8/16/32, forward et backward ; machine spécifique |
| **A3c : budgets compute-fair** | **NON COMMENCÉ / À REPRENDRE** | FLOPs/MACs, pic mémoire, latence, séquences longues, budgets d'entraînement |
| A4 : Mamba-2 + Mamba-3 réels | Non implémenté | GRU n'est ni Mamba ni SSM sélectif |
| A5 : hybrides attention/SSM et décodeurs | Non implémenté | Aucun équivalent industriel revendiqué |
| A6 : TimesFM-3 / Chronos-2 / Moirai-2 | Qualification documentaire seulement | Pas de poids téléchargés ni évalués |
| A7 : évaluation BTC réelle et multi-actifs | Infrastructure BTC préparée, **pas de campagne réelle validée** | Données D1/H1/M1 accessibles sur machine autorisée ; source BTC distincte d'un banc point-in-time multi-actifs certifié |
| A8 : Research Lab | Démonstrateur HTML/JSON synthétique en place | À étendre aux comparatifs réels, sans masquer les limites |
| TRAME Predictive v1 | **Non livré** | Recherche prédictive, évaluation et packaging restant à faire |

**Git / chaîne de travail** :
- PR #8 (draft), `chatgpt/trame-multi-architecture-20261025` :
  https://github.com/goldaj/trame-chartist-research/pull/8
- PR #9 (draft), `chatgpt/btc-h1-m1-20261025`, **basée sur la PR #8** :
  https://github.com/goldaj/trame-chartist-research/pull/9
- Les PR antérieures forment elles aussi une chaîne de dépendances. **Pas de merge
  automatique, de changement de base improvisé ni de réouverture des audits scellés.**
- La branche historique `chatgpt/btc-history-bridge-20261025` a été abandonnée :
  ne pas utiliser son chargeur D1 comme nouveau point de départ.
- Ce document est ajouté sur la branche supérieure #9 pour être présent dans
  la passation accumulée. Ne pas supposer qu'il est déjà sur `main`.

## 3. Ordre de reprise prévu (ne PAS exécuter durant la pause)

### A3c — Consolider les comparaisons compute-fair (première tâche)

1. **A3c.1, contrat de mesure** : figer la tâche, les horizons, origines,
   représentations, tailles de contexte, precision/dtype, hardware, seeds,
   batchs et critères d'arrêt. Séparer comparaison « mêmes mini-lots »
   (test de câblage) de comparaison « même budget compute » (science).
2. **A3c.2, instrumentation** : compter paramètres totaux/actifs et
   FLOPs ou MACs *avec méthode documentée* ; mesurer pic mémoire CPU/GPU,
   latence d'inférence, débit et coût forward+backward. Identifier les
   opérations non couvertes ou estimées par des proxies.
3. **A3c.3, échelles** : évaluer plusieurs largeurs et longueurs de
   contexte, pas seulement les huit codes et trois largeurs de l'actuel
   micro-benchmark. Distinguer chauffe, CPU, GPU, noyaux, transfert et I/O.
4. **A3c.4, budgets appariés** : prédéclarer une grille de recherche
   d'hyperparamètres comparable, un budget par bras et des seeds
   répétées ; inclure les témoins statistiques.
5. **A3c.5, contrôles et décision** : tests de causalité/fuite, gradients,
   répétabilité, métriques et incertitudes ; publier le registre des
   exclusions, l'environnement, les coûts et les comparaisons appariées.
   **Sortie A3** : tableau reproductible expliquant *en quoi* la
   comparaison est équitable et ce qui ne l'est toujours pas.

Critère de sortie : un comptage de paramètres proche **ne suffit pas**.
Les simples durées CPU du prototype actuel ne suffisent pas non plus.
Aucun classement de prévision de marché ne découle d'A3c seul.

### A4 — Véritables SSM sélectifs

1. Requalifier versions officielles, API, licences, matériel et kernels
   de **Mamba-2 et Mamba-3** à la date de reprise.
2. Construire des bras réels isolés, compatibles avec le contrat
   expérimental commun ; documenter si un fallback CPU est fidèle ou
   limité. Ne pas renommer GRU en Mamba.
3. Vérifier causalité, shapes, sortie commune, gradients, reproductibilité,
   dépendances opt-in et comportement sur séquences longues.
4. Refaire le protocole A3 (budgets/latence/mémoire/seeds), puis décider
   quels bras retenir pour la suite, sans annoncer de vainqueur financier.

### A5 — Hybrides et décodeurs alternatifs

1. Prioriser hypothèses attention + SSM, attention linéaire, GQA/MoE,
   variantes de représentation et de têtes probabilistes.
2. Tester chaque bras sur **les mêmes origines, horizons et critères** ;
   distinguer modèle « inspiré de » et implémentation fidèle d'un tiers.
3. Comparer ablations, performances statistiques et coût réel ;
   documenter les bras reportés et leur justification.

### A6 — Modèles de fondation temporelle

1. Requalifier **TimesFM-3, Chronos-2 et Moirai-2** : version précise,
   code, licence **des poids**, contraintes d'usage, données de
   préentraînement, coût et éventuelle contamination des périodes testées.
2. Adapter les inférences aux tâches, unités, contextes, horizons et
   protocoles de disponibilité temporelle de TRAME.
3. Rapporter séparément `zero-shot/pretrained` et `from_scratch` :
   il est impossible de rendre identique le compute de préentraînement
   historique de modèles tiers. Exclure les poids non éligibles à la
   commercialisation du périmètre produit.

### A7 — Validation sur séries financières et méthode scientifique

1. **Démarrage exploratoire BTC possible seulement après la reprise** :
   utiliser la release privée épinglée, les lecteurs D1/H1/M1, et
   confirmer les contrats et résultats sur des runs effectivement
   exécutés ; ne jamais déduire un score réel d'une CI fictive.
2. Maintenir train/développement/test, ordres temporels et
   `available_at` sans look-ahead. La partition 2026 des premiers
   essais H1/M1 est **réservée**, non à explorer pour choisir des modèles.
   Toute évolution des partitions doit être documentée avant usage.
3. Conserver baselines (persistance, AR/Ridge, volatilité/quantiles),
   MAE/RMSE en prix natifs, CRPS/pinball/couverture/calibration et
   tests par régimes, horizon et contexte. H1 et M1 ne prédisent pas
   le même horizon ; ne pas comparer leurs NLL brutes.
4. **Ne pas confondre deux niveaux de preuve** : la demande utilisateur
   d'accepter les fichiers BTC sans réauditer leur provenance **n'est
   pas** une démonstration de disponibilité historique exacte,
   d'indépendance des tests ou de droits sur d'autres marchés. La
   qualification générale `stage 3.6` multi-actifs et la validation
   confirmatoire demeurent une porte séparée. Pas de pseudo-holdout.
5. Évaluer la robustesse aux régimes extrêmes, au transfert inter-actifs
   lorsque des sources sont disponibles, aux horizons et au coût. Puis
   geler une évaluation indépendante **avant** de regarder ses résultats.

### A8 — TRAME Research Lab utilisable

1. Étendre les rapports HTML/JSON versionnés aux résultats multibras
   scientifiques, incluant modèles/baselines, comparaisons appariées,
   graphes, intervalles, seeds, coûts, exclusions et artefacts.
2. Compléter audit navigateur/accessibilité, intégrité de la paire
   HTML/JSON, reproductibilité Windows/Linux/PyCharm.
3. Éviter toute formulation suggérant un avantage économique,
   un test indépendant ou une égalité de compute lorsque non établis.

### P1 à P4 — De la recherche au produit livrable

- **P1 — sélection et entraînement** : retenir plusieurs bras réellement
  prometteurs, améliorer représentations/horizons/têtes, tuning borné et
  checkpoints reproductibles ; ne pas sélectionner uniquement sur NLL.
- **P2 — robustesse indépendante** : généralisation hors échantillon,
  calibration, dérive, changement de régime, stress extrêmes,
  comparaisons statistiques et limites d'utilisation.
- **P3 — valeur économique** : simulations *offline* rigoureuses,
  coûts de transaction, spreads, glissement, disponibilité et règles
  ex ante ; une bonne prévision ne garantit pas une stratégie rentable.
- **P4 — TRAME Predictive v1** : interface et API *offline*,
  artefacts de modèles versionnés, installation reproductible,
  documentation utilisateur/technique, tests et revue des droits.
  **Aucune connexion au bot réel sans nouvelle décision explicite.**

Ces phases P1–P4 sont une projection produit et non les étapes
historiques numérotées 1–8 de TRAME ; ne pas confondre les nomenclatures.

## 4. Contrat des historiques BTC, sans relancer leur chantier

- Dépôt privé unique : `goldaj/btc-historical-data`.
- Tag fixé : `btcusd-bitstamp-2010-2026-reference-v1`.
- 21 assets : trois D1, un H1, quinze M1, manifeste et sommes SHA256.
- Pas d'archives committées dans TRAME public ; acquisition authentifiée
  **explicite** avec `gh` et cache **hors du clone**.
- Conserver les formats, les trous, les volumes nuls et la chronologie ;
  ne pas confondre les closes indicatifs anciens avec des OHLCV observés.
- **Instruction utilisateur : utiliser les fichiers en l'état, sans
  recommencer l'audit de provenance.** Respecter cette instruction.
- Le BTC/USD historique spot/indicatif ne représente pas les
  conditions d'exécution des perpétuels Hyperliquid.
- CI publique sans token privé et sans archive de cours réels.

Voir `research/btc_h1_m1/README.md` pour les commandes déjà câblées.
Durant la pause, **ne lancer aucune de ces commandes**.

## 5. Mode opératoire pour Codex après autorisation de reprise

1. Relire ce document et **vérifier le HEAD réel des PR #8/#9**
   et de leurs bases ; les fichiers et statuts peuvent avoir évolué.
2. Confirmer explicitement dans la PR/issue de reprise quelle sous-étape
   est ouverte. **Première sous-étape nominale : A3c.1**, puis avancer
   par baby steps documentés ; prévenir l'utilisateur à chaque jalon.
3. Créer une branche dédiée appropriée et une PR **draft** sans merge
   implicite ; ne pas écraser le travail parallèle de Codex ou
   d'autres agents. Préserver l'historique exact de dépendances.
4. Pour chaque modification : tests adaptés, reproductibilité, liens vers
   preuves, résultats authentiques vs fictifs, Go/No-Go, limitations et
   prochaines sous-étapes ; mettre à jour `AGENTS.md`, le registre,
   ce handoff et `docs/CHATGPT_PROJECT_HISTORY.md` si pertinent.
5. Ne jamais modifier le bot Hyperliquid, ouvrir le holdout réservé,
   envoyer d'ordres, divulguer de secrets, prétendre avoir testé des
   données réelles sans exécution ou rapprocher des métriques
   hétérogènes comme si elles étaient comparables.

**Dernier ordre de l'utilisateur : pause de l'exécution. Aucun des points
ci-dessus n'est une autorisation de développement autonome.**
