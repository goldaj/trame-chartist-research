# TRAME — tableau de bord de la reprise scientifique

## Point de clôture de session — 26 octobre 2026 (instruction la plus récente)

**Reprise autonome de développement interrompue volontairement APRÈS clôture.**
L'utilisateur a demandé de terminer trois opérations puis de
**s'arrêter proprement** : (1) analyser le rapport réel H1
par année et régime, (2) en documenter les résultats, (3)
actualiser la passation Codex et vérifier l'état GitHub.
**Ces trois opérations ont été effectuées dans la PR #14.**
Ne pas interpréter l'ancien ordre « continuer sans s'arrêter »
comme une autorisation de recommencer un chantier après
cette clôture de session ; attendre de nouvelles consignes.

**Données réelles désormais exécutées :** études exploratoires
H1 et M1, puis témoins statistiques H1 par année/volatilité
passée ; **2026 non ouvert**. Voir :
- [A7 état consolidé](../research/btc_h1_m1/A7_STATUS_20261025.md)
- [A7 résultats H1](../research/btc_h1_m1/A7_H1_REAL_RESULTS_20261025.md)
- [A7 résultats M1](../research/btc_h1_m1/A7_M1_REAL_RESULTS_20261025.md)
- [A7 résultats H1 par régimes](../research/btc_h1_m1/A7_H1_REGIMES_REAL_RESULTS_20261025.md)

**Priorité à la prochaine vraie reprise :** A7.5 sur M1 et modèles
neuronaux par régimes, intervalles appariés et stress. A4
Mamba GPU, A6 fondations temporelles, A7.6 holdout indépendant,
A7.7 multi-actifs et P1–P4 restent partiellement ou totalement ouverts.
**TRAME Predictive v1 n'est pas livrable.**



**ARCHIVE DES INSTRUCTIONS DU 25/10 : REPRISE AUTORISÉE À CETTE DATE,\nREMPLACÉE PAR L'ARRÊT DE SESSION DU 26/10 CI-DESSUS.**
Cette nouvelle instruction utilisateur **remplace la pause** notée dans
`docs/CODEX_REPRISE_TRAME_PAUSE_20261025.md` (qui reste comme archive
datée). L'utilisateur demande de poursuivre **sans demander une validation
à chaque étape**, de décomposer chaque tâche en sous-tâches au lancement,
de signaler chaque achèvement, et de travailler à la fois comme
**chercheur** et **ingénieur**.

Il est cependant interdit de prétendre à une tâche terminée sans
preuve, de déduire une validation réelle d'un essai synthétique,
d'ouvrir un holdout prématurément, de mettre en production, d'utiliser
des secrets non fournis ou de fusionner implicitement les PR.

## Hiérarchie et statuts

| Phase | Sous-tâches livrables | Statut documenté |
| --- | --- | --- |
| A3c budget équitable | 1. Protocole ; 2. profil opérations/CPU ; 3. extensions contexte ; 4. pilote apparié à budget proxy ; 5. rapport et critères d'équité | 1–5 livrés en mode exploratoire ; **No-Go** pour vraie égalité des FLOPs, mémoire GPU et tuning |
| A4 Mamba | 1. Versions/API officielles ; 2. isolation matériel/dépendances ; 3. backbones réels ; 4. causalité et gradients ; 5. benchmark multi-seed | PR #11 : adaptateurs officiels CPU-guardés ; **aucune validation GPU** (A4.4–5 ouvertes) |
| A5 hybrides | 1. hypothèses ; 2. bras d'architecture ; 3. ablations ; 4. équité/rapport | PR #12 : témoin attention+GRU synthétique et résultats ; hybrides Mamba véritables non testés |
| A6 fondations temporelles | 1. versions/licences ; 2. contamination ; 3. adapteurs ; 4. test zéro-shot ; 5. comparaison | PR #13 : licences et contrat temporel en CI ; poids réels/zéro-shot non testés |
| A7 données réelles | 1. reprise cache BTC ; 2. horizons/splits ; 3. témoins ; 4. campagne multibras ; 5. évaluation robuste ; 6. gel hors-échantillon ; 7. extension multi-actifs | PR #14 : H1 et M1 réels exécutés ; régimes H1 témoins analysés ; A7.5 globale partielle, A7.6–7 non faits |
| A8 Research Lab | 1. export résultats ; 2. visualisation ; 3. traçabilité ; 4. qualité/packaging ; 5. évaluation utilisabilité | PR #15 : evidence reports offline, CI Linux/Windows ; audit UX réel non fait |
| P1 modèles | 1. sélection justifiée ; 2. représentations ; 3. entraînement/tuning ; 4. checkpoints | PR #16 : manifeste technique/checkpoints et contrat P1 ; sélection réelle P1.5 non faite |
| P2 robustesse | 1. stress ; 2. calibration ; 3. dérive ; 4. test indépendant ; 5. limites et Go/No-Go | PR #16 : diagnostics calibration/abstention de dev ; holdout P2.5 non fait |
| P3 économie | 1. contrat de simulation ; 2. frais/spread/slippage ; 3. comparateurs ; 4. intervalles ; 5. analyse de risque | PR #16 : simulation de coûts uniquement fictive ; P3.5 réel non fait |
| P4 produit | 1. API locale ; 2. interface ; 3. gestion de modèles ; 4. installation ; 5. audits ; 6. livraison et documentation | PR #16 : garde-fou de livraison NO-GO ; pas de modèle produit |

## Périmètre de la nouvelle branche

- PR #8 : `chatgpt/trame-multi-architecture-20261025` (draft).
- PR #9 : `chatgpt/btc-h1-m1-20261025` (draft, basée sur #8).
- **PR #10 : `chatgpt/trame-compute-fair-20261025`** (draft,
  basée sur #9, travaux A3c).
- Ni le dépôt `goldaj/hyperliquid-btc-pilot` ni les fichiers bruts
  de `goldaj/btc-historical-data` ne sont modifiés ici.
- Les premières CI mesurent des données **inventées** ; **trois
  campagnes séparées** ont ensuite été exécutées sur la release privée
  en workflows privés, avec sorties agrégées documentées dans A7.

## Conventions de suivi des baby steps

Pour chaque sous-tâche :
1. expliciter hypothèse scientifique, contrat d'ingénierie et test de
   sortie dans une documentation versionnée ;
2. committer code + tests (ou une note de No-Go motivée) ;
3. vérifier la CI du **dernier commit** et signaler au propriétaire
   le livrable effectivement terminé ;
4. conserver les écarts, limitations, refus d'exécution et preuves
   pour Codex ;
5. **passer à la suivante sans solliciter une autorisation**, sauf
   si une opération exige une décision ou un accès absent.

Les tâches qui exigent GPU compatible, données privées lisibles par un
runner authentifié, audits de licences ou tests financiers indépendants
sont **bloquées tant que les conditions objectives ne sont pas remplies**.
On peut préparer leurs interfaces, mocks et documentations sans inventer
de validation sur le matériel ni sur les données.

### Notes A3c

- Protocole : `research/architecture_comparison/A3C_PROTOCOL_20261025.md`.
- A3c.2 `compute_audit.py` instrumente seulement les FLOPs que
  `torch.profiler` sait comptabiliser. Les allocs événementielles
  **ne représentent pas la mémoire de processus au pic**.
- A3c.3 opt-in `length<=128` pour les trois prototypes, test
  causal et dérivabilité à 64 tokens, charges jusqu'à 128.
- A3c.4 `budget_pilot.py` répartit les pas par **proxy de compteurs
  partiels**, garde la même suite de mini-lots par seed et inscrit
  systématiquement `true_compute_matched=False`.
- Le véritable équilibrage FLOPs de **toutes** les opérations,
  les budgets de tuning et la comparaison CPU/GPU équivalente sont
  encore des portes non franchies. Ne pas utiliser « compute-fair
  validé » dans un rapport.

## Sources techniques initiales pour A4

- Officiel : https://github.com/state-spaces/mamba (inclut Mamba2 et Mamba3).
- `Mamba2(d_model, d_state, d_conv, expand)` avec GPU CUDA.
- `Mamba3(d_model, d_state, headdim, is_mimo, ...)` est un
  moteur matériel différent, conçu notamment pour bf16 et
  dépendances kernels CUDA récentes. L'exemple officiel emploie
  768 dimensions ; une miniature largeur 16 ne peut **pas** être
  déclarée fidèle sans valider ses contraintes.
- Les bibliothèques, versions, licences et APIs doivent être figées
  **à la date de l'exécution GPU**, sans installer des wheels CUDA
  dans les CI CPU existantes.

Cette feuille de route s'applique **après** l'ordre utilisateur de
reprise. Elle ne déclare pas toutes les phases achevées.


## Résultat du jalon A3c (confirmé par Actions)

[A3C_RESULTS_20261025.md](../research/architecture_comparison/A3C_RESULTS_20261025.md)
consigne un audit CPU à 8/20/64 tokens, un pilote trois graines et
un budget rapproché **sur compteurs partiels uniquement**. Les deux
artefacts JSON du run #40219261965 sont la preuve reproductible.
La recherche multi-architectures se poursuit par A4 sous statut
exploratoire, **sans** classement de modèle, FLOPs réels alignés
ou sélection d'un gagnant. Depuis cette étude A3c,
**des campagnes exploratoires BTC H1/M1 ont été exécutées** ;
voir le statut A7 ci-dessus.
