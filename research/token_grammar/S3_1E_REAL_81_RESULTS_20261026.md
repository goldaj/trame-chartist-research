# TRAME S3.1E — 27 entraînements BTC réels / 81 checkpoints
**26 octobre 2026 — TERMINÉ.** [GitHub Actions #40318969005](https://github.com/goldaj/trame-chartist-research/actions/runs/40318969005) : **4/4 jobs SUCCESS**, D1/H1/M1, agrégateur final compris. Git SHA exact des 3 jobs réels : `73b56883dd09b3ad533aeeb4546eb1d402f2c003`.

## Méthode et causalité
Protocole S3.1E enregistré **AVANT toute mesure BTC réelle** :
`research/token_grammar/S3_1E_RECONCILIATION_PROTOCOL_20261026.md`.
Trois objectifs sur le **même réseau de 2 418 paramètres**
(width16/depth1/JOINT, contexte 20, grammar G2 signée
décodée en bps, mêmes seeds, poids initiaux, batches et optimizer) :
- `legacy` : Huber(`mu`,retour vrai)+0,5 BCE(`logit`,sens vrai),
- `reconciled_025` : legacy + 0,25 Huber(`tanh(logit/2)*sqrt(mu²+eps²)`, retour vrai),
- `reconciled_100` : legacy + 1,00 fois la même Huber.
Le retour *soft* est un surrogate différentiable. La sortie
**HARD VRAIMENT SERVIE** est toujours
`sign(logit>=0)*abs(mu)`, utilisée pour
le calcul BA, MAE **prix USD/bps** et amplitude.
Ne pas présenter la performance du soft comme du pricing réel.

**27 trajectoires véritables**, trois horizons ×trois
losses ×trois graines (20261025, 20261026, 20261027),
2000 updates par modèle, checkpoints continus
**200/800/2000 = 81 mesures dépendantes**.
TRAIN interne : D1 2876 cas, H1/M1 4096 cas,
labels connus **avant le 01/01/2020**.
MONITOR interne : D1 731, H1/M1 1024,
labels connus **2020–21** ; jamais gradient,
fit quantile/scale/prior ou calibration.
Ancien développement externe 2022–25
et holdout 2026 NON UTILISÉS.
BTC/USD SPOT Bitstamp public SHA vérifié,
pas de secrets/transactions/Hyperliquid.

## Tableau complet 2000 updates, sorties HARD
BA direction équilibrée %, MAE prix en bps ancrés,
AMP erreur magnitude bps, SOFT MAE en bps
*diagnostic seulement*, **désaccord entre têtes**
= fraction de cas où signe du retour `mu`
diffère du signe du logit, UP = % hausses
prédites par la sortie HARD, MONO = modèles
à ≥99% une seule classe (sur 3 seeds).

| Horizon | Loss | BA hard % | Prix hard MAE bps | AMP hard bps | Prix SOFT MAE bps | Désaccord têtes % | UP hard % | Mono/3 | Brier skill |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| D1 | legacy | 52,24 | **282,704** | 248,938 | **280,707** | 7,9 | 69,3 | 0 | −0,00272 |
| D1 | reconciled_025 | 51,67 | 284,620 | 245,773 | 281,168 | 10,2 | 73,7 | 0 | −0,01066 |
| D1 | reconciled_100 | **52,83** | 285,563 | **241,866** | 281,657 | 7,4 | 74,6 | 0 | −0,01156 |
| H1 | legacy | **51,93** | **54,611** | 48,955 | 54,511 | 19,0 | 61,6 | 0 | −0,00303 |
| H1 | reconciled_025 | 51,17 | 54,677 | 48,803 | 54,515 | 18,0 | 52,2 | 0 | −0,00624 |
| H1 | reconciled_100 | 50,52 | 54,945 | **47,561** | **54,520** | 14,3 | 69,1 | 1 | −0,00742 |
| M1 | legacy | 53,02 | **8,368** | 7,319 | 8,337 | 26,7 | 49,7 | 0 | +0,00119 |
| M1 | reconciled_025 | **53,13** | 8,380 | 7,383 | **8,332** | 28,4 | 54,5 | 0 | +0,00180 |
| M1 | reconciled_100 | 52,73 | 8,398 | **7,307** | 8,338 | 28,2 | 52,1 | 0 | +0,00203 |

Le panneau Actions fournit **27 lignes de synthèse** pour 200/800/2000 (3 horizons ×3 arms ×3 checkpoints) plus **18 familles de deltas appariés** et 81 lignes individuelles des modèles avec MAE USD, gradients, pertes et SHA. Toutes les moyennes sont descriptives ; 3 graines ne donnent PAS trois histoires financières indépendantes.

## Analyse critique
1. **La nouvelle perte de réconciliation ne gagne pas conjointement.** D1 +1 améliore BA 52,24→52,83 et AMP 248,938→241,866, **mais** dégrade MAE du prix final 282,704→285,563 bps et Brier skill −0,00272→−0,01156. H1 +1 fait même baisser BA 51,93→50,52, dégrade MAE prix 54,611→54,945, et introduit un modèle monoclasse /3. M1 +0,25 améliore BA 53,02→53,13 légèrement, mais MAE prix 8,368→8,380 et AMP 7,319→7,383 empirent.
2. **Désaccord structurel entre têtes** avec la perte historique : D1 **7,9%**, H1 **19,0%**, M1 **26,7%** des monitor observations ont signe de `mu` contradictoire avec `logit`. La loss douce +1 réduit un peu ce taux sur H1 (14,3%) sans améliorer le vrai MAE prix ; elle l'augmente légèrement en M1 (28,2%). Ces fractions sont descriptives, pas une cause prouvée.
3. **Le SOFT peut afficher un MAE prix plus faible que le HARD**, mais ce n'est **pas** le prix actuellement servi ; le soft est souvent plus proche de zéro, ce qui peut ressembler à la persistance. Remplacer la sortie HARD après avoir vu les scores MONITOR serait un changement **post-hoc** et ne vaut pas validation.
4. **Persistance train-free MAE prix baseline**, même cohorte monitor : D1 **281,037 bps**, H1 **54,535**, M1 **8,347**. Même legacy à 2000 steps est légèrement moins bon en prix, ce qui interdit de parler de prévisions monétaires meilleures, de façon robuste, que rester au prix actuel.
5. **Brier skill** D1/H1 reste négatif, M1 très proche de zéro ; aucun gain sérieux de probabilité directionnelle. Dev 2022–25 déjà saturé et 2020–21 déjà consulté en S3.1C/D, donc expérience encore exploratoire. **Holdout 2026 non ouvert**.
6. **Verdict** : NO-GO pour un edge direction + prix final + amplitude, et pour l'augmentation immédiate des tailles de modèle. Les deux têtes présentent un vrai problème potentiel de cohérence, mais ajouter une loss douce ne le résout pas.

## Suite : S3.1F proposée, sans réentraînement supplémentaire inutile
**Comparer des règles d'inférence sur des poids strictement identiques**, préenregistrer avant d'observer des scores BTC :
- `joint_hard` EXISTANT : signe logit × |mu|;
- `signed_direct` : retour `mu` directement sans changement de poids;
- `joint_soft` : `tanh(logit/2)*abs(mu)`, comme diagnostic distinct.
Une étude appariée isolerait le **post-traitement/pricing**
plutôt que de changer modèle, loss et grammaire ensemble.
Pour être rigoureux, conserver EXACTEMENT les modèles
legacy S3.1E et comparer les trois règles sur les
mêmes cas MONITOR 2020–21, en notant que
le MONITOR est déjà utilisé pour la recherche.
Ne pas ouvrir 2026 pour sélectionner une règle,
et ne pas promettre de gains de trading.
L'architecture plus grosse et le nouvel encodage
de tokens ne sont pas encore justifiés.

## SHA256 des cinq artefacts scientifiques
- D1 27 scores individuels : `1479a7fde682b36ca08b9cfeb1404e0b1227e8d4741673af660f4858d108ded2`.
- H1 27 scores : `4bb16378e4b29fcff0432b76b7a1548a515c95685882dbb0456d1890b20a9540`.
- M1 27 scores : `e2540a74eda6d37ecc25b92f801cb505937f97f96c2d061b80446b4b502578b0`.
- Panel final JSON : `3c0b81da55272d7d4cbd59e6501ef738c0a9653beb5212b6840697b0118716a3`.
- Tableau Markdown : `34718aa57202f97a32dc562644719332b387c85f193d963c069dac18193eaee8`.
- Commit modèle exécuté `73b56883dd09b3ad533aeeb4546eb1d402f2c003`.
- [Actions source #40318969005](https://github.com/goldaj/trame-chartist-research/actions/runs/40318969005), 4/4 jobs SUCCESS. Artefacts publics retenus 30 jours. Copie ZIP avec manifeste SHA archivée dans la conversation au nom `trame_s3_1e_27_81_resultats.zip`.

**NO trading, NO wallet/API, NO PnL cumulatif**, frais ignorés conformément à l'utilisateur ; aucune preuve d'edge financier ni validation indépendante.
