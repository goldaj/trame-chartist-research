# TRAME — candidat documentaire P1-D 0.2

État du 15 octobre 2026 : conception scientifique, non gelée, non préenregistrée, non implémentée comme prédicteur et non entraînée. Aucun résultat de prévision. La publication PDF reste l'édition 2.1 ; ce répertoire et les quatre notes associées constituent le travail préparatoire suivant.

## Lecture

- `protocol_candidate.json` : choix courants et points ouverts.
- `../../dossier/recherche_lcm/notes_p1d_candidat_20261015.md` : fiche générale.
- `../../dossier/recherche_lcm/notes_alphabet_information_egale_20261015.md` : équivalence des codes, précision numérique, encodeurs minimaux, comptes de paramètres, antériorités et panel fictif.
- `../../dossier/recherche_lcm/notes_temoins_p1d_20261015.md` : formules des témoins et calibration chronologique proposée.
- `../../dossier/recherche_lcm/notes_ancres_causalite_dpcm_20261015.md` : causalité, ancres et proposition conceptuelle de codage différentiel.

La révision 0.1 et sa fiche sont conservées dans `versions/candidate_0_1`. Aucune de ces révisions n'est un protocole gelé. Les hypothèses restent amendables avec une trace.

## Ce qui a été exécuté

`count_calendar.py` et `calendar_counts.json`, le 15 octobre à 09:52 UTC : comptage des origines admissibles à partir des dates BCE déjà acquises. Le script contrôle l'empreinte du fichier, lit les dates/statuts et ne calcule aucun score ni statistique des prix.

`verify_design_arithmetic.py` et `design_arithmetic_checks.json`, à 12:22 UTC : arithmétique du gabarit documentaire, bijection des 4 096 cellules principales, exemples de précision float32 et différence entre deux conventions d'interpolation. Ce script utilise la bibliothèque standard Python et ne lit aucun fichier de marché. Ses exemples sont construits pour vérifier les formules, sans statut de données de marché synthétiques destinées à l'apprentissage.

Pour reproduire uniquement cette vérification arithmétique, lancer `python research/trame_protocol_p1d/verify_design_arithmetic.py` depuis la racine du dossier. Elle réécrit son rapport horodaté ; conserver une copie si l'empreinte exacte de l'exécution précédente est nécessaire. Ce script n'est pas un modèle ni un tokenizer entraînable.

`source_audit_02.json` consigne quatre lectures ciblées et leurs limites. `qa_candidate_02.json` consigne les contrôles de cohérence documentaire et d'intégrité des sources/publications antérieures, sans nouvelle analyse des prix.

## Ce qui reste proposé

Audit des plages numériques réelles et des blocs annuels des témoins ; choix des encodeurs numériques plus expressifs, de l'optimiseur, des initialisations et budgets ; règles de passage à plus grande capacité ; qualification des versions historiques et d'un test indépendant. Aucun de ces points ouverts ne doit être transformé silencieusement en autorisation de construire ou d'entraîner un modèle.

L'archive de travail 0.2 est un complément documentaire. Elle ne duplique pas les données et les PDFs de l'archive scientifique 2.1. Pour les analyses de calendrier, le fichier BCE et son audit doivent se trouver aux chemins de `research/trame_poc0/ecb_exploratory` déjà présents dans le dossier complet. Les mois crypto réservés restent protégés.
