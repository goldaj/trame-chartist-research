# TRAME S3.1C — convergence et biais directionnel, 81 checkpoints BTC réels
**26 octobre 2026 — TERMINÉ.** [GitHub Actions #40309653884](https://github.com/goldaj/trame-chartist-research/actions/runs/40309653884) : **4/4 jobs verts** (D1/H1/M1 et agrégateur).

## Cohortes et méthode
Cette expérience **N'UTILISE PAS** les cibles du développement externe **2022–2025**, déjà trop étudié dans S1–S3.1B, ni le holdout **2026**.

Les sources sont toujours les véritables cours publics BTC/USD Bitstamp spot, vérifiés par empreintes Git :
- TRAIN_INTERNE : labels disponibles **strictement avant le 01/01/2020** ; D1 **2876**, H1/M1 **4096** cas. Seulement ces cas entraînent les réseaux, quantiles G2, normaliseur, prior directionnel et baselines.
- MONITOR_INTERNE : labels disponibles **du 01/01/2020 au 31/12/2021**, jamais gradients ; D1 **731**, H1/M1 **1024** cas. Sélectionnée par réservoir **indépendant** et RNG différent de TRAIN.
- Tout exemple dont le label n'était disponible qu'au **01/01/2022** est explicitement exclu.

Un seul choix d'architecture préenregistré : G2 signed quantiles TRAIN-only, width16/depth1, Joint Huber +0,5 BCE direction, trois graines 20261025/26/27, trois bras decoded, embedding_ordered et embedding_random. **27 trajectoires véritables** au total (3 horizons ×3 bras ×3 seeds), chacune avec **un même optimiseur continuant jusqu'à 2000 updates**, et des checkpoints à 200, 800, 2000 = **81 mesures**, PAS 81 entraînements indépendants.

Les bras learned ont +11 paramètres vs decoded, ordered/random strictement param-matched. Même backbone initial SHA, séquence minibatches, cible future et normalisation figée TRAIN.

## Tableau complet de la validation INTERNE 2020–2021
BA = balanced accuracy directionnelle % ; MAE = erreur prix en bps ; Amp = erreur d'amplitude absolue en bps ; UP = fraction de prédictions haussières ; mono = nombre de modèles presque monoclasse (≥99% d'un sens) sur 3 seeds ; Brier skill = amélioration vs prior P(up) de TRAIN (<2020), zéro = égal prior.

| Horizon | Bras | Updates | BA % | MAE bps | Amp bps | UP % | Mono/3 | Brier skill |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| D1 | decoded | 200 | **53,20** | **280,780** | **244,806** | 63,7 | 0 | +0,00069 |
| D1 | decoded | 800 | 51,18 | 282,671 | 249,874 | 85,3 | 0 | −0,00459 |
| D1 | decoded | 2000 | 52,24 | 282,704 | 248,938 | 69,3 | 0 | −0,00272 |
| D1 | ordered | 200 | 52,47 | 280,933 | 245,532 | 65,8 | 0 | +0,00094 |
| D1 | ordered | 800 | 51,99 | 282,289 | 252,168 | 86,0 | 1 | −0,00434 |
| D1 | ordered | 2000 | 52,30 | 284,334 | 252,847 | 75,9 | 0 | −0,00575 |
| D1 | random | 200 | 49,95 | 281,451 | 258,899 | 67,2 | 2 | −0,00458 |
| D1 | random | 800 | 50,15 | 282,261 | 252,086 | 97,8 | 2 | −0,00725 |
| D1 | random | 2000 | **48,77** | 284,348 | 250,133 | 88,1 | **2** | −0,01597 |
| H1 | decoded | 200 | 49,02 | 54,802 | 51,100 | 66,9 | 0 | −0,00636 |
| H1 | decoded | 800 | 50,37 | 54,890 | **47,995** | 42,5 | 0 | −0,00890 |
| H1 | decoded | 2000 | **51,93** | **54,611** | 48,955 | 61,6 | 0 | −0,00303 |
| H1 | ordered | 200 | 48,53 | 54,825 | 51,024 | 68,7 | 0 | −0,00771 |
| H1 | ordered | 800 | 49,74 | 54,924 | 48,607 | 66,8 | 1 | −0,01280 |
| H1 | ordered | 2000 | 51,42 | 54,656 | 49,104 | 58,2 | 0 | −0,00638 |
| H1 | random | 200 | 49,46 | **54,584** | 53,044 | 76,0 | 2 | −0,00052 |
| H1 | random | 800 | 50,35 | 54,703 | **50,819** | 72,4 | 1 | −0,00634 |
| H1 | random | 2000 | 50,56 | 54,727 | 51,104 | 63,0 | **0** | −0,00785 |
| M1 | decoded | 200 | 52,06 | 8,599 | **6,998** | 74,5 | 0 | +0,00359 |
| M1 | decoded | 800 | 51,27 | 8,387 | 7,483 | 45,3 | 0 | −0,00011 |
| M1 | decoded | 2000 | **53,02** | **8,368** | 7,319 | 49,7 | 0 | +0,00119 |
| M1 | ordered | 200 | 52,31 | 8,593 | **6,936** | 76,4 | 0 | +0,00325 |
| M1 | ordered | 800 | 51,49 | 8,381 | 7,369 | 45,8 | 0 | +0,00018 |
| M1 | ordered | 2000 | 52,65 | **8,366** | 7,410 | 52,5 | 0 | +0,00168 |
| M1 | random | 200 | 51,26 | 8,829 | 7,399 | 79,1 | 1 | +0,00175 |
| M1 | random | 800 | 51,57 | **8,368** | 7,325 | 55,7 | 0 | +0,00193 |
| M1 | random | 2000 | 52,34 | 8,392 | 7,225 | 55,8 | 0 | +0,00319 |

Les JSON rapportent AUSSI MAE USD, accuracy brute, loss TRAIN et monitor, norme de gradient moyenne sur les 50 dernières étapes, fraction de gradients clippés, Brier/CE détaillés et SHA initial modèle. Ne pas convertir les scores de prévision ponctuelle ci-dessus en croissance de capital.

## Conclusions chercheur et ingénieur
1. **Il n'existe pas de durée universelle d'entraînement.** D1 decoded a BA 53,20%/MAE 280,78 bps après 200, puis BA 52,24%/MAE 282,70 à 2000 : prolonger dégrade la direction ET le montant. H1 decoded s'améliore en BA 49,02→51,93 et légèrement en MAE 54,80→54,61 bps. M1 decoded 52,06→53,02 et 8,599→8,368 bps, MAIS l'erreur d'amplitude **se dégrade** 6,998→7,319 bps.
2. **Sous-entraînement explique une partie du collapse monoclasse** : H1 random 2/3 → 0/3 avec 200→2000 updates ; M1 random 1/3→0/3. Mais **D1 random reste 2/3 monoclasse**, et sa BA tombe à 48,77%, Brier skill −0,01597. Donc allonger sans discernement n'est pas une solution.
3. Norme moyenne de gradient (sur dernières 50 updates) a tendance à **décroître**, ex. H1 decoded 0,501 à 200→0,286 à 2000 ; M1 decoded 0,524→0,283 ; aucun signal général d'explosion constaté. C'est insuffisant pour déclarer la convergence.
4. **Brier skill** généralement près de zéro, parfois négatif sur H1/D1 ; classifieur directionnel peu calibré, même si BA s'améliore. La hausse de BA M1 ne démontre pas une stratégie financière viable.
5. **Loss Train vs monitor** ne doit pas être comparée directement d'un horizon ou régime à l'autre comme preuve d'overfit : amplitudes des retours et contextes diffèrent ; observer plutôt la tendance de chaque série et le décalage entre elles à budget donné. D1 monitor loss augmente globalement à 2000 ; H1 varie faiblement ; M1 baisse légèrement.
6. Toute l'étude est un **diagnostic interne 2020–2021**, pas un test indépendant de trading, ni une affirmation de généralisation 2022–25/2026. Les trois checkpoints d'une trajectoire sont corrélés, tout comme les contextes de bougies recouvrantes.

**Décision** : GO recherche vers comparaison causale **des fonctions de pertes direction vs magnitude** et/ou stabilité de l'optimiseur **avant** les gros embeddings vectoriels. Ne pas ouvrir 2026, ni réutiliser le dev externe 2022–25 pour ajuster une architecture. NO-GO sur une IA autonome de trading et une projection de PnL.

## Preuve et reproductibilité
[GitHub Actions run #40309653884](https://github.com/goldaj/trame-chartist-research/actions/runs/40309653884), 4/4 jobs verts, validation stricte : **27 trajectoires, 81 checkpoints, 27 lignes de synthèse et 18 contrastes appariés**. 5 fichiers sources JSON/Markdown agrégés, rétention Actions 30 jours :
- D1 `D1_S3_1C_pre2022_convergence.json` SHA256 `b755254a433099d6ea1cdaba19d6c3683af2daa4c673d425ccc579711255a38b`
- H1 `H1_S3_1C_pre2022_convergence.json` SHA256 `9b02cf9ca98e647a5472feb9bbe51c94b7238af5b61d8e6f41b55239011a4547`
- M1 `M1_S3_1C_pre2022_convergence.json` SHA256 `8e5b737621ee9ca0f50fb0776c9d2300dab5e1add6fa90346174ea3ce6e9b8ea`
- panel `S3_1C_81_internal_checkpoints.json` SHA256 `82e970a5303361174a1e46739deb8657e1678a5a2af2752c8694cf9fa11a3c2a`
- tableau `S3_1C_81_internal_checkpoints.md` SHA256 `db083e0d8c076ec47a084a4286c1b6621acadc0fe63d4a45b8e9fdd628e96b14`
- Modèle code exécuté Git SHA `e0dae968998cb7f19c37b9f819e1de5d7524dd27`.

## Prochaine sous-étape S3.1D proposée
Préenregistrer **une ablation pure de fonction de perte** sur train interne <2020/monitor 2020–21, G2 mêmes tokens, modèle, seed, budget d'updates, quantiles TRAIN-only ; comparer weighting BCE, loss de prix vs amplitude et entraînement dual-head. Ne pas changer en même temps la taille du réseau. Inclure contrôle random/ordered, direction équilibrée et montant. Privilégier un protocole minimal, pas une recherche infinie de winners sur 2020–21. Le DEV 2022–25 et HOLDOUT 2026 doivent rester hors sélection.
