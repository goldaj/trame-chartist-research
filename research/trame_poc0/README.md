# TRAME POC0 : appareil de mesure documentaire

Ce dossier contient les analyses de données réelles qui accompagnent la version scientifique 2 du dossier TRAME. Il ne contient pas de réseau prédictif entraîné. Les mesures de reconstruction ne prédisent aucune valeur future.

## Reproduire le comparatif OHLCV

Environnement des mesures : Python 3.12, NumPy 2.3.5, CPU. La version précise du runtime est enregistrée dans environment.json. Depuis ce dossier, avec cet environnement :

```text
python -m unittest -v test_research.py
python run_research.py
```

Le programme vérifie les empreintes du protocole et du script, puis réutilise les archives déjà présentes. Si une archive autorisée manque, il la reçoit depuis la source publique et vérifie le CHECKSUM. Il n'accède qu'aux huit actifs et dix mois explicitement listés dans protocol.json. Les mois réservés ne sont pas autorisés.

Ne pas modifier un fichier gelé puis remplacer silencieusement son empreinte. Pour une autre expérience, conserver les anciennes versions et créer un nouvel identifiant avec justification. L'amendement 1.1 a été nécessaire après découverte d'une bougie à fermeture anticipée ; aucune mesure de représentation n'avait encore été produite. Le protocole précédent est conservé dans versions.

## Artefacts

- protocol.json, freeze.json : règles et historique des empreintes.
- raw : archives sources, CHECKSUM et provenance par fichier.
- results/data_manifest.json : observations présentes, heures absentes et bougies exclues.
- results/codebook_1h.json et codebook_4h.json : quantiles et amplitudes ajustés seulement sur calibration.
- results/measurements.json : métriques par langue, actif et résolution.
- results/summary.json : agrégations descriptives utilisées dans le rapport 07.
- results/reconstruction_errors.png et .svg : figure statique du rapport.
- ecb_exploratory : acquisition et audit distincts des cours de référence BCE 1999–2020. Aucun OHLCV n'y est fabriqué.

Le rapport principal est dossier/recherche_lcm/07_premieres_mesures_reelles.md, depuis la racine documentaire du projet. Les neuf tests utilisent de petits exemples construits pour vérifier les calculs, jamais comme observations de l'expérience réelle. La génération de la figure utilise Matplotlib ; cette dépendance n'est pas requise pour les mesures.

## Attribution et portée

Les bougies proviennent de Binance Vision, avec leurs conditions de données, dont attribution et CC-BY-NC-SA-4.0 pour les datasets et dérivés concernés. Les fichiers et résultats dérivés sont fournis pour cette recherche personnelle, avec attribution conservée : https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md . Les termes des données sont distincts de la licence des outils.

Les cours de référence proviennent des statistiques BCE. Les fichiers bruts et métadonnées restent intacts. Les agrégations et commentaires sont des analyses TRAME à partir de ces statistiques, sans approbation de la BCE : https://www.ecb.europa.eu/stats/ecb_statistics/governance_and_quality_framework/html/usage_policy.en.html .

Une vérification d'intégrité ne certifie pas que les archives sont une version point-in-time des observations anciennes. Ni cette collecte ni le comparatif ne démontrent la prévisibilité des prix, le transfert multi-marchés ou les bénéfices d'un GPT.
