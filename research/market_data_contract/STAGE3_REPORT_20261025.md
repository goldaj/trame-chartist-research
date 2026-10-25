# Étape 3 : contrat de données financières point-in-time

**25 octobre 2026.** Revue scientifique, code d'audit et tests, **aucun
nouveau téléchargement de données de marché**. Étape 3 **partiellement
terminée** (3.1–3.5) avec arrêt argumenté sur 3.6.

## Décision fondamentale

Une date de cours \`observed_at\` ne signifie pas que sa valeur était
disponible à cette date. Pour reconstruire ce qu'un modèle pouvait
savoir, TRAME requiert une seconde date \`available_at\` avec la
provenance et une preuve de disponibilité. Une révision survenue des
années plus tard ne doit pas remplacer silencieusement la version
initialement accessible.

La BCE indique qu'elle publie généralement ses cours de référence
vers 16:00 CET les jours ouvrés, qu'ils sont informatifs et qu'ils ne
sont pas des prix d'exécution. Une heure *usuelle* ne suffit pas à
attester la disponibilité exacte **pour chaque publication passée**.
https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.fr.html

ALFRED permet des millésimes de données économiques, mais ses dates de
vintage ne certifient pas automatiquement une heure de publication
intrajournalière. Les droits sur les séries FRED peuvent appartenir à
des tiers : accessibilité API n'est pas une licence universelle de
redistribution.
https://fred.stlouisfed.org/docs/api/fred/realtime_period.html
https://fred.stlouisfed.org/docs/api/terms_of_use.html

## Réalisations (baby steps)

| Sous-étape | Statut | Livrable |
| --- | --- | --- |
| 3.1 Cartographie des sources | Fait, **toutes non qualifiées pour ingestion réelle** | \`candidate_sources.json\` : BCE EXR, ALFRED/FRED, crypto spot candidats, tous bloqués jusqu'aux vérifications |
| 3.2 Schéma de provenance | Fait pour le laboratoire | \`asof.py\` : \`source_id\`, actif, événement, disponibilité UTC, prix décimal exact, unité et révision |
| 3.3 Validateur adversarial | Fait, CI | Refus licences absentes, non-UTC, prix nuls/NaN, dates impossibles, doublons, révisions incohérentes, unité mutée |
| 3.4 Éligibilité temporelle | Fait pour les fixtures | \`as_of\` ne retourne que la dernière révision connue à la date décisionnelle ; \`forecast_origin_evidence\` vérifie le contexte et que les **dates cibles** restent dans la partition (sans révéler leurs prix) |
| 3.5 Encodage causal P1-D | Fait pour les fixtures | \`p1d_features.py\` : 256 prix *disponibles*, échelle sur 64 incréments précédents, float32/float64 contrôlé, codes Q, sans imputation |
| 3.6 Acquisition multi-marchés qualifiée | **Bloqué** | Aucune source réelle n'a encore une licence, une méthode de \`available_at\` et un audit archivés suffisants pour ce protocole |
| 3.7 Qualité/Go-No-Go | Verdict partiel | **No-Go** sur entraînement et évaluation réels présentés comme point-in-time ; Go pour construire témoins et évaluation **synthétiques** |

## Reproduction sans aucune donnée financière

~~~bash
python -m pip install 'numpy==2.3.5'
python -m unittest discover -s research/market_data_contract -p 'test_*.py' -v
~~~

Une absence de cote reste une absence ; aucune interpolation,
aucun calendrier de bourse inventé et aucune valeur future ne sont
introduits dans le contexte du modèle.

Une fixture à 260 jours de prix fabriqués et une révision fictive
publiée après l'origine démontrent que le même vecteur P1-D sort
avant/après l'ajout rétrospectif de cette révision.

## Limites / risques d'interprétation

- \`approved_synthetic\` signifie « source artificielle »,
  **pas** « vraie source autorisée ». Pour le réel,
  \`verified_real\` impose preuves et méthode de disponibilité.
- Le validateur ne peut pas prouver la véracité des dates que
  lui fournit l'utilisateur. Il **refuse** celles non documentées
  et attend un manifeste attesté avec archivage des téléchargements.
- La purge de fenêtres intervient en plus des contrôles d'éligibilité
  des labels; il faut éviter le chevauchement des labels entre
  train/dev/test, contrôler les transformations entraînées,
  et préserver le test indépendant. Les séries historiques
  explorées antérieurement n'en constituent pas un.
- Pour de l'intraday, la date/heure réelle de clôture et de
  publication doit être démontrée ; un cours de référence BCE
  n'est pas directement un actif tradable exécuté à cette cote.
- \`forecast_origin_evidence\` est une **fonction de préparation
  rétrospective des partitions**, jamais une feature de
  prédiction (elle examine des dates cibles postérieures).

## Sous-étapes de l'étape 4 (benchmark équitable)

4.1. Contrat unique d'origines, cibles et unités, lisible
     par la persistance comme par tous les modèles.

4.2. Baseline de persistance sur prix natifs, sans apprentissage,
     et témoin saisonnier quand les données l'autorisent.

4.3. Baselines numériques (gaussienne à volatilité roulante,
     AR/Ridge et quantiles) entraînées **sur passé disponible
     uniquement**, sans imputation globale.

4.4. Scores communs : MAE / RMSE / CRPS / pinball, couvertures,
     erreurs MC ; comparaison à horizons distincts et actifs
     distincts, sans prétendre qu'une NLL des codes est une
     probabilité continue de prix.

4.5. Tests anti-fuite sur prédictions préparées, audits
     du déterminisme, traçabilité des graines et du budget.

4.6. Inférence statistique tenant compte des origines
     recouvrantes et risques de comparaisons multiples,
     avec effet minimum utile défini avant test.

4.7. Gel du benchmark préalable à toute découverte ou
     entraînement financier confirmatoire. En l'absence de
     source réelle qualifiée : benchmark réalisable
     seulement sur fixtures synthétiques.

## Consignes pour Codex

Branche \`chatgpt/point-in-time-data-contract-20261025\` basée
sur \`chatgpt/mini-transformer-synthetic-20261025\`. Les
PR historiques sont conservées. Ne pas importer le CSV BCE
historique comme test point-in-time certifié :
\`research/trame_poc0\` et les auditions antérieures l'ont
déjà exploré, et les vintages d'origine ne sont pas établis.
