# A4 — vrais moteurs Mamba-2 et Mamba-3 (voie GPU séparée)

**25 octobre 2026. A4.1 : qualification documentaire effectuée.**
A4 n'a pas pour objet d'imposer un SSM aux données financières.
Il s'agit de tester des moteurs SSM *officiels*, confrontés aux témoins
Transformer/mini-GPT/GRU, sur **la même tâche** et avec un budget
quantifié. Le GRU n'est pas et ne sera jamais appelé « Mamba ».

## A4.1 : état de l'implémentation officielle

Source du fournisseur : https://github.com/state-spaces/mamba  
Référence GitHub release v2.3.2.post1 (09/05/2026) :
https://github.com/state-spaces/mamba/releases/tag/v2.3.2.post1  
Licence du dépôt de code : **Apache-2.0** au contrôle du 25/10/2026
(licences de paquets tiers à examiner séparément).

Exemples API officiels à cette date :

```python
from mamba_ssm import Mamba2, Mamba3
Mamba2(d_model=64, d_state=64, d_conv=4, expand=2)
Mamba3(d_model=64, d_state=128, headdim=64,
       is_mimo=False, chunk_size=64, dtype=torch.bfloat16)
```

Le deuxième exemple ci-dessus est une **hypothèse d'intégration
TRAME en largeur 64**. L'exemple fournisseur Mamba-3 est plus grand
(768 dimensions), emploie MIMO, bf16 et CUDA. La variante
SISO/largeur 64 ne doit pas être réputée validée avant un
véritable *smoke test* GPU/gradients : ce n'est pas un benchmark
fidèle au modèle fournisseur de référence.

La branche `main` officielle documente Mamba-3 dans
`mamba_ssm/modules/mamba3.py` ; le fournisseur recommande
l'installation depuis les sources pour cette architecture,
alors que ses wheels et kernels peuvent dépendre strictement
du couple CUDA / PyTorch / machine.

Préconditions **réelles** pour valider A4 :
- Linux avec GPU NVIDIA, CUDA compatible et pilote, PyTorch CUDA ;
- `torch.cuda.is_available()` et prise en charge effective du bf16 ;
- bibliothèques `mamba-ssm`, kernels Triton/CUDA et dépendances
  installées dans un environnement **isolé**, versions et commit
  exacts gelés ; revue `pyproject.toml` du dépôt fournisseur ;
- essai complet *forward*, forme, gradient, causalité par perturbation
  des entrées futures, pertes finies et comparaison coût/mémoire ;
- pas d'installation Mamba dans la CI CPU de TRAME ;
- pas de création de faux résultats GPU par simulations/mocks.

## A4 : décomposition des sous-tâches

- [x] **A4.1** : vérifier officiel Mamba-2 / Mamba-3, versions,
  API et licences documentaires. À requalifier si le fournisseur
  a changé à la date de véritable exécution.
- [ ] **A4.2** : isoler l'environnement GPU et documenter la
  capacité matérielle, notamment bf16 ; ajouter un CLI
  *opt-in* qui refuse la simulation.
- [ ] **A4.3** : brancher les classes **réelles** Mamba2/Mamba3
  du paquet officiel sur l'encodage et la sortie probabiliste
  de TRAME, sans changer les mêmes cibles.
- [ ] **A4.4** : exécuter sur un GPU compatible les tests de
  causalité, longueur de contexte, gradients et stabilité
  numérique. Une CI CPU qui teste seulement les garde-fous
  n'est pas une preuve de fonctionnement des moteurs GPU.
- [ ] **A4.5** : entraîner et comparer à seeds multiples avec
  budgets/paramètres/mémoire mesurés, vrais témoins, mêmes
  origines et horizons ; expliquer les limites des comparaisons
  GPU vs CPU et des types numériques différents.

## Statut matériel réel

Dans la session courante, aucun essai sur GPU CUDA compatible
n'est enregistré. Tant que A4.4 n'est pas passé, Mamba-2/Mamba-3
restent des candidats **câblés mais non validés en exécution** ;
ne jamais les afficher comme « fonctionnels » ou « meilleurs ».
Le CPU `torch==2.10.0+cpu` des runners de recherche ne valide
aucun kernel Mamba.

## Référence TRAME

A3c a donné un comparateur synthétique et des temps CPU de
diagnostic, avec GO exploration / NO-GO pour la parité FLOPs
intégrale. Voir
[`A3C_RESULTS_20261025.md`](../architecture_comparison/A3C_RESULTS_20261025.md).

Les fichiers de prix BTC privés ne sont pas nécessaires à A4.1–A4.4 ;
aucun transfert de tokens GitHub vers CI.
