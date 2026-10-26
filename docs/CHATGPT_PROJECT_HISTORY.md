# Historique ChatGPT — TRAME

**Index de contexte Codex créé le 2026-10-24. Non exhaustif.** Ce document n'est pas une transcription complète de toutes les séances ChatGPT ; les contenus originaux non récupérés ne sont pas inventés.

## Projet
Recherche indépendante sur l'encodage causal de séries de marché et la prédiction générative brute, sans stratégie de trading déployée.

## Documents déjà sources de vérité
Respecter les jeux train/validation/test et les résultats négatifs, préserver les protocoles gelés, ne pas confondre codec validé et preuve de prédiction. Ne pas toucher au bot Hyperliquid.

## Échanges historiquement identifiés
2026-10-16/18 — Assistant, résumé reconstruit, non verbatim : rédaction du dossier TRAME et protocole d'audit, sans modèle prédictif entraîné ni avantage démontré.

- **2026-10-18 13:24:13 UTC** — Utilisateur (extrait verbatim) : « N'écrase aucun repo existant. »
- **2026-10-24** — Utilisateur (résumé fidèle, non verbatim, heure inconnue) : demande un AGENTS.md pertinent et un journal par projet avec ses questions, les réponses, rôles et horodatages récupérables, à maintenir lors des changements Git.

## Restant à intégrer
Les conversations complètes, toutes les réponses exactes de l'assistant et les horodatages manquants nécessitent un export authentique. Quand il est disponible, ajouter les messages dans l'ordre en distinguant Utilisateur (verbatim), Assistant (verbatim) et résumé reconstruit. Examiner d'abord la confidentialité. Ne jamais modifier les anciens documents de contexte sans nécessité.

## 2026-10-25 — Recherche TRAME / laboratoire numérique P1-B0

**Utilisateur (verbatim, heure locale non enregistrée)** :
> tu vas maintenant retravailler sur TRAME. Continue les avancées de la recherche. Si tu as tous les éléments, tu peux commencer les développements pour des expériences. Sinon, continue d'avancer jusqu'à avoir le nécessaire.

**Assistant (résumé reconstruit, non verbatim)** :
- Contrôle GitHub : `main` sans nouvelle intervention depuis la
  revue du 24 octobre ; précédente PR `chatgpt/review-20261024`
  laissée intacte. Nouvelle branche parallèle autonome
  `chatgpt/p1b0-numerical-lab-20261025`.
- Relecture du candidat P1-B0 0.2, de ses audits et limites. Choix :
  la spécification est suffisante pour tester la **tête probabiliste**,
  pas pour entraîner ni certifier un GPT de prévision multi-marchés.
- Implémentation d'une loi numérique et de ses corrections BASE/FLAT/HIER,
  calcul log-domain, deux queues, gradient sur logit de correction,
  échantillonnage avec limites du sous-flux explicitement documentées.
- **Expérience construite** : 15 configurations de stress, 15 contrôles,
  amélioration de NLL sur une loi bimodale artificielle avec corrections
  entraînées, rejouabilité de 20 pas et score CRPS sur prix fictifs.
- Aucun accès aux données de marchés réservées, téléchargement,
  ordre, déploiement, modèle GPT entraîné ou prétention de prévision.
  Fichiers de protocole gelés et sources `main` inchangés.
- Les résultats numériques ont été exécutés localement sur fixtures
  artificielles. La CI GitHub sur branche vérifie et archive les
  rapports ; vérifier son verdict pour le HEAD avant fusion.

## 2026-10-25 — Demande de continuité autonome, étape 1 P1-B0

**Utilisateur, verbatim (heure locale non documentée) :**
> vas-y, avance sous étape par sous étape. Tu m'écrieras quand t'en finiras une, mais tu ne t'arrêteras pas pour autant. De la même façon, tu détailleras les sous étapes de la prochaine étape lorsque tu auras fini la première, puis tu commenceras la première sous étape de l'étape suivante. Etc... À chaque fois tu me préviens quand tu termines quelque chose, mais tu ne t'arrêtes jamais. Tu continueras jusqu'à avoir terminé toutes les étapes au complet, du mieux que tu puisses.

**Assistant, synthèse non verbatim et vérifiable dans les commits :**
- Branche superposée `chatgpt/p1b0-stage1-validation-20261025` basée sur
  `chatgpt/p1b0-numerical-lab-20261025`, sans fusion.
- 1.1 : P1-B0 différentiable en PyTorch CPU f64, croisements SciPy
  par différences finies et comparaisons sur corrections.
- 1.2 : mapping tanh / sigmoid borné, gradients saturés documentés.
- 1.3 : queue log-space et sampler conditionnel de stress via ndtri_exp ;
  tirage inconditionnel rare non certifié.
- 1.4 : replay causal 20 pas, état entier, teacher forcing ordonné.
- 1.5 : quantiles, couverture, CRPS prix et incertitude MC séparée.
- 1.6 : programme CPU incluant normalisateur ; coûts dépendants du matériel.
- 1.7 : décision de passage limité vers étape 2 **synthétique**, jamais marché réel.
- Aucune donnée financière réelle nouvelle, aucun réseau métier, compte ou transaction.
- Relever les runs CI de la branche avant d'affirmer qu'un commit particulier est vert.

## 2026-10-25 — Étape 2, poursuivie sans nouvelle validation utilisateur

**Utilisateur, instruction verbatim dans le bloc précédent de ce journal** :
continuer sans attendre à chaque jalon, documenter pour Codex.

**Assistant, résumé non verbatim et vérifiable :**
- Branche `chatgpt/mini-transformer-synthetic-20261025` à base de la
  branche de qualification de l'étape 1 ; aucun merge.
- Générateur de codes gaussiens arrondis AR(1) avec oracle connu,
  graines distinctes train/développement/test réservé, dernier verrouillé.
- Backbone Transformer minimal en f64, entrée de codes strictement antérieurs,
  masque causal vérifié par perturbation des futures entrées.
- Entraînement CPU de développement à budget fixé, comparaison oracle,
  sigma de persistance ajusté uniquement sur train, témoin régression
  linéaire ajusté seulement sur train ; tous les chiffres dans JSON CI.
- Préliminaire HIER et FLAT avec normaliseur 4096 complet, six
  mises à jour comparables en pas mais pas en capacité/compute.
- Sous-étapes 3.1 à 3.7 décrites dans
  `research/mini_gpt_synthetic/README.md` ; corpus réel qualifié absent.
- Pas de trading, d'API payante, de holdout ouvert ni de revendication
  de prévision financière.

## 2026-10-25 — Étape 3 point-in-time, arrêt scientifique motivé

**Utilisateur** : instruction de continuation autonome citée intégralement
plus haut, sans nouvelle demande de fusion ou d'exécution de trading.

**Assistant, résumé non verbatim :**
- Branche `chatgpt/point-in-time-data-contract-20261025`, dépendante
  de la branche `chatgpt/mini-transformer-synthetic-20261025`.
- Schéma à disponibilité UTC et révisions `asof.py`, refus des fournisseurs
  sans preuves de droits et provenance, tests adversariaux de
  fuite par révisions et valeurs impossibles.
- Codec P1-D `p1d_features.py` sur les 256 dernières observations
  disponibles, échelle sur 64 rendements passés uniquement,
  préservation du contrat float32/float64, tests sur 260 cours fictifs.
- Sources candidates BCE, FRED/ALFRED, crypto : non qualifiées;
  aucune nouvelle valeur de marché acquise.
- No-Go sur acquisition et entraînement réels, Go sur l'instrumentation
  méthodologique d'un benchmark synthétique.
- Prochaines sous-étapes 4.1–4.7 détaillées dans
  `research/market_data_contract/STAGE3_REPORT_20261025.md`.

## 2026-10-25 — Étape 4 scores appariés et arrêts explicites

**Utilisateur** : poursuivre TRAME sans attendre une validation
à chaque baby step, documenter pour Codex, commande verbatim plus haut.

**Assistant, résumé non verbatim et vérifiable :**
- Branche `chatgpt/paired-benchmark-sandbox-20261025`, basée sur
  la branche de qualification des sources étape 3.
- `research/benchmark_synthetic/bootstrap.py` : score MAE natif
  apparié par actif/horizon, horizon cohérent, interdiction des
  doublons de même origine, bootstrap par blocs déterministe.
- Tests synthétiques sans marché ; baseline persistance et
  témoins linéaires/oracle de l'étape 2 sont conservés.
- Étape 4 **incomplète** sur témoin financier réel et gel confirmatoire :
  aucune source qualifiée; étapes 5–7 sont explicitement No-Go.
- Ébauche autorisée d'un outil offline research-only étape 8,
  pas de produit financier prétendument prédictif.

## 2026-10-25 — Reprise après interruption de conversation

**Utilisateur (verbatim, heure locale non certifiée)** :
> la conversation Avancement_projets_codex_2_discussion_trop_longue a planté, sûrement parce que trop longue.
> J'aimerais que tu continues là où tu t'étais arrêté dans cette conversation.
> Fait moi un résumé de la consigne et un second résumé de là où tu en es,
> puis enchaîne tout de suite sur continuer.

**Assistant (résumé non verbatim)** : après recherche du contexte,
contrôle des branches et PR GitHub, confirme une version offline
`chatgpt/trame-research-lab-v01-20261025`. Branches d'étapes
1–4 présentes ; blocage confirmé de la qualification réelle des
sources point-in-time et des étapes financières 5–7. Continue par
une branche distincte `chatgpt/trame-lab-hardening-20261025`.

**Sous-étapes d'implémentation (vérifiables dans Git)** :
- 8.2a : affichage sémantique et textuel des NLL parallèlement au
  graphique SVG décoratif, lien clavier de contournement, tests HTML.
- 8.6a : plage 1–200 strictement validée avant entraînement,
  métriques artificielles finies, quantiles ordonnés, CRPS positif
  ou nul et mention obligatoire du benchmark fabriqué.
- Une note `research/trame_lab/HARDENING_NOTE_20261025.md` décrit
  le périmètre, l'absence d'audit navigateur réel et le risque de
  paire HTML/JSON non atomique.
- Aucun changement de modèle, de données, de partition, de marché,
  de déploiement ou de transaction.

**Attention** : ce journal reste un registre partiel. Les anciennes
réponses complètes et certains horaires ne sont pas disponibles ;
ne pas les inventer. Les checks CI doivent être contrôlés avant
que cette branche soit déclarée entièrement testée.

## 2026-10-25 — Suite du durcissement Research Lab

**Assistant (résumé non verbatim)** : étape 8.6b sur la même branche,
préparation de deux fichiers temporaires dans le dossier cible avant
remplacement, nettoyage systématique et test d'injection d'erreur
pré-publication qui protège la paire préexistante. Ne pas annoncer
une atomicité complète de deux chemins distincts : panne entre les
`replace`, exécution concurrente et `fsync` restent ouverts.


## 2026-10-25 — Utilisateur : généraliser la comparaison des architectures

**Utilisateur (verbatim, heure locale non enregistrée)** :
> Je te coupe vite fait pour te faire par d'une de mes craintes : Est-ce
> qu'on est sûrs que le transformer auto-régressif soit la bonne approche
> technique ? Je crois que c'est la techno qui était utilisée avant
> celle des LLM actuels. J'aimerais bien quand même la comparée en
> parallèle (sur tout ce qu'on va faire à partir de maintenant) à la
> techno des LLM actuels. Pour être sûr de ne pas rater quelque chose.
>
> Tu peux reprendre là où je t'ai coupé, en prenant en compte ces
> nouveaux éléments et en les documentant pour codex, comme tout le
> reste d'ailleurs.

**Assistant (résumé non verbatim)** :
- Clarification : l'autorégression n'est pas une famille d'architectures
  révolue ; les LLM GPT restent généralement décodeurs causaux.
  Mais le mini-Transformer initial de TRAME ne recouvre pas l'évolution
  des décodeurs et des familles SSM/hybrides.
- Instaure un programme multi-architectures permanent, sans hypothèse
  privilégiant les Transformers : `research/architecture_comparison/README.md`.
- Implémente une première comparaison **uniquement synthétique** entre
  `MiniTRAME` (attention classique), `ModernGPTMini` (mini décodeur
  RoPE/RMSNorm/GQA/SwiGLU), et `GRUMini` (témoin récurrent).
- Tests causaux, backprop, même mini-lots par seed, même sortie gaussienne
  et métrique NLL de développement ; **pas** de FLOPs/capacités égales,
  ni entraînement d'un LLM réel, ni Mamba.
- Prévoit Mamba-2 (et désormais Mamba-3), hybrides, modèles de fondation chronologiques
  et comparaisons compute-fair dès que le périmètre de recherche
  et les licences le permettent.
- Aucune modification des expériences scellées ni du bot Hyperliquid ;
  CI de la branche à vérifier avant toute affirmation de succès GitHub.


## 2026-10-25 — Intégration de la comparaison à TRAME Research Lab

**Assistant (résumé non verbatim)** : ajoute `architecture_comparison`
au JSON émis par `run_lab` et un tableau HTML avec chaque architecture,
seed, paramètres et NLL de développement artificiel. Contrôles
bloquant les présentations mensongères de données réelles ou d'équité
de calcul ; tests du rendu et des garde-fous. L'entraînement reste
CPU synthétique, sans marché. Les runs GitHub Actions du HEAD exact
doivent être vérifiés avant de conclure que l'intégration est verte.


## 2026-10-25 — Étape A3a, contrôle du nombre de paramètres

**Assistant (résumé non verbatim)** : ajoute `choose_widths`
pour choisir les largeurs des trois bras à proximité de
2 610 paramètres (référence Transformer). Des tests locaux
sur le POC artificiel démontrent le choix de largeur 16
pour les deux attention et 20 pour GRU. Les nombres
2 610 / 2 418 / 2 602 apparaissent dans les sorties,
sans prétendre une égalisation de FLOPs, de puissance,
ni une préférence financière. Le rapport HTML expose aussi la largeur.
La CI du dernier commit reste la source de vérité pour les tests GitHub.


## 2026-10-25 — Étape A3b : diagnostic CPU complémentaire

**Assistant (résumé non verbatim)** : ajoute
`research/architecture_comparison/cost_audit.py` et ses
tests, avec temps médians forward et forward+backward sur
entrée artificielle, trois familles × trois largeurs.
Les JSON sont archivés par GitHub Actions dans le même artéfact
que l'étude NLL, avec vérification synthétique explicite.
Aucune déclaration de FLOPs équivalents ou de prévision réelle.


## 2026-10-25 — Mise à jour Mamba-3 et licences

**Assistant (résumé non verbatim)** : vérifie les sources officielles
et découvre Mamba-3 (mars 2026), à inclure au même titre que Mamba-2.
La fiche d'admissibilité des modèles externes documente les besoins
GPU et les différences entre licence du code et des poids.
TimesFM 3.0 est identifié comme **non commercial/non production**
pour les poids publiés par Google à cette date. Rien n'a été
téléchargé, installé ni évalué sur de vrais cours.


## 2026-10-25 — Référentiel Bitcoin privé dédié : décision courante

**Utilisateur (verbatim, sans horodatage intra-journalier fiable)** :
> en fait j'ai rechangé d'idée. À la place on va utiliser un repo privé dédié à l'exposition des données bitcoin. C'est ça que tu va référencer à partir de maintenant. Si besoin tu peux les télécharger et les copier dans ton propre repo, mais si pas besoin c'est peut être mieux de juste les lire directement depuis le repo privé à chaque fois, pour ne pas alourdir le repo de recherche inutilement.
> Normalement le repo privé est déjà créé, tu devrais pouvoir t'en servir en l'état. C'est dans une release dédiée normalement. Même consigne qu'avant, ne regarde pas la provenance, utilise en l'état, on fait confiance à ces données.

**Assistant (résumé non verbatim)** :
- Confirme que goldaj/btc-historical-data est privé et dispose de la
  release btcusd-bitstamp-2010-2026-reference-v1, publiée le 25/10.
- 21 assets (3 fichiers de D1, 16 gzip H1/M1, manifeste, SHA256).
  Cette release n'est pas limitée à 90 jours comme les artifacts Actions.
- Arrête la piste « copier les prix du repo bot dans TRAME ».
  TRAME conserve l'intégralité des codes et tests ; les prix réels
  restent dans la bibliothèque dédiée, avec acquisition explicite
  dans le cache utilisateur authentifié par GitHub CLI.
- Le tag de release est fixé pour la répétabilité ; ne jamais
  utiliser implicitement la dernière version d'un fichier.
- Les expériences continuent à respecter les partitions temporelles,
  gaps et volumes nuls. Aucun audit de provenance effectué ni demandé.
- Consignes détaillées pour Codex dans research/btc_h1_m1/README.md
  et AGENTS.md ; CI avec archives fictives, sans accès au repo privé.

## 2026-10-25 — Fin de la parenthèse BTC, rappel de la roadmap et PAUSE

**Utilisateur (verbatim, heure locale non enregistrée)** :
> ok maintenant que c'est fait on peut reprendre là où on en était avant tout ce tintouin sur l'historique btc. C'était quoi déjà ? Liste moi les prochaines étapes. Ne les reprends pas pour l'instant. On va stopper l'execution temporairement.

**Assistant (résumé non verbatim)** : identifie le point d'arrêt
sur le chantier multi-architectures : A1/A2 achevés en synthétique,
A3a (rapprochement de paramètres) terminé, A3b (diagnostic CPU)
partiel, **A3c compute-fair** prochaine sous-étape, puis A4 Mamba-2
et Mamba-3, A5 hybrides, A6 séries temporelles préentraînées,
A7 validations financières, A8 Research Lab. Projette ensuite des
phases de produit P1 sélection/entraînement, P2 robustesse,
P3 évaluation économique, P4 TRAME Predictive v1. Rappelle que les
releases BTC existent mais qu'aucun avantage prédictif réel n'est
établi. **Aucune reprise ni merge autorisés pendant cette pause.**

**Utilisateur (verbatim, heure locale non enregistrée)** :
> Documente tout ça correctement dans le repo pour quand codex reprendra le relai.

**Assistant (résumé non verbatim, intervention documentaire)** :
crée `docs/CODEX_REPRISE_TRAME_PAUSE_20261025.md`, référence cet
état dans `AGENTS.md`, le README racine et les documents des
architectures/données, puis consigne ces échanges. Seules des
modifications documentaires sont demandées. Aucun entraînement,
téléchargement d'assets, ouverture du holdout, travail Mamba, merge
ou opération sur le bot n'est effectué à cette occasion.

**Instruction prioritaire pour Codex** : ne pas interpréter la
feuille de route comme une autorisation de continuer. Attendre
une demande explicite de reprise, puis commencer par **A3c.1**
avec garde-fous et compte rendu de chaque baby step.

## 2026-10-25 — Reprise autonome de TRAME après la pause (dernier ordre)

**Utilisateur (verbatim ; heure précise non enregistrée dans le journal)** :
> continue en tant que chercheur, avec une composante ingénieur. Tu liste l'ensemble des tâches à réaliser de façon assez détaillées, puis à chaque fois de commencer une tâche tu listes ses sous-tâches.
> Ensuite tu me préviens à la réalisation de chaque nouvelle sous tâche. Tu ne t'arrêtes pas tant que tu n'as pas intégralement fini toutes les tâches, et donc toutes leurs sous tâches aussi.

**Assistant (résumé non verbatim)** : considère cet ordre comme la levée
explicite de la pause précédente et crée le tableau de bord actif
`docs/CODEX_EXECUTION_BOARD_20261025.md`. Il commence A3c sur une
branche dépendante de la PR #9 et ouvre la PR #10 (draft).

**A3c.1–A3c.5 (résumé non verbatim, artefacts vérifiables)** :
- Protocole enregistré, instrumentation `torch.profiler` CPU, tests
  synthétiques, extension optionnelle des trois modèles à 128 tokens,
  invariance causale/gradient vérifiée à 64 tokens.
- Pilote à trois graines et budget *d'opérations partiellement
  comptées*, avec plan de pas appariés, sans test réservé.
- GitHub Actions #40219261965 : succès avec deux JSON archivés ;
  résultats chiffrés et limites dans
  `research/architecture_comparison/A3C_RESULTS_20261025.md`.
- **GO** pour les recherches exploratoires suivantes ; **NO-GO**
  pour une quelconque affirmation de parité compute complète,
  modèle gagnant, avantage financier ou produit prêt.

**Prochain démarrage scientifique : A4** Mamba-2/Mamba-3 sur
vraies implémentations GPU isolées, après qualification officielle.
Les PR #8/#9/#10 restent en draft, aucune fusion automatique.


## 2026-10-26 — Clôture A7.5-H1 après interruption, sur instruction utilisateur

**Utilisateur (verbatim, heure locale exacte non enregistrée)** :
> tu t'es arrêté en plein milieu de quelque chose je crois. Explique moi ce que tu dois continuer avant de t'arrêter proprement ou dit moi que c'est bon si t'as fini ce que tu voulais faire et que c'est juste l'arrêt qui a crash.

**Assistant (résumé non verbatim)** : signale que l'analyse du rapport
H1 réel par régimes n'a pas été lue/documentée, et liste trois
opérations de clôture : (1) lire le JSON H1 par années et volatilité,
(2) consigner les constats dans TRAME, (3) terminer la passation Codex
et la vérification GitHub, puis **s'arrêter**.

**Utilisateur (verbatim, heure locale exacte non enregistrée)** :
> vas-y continue alors

**Assistant (résumé non verbatim, travaux effectivement accomplis)** :
- Récupère l'artefact **privé** issu du succès GitHub Actions
  #40224149619 ; lit `btc_h1_real_regime_development.json`,
  et vérifie ses champs et son SHA-256 :
  `95be1bc04dd44aa6534ef298916f7ecb9802c27f0280199d92ca32783dfb9236`.
  Aucune archive de prix brute copiée dans TRAME public.
- Contrôle que les découpages H1 développement font chacun
  **1 024** observations (années 2022/23/24/25 :
  257/284/228/255 ; volatilité passée faible/moyenne/forte :
  541/361/122). Les moyennes pondérées reconstituent la
  persistance globale **MAE 183,51822265625 USD**,
  Ridge **MAE 183,72069709370587 USD**,
  couverture **95,3125 % / 95,5078 %**.
- Constate que la MAE relative persistance en bps va de
  **21,929** en faible volatilité à **71,785** en forte.
  Les intervalles théoriques 80 % couvrent 99,261 % des
  observations calmes et 83,607 % des plus volatiles.
  Ces différences sont **descriptives**, aucune preuve
  de généralisation ou avantage économique.
- Crée
  `research/btc_h1_m1/A7_H1_REGIMES_REAL_RESULTS_20261025.md`
  dans la branche de [PR #14](https://github.com/goldaj/trame-chartist-research/pull/14),
  puis met à jour `A7_STATUS_20261025.md`,
  `docs/CODEX_EXECUTION_BOARD_20261025.md`,
  `AGENTS.md` et ce journal.
- **État réel** : A7.4 H1/M1 et A7.5-H1 témoins exécutés,
  mais A7.5 complète, Mamba GPU, fondations zéro-shot,
  tests indépendants et produit P4 non achevés. Aucun
  merge, ordre de trading, usage du test 2026 ou
  promesse de travaux asynchrones.

**Dernière décision** : arrêt propre à la fin de cette
passation. Une prochaine session pourra suivre les tâches
encore ouvertes uniquement sur nouvelle instruction explicite.


## 2026-10-26 — Nouvelle séance S1 : mise à l'échelle et justesse directionnelle

**Horodatage** : date connue, heure exacte non attestée. Le texte utilisateur
ci-dessous provient de la conversation courante, sans prétendre reproduire
l'intégralité des échanges précédents.

**Utilisateur, demande initiale (verbatim)** :
> Faisons ça. D'ailleurs tu parlais de models 1 couche, peut être qu'il faudra aussi en parallèle tester des models multi-couches (3 niveau de couches différents ? A appliquer sur chacune des tailles de model qu'on veut tester ?). Documente bien tout, puis prépare tout le nécessaire pour lancer tout ce que tu viens de dire. Et oui ton intuition est importante ; la justesse directionnelle est hyper importante et doit aussi faire partie des résultats qu'on étudiera dans le tableau final. Continue en tant que chercheur ET qu'ingénieur vers ces solutions. Liste les étapes, réfléchi aux sous étapes avant d'avance sur la prochaine étape. Puis annonce moi chaque sous étape terminée, avant de continuer automatiquement.

**Utilisateur, précision intervenant pendant le développement (verbatim)** :
> ne te soucis pas des frais dans ces simulations. On extrapole que si le sens est bon, un trader saura si ça vaut le coup d'acheter ou pas. C'est là où la précision du montant déduit fait son importance

**Assistant, synthèse de décisions et travail réel (NON verbatim)** :
- Matrice 5 cibles de paramètres × 3 profondeurs 1/2/4 × 3 familles de modèles ;
  2 horizons H1/M1 × 3 seeds soit 270 entraînements envisagés.
- Justesse directionnelle, couverture du signal et erreur d'amplitude prévues
  au même niveau que MAE et NLL. Illustration de rendement brut par bougie
  sans frais, **jamais** confondue avec capitalisation ou PnL validé.
- Nouveau protocole, modèles multicouches, métriques, orchestrateur,
  tests et documentation sur la branche
  `chatgpt/trame-scaling-depth-direction-20261026`, basée sur PR #14.
- La qualification CI doit être vérifiée ; ni vraie campagne 270 modèles ni
  validation indépendante 2026 annoncées sans run effectif.
- Les données BTC brutes restent privées, le bot Hyperliquid inchangé.


## 2026-10-26 — Instruction corrective D1, au cours de la séance S1
**Heure exacte non fournie pour le message individuel.** La citation
Utilisateur qui suit est **verbatim** de la conversation en cours.

**Utilisateur** :
> **dans tous nos calculs, là, on a H1 et M1, pourquoi on n'a pas D1 (en daily), c'était aussi dans le repo, même si c'était peut être dans une autre forme. Reprends TOUT depuis qu'on a utilisé les nouvelles données et inclus aussi D1. Fait ça avant de reprendre la suite. Tu me préviendras quand tu y seras (mais sans t'arrêter pour autant).**

**Assistant, synthèse non verbatim de la mise en œuvre** :
- Après audit, trouve que `research/btc_h1_m1/daily.py` savait déjà
  lire les trois fichiers D1, mais qu'aucun des pipelines de prévision
  A7/S1 n'acceptait D1. Réutilise ce lecteur unique sans fabriquer
  de bougies de 2010–2011 (segment indicatif close-only).
- Ajoute D1 à `stream.iter_cases`, modèles A7, témoins Ridge/persistance,
  analyse par régimes et matrice de scaling 5 tailles × 3 profondeurs
  × 3 familles ; D1/H1/M1 total théorique 405 fits avec 3 seeds.
- PR #18 draft empilée sur PR #17 puis PR #14.
- Réexécute réellement D1 A7/témoins/régimes/direction : privé
  [#40280347574](https://github.com/goldaj/btc-historical-data/actions/runs/40280347574),
  succès ; H1/M1 harmonisés : privé
  [#40280464439](https://github.com/goldaj/btc-historical-data/actions/runs/40280464439),
  succès des deux jobs ; test 5 tailles × 3 profondeurs sur les
  trois résolutions : privé
  [#40281223578](https://github.com/goldaj/btc-historical-data/actions/runs/40281223578),
  6/6 jobs réussis, **mais une seule graine, et 8 updates pour
  les grands modèles**.
- La précision directionnelle est trompeuse si les modèles
  prédisent toutes les observations en hausse. Ajoute des témoins
  toujours-up/down et un résumé de la balanced accuracy. Aucun
  « gagnant » ni avantage financier n'est déclaré.
- Lance une expérience de convergence séparée 200 updates, 3 graines,
  trois tailles de modèles, les trois profondeurs et trois
  résolutions sur la branche privée
  `chatgpt/trame-private-scaling-convergence-20261026`
  (workflow #40281657954 ; vérifier l'état au moment de lecture).
- Documente preuves et limites dans
  `research/btc_h1_m1/D1_H1_M1_REAL_RESULTS_20261026.md`,
  `research/scaling_study/S1_REAL_GRID_CANARY_20261026.md`
  et `docs/CODEX_D1_HANDOFF_20261026.md`.
- Les prix bruts restent privés ; jamais d'ouverture 2026,
  pas de frais ni de trading exécuté ; H1/M1 historique conservé.


## 2026-10-26 — Poursuite S1 scientifique, puis branche S2 (résumé)
**Horodatage du message utilisateur individuel non disponible.**
Les réponses/étapes ci-dessous sont un relevé d'activités,
**pas un verbatim assistant**.

**Instruction utilisateur applicable (présente dans les échanges
précédents de cette séance)** : inclure D1 avant toute suite,
chercher et ingénierie par sous-étapes, profondeur 1/2/4
pour chaque taille, donner une importance majeure à la
justesse directionnelle et à l'amplitude, aucun frais de trading.

**Assistant — preuves finalisées avant S2 :**
- Reprend D1 depuis la release originale, données réelles D1/H1/M1,
  inclut tous les rapports A7, régimes, témoins statistiques,
  justesse directionnelle et montant.
- Exécute sur la vraie release privée 135 fits (5 tailles × 3
  profondeurs × 3 familles × 3 horizons, une graine / 40 steps
  petits modèles ou 8 grands), GitHub Actions
  [#40281223578](https://github.com/goldaj/btc-historical-data/actions/runs/40281223578),
  6 jobs réussis, param count réel ~1.7k–2.39M.
- Exécute ensuite 243 fits (3 tailles × 3 profondeurs × 3 familles
  × 3 graines × 3 horizons, 200 steps), GitHub Actions
  [#40281657954](https://github.com/goldaj/btc-historical-data/actions/runs/40281657954),
  3 jobs réussis. Balanced accuracy pratiquement à 50 % sur
  beaucoup de bras ; malgré l'entraînement plus long aucun
  « plus gros = mieux » validé.
- Publie uniquement les rapports chiffrés agrégés et SHA sur
  les branches PR #18, conserve les JSON complets dans les
  artefacts du dépôt de données **privé**. Aucune label 2026
  ouverte, jamais d'ordre ni de bots modifiés.

**Assistant — nouvelle expérimentation, sans résultat BTC réel :**
- Pré-enregistre S2 : `research/continuous_direction/PROTOCOL_20261026.md`.
- Développe une entrée bps continue causale, régression Huber
  et double objectif Huber+BCE du sens, 2 profondeurs/2 largeurs,
  3 graines sur les trois horizons.
- Crée la PR draft #19, tests CI publics synthétiques réussis,
  documentation et passation Codex.
- Tentative de créer la CI privée d'exécution S2 **refusée
  par contrôle de sécurité du connecteur** ; la branche privée
  dédiée existe mais ne comporte aucun workflow S2 exécutable,
  aucune campagne S2 réelle lancée. Pas de contournement tenté.
- Statut scientifique : résultats S1 A7 réels acquis,
  S2 implémenté et testé **sur cas fabriqués uniquement**.
