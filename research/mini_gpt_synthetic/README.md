# Étape 2 TRAME : mini-Transformer autoregressif et expériences synthétiques

**25 octobre 2026.** Code effectivement exécutable en CPU, uniquement sur
codes fabriqués. Ce n'est ni le Transformer P1-D/P1-B0 complet ni une
démonstration de prévision financière.

## Résultats techniques et état des sous-étapes

| Sous-étape | Acquis |
| --- | --- |
| 2.1 Corpus synthétique | Loi génératrice explicite k[t]=round(0.75*k[t-1]+Normal(0,3)). Flux de train (192), développement (96), test synthétique réservé (96) à graines distinctes ; accès au dernier interdit par défaut |
| 2.2 Backbone | Transformer autoregressif CPU f64, 1 couche, largeur 16, 2 têtes, masque causal, codes précédents et BOS implicite zéro |
| 2.3 Test causalité | Perturber les entrées futures ne modifie pas les distributions antérieures ; backward fini et poids réellement modifiés |
| 2.4 Apprentissage | 40 mises à jour AdamW à graines fixes ; NLL train/développement produit dans artefact CI |
| 2.5 Témoins | Oracle de la loi de génération, persistance probabiliste mu=0 dont sigma est appris uniquement sur train, et régression linéaire conditionnelle ajustée uniquement sur train |
| 2.6 Ablation initiale | Têtes BASE/HIER/FLAT liées au même backbone; correction bornée, normalisateur complet à 4096 termes et cibles hors dictionnaire conservées. 6 mises à jour et mêmes minibatchs par bras sur séquences de 8 codes et 16 chemins de développement ; **capacités et FLOPs différents** |
| 2.7 Rapport | Ce document, code, tests, CI, passage vers étape 3 **uniquement pour la préparation des données** |

## Conditions et honnêteté scientifique

- La loi connue AR(1) a un **oracle exact** : conditional normal arrondie
  de moyenne 0.75 fois le code antérieur et sigma 3.
- Le modèle BASE calcule directement la masse de cellule sans sommer
  les 4096 états : avec corrections identiquement nulles, Z=1 **en
  arithmétique exacte**. Le benchmark HIER/FLAT **doit**, lui,
  sommer le normalisateur entier.
- La causalité se rapporte aux **codes précédents seulement**, non
  à l'information complète P1-D de 256 points et six devises.
- Le développement sert à diagnostiquer et pourrait conduire à
  modifier la méthode. Ne jamais le baptiser « test indépendant ».
  L'ensemble \`reserved_synthetic_test\` n'est pas ouvert par les
  scripts de CI et ne doit pas être ouvert pour une retouche.
- Les contrôles fort (oracle et modèle linéaire train-only) sont
  présents même si les résultats sont négatifs pour le Transformer.
- L'ablation des trois têtes ne constitue PAS une comparaison
  compute-fair : 4096 sorties FLAT contre 518 sorties HIER et
  deux sorties BASE, tailles et FLOPs affichés par l'expérience.
- Aucun checkpoint n'est encore proposé pour marchés réels et
  aucune stratégie de trading ne découle du score NLL synthétique.

## Exécution et artefacts

~~~bash
python -m pip install 'numpy==2.3.5' 'scipy==1.17.0'
python -m pip install 'torch==2.10.0' --index-url https://download.pytorch.org/whl/cpu
python -m unittest discover -s research/mini_gpt_synthetic -p 'test_*.py' -v
python -m research.mini_gpt_synthetic.experiment --steps 40 > stage2_development.json
python -m research.mini_gpt_synthetic.ablation > stage2_ablation.json
~~~

La CI \`.github/workflows/trame-mini-transformer.yml\` exécute
ces commandes avec succès et conserve les deux JSON en artefact.
Il est volontairement interdit d'affirmer de chiffres
d'apprentissage sans citer le JSON/commit exact. Aucun benchmark
CPU d'ablation ne peut se généraliser automatiquement au GPU.

## Verdict de recherche

**Go limité pour l'étape 3** : contracter les sources, leurs droits
et leurs calendriers de disponibilité, préparer un validateur de
corpus qui empêche fuite de futur et révisions silencieuses.
**No-Go** pour entraîner un grand modèle sur vrai marché, réserver un
test indépendant, publier une performance financière ou ouvrir une
API de négociation ; le benchmark synthétique ne justifie rien
de tel.

## Étape 3 : sous-étapes proposées et exécutables

3.1. Déclarer les familles de marché et fournisseurs admissibles
     dans un manifest légal et point-in-time ; identifier les
     permissions de redistribution, l'unité et l'horodatage connu.
3.2. Spécifier schéma machine d'une observation : date d'événement
     **et** date de première disponibilité, source, unité,
     révisions, qualité, identification stable.
3.3. Construire un validateur sur mini-fixtures synthétiques :
     doublets, ordre, valeurs non-positives, missing, révisions,
     connaissance au moment de l'origine.
3.4. Proposer splits temporels à purge explicite des labels
     et du contexte, auditables sur tables de métadonnées seules.
3.5. Vérifier les calculs du codec TRAME et de son échelle
     exclusivement sur passée disponible.
3.6. Acquérir seulement les séries dont droits, point-in-time et
     provenance sont vérifiés ; pas de source externe implicite.
3.7. Publier une fiche de qualité par source, lacunes et veto
     vers entraînement. Une absence de source licite est
     un **No-Go documenté**, pas un permis de bricoler le test.

## Codex

La branche \`chatgpt/mini-transformer-synthetic-20261025\` est
superposée à \`chatgpt/p1b0-stage1-validation-20261025\`,
elle-même superposée à la PR #2. Ne jamais squasher sans maintenir
la traçabilité. Le journal \`docs/CHATGPT_PROJECT_HISTORY.md\`
doit être continué ; conserver chaque contre-exemple.
