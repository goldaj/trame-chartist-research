# TRAME — veille et admissibilité des architectures externes
Date de vérification documentaire : **25 octobre 2026**.

Aucun modèle ci-dessous n'a été téléchargé ni exécuté dans TRAME.
Les versions, licences, prérequis et formats devront être
**revérifiés** au moment de l'intégration. Pas de réseau en CI
de recherche synthétique ; installation uniquement dans environnement
séparé avec provenance et empreintes.

| Candidat | Source primaire | Admissibilité actuelle TRAME |
| --- | --- | --- |
| Mamba-2 | https://github.com/state-spaces/mamba ; ICML 2024 https://proceedings.mlr.press/v235/dao24a.html | À implémenter/tester dans branche dédiée, non présent ici. Requiert une installation Linux/PyTorch spécifique ; les extensions accélérées sont dépendantes CUDA/HIP et doivent être opt-in. |
| **Mamba-3 (mars 2026)** | https://arxiv.org/abs/2603.15569 ; https://github.com/state-spaces/mamba | Ajouter en parallèle de Mamba-2, ne pas supposer que Mamba-2 reste la référence actuelle. Interface et précision matérielle à qualifier avant toute exécution. |
| Qwen3-Next / familles hybrides | https://qwen.ai/blog?id=qwen3-next | Inspirer un bras expérimental reproductible ; ne pas qualifier une simplification comme équivalente à l'implémentation du fournisseur. |
| TimesFM 3.0 | https://github.com/google-research/timesfm | **Poids 3.0 : licence non commerciale et non production** selon le dépôt officiel à la date de contrôle ; code Apache-2.0. Bras zero-shot *recherche seulement*, sous réserve de permission adaptée ; NO-GO par défaut pour une commercialisation locale de ces poids. Les anciennes versions peuvent avoir une licence distincte. |
| Chronos-2 | https://github.com/amazon-science/chronos-forecasting | Modèle préentraîné candidat zero-shot. Dépendances PyTorch/Transformers ; inspecter les licences du dépôt et du checkpoint précis, le corpus d'entraînement et l'éventuelle contamination, puis le coût local. |
| Moirai-2.0 | https://github.com/SalesforceAIResearch/uni2ts | Candidat de fondation temporelle ; inspecter code, poids/checkpoint, droits, provenance et traitement des variables exogènes avant usage. |

## Plan d'intégration prudent

1. Déclaration machine : `candidate_id`, `paper`,
   `source_repository`, `version_commit_or_tag`, `weights_uri`,
   `code_license`, `weight_license`, `commercial_eligible`,
   `training_data_known`, `hardware`, `download_size`,
   `forecast_interface`, `provenance`. Valeur inconnue = non qualifiée.
2. Pour Mamba-2 **et Mamba-3**, déployer un chemin expérimental
   explicitement distinct de la CI CPU actuelle, avec contrôles
   de device et équivalence des sorties/gradients ; ne pas installer
   des extensions CUDA silencieusement dans les pipelines.
3. Adapter chaque modèle au même contrat `observed_at` /
   `available_at` de l'étape 3. Les covariables futures ne sont
   autorisées que si elles étaient réellement connues à l'origine
   de prévision (calendriers déterministes ou publications attestées).
4. Mettre en place deux pistes non substituables :
   **from scratch** avec entraînement/données comparables,
   **zero-shot/pretrained** avec preuve de provenance et
   décontamination ; impossible de prétendre égaliser l'historique
   de préentraînement d'un fournisseur.
5. Pas de classement de performance financière tant que les
   données de marché point-in-time et les droits de leur
   utilisation restent **No-Go**, et pas d'intégration de poids
   non commerciaux dans un produit commercial.

## Pourquoi ne pas installer Mamba immédiatement en CI CPU ?

La CI existante se limite à un CPU standard avec PyTorch
et packages numériquement épinglés. Les accélérations Mamba
sur GPU imposent matériel et chaîne CUDA/HIP compatibles ;
l'API Mamba-3 évolue encore. L'objectif n'est pas de créer un
« Mamba » approximatif en le baptisant modèle officiel, ni
d'introduire des dépendances incontrôlées dans le projet.
Le GRU actuel est uniquement un **témoin récurrent**, jamais un
substitut de cette implémentation.
