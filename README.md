# TRAME — recherche sur un modèle chartiste génératif

Projet scientifique indépendant du bot BTC-PERP Hyperliquid. TRAME étudie comment représenter des courbes de marché comme un langage causal, puis comparer des architectures génératives de type GPT sur la prédiction de prix bruts. L'étude concerne plusieurs marchés et ne constitue pas une stratégie de trading déployée.

## État réel au 16 octobre 2026

Édition 2.4 : quatorze documents et un dossier consolidé de 102 pages. La conception du langage et les audits de données réelles sont engagés. Aucun modèle génératif n'a été entraîné et aucun avantage prédictif n'est démontré. Les tests synthétiques vérifient les outils de mesure ; ils ne sont pas des observations de marché.

## Parcours de lecture

- [Index scientifique et état courant](dossier/recherche_lcm/LIRE_EN_PREMIER.md)
- [Synthèse accessible](dossier/recherche_lcm/00_synthese_accessible.md)
- [Dossier PDF consolidé](output/pdf/TRAME_Dossier_complet.pdf)
- [Bibliographie](dossier/recherche_lcm/BIBLIOGRAPHIE_LIENS.md)
- [Journal des versions](dossier/recherche_lcm/JOURNAL_DES_VERSIONS.md)
- `research/` : protocoles, scripts d'acquisition, audits et rapports de qualification.
- `tools/pdf/` : générateurs historiques des documents, avec conventions de chemins à adapter avant réutilisation.

## Données et reproduction

Les données brutes téléchargées et archives complètes restent sur le poste local et sont exclues de Git dans l'attente d'une revue des droits de redistribution de chaque fournisseur. Les scripts, URLs de provenance et empreintes permettent d'en retrouver l'origine. Les liens vers les archives ZIP dans les documents historiques ne sont donc utilisables que dans la copie locale complète. Cette séparation ne modifie ni les documents scellés ni leurs conclusions.

Tests du premier appareil de mesure : depuis `research/trame_poc0`, exécuter `python -m unittest test_research` avec NumPy installé. Les contrôles datés ont leurs propres instructions ; ne pas ouvrir des partitions de test pour une simple vérification de dépôt.

## Relation au bot

[hyperliquid-btc-pilot](https://github.com/goldaj/hyperliquid-btc-pilot) reste un projet distinct. Aucune intégration au bot, aucun déploiement ni aucune transaction ne découle de cette publication.

Les fichiers d'origine sont conservés dans leur ancien dossier pour préserver les liens des conversations existantes. Pour la suite, utiliser ce dépôt comme source de vérité TRAME ; ne pas développer les deux copies en parallèle.
