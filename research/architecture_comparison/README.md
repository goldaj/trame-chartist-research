# TRAME — protocole obligatoire multi-architectures (v0.1)

**Date : 25 octobre 2026. Nouvelle consigne utilisateur : comparer en parallèle
les approches classiques et les familles des LLM récents.**

## Clarification technique

« Autorégressif » est un **objectif/factorisation de prévision** (le prochain
élément dépend du passé), pas une architecture obsolète. Les GPT modernes sont
majoritairement des modèles *decoder-only* causaux et autorégressifs.
En revanche, un mini-`TransformerEncoder` masqué de 2026 n'est **pas**
automatiquement l'architecture d'un LLM industriel moderne. Les variantes
RMSNorm, RoPE, GQA, SwiGLU, MoE, attention linéaire et hybrides/SSM sont des
hypothèses distinctes à comparer selon les preuves et le budget.

L'objectif scientifique ne devient pas « prouver un Transformer » mais
**comparer les représentations, objectifs, architectures et têtes de sortie
sur un protocole commun**, tout en gardant les contrôles statistiques.

## Registre des familles, sans sélection anticipée du vainqueur

| Famille | Premier bras | État | Limites |
| --- | --- | --- | --- |
| Persistence / AR / Ridge / volatilité, oracle si synthétique | `research/mini_gpt_synthetic/experiment.py` | témoins partiels | pas encore panel financier réel |
| Transformer causal 2017–2024 | `MiniTRAME` | fonctionnel synthétique | 1 couche, 16 dimensions |
| Décodeur GPT-style modernisé | `ModernGPTMini` | fonctionnel synthétique | RoPE, RMSNorm, GQA, SwiGLU miniatures ; non préentraîné |
| Récurrent traditionnel | `GRUMini` | fonctionnel synthétique | GRU n'est **pas** Mamba ni xLSTM |
| SSM sélectifs | Mamba-2 | **prévu, pas implémenté** | vérifier kernels, CPU/GPU, causalité |
| Hybride SSM + attention / attention linéaire | Qwen3-Next / Jet-Nemotron inspirés | **prévu, pas implémenté** | ne pas déclarer fidèle sans implémentation validée |
| Time-series foundation models | TimesFM-3, Chronos-2, Moirai-2 | **évaluation prospective** | licence de poids, contexte, fréquence, données d'entraînement inconnues et contamination |
| Modèles probabilistes alternatifs | mixture, quantiles, flows / diffusion | **à étudier** | rendre comparables densités, CRPS et calibration |

**Architecture et objectif d'entraînement doivent être séparés** :
une architecture non autorégressive peut prédire plusieurs horizons directement ;
une autre peut générer un chemin un pas après l'autre. Elles doivent être
comparées sur le **même problème final** (horizons, calendrier, prix natifs,
distribution, délai et coût), sans assimiler leur NLL de tokens différentes.

## Règles permanentes applicables à TOUTES les prochaines étapes TRAME

1. Toute expérience a un manifeste immuable : `architecture_id`,
   `family`, `representation_id`, `forecast_objective`,
   `output_distribution`, `split_version`, `origin_policy`,
   `training_budget`, `seed`, `code_commit`, `environment`,
   `data_rights` et `as_of_evidence`.
2. Même train/développement/test, mêmes origines et cibles éligibles,
   aucune fuite de `available_at`, aucune modification après examen du holdout.
3. Deux niveaux de comparaison séparés :
   **A. mêmes pas/minibatchs** pour vérifier le câblage ;
   **B. même compute/latence/mémoire et recherche d'hyperparamètres**
   (avec plages pré-déclarées) pour les conclusions d'architecture.
   Le niveau A ne permet **aucun** classement scientifique final.
4. Retenir la persistance, AR/Ridge et les probabilités naïves comme témoins ;
   le meilleur résultat ne peut jamais être présenté seul.
5. Scores obligatoires selon sortie : MAE/RMSE native par actif-horizon,
   CRPS/pinball/couverture/fiabilité probabiliste, coût GPU/CPU,
   mémoire max, temps de prévision, comportement extrême.
   Distinguer métriques point forecast, distributions et génération de chemins.
6. 3–5 seeds au minimum pour une exploration raisonnable ; plus au stade
   confirmatoire avec budget préenregistré. Comparaison appariée/blocs,
   risques de tests multiples, dérive de régimes et calibration.
7. Tester séparément transfert inter-actifs, horizons, contextes longs et
   prévisions pendant régimes extrêmes, après acquisition d'une source
   point-in-time qualifiée. Interdire tout pseudo-holdout fabriqué à
   partir de données déjà explorées.
8. Les poids préentraînés externes forment un bras `pretrained/zero-shot`
   séparé des modèles `from_scratch`. Auditer entraînement antérieur,
   accès aux observations évaluées, licences et traitements de données ;
   ne jamais revendiquer la même consommation de calcul historique.
9. Chaque PR/étape future met à jour le registre avec **bras inclus,
   bras différés, raisons et preuves de contrôle**. N'interrompre la
   comparaison qu'avec une justification et un Go/No-Go explicites.
10. Aucun pipeline n'est relié au bot Hyperliquid, ni exécuté contre
    un portefeuille ou un marché en production par ce protocole.

## Premier essai branché au dépôt

```bash
python -m unittest discover -s research/architecture_comparison -p "test_*.py" -v
python -m research.architecture_comparison.experiment --steps 20 --seeds 20261025 20261026 20261027 > synthetic_architectures.json
```

Entrées : le générateur **artificiel** AR(1) déjà présent en étape 2.
Trois bras utilisent `float64`, la même sortie gaussienne arrondie BASE,
les mêmes mini-lots par seed, AdamW et les mêmes tests de causalité. Le
programme refuse les seeds dupliquées et n'ouvre jamais
`reserved_synthetic_test`. Le JSON affiche le nombre de paramètres
et la durée CPU pour rendre visibles les différences.

Le bras moderne est **une miniature GPT-style entraînée de zéro**, non
un modèle GPT commercial, Qwen, Mamba ou TimesFM.
Le GRU est un témoin récurrent. Aucun résultat réel, ni tableau
de performance prédictive financière. **Capacités et FLOPs non égalisés**.

Les tests valident l'invariance aux entrées futures, les dérivées finies
et la répétabilité de pertes (pas le temps d'exécution). Ne jamais
se servir de ce mini-corpus pour sélectionner « la meilleure
architecture financière ».

## Sous-étapes scientifiques suivantes

- **A1** : finir le registre et les invariants causaux (cette PR).
- **A2** : mettre un comparateur expérimental 3 bras (cette PR, premier essai).
- **A3** : mesurer FLOPs, mémoire, nombre de paramètres, temps inférence et
  élargir les tailles pour isoler les effets capacité/compute.
- **A4** : ajouter Mamba-2/SSM sur une branche dédiée, avec dépendances
  et variantes CPU/GPU explicites ; ne pas appeler une GRU « Mamba ».
- **A5** : hybrides attention/SSM et variantes de décodeur, même tête P1-B0.
- **A6** : analyser les modèles spécifiques aux séries chronologiques
  (TimesFM-3, Chronos-2, Moirai-2), leurs licences et contamination.
- **A7** : évaluation financière multi-actifs exclusivement une fois
  l'étape 3.6 admissible, puis gel confirmatoire.
- **A8** : affichage comparatif et export versionnés dans Research Lab,
  avec avertissements de statut et exclusions.

## Sources primaires consultées (ne pas inférer leurs performances sur TRAME)

- Dao & Gu, ICML 2024, Mamba-2 / SSD :
  https://proceedings.mlr.press/v235/dao24a.html
- NVIDIA, comparaison empirique Mamba / Transformer / hybride :
  https://research.nvidia.com/publication/2024-06_empirical-study-mamba-based-language-models
- Qwen Team, Qwen3-Next hybrid attention / MoE / multi-token (2025) :
  https://qwen.ai/blog?id=qwen3-next
- NVIDIA, Jet-Nemotron (2025), variantes attention :
  https://research.nvidia.com/labs/eai/publication/jetnemotron/
- Google Research, TimesFM-3 (31 août 2026), séries multivariées :
  https://www.research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/

Lire les publications et licences sources **à la date de toute intégration** ;
la popularité en NLP ou sur séries généralistes n'est pas une preuve
de qualité pour des cours financiers ni d'une propriété de long terme.
