# Piste de recherche — architecture locale tri-hybride LFM3 (2026-11-03)

**Origine :** nouvelle piste du propriétaire pour le modèle chartiste/TRAME, communiquée le 3 novembre 2026.
**Statut :** suggestion d'architecture à évaluer ; aucun entraînement, benchmark ni remplacement de l'architecture actuelle n'est autorisé par cette note.

## Hypothèse à tester

Explorer un modèle de type **LFM3**, présenté comme une architecture **tri-hybride**, pour les besoins de TRAME, notamment la faisabilité d'entraînement et d'inférence en local avec un budget matériel restreint.

Le propriétaire signale une comparaison rapportée où LFM3 dépasserait un **Qwen 3.5 9B**, malgré une taille annoncée comme environ six fois inférieure. **Ces chiffres et le périmètre du benchmark restent à vérifier auprès des sources techniques** (modèles précis, taille effective, matériel, tâche, métrique, débit, qualité, contexte, quantification).

## Critères de recherche pour une reprise ultérieure

1. Vérifier l'architecture effective de LFM3, les poids et licences disponibles, les outils d'inférence et d'entraînement, ainsi que la viabilité pour un langage causal de séries temporelles.
2. Comparer à des témoins pertinents pour TRAME (Transformers compacts, Mamba/SSM, autres architectures hybrides), **à données, tâches, budgets et métriques identiques**.
3. Mesurer mémoire/RAM/VRAM, débit, latence, qualité prédictive hors échantillon, consommation et complexité d'intégration locale.
4. Au moment du lancement effectif, **réévaluer l'état de l'art** : LFM3 n'est pas un choix figé. Conserver un protocole reproductible et ne pas annoncer de progrès sans essai réel.
5. Respecter les jeux temporels réservés et la séparation stricte entre recherche TRAME, données `market-data-library` et trading Hyperliquid. Aucun live ni performance financière revendiquée.

Le verbatim privé de l'utilisateur est conservé dans le dépôt privé Notepad ; ce document public ne reproduit pas la conversation.
