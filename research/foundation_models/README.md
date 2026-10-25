# A6 — modèles de fondation temporelle, voies zero-shot séparées

**25 octobre 2026. Aucun poids téléchargé ni exécution zero-shot
dans TRAME** lors de la rédaction de ce protocole. Cette branche
ne peut pas prouver des performances financières.

## A6.1 : candidats et droits vérifiés

| Modèle | Checkpoint de référence (à épingler au téléchargement) | Licence poids affichée le 25/10/2026 | Produit commercial TRAME |
| --- | --- | --- | --- |
| TimesFM-3 | `google/timesfm-3.0-pytorch` | `timesfm-non-commercial-license-v1.0` | **NO-GO** pour les poids par défaut |
| Chronos-2 | `amazon/chronos-2` | Apache-2.0 | Candidat, sous réserve de revue finale et conditions |
| Moirai-2 | `Salesforce/moirai-2.0-R-small` | `cc-by-nc-4.0` | **NO-GO** pour l'usage commercial des poids |

Le code TimesFM 3.0 est Apache-2.0 **mais pas ses poids**.
Les versions antérieures des poids ont d'autres conditions ;
une licence du code ne peut jamais être substituée à une licence
des checkpoints. Un modèle non commercial peut être testé
dans le cadre permis par sa licence, sans l'insérer dans P4.
Ne pas présenter le statut de Chronos-2 comme une approbation
juridique complète.

Sources officielles à cette date :
- https://github.com/google-research/timesfm
- https://huggingface.co/google/timesfm-3.0-pytorch
- https://github.com/amazon-science/chronos-forecasting
- https://huggingface.co/amazon/chronos-2
- https://github.com/SalesforceAIResearch/uni2ts
- https://huggingface.co/Salesforce/moirai-2.0-R-small

## Sous-tâches

- [x] **A6.1** : registre des checkpoints et licences
  avec exclusion produit des poids non commerciaux.
- [ ] **A6.2** : recenser les ensembles de préentraînement
  et tests de contamination potentielle au niveau de la date,
  du dataset et des identifiants ; **inconnu = non résolu**,
  jamais interprété comme « absence de contamination ».
- [ ] **A6.3** : contrat causal de séries et de prévision
  (contextes observés, covariables temporellement disponibles,
  horizon/prix natifs, impossibilité d'utiliser des cibles
  futures comme features), format de sortie comparable.
- [ ] **A6.4** : chargement opt-in des vrais checkpoints
  avec commit/revision figés et test zero-shot authentique sur
  des données admissibles. **Non exécuté** tant que runtime/poids/
  benchmark adéquats manquent.
- [ ] **A6.5** : rapport comparatif par horizon et modèle,
  temps, mémoire, calibration et licence ; séparation
  `pretrained/zero-shot` vs `from_scratch`.

## Invariants scientifiques

1. Une prévision directe et une génération autorégressive ne
   s'alignent pas par comparaison naïve de la NLL sur des tokens.
   Définir les mêmes prix natifs et horizons au moment du score.
2. Comparer les modèles préentraînés dans un bras **séparé**
   de TRAME entraîné de zéro : leurs budgets préhistoriques
   ne sont pas comparables.
3. Conserver l'origine temporelle d'une prévision et les dates
   réellement disponibles pour chaque variable exogène.
4. La période BTC de développement 2022–2025 a déjà servi
   à l'exploration de TRAME : ne pas recycler ce jeu comme
   validation indépendante d'un modèle de fondation.
5. Aucun téléchargement en CI CPU, aucun poids ou jeton
   committé, aucun modèle hors licence dans la v1 commerciale.
6. Un registre de modèles n'est **pas** un run effectif.

## Go / No-Go

**GO** pour des contrats, des tests synthétiques et
l'intégration future de Chronos-2 dans un environnement isolé.

**NO-GO** pour une comparaison financière confirmatoire sans
contamination évaluée, origines gelées et checkpoints réellement
chargés. **NO-GO commercial** pour TimesFM-3 et Moirai-2
sous les licences de poids indiquées.
