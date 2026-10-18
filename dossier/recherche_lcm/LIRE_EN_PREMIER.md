# TRAME : dossier scientifique actif

**Édition 2.4 du 16 octobre 2026 : quatorze documents, 102 pages.** Le chapitre 13 précise une sortie générative GPT et présente le nouvel audit réel. Le plan général reste dans 11. P1-D est en révision 0.4 ; P1-B0 est en révision théorique 0.2, qualifiée partiellement et non entraînée.

La synthèse 00 reste une introduction de trois pages. Lire ensuite la section 1 du chapitre 13 pour l'avancée actuelle. Les documents 00-12 sont préservés exactement ; 13 amende les propositions génératives de 12 quand elles diffèrent. Aucun modèle, entraînement, achat ou résultat prédictif n'est annoncé.

| Document | Pages | PDF | Source modifiable |
|---|---:|---|---|
| 00 Synthèse accessible | 3 | [Lire](../../output/pdf/TRAME_00_synthese_accessible.pdf) | [Markdown](00_synthese_accessible.md) |
| 01 Papier de recherche | 5 | [Lire](../../output/pdf/TRAME_01_papier_recherche.pdf) | [Markdown](01_papier_recherche.md) |
| 02 Atlas des langages | 9 | [Lire](../../output/pdf/TRAME_02_atlas_des_langages.pdf) | [Markdown](02_atlas_des_langages.md) |
| 03 Faisabilité technique | 3 | [Lire](../../output/pdf/TRAME_03_faisabilite.pdf) | [Markdown](03_faisabilite.md) |
| 04 Tutoriel du POC au système | 3 | [Lire](../../output/pdf/TRAME_04_tutoriel_du_poc_au_systeme.pdf) | [Markdown](04_tutoriel_du_poc_au_systeme.md) |
| 05 Validation et panel critique | 15 | [Lire](../../output/pdf/TRAME_05_validation_et_panel.pdf) | [Markdown](05_validation_et_panel.md) |
| 06 État de l'art et sources | 12 | [Lire](../../output/pdf/TRAME_06_etat_art_sources_audit.pdf) | [Markdown](06_etat_art_sources_audit.md) |
| 07 Premières mesures réelles | 5 | [Lire](../../output/pdf/TRAME_07_premieres_mesures_reelles.pdf) | [Markdown](07_premieres_mesures_reelles.md) |
| 08 Marché latent et GPT | 7 | [Lire](../../output/pdf/TRAME_08_marche_latent_et_gpt.pdf) | [Markdown](08_marche_latent_et_gpt.md) |
| 09 Corpus, langage typé et protocole | 9 | [Lire](../../output/pdf/TRAME_09_corpus_langage_type_et_protocole.pdf) | [Markdown](09_corpus_langage_type_et_protocole.md) |
| 10 Du langage à l'expérience contrôlée | 12 | [Lire](../../output/pdf/TRAME_10_langage_hybride_et_experience_controlee.pdf) | [Markdown](10_langage_hybride_et_experience_controlee.md) |
| 11 Plan de recherche et personas | 4 | [Lire](../../output/pdf/TRAME_11_plan_recherche_et_personas.pdf) | [Markdown](11_plan_recherche_et_personas.md) |
| 12 Témoins numériques et génération causale | 7 | [Lire](../../output/pdf/TRAME_12_controles_numeriques_et_generation_causale.pdf) | [Markdown](12_controles_numeriques_et_generation_causale.md) |
| 13 Tête générative et audit des cibles | 7 | [Lire](../../output/pdf/TRAME_13_tete_generative_et_audit_des_cibles.pdf) | [Markdown](13_tete_generative_et_audit_des_cibles.md) |

[Dossier complet](../../output/pdf/TRAME_Dossier_complet.pdf) - [Archive complète actuelle](../../output/TRAME_dossier_et_sources.zip) - [Édition 2.4 figée](../../output/versions/TRAME_dossier_v2_4_scientifique_20261016.zip).

## Résultats de cette étape

Le codec en écarts depuis le prix reconstruit équivaut exactement à un état entier sur une grille logarithmique fixe. Le candidat décrit 276 positions GPT et trois sorties BASE/FLAT/HIER. HIER réduit les poids de sortie mais conserve les 4 096 contributions centrales du normalisateur à chaque pas.

L'audit porte sur la seule partition BCE 1999-2009 : 304 920 présentations recouvrantes, 15 360 cotations cibles distinctes. Zéro divergence entre les deux formulations ; borne de reconstruction satisfaite dans les calculs contrôlés. L'union contient 156 codes de -82 à 101, sans sortie du dictionnaire. Aucun résultat prédictif n'en découle.

Les bornes de paramètres proposées rendent mathématiquement presque nulle la masse hors dictionnaire. Elles restent des hypothèses de comparaison, pas une solution validée pour les crises. La normalisation stable, les gradients, la simulation et les scores en prix natifs demandent encore qualification. Un douzième cycle de personas simulés a produit ces objections ; aucune nouvelle validation indépendante.

## Sources et reproduction

[Statut actuel du plan](../../research/trame_research_plan/20261016/progress.json) - [Plan original](../../research/trame_research_plan/20261015/plan.json) - [P1-D 0.4](../../research/trame_protocol_p1d/protocol_candidate.json) - [P1-B0 0.2](../../research/trame_research_plan/20261016/p1b0_candidate.json).

[Déclaration d'audit](../../research/trame_research_plan/20261016/audit_protocol.json) - [Gel local](../../research/trame_research_plan/20261016/freeze.json) - [Résultats réels](../../research/trame_research_plan/20261016/target_audit_report.json) - [Contrôles arithmétiques](../../research/trame_research_plan/20261016/design_report.json) - [Lectures et limites](../../research/trame_research_plan/20261016/source_audit.json) - [Conventions de reproduction](../../research/trame_research_plan/20261016/README.md).

Les fichiers et données de 2.3 sont conservés. L'ancienne version P1-B0 0.1 reste dans le dossier daté 20261015 ; les contrôles 0.2 sont dans 20261016. Les labels futurs analysés étaient des valeurs historiques connues de la partition d'ajustement, pas des prédictions ni de nouveaux tests indépendants.

## Prochaine tâche concrète

Définir les scores communs en prix bruts et le contrôle d'erreur de simulation ; challenger les distributions et bornes sur une matrice de corpus et régimes déclarée. Puis qualifier les primitives numériques et gradients lors de la phase technique appropriée. Le réglage de P1-B0 et le test indépendant multi-marchés restent ouverts.

[Édition 2.3, 95 pages](../../output/versions/TRAME_dossier_v2_3_scientifique_20261015.zip) - [2.2, 84 pages](../../output/versions/TRAME_dossier_v2_2_scientifique_20261015.zip) - [2.1, 72 pages](../../output/versions/TRAME_dossier_v2_1_scientifique_20261015.zip) - [2, 63 pages](../../output/versions/TRAME_dossier_v2_scientifique_20261014.zip) - [1](../../output/versions/TRAME_dossier_v1_documentaire_20261014.zip).

[Journal](JOURNAL_DES_VERSIONS.md) - [Bibliographie](BIBLIOGRAPHIE_LIENS.md) - [Continuité](CONTINUITE.md).
