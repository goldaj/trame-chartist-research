# TRAME — tableau de bord de la reprise scientifique

**25 octobre 2026. Statut courant : REPRISE AUTORISÉE.**
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
| A4 Mamba | 1. Versions/API officielles ; 2. isolation matériel/dépendances ; 3. backbones réels ; 4. causalité et gradients ; 5. benchmark multi-seed | Recherche préalable ; GPU/test de Mamba-3 à effectuer |
| A5 hybrides | 1. hypothèses ; 2. bras d'architecture ; 3. ablations ; 4. équité/rapport | A5 témoin attention+GRU achevé PR #12 ; véritables SSM hybrides non exécutés |
| A6 fondations temporelles | 1. versions/licences ; 2. contamination ; 3. adapteurs ; 4. test zéro-shot ; 5. comparaison | A6.1–3 implémentés PR #13 ; A6.4–5 sans poids ni audit contamination |
| A7 données réelles | 1. reprise cache BTC ; 2. horizons/splits ; 3. témoins ; 4. campagne multibras ; 5. évaluation robuste ; 6. gel hors-échantillon ; 7. extension multi-actifs | A7.1–3 disponibles PR #14 ; campagnes BTC réelles et test indépendant non exécutés |
| A8 Research Lab | 1. export résultats ; 2. visualisation ; 3. traçabilité ; 4. qualité/packaging ; 5. évaluation utilisabilité | Rapport HTML/JSON de preuves synthétiques PR #15 ; rendu financier et produit à faire |
| P1 modèles | 1. sélection justifiée ; 2. représentations ; 3. entraînement/tuning ; 4. checkpoints | À faire |
| P2 robustesse | 1. stress ; 2. calibration ; 3. dérive ; 4. test indépendant ; 5. limites et Go/No-Go | À faire |
| P3 économie | 1. contrat de simulation ; 2. frais/spread/slippage ; 3. comparateurs ; 4. intervalles ; 5. analyse de risque | À faire |
| P4 produit | 1. API locale ; 2. interface ; 3. gestion de modèles ; 4. installation ; 5. audits ; 6. livraison et documentation | À faire |

## Périmètre de la nouvelle branche

- PR #8 : `chatgpt/trame-multi-architecture-20261025` (draft).
- PR #9 : `chatgpt/btc-h1-m1-20261025` (draft, basée sur #8).
- **PR #10 : `chatgpt/trame-compute-fair-20261025`** (draft,
  basée sur #9, travaux A3c).
- Ni le dépôt `goldaj/hyperliquid-btc-pilot` ni les fichiers bruts
  de `goldaj/btc-historical-data` ne sont modifiés ici.
- Les premières CI mesurent des données **inventées** ; aucun résultat
  de prévision BTC ne peut être inventé à partir de celles-ci.

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
ou campagne sur historiques BTC.


## Synthèse d'intégration : branches PARALLÈLES et PR draft

| PR | Domaine | Base | Évidence | État scientifique |
| --- | --- | --- | --- | --- |
| [#10](https://github.com/goldaj/trame-chartist-research/pull/10) | A3c coûts/proxy | #9 | Actions #40219261965, deux JSON | tests CPU verts, **No-Go compute-fair intégral** |
| [#11](https://github.com/goldaj/trame-chartist-research/pull/11) | A4 Mamba2/3 adaptateurs | branche #10 | Actions #40220143641 | gardes CPU verts, kernels CUDA **non testés** |
| [#12](https://github.com/goldaj/trame-chartist-research/pull/12) | A5 hybride attention+GRU | branche #10 | Actions #40220598879 | micro-synthétique négatif ; hybride SSM non testé |
| [#13](https://github.com/goldaj/trame-chartist-research/pull/13) | A6 fondations temporelles | branche #10 | Actions #40221061337 | licences/horodatages testés ; zéro-shot non exécuté |
| [#14](https://github.com/goldaj/trame-chartist-research/pull/14) | A7 baselines BTC | branche #10 | Actions #40221411599 | fixtures vertes ; **aucun résultat BTC réel** |
| [#15](https://github.com/goldaj/trame-chartist-research/pull/15) | A8 digests HTML/JSON | branche #10 | Actions #40222019571 | export de preuves synthétiques ; produit non livré |

**IMPORTANT pour Codex : #11 à #15 sont des branches soeurs, pas une
chaîne linéaire.** Leur ordre de merge/rebase devra être déterminé
lors d'une revue des diffs, pas présumé. Dans cette conversation,
les commits de chacune de ces branches n'ont jamais été fusionnés
à la branche #10, à #9, à #8 ou à `main`.

Les runs mentionnés correspondent aux derniers commits de **code**
testés ; des commits uniquement documentaires `[skip ci]` sont
ensuite intervenus, ne pas affirmer qu'un HEAD de docs est revalidé
sans contrôle effectif. Les empreintes d'artefacts s'appuient sur
les runs cités.


## Étape produit P1–P4 : code de sécurité et No-Go explicite

Nouvelle [PR #16](https://github.com/goldaj/trame-chartist-research/pull/16)
(`chatgpt/trame-predictive-delivery-gates-20261025`), branche soeur
des PR #11 à #15, basée sur PR #10 :

- P1.1–P1.4 : critères et manifeste d'entraînement/checkpoints
  **définis**, mais aucune sélection confirmatoire n'a eu lieu
  (P1.5 **NON FAITE**).
- P2.1–P2.4 : protocole et catalogue de tests de robustesse
  **définis**, tests financiers indépendants P2.5 **NON FAITS**.
- P3.1–P3.4 : code `transaction_sandbox.py` vérifié sur
  **prix inventés**, décisions connues avant l'origine, coûts
  et drawdown ; P3.5 test économique réel **NON FAIT**.
- P4.1 : `release_preflight.py` interdit le feu vert
  automatique ; P4.2–P4.5 seulement contrats et outillage
  partiel ; P4.6 Predictive v1 **NON LIVRÉ**.
- CI [#40222500744](https://github.com/goldaj/trame-chartist-research/actions/runs/40222500744)
  réussie pour la dernière version de **code** P3/P4 ;
  les modifications documentaires ultérieures ne
  revendiquent pas de revalidation.

### Liste ordonnée des dépendances objectives restantes

1. **Matériel** : machine CUDA/bf16 compatible pour
   installation/tests réels `mamba_ssm.Mamba2/Mamba3`.
   Ne jamais remplacer par un résultat GRU CPU.
2. **Données** : exécution sur ordinateur disposant du cache
   release privé BTC versionné et de l'authentification
   GitHub requise. Ne pas committer les prix dans TRAME.
3. **Science** : régimes et multiples horizons, baselines,
   vraie couverture des coûts de calcul, budget de tuning,
   préenregistrement et gel d'un test indépendant.
4. **Poids préentraînés** : versions figées, audit de
   contamination et conformité des licences ;
   TimesFM-3 et Moirai-2 non commerciaux hors produit.
5. **Produit** : checkpoints effectifs, API/UI de prévision,
   installation Windows/Linux vérifiée, sécurité,
   accessibilité et revue humaine avant tout Go.

**Impossible de déclarer toutes les tâches « terminées » tant
que ces cinq dépendances restent ouvertes.** Les tests
synthétiques réussis ne constituent pas de telles preuves.

### Actualisation A8

La PR #15 a également livré un visualiseur complémentaire
`research/trame_lab/evidence.py` avec imports A3c/A5/A7,
empreintes des JSON, tests CI Linux/Windows
[run #40222427770](https://github.com/goldaj/trame-chartist-research/actions/runs/40222427770).
Le document `research/trame_lab/A8_EVIDENCE_20261025.md` porte
les instructions détaillées. Il n'y a toujours aucune
certification WCAG navigateur/lecteur d'écran et aucune
démonstration financière réelle.

### État d'intégration de Git

Les PR #8–#16 demeurent en **draft**, sans merge.
Surtout ne pas considérer les PR #11–#16 comme des
commits empilés les uns sur les autres : ce sont des
branches sœurs, et chaque intégration nécessitera une
revue de conflit/de tests avec PR #10 comme parent.
