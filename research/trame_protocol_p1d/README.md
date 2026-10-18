# TRAME - candidat documentaire P1-D 0.4

Mise à jour du 15 octobre 2026 : témoins numériques résiduels, initialisation et budget proposés, sans entraînement. L’édition 2.2 et son candidat 0.3 sont conservés ; les documents 11-12 portent la révision 0.4. Le générateur P1-B0 est un candidat théorique séparé dans research/trame_research_plan/20261015. Le protocole prédictif reste non gelé.

## Historique 0.3 conservé ci-dessous

# TRAME — candidat documentaire P1-D 0.3

État du 15 octobre 2026 : conception scientifique, non gelée, non préenregistrée, non implémentée comme prédicteur et non entraînée. Aucun résultat de prévision. La publication PDF reste l'édition 2.1 ; ce répertoire et les cinq notes associées constituent le travail préparatoire suivant. La révision 0.3 corrige un chemin d'encodeur qui n'aurait reçu aucun exemple d'apprentissage, après un audit descriptif sur les données réelles.

## Lecture

- `protocol_candidate.json` : choix courants et points ouverts.
- `../../dossier/recherche_lcm/notes_p1d_candidat_20261015.md` : fiche générale.
- `../../dossier/recherche_lcm/notes_alphabet_information_egale_20261015.md` : équivalence des codes, précision numérique, encodeurs minimaux, comptes de paramètres, antériorités et panel fictif.
- `../../dossier/recherche_lcm/notes_temoins_p1d_20261015.md` : formules des témoins et calibration chronologique proposée.
- `../../dossier/recherche_lcm/notes_ancres_causalite_dpcm_20261015.md` : causalité, ancres et proposition conceptuelle de codage différentiel.
- `../../dossier/recherche_lcm/notes_audit_reel_et_langage_hybride_20261015.md` : résultats réels, cas de normalisation CHF, correction hybride 0.3 et limites.

Les révisions 0.1 et 0.2 sont conservées dans `versions/candidate_0_1` et `versions/candidate_0_2`. Aucune de ces révisions n'est un protocole prédictif gelé. Les hypothèses restent amendables avec une trace. Le gel dans `audits/preflight_01` concerne seulement l'analyse descriptive exécutée, pas l'entraînement de P1-D.

## Ce qui a été exécuté

`count_calendar.py` et `calendar_counts.json`, le 15 octobre à 09:52 UTC : comptage des origines admissibles à partir des dates BCE déjà acquises. Le script contrôle l'empreinte du fichier, lit les dates/statuts et ne calcule aucun score ni statistique des prix.

`verify_design_arithmetic.py` et `design_arithmetic_checks.json`, à 12:22 UTC : arithmétique du gabarit documentaire, bijection des 4 096 cellules principales, exemples de précision float32 et différence entre deux conventions d'interpolation. Ce script utilise la bibliothèque standard Python et ne lit aucun fichier de marché. Ses exemples sont construits pour vérifier les formules, sans statut de données de marché synthétiques destinées à l'apprentissage.

Pour reproduire uniquement cette vérification arithmétique, lancer `python research/trame_protocol_p1d/verify_design_arithmetic.py` depuis la racine du dossier. Elle réécrit son rapport horodaté ; conserver une copie si l'empreinte exacte de l'exécution précédente est nécessaire. Ce script n'est pas un modèle ni un tokenizer entraînable.

`source_audit_02.json` consigne quatre lectures ciblées et leurs limites. `qa_candidate_02.json` consigne les contrôles de cohérence documentaire et d'intégrité des sources/publications antérieures, sans nouvelle analyse des prix.

`audits/preflight_01` : protocole descriptif figé à 14:38:46 UTC, script, copie du candidat 0.2 analysé et rapport réel. 8 166 912 présentations de valeurs, 33 672 prix sources distincts, aucun échec des conditions numériques. Aucune valeur hors vocabulaire à l'ajustement ; 195 présentations dans 40 contextes CHF au développement. Le diagnostic ciblé supplémentaire est déclaré après ces résultats et marqué exploratoire ; il n'est pas une confirmation indépendante. Aucun de ces scripts n'ajuste de modèle. Leurs rapports existants sont protégés contre l'écrasement lors d'une réexécution.

`source_audit_03.json` donne le contexte institutionnel BNS du cas CHF, sans prétention d'identification causale. Le candidat 0.3 réutilise le module numérique de F/H sur tous les exemples et initialise leurs corrections symboliques à zéro. Les opérations changent, les comptes de paramètres restent inchangés. Aucune vérification sur un réseau instancié n'a été réalisée.

## Ce qui reste proposé

Choix des encodeurs numériques plus expressifs, de l'optimiseur, des initialisations du cœur et de la base, et des budgets ; contrôles futurs des corrections non visitées ; règles de passage à plus grande capacité ; qualification des versions historiques et d'un test indépendant. Les bornes numériques et blocs calendaires sont désormais vérifiés, sans garantie de performance. Aucun point ouvert ne doit être transformé silencieusement en autorisation de construire ou d'entraîner un modèle.

L'archive de travail actuelle 0.3 est un complément documentaire et d'audit, distinct de l'ancienne 0.2 conservée. Elle ne duplique pas les données et les PDFs de l'archive scientifique 2.1. Pour les analyses, le fichier BCE et son audit doivent se trouver aux chemins de `research/trame_poc0/ecb_exploratory` déjà présents dans le dossier complet. Les mois crypto réservés restent protégés.
