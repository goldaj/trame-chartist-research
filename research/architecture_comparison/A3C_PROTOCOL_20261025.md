# A3c : plan préenregistré de comparaison de coût des architectures

Statut : **en cours, commencé le 25 octobre 2026** après autorisation explicite
de reprise par le propriétaire. Aucune conclusion financière n'est autorisée.

## Hypothèse scientifique
Le rapprochement du nombre de paramètres (A3a) et les durées sur 8
trajectoires de 8 tokens (A3b) ne démontrent pas une égalité de budget de
calcul, ni un effet architectural. La comparaison exige des témoins,
la même tâche et une comptabilité transparente du coût.

## Sous-tâches / portes de sortie

- [x] **A3c.1 : figer le périmètre expérimental.**
  Origine artificielle AR(1), mêmes partitions train/development,
  aucune utilisation du test réservé, même entrée x/cible y
  et même tête BASE gaussienne arrondie. Les trois bras actuels sont
  `MiniTRAME`, `ModernGPTMini` et `GRUMini`. CPU float64, un
  thread ; contrôler les graines, nombres de paramètres, contextes
  et budget. Les chronomètres et le profiler sont des instruments,
  pas une métrique de qualité prédictive.
- [x] **A3c.2 : instrumentation** des opérations, allocations et temps ;
  comptage explicite de la couverture des FLOPs. Des FLOPs omis ne
  valent pas zéro. Les périodes profilées excluent téléchargement,
  entraînement préalable et préparation des données.
- [x] **A3c.3 : diversité de tailles/contextes** ; mesurer des contextes
  courts à la limite actuelle 20. Une séquence plus longue nécessite
  d'abord une évolution des trois implémentations et tests causaux.
- [x] **A3c.4 : pilote à budget proxy uniquement** sur plusieurs graines, choix de
  configurations piloté par les coûts mesurés sans sélectionner sur le
  développement du test réservé ; vérifier les mêmes cibles et
  le coût du tuning. Deux comparaisons séparées : mêmes pas de
  gradient (diagnostic) et budgets compute/tuning (analyse).
- [x] **A3c.5 : publier les résultats et limites** dans artefacts
  JSON et Research Lab, avec `environment`, commit, seeds, exclure
  les faux classements de marchés ; comparer contre baselines
  classiques lors de l'étape financière.

## Définition de « terminé »

1. Mesures obtenues sur une infrastructure explicitée et code testé.
2. Paramètres totaux/actifs, durée d'entraînement, débit, mémoire et
   FLOPs comptabilisés avec taux de couverture déclaré.
3. Plusieurs tailles, au moins trois graines, intervalles/dispersion,
   budget de tuning documenté et parité d'origines et de cibles.
4. Aucune revendication d'égalité FLOPs si les noyaux non comptabilisés
   rendent la comparaison inexacte.
5. Les résultats synthétiques ne deviennent pas des performances BTC.

## Décisions gelées, sans débloquer le holdout

Les coûts sont mesurés sur les mêmes données synthétiques de *train*.
Les distributions de développement peuvent servir au diagnostic sans
ouvrir le `reserved_synthetic_test`. L'historique privé BTC
`btcusd-bitstamp-2010-2026-reference-v1` est destiné aux phases
financières exploratoires ultérieures, non à calibrer ce micro-benchmark.

## Matrice minimale envisagée

| Variable | Premier niveau | Extension |
| --- | --- | --- |
| Famille | Transformer original, GPT-style, GRU | Mamba-2/3, hybrides |
| Largeur | 8, 16, 32 (A3b) | grilles paramètre/compute comparables |
| Contexte | 8, 16, 20 (limite actuelle du modèle) | 32/64/128 après élargissement du contrat |
| Device | CPU float64, un thread | GPU séparé, kernels et precision explicités |
| Mesure | forward, forward+backward, pic mémoire, operations instrumentées | tuning à budget fixe et compteurs matériels |
| Validité | 3 à 5 graines au minimum | contrôle d'incertitude puis campagnes confirmatoires |

## Notes d'ingénierie pour Codex

- `research/architecture_comparison/cost_audit.py` et ses tests :
  conserver le premier diagnostic A3b. Développer une **étude A3c
  séparée**, pas un changement silencieux de la sémantique ancienne.
- L'API `MiniTRAME(length=20)` limite explicitement les contextes
  à 20 tokens. Les prototypes modernes aussi. Ne pas prétendre
  profiler du contexte 256 tant qu'ils le refusent.
- Ne jamais confondre FLOPs de certains opérateurs vus par le profiler
  et FLOPs complets incluant softmax, normalisation, activations,
  fonctions spéciales de la NLL, changements d'implémentation ou
  passes arrière.
- Tests unitaires/CI CPU sans secrets ni données BTC réelles.
- Documenter code, versions, tailles, vitesses et limites dans la PR
  et `docs/CHATGPT_PROJECT_HISTORY.md`.


## Résultat d'A3c : GO exploratoire / NO-GO compute-fair conclusif

Voir [`A3C_RESULTS_20261025.md`](A3C_RESULTS_20261025.md) :
A3c.1–3 livrés ; A3c.4 est **un pilote à budget d'opérations
incomplètement comptées**, pas une égalisation intégrale FLOPs;
A3c.5 documente les résultats et le **No-Go** pour tout classement
scientifique ou financier. Les critères plus ambitieux de la
« Définition de terminé » restent **ouverts** avant une comparaison
compute-fair validée. A4 peut démarrer en tant que voie expérimentale,
pas comme exploitation d'un résultat définitif.
