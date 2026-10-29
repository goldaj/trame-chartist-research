# TRAME — consolidation Git et passation Codex (29 octobre 2026)

## Branche unique de référence

- **PR d'intégration :** https://github.com/goldaj/trame-chartist-research/pull/30
- **Branche :** `chatgpt/trame-s3-selective-forecast-20261026`
- **Base :** `main`. Les autres PR expérimentales GPT6 sont historiques une fois leur ancêtre intégré.
- **Statut :** recherche scientifique, pas de produit prédictif validé ni de système de trading. Aucune exécution live, aucun ordre, aucun résultat financier revendiqué.

## Contenu de la consolidation

La chaîne initiale P1-B0 -> validation -> mini-Transformer -> point-in-time -> benchmark -> architecture -> données D1/H1/M1 -> expériences S1/S2/S3.1A-G correspond aux PR #2-#10, #14, #17-#19, #21-#30. Tous leurs commits sont ancêtres de la PR #30. Les anciennes PR superposées ont été closes sans effacer leurs branches.

Six travaux auparavant **parallèles**, désormais fusionnés par commits Git réels à deux parents sur la même branche :

| Origine | Contenu conservé | Limites |
| --- | --- | --- |
| PR #1 | validation CI synthétique et score points | tests de contrat, pas une preuve financière |
| PR #11 / A4 | adaptateur GPU Mamba-2/Mamba-3 optionnel, smoke tests | pas de GPU validé dans cette consolidation |
| PR #12 / A5 | contrôle hybride attention/GRU, expérience et tests | témoin, pas un vrai modèle Mamba |
| PR #13 / A6 | registre de checkpoints, licences, contrat temporel | aucun gain zéro-shot démontré |
| PR #15 / A8 | rapports de preuve et audits synthétiques | ne vaut pas résultats sur marché réel |
| PR #16 / P1-P4 | critères NO-GO, contrat produit, sandbox de coûts | aucun passage en production autorisé |

Les fichiers nouveaux de chaque piste ont été intégrés à leurs chemins d'origine. Les versions divergentes d'`AGENTS.md`, du journal et de l'ancien tableau de pilotage ont été **archivées** sous `docs/merge-archive/`, sans écraser les consignes plus récentes du parcours S3.1. Les commits parents des six branches sont conservés. Les instructions historiques « PR indépendante, ne pas fusionner » décrivent l'état avant le 29/10 et ne constituent plus la cible de reprise.

## Prochain opérateur : reprise sûre

1. Lire `AGENTS.md`, ce fichier, `docs/CODEX_EXECUTION_BOARD_20261025.md` et l'historique, puis inspecter la PR #30 et tous les workflows déclenchés sur **son dernier SHA**.
2. Faire tourner les tests des sous-projets indépendants (A4, A5, A6, A8, P1-P4) et vérifier qu'ils n'entrent pas en conflit avec les protocoles S3.1. **Le résultat des anciens workflows réussis ne prouve pas l'exécution du HEAD consolidé.**
3. Vérifier les frontières causales, le gel train/validation/test, les permissions et licences des modèles, la provenance D1/H1/M1, ainsi que les risques de coût mémoire et GPU.
4. Établir les verdicts scientifiques par piste. Ne pas confondre protocole défini, code exécuté sur données synthétiques et expérience BTC réelle.
5. Ne fusionner dans `main` qu'après validation des workflows du HEAD, revue des écarts et vérification des archives de données. Conserver la PR #30 comme seul point d'entrée de revue.

## Pourquoi ces archives existent

La plupart des conflits Git concernaient la réécriture concurrente des mêmes documents de consignes, parfois avec des recommandations datées devenues contradictoires. Écraser le tableau S3 avec les conseils anciens des branches A4-A8 aurait détruit l'information la plus récente ; écraser les anciennes versions aurait détruit le contexte expérimental. L'archivage explicite des variantes est une résolution volontaire, pas un résultat de merge automatique affirmé sans examen.

**Aucune garantie de réussite CI post-fusion n'est énoncée ici.** Lire les GitHub Actions actuelles avant intégration.
