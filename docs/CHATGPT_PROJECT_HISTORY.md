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


## 2026-10-26 — Reprise après interruption (messages et état)
**Utilisateur, citation textuelle (horodatage précis non disponible)** :
> t'as crash, reprends

**Assistant, activité réellement effectuée (résumé, non verbatim)** :
- Relit l'état du dépôt GitHub TRAME PR #19 et la CI réussie
  initiale. Conserve l'arrêt sécurité du workflow privé S2
  et refuse d'inventer des résultats BTC S2.
- Audite la calibration de la tête binaire : introduit
  `research/continuous_direction/diagnostics.py` et ses
  tests. Les probabilités du bras régression sont non entraînées :
  elles sont explicitement non scorées. La classe haussière
  train-only a un prior lissé Jeffreys, et Brier/entropie sont
  comparés à ce prior.
- Ajoute le témoin naïf du rendement moyen d'entraînement,
  pour comparer le montant prévu et non seulement le signe.
- Sépare le SHA de la version du code modèle et le SHA de
  la CI privée ; ajoute un hash du calendrier d'origines
  sans prix ni label, et refuse un SHA de code absent pour
  tout résultat étiqueté BTC réel.
- Corrige la conversion de prévisions extrêmes : rejet
  explicite plutôt que plafond silencieux.
- Crée `research/continuous_direction/panel.py`,
  `test_panel.py`, et fait exécuter les tests sur fixtures
  uniquement, pour un tableau apparié sign+amplitude+Brier.
- Recalcule le diagnostic original de 243 entraînements réels
  S1 (aucun nouvel entraînement) et constate monoclasse
  ≥99 % : D1 72/81, H1 45/81, M1 34/81. L'architecture
  H1 meilleure sur balanced accuracy moyenne (52,10 %)
  ne bat pas la persistance sur MAE bps.
- Place les preuves et limites dans
  `research/scaling_study/S1_SIGN_COLLAPSE_REAUDIT_20261026.md`,
  `research/continuous_direction/PROTOCOL_20261026.md`,
  `docs/CODEX_S2_HANDOFF_20261026.md`, et la PR #19.
- Aucun nouveau workflow privé ni campagne réelle S2
  n'ont été lancés à cause du refus de sécurité précédent.
  Néanmoins, la suite a pu avancer en code/CI/tests/documentation.


## 2026-10-26 — Demande « différentes grammaires » (verbatim)
**Utilisateur (date connue, heure individuelle non attestée)** :
> continue ce que tu propooes.
> Par contre j'aimerais qu'on réfléchisse aussi à différente grammaires prochainement. C'est à dire la façon dont on converti les courbes en token. Peut être qu'il y a d'autres pistes à étudier que celle qu'on a testé. Faut documenter cette intuition et la caler dans les choses à faire un jour. Je te laisse trouver la bonne temporalité pour se lancer dans ce sujet.
> Et comme d'hab, documente tout bien pour codex aussi.

**Assistant (résumé non verbatim, étapes réalisées)** :
- Confirme la poursuite de S2, mais S2 réel demeure bloqué par
  le refus de création de workflow privé au tour précédent ;
  pas de contournement ni faux résultats BTC S2.
- Détermine un calendrier scientifique : S3.0 revue et tests
  de perte d'information sur séries inventées **maintenant**,
  S3.1 vraies ablations de grammaire **après S2 réel**, et
  **avant** le retour à du scaling massif sur de nouveaux réseaux.
- Etudie des références existantes Chronos (quantification),
  PatchTST (patch tokens), TOTEM (codebooks/quantification
  apprise), TimesFM (patch continu), et huit familles
  supplémentaires de représentations possibles.
- Consigne hypothèses, critères de validation, schémas D1/H1/M1,
  train-only pour les seuils, risque de fuite de clôture H1/D1
  dans `research/token_grammar/ROADMAP_20261026.md`.
- Implémente PoC purement diagnostic
  `research/token_grammar/diagnostics.py` et tests
  `test_diagnostics.py` sur séries chiffrées **inventées** :
  quantification ancienne, retour continu, bandes
  signées fixes, quantiles de magnitude train-only.
  Aucun entraînement ou benchmark BTC réel S3.
- CI publique du module passée, intégrée à
  `.github/workflows/trame-s2-continuous.yml`.
- Crée issue de backlog dédiée
  https://github.com/goldaj/trame-chartist-research/issues/20 ;
  met à jour `AGENTS.md` et
  `docs/CODEX_S2_HANDOFF_20261026.md` afin que Codex
  priorise le chantier au bon moment.


## 2026-10-26 — Demande de poursuite S2/S3 (verbatim)
**Utilisateur** :
> continue

**Assistant, résumé non verbatim du travail autorisé en conséquence** :
- Avant une campagne BTC réelle S2 (toujours bloquée par une
  précédente décision de sécurité sur le workflow privé),
  examine le protocole : S1 changeait à la fois codec de
  rendement, cible, tête/objectif et architecture ;
  comparer S1 à S2 ne permet pas d'attribuer un gain
  éventuel à la « grammaire » des tokens.
- Crée une **nouvelle branche / PR #21** S2b, basée sur
  PR #19 S2 : `chatgpt/trame-representation-ablation-20261026`.
- Préenregistre `research/representation_ablation/PROTOCOL_20261026.md`
  avant mesure BTC réelle : ablation entrée arrondie
  vs entrée continue, toutes deux prédites sur les
  **mêmes vraies cibles continues**, à loss Huber
  ou Huber+BCE identique, mêmes minibatches,
  graines, initialisation et contexte causal de 20 bougies,
  normalisation des entrées train-only et échelle
  de cible commune train-only.
- Matrice potentielle : 2 codecs × 2 losses × 2 largeurs
  × 2 profondeurs × 3 horizons (D1/H1/M1) × 3 graines =
  **144 entraînements réels prévus, non lancés**.
- Implémente `runner.py` avec SHA256 des poids initiaux,
  contrôle des rendements arrondis nuls, traces de
  modèles et origines, refus de 2026, sans transaction.
- Implémente `panel.py` avec différences appariées
  `continuous - quantized`, erreur d'amplitude en
  bps/USD et balanced accuracy, contrôle de l'intégrité
  des SHA d'initialisation. Tests sur données inventées
  `test_ablation.py`, `test_panel.py`, et ajout
  d'un test de réplication numérique exact de S2
  pour le bras continu.
- La CI publique `.github/workflows/trame-s2b-representation.yml`
  qualifie uniquement des fixtures synthétiques et les
  anciens tests S2/S3. La passation détaillée Codex
  est `docs/CODEX_S2B_HANDOFF_20261026.md`.
- L'issue S3
  https://github.com/goldaj/trame-chartist-research/issues/20
  reste la priorité **après** une première évaluation
  réelle de S2/S2b et **avant** les grands modèles.
- Aucune donnée ni clé privée publiée, aucune cible 2026
  ouverte, aucun ordre de trading ou changement Hyperliquid.
  Le refus précédent de créer un nouveau workflow
  privé S2 **n'a pas été contourné**.


### 26 octobre 2026 — S2b, correction méthodologique AVANT tout run BTC réel
**Assistant, synthèse non verbatim** :
- Après la création de PR #21 et un premier passage CI,
  constate qu'une normalisation d'entrée différente par
  représentation confondrait en partie l'effet du codec
  et celui de l'échelle de ses entrées.
- **Remplace** les normalisations d'entrée propres à chaque
  bras par `std(continuous_train_past_bps)`, **unique pour
  les deux bras**, calculée sur TRAIN exclusivement.
  L'échelle des cibles reste la MÊME valeur train-only.
  La variance native de l'entrée quantifiée est toujours
  consignée uniquement comme diagnostic ; la valeur
  d'un retour n'est jamais censurée ou « recréée ».
- Les tests vérifient parité des échelles en plus des
  SHA des poids initiaux, et l'analyse finale rejette
  les couples non appariés. **Ce changement précède
  toutes les mesures BTC réelles S2b.**
- Aucun workflow privé créé, pas de contournement du
  blocage précédent de la campagne S2, pas de résultats
  de direction BTC S2b calculés ou inférés.


## 2026-10-26 — Poursuite « continue » : S3.0c diagnostic de grammaires
**Instruction utilisateur appliquée (verbatim du message le plus
récent ; aucune nouvelle instruction utilisateur depuis)** :
> continue

**Assistant, activité non verbatim réellement effectuée** :
- Après S2b PR #21 (input quantifié/continu à loss/cible
  et échelles d'entrée/sortie communes, CI synthétique
  réussie), poursuit la partie S3.0 de la demande
  « différentes grammaires » formulée précédemment.
- Crée une branche enfant **PR #22**
  `chatgpt/trame-grammar-audit-20261026`, base PR #21,
  sans fusionner ni modifier les branches sœurs.
- Implémente `research/token_grammar/audit.py` :
  diagnostic **strictement NON prédictif** sur les
  20 returns passés de chaque `Case`, des
  quatre grammaires initiales G0a (entier historique),
  G0b (continu), G1 (magnitudes signées fixes),
  G2 (magnitudes signées quantiles fit TRAIN ONLY).
  Tests `test_audit.py` sur données inventées.
- Les chiffres de tokens sont calculés sur contextes
  qui se recouvrent fortement ; la colonne
  `context_token_observations_overlapping=true`
  doit empêcher toute fausse interprétation
  d'indépendance statistique.
- Prépare les commandes éventuelles de diagnostic
  D1/H1/M1 sur les archives **privées**
  dans `research/token_grammar/AUDIT_README_20261026.md`,
  mais **aucune exécution BTC réelle ni téléchargement
  privé n'a été réalisé** pour S3.
- CI publique `.github/workflows/trame-s3-grammar-audit.yml`
  sur fixtures uniquement. Documentation Codex dans
  `docs/CODEX_S3_HANDOFF_20261026.md` et `AGENTS.md`,
  issue #20 comme backlog de S3.1+.
- Conservé : train avant 2022, développement 2022–2025,
  2026 non ouvert, prix indicatifs D1 2010–2011 non
  transformés en fausses OHLCV, aucun ordre ou trading.
  Précédent blocage sécurité sur workflow privé
  S2/S2b non contourné ; les sorties S3 ne
  sont pas des résultats de prévision financière.


## 2026-10-26 — Demande d'utiliser directement les données BTC et autorisation de publication
**Utilisateur (verbatim, horodatage individuel non attesté)** :
> et qu'est-ce qui te bloque pour accéder aux données du repo privé ? Tu peux juste les dl et les intégrer dans ton repo en fait

**Utilisateur, précision intervenant immédiatement après (verbatim)** :
> si si tu peux les considérer publics, si tu prends les données historiques btc c'est rien de grave

**Assistant (synthèse non verbatim, actions réellement observées)** :
- Vérifie les permissions GitHub : accès en lecture **et**
  écriture confirmé sur `goldaj/btc-historical-data`.
  L'ancienne difficulté venait de la création d'un
  workflow GitHub Actions privé, puis de l'absence de
  transfert binaire direct des gzip dans le runtime,
  et non d'une impossibilité d'accéder à l'information.
- Constate que les 16 archives H1/M1 d'origine
  proviennent du dépôt **public** `alessiostomeo/btc-cycle-data`,
  commit `b57f460fab1afb82705eb813cee2ef4afb1f6848`.
  Conserve SHA Git blob et taille de chaque archive.
- Nouvelle branche **PR #23**
  `chatgpt/trame-public-btc-data-import-20261026`.
  Copie effectivement le CSV D1 2012–2026H1 dans
  **le repo public** TRAME (372096 octets,
  Git blob SHA `a8f2da91cb00fce75117ba5bf000384f240abd56`,
  preuve d'identité avec l'original privé).
  Adaptation du lecteur D1 pour travailler avec 2012+
  seulement **ou** avec les trois anciens fichiers,
  sans fabriquer de fausses bougies 2010/2011.
- Ajoute `research/data/public_data.py` pour télécharger
  les gzip H1/M1 depuis le dépôt public amont, vérifier
  octets et SHA Git, utiliser le même cache existant
  `TRAME_BTC_CACHE_DIR`, **sans aucun jeton privé**.
  Ne commit pas les ~113 Mo compressés directement dans
  Git pour éviter le gonflement de l'historique ;
  les téléchargements ont bien lieu sur runner GitHub
  au moment des expériences.
- Vérifie la source D1 en CI [#40295478147](https://github.com/goldaj/trame-chartist-research/actions/runs/40295478147).
  Puis exécute de vraies expériences BTC :
  D1 [#40295846917](https://github.com/goldaj/trame-chartist-research/actions/runs/40295846917),
  H1/M1 [#40296158821](https://github.com/goldaj/trame-chartist-research/actions/runs/40296158821),
  **trois jobs scientifiques authentiques réussis** ;
  4 bras S2b par horizon, 1 graine / 40 steps.
  Les résultats et SHA sont publiés dans
  `research/data/REAL_PUBLIC_BTC_RESULTS_20261026.md`.
- Audit information S3 sur vrais historiques :
  l'encodage entier historique perd le signe de
  ~2.86 % de rendements non nuls D1, 13.74 % H1,
  **64.26 % M1** dans les contextes dev étudiés.
  Ce n'est PAS une mesure de prédiction du futur.
- Lancement du protocole S2b complet à 144 fits
  3 graines/200 updates, workflow public
  [#40296933559](https://github.com/goldaj/trame-chartist-research/actions/runs/40296933559) ;
  **vérifier son résultat final** avant toute
  déclaration de réussite. Aucun ordre ni backtest
  de portefeuille exécuté.
- Préserve les attributions CC BY-SA/CC BY pour
  l'historique Bitstamp, et conserve D1 2010/2011
  hors repo public lorsque licence externe incertaine.
  Le consentement du propriétaire ne remplace pas
  des droits tiers. Gel 2026 toujours appliqué
  dans tous les runners ; frais de simulation ignorés.


### 26/10/2026 — Comparaison réelle 144-fit achevée (non verbatim assistant)
- À la suite de la permission explicite d'utiliser les
  cours BTC en public, exécute les vrais modèles S2b,
  sans workflow ni jeton du repo privé, sur Actions
  [#40296933559](https://github.com/goldaj/trame-chartist-research/actions/runs/40296933559),
  **3/3 jobs réussis**.
- 144 fits = trois horizons D1/H1/M1 × 2 codecs
  continu/arrondi × 2 losses Huber/joint ×
  2 largeurs 16/32 × 2 profondeurs 1/2 ×
  3 graines, **200 updates** chacun.
- 2026 demeure hors train/dev ; train D1 3608,
  H1/M1 4096, dev 1024 par résolution.
  Source Git publique épinglée, octets validés,
  aucune donnée de compte ou clé de trading.
- Conserve les 3 rapports sources agrégés sur
  Actions, SHA256 et tableau dans
  `research/data/S2B_REAL_PUBLIC_144_RESULTS_20261026.md`.
- Constate **absence de victoire récurrente**
  de l'entrée continue sur l'entrée arrondie en
  balanced accuracy et erreur amplitude/prix.
  De nombreux modèles restent monoclasse.
  L'information signée perdue par l'encodage
  n'est **pas** automatiquement une information
  prédictive utile.
- Priorité documentaire donnée à S3.1
  (grammaires token signés/magnitude,
  patch tokens ensuite) avec protocole
  apparié et 2026 réservé. Aucun ordre
  Hyperliquid, aucun PnL validé.


## 2026-10-26 — Reprise explicite après interruption (message utilisateur VERBATIM)
> continue, t'as crash

**Assistant, opérations effectivement réalisées (résumé, NON verbatim)** :
- Reprend au point exact après S2b, où 144 fits
  BTC PUBLICS D1/H1/M1 avaient réellement été
  exécutés et où la roadmap grammaires #20
  restait à transformer en expérience prédictive.
- Crée [PR #24](https://github.com/goldaj/trame-chartist-research/pull/24)
  enfant de #23 BTC public : projet S3.1A
  de comparaison **G0b continu, G0a arrondi,
  G1 magnitude à bins fixes signés et G2
  magnitude à quantiles estimés TRAIN ONLY**.
- Préenregistre `research/token_grammar/PREDICTIVE_PROTOCOL_20261026.md`,
  **AVANT tout nouvel essai BTC réel S3.1A**.
  Les tokens sont **reconstruits en scalaires**
  afin que l'architecture S2b, initialisation,
  cibles vraies, losses, mini-batches, échelles
  de normalisation restent appariés.
  Les embeddings catégoriels appris restent
  une étape S3.1B séparée.
- Étend le runner S2b par `feature_provider`
  *optionnel et rétrocompatible*, crée
  `research/token_grammar/predictive.py`,
  `predictive_panel.py`, tests pour train-only
  et réplication numérique stricte G0a/G0b.
- Corrige un YAML CI initial contenant un
  nom d'étape avec un deux-points non guillemeté.
  La CI devient verte sur fixtures inventées.
- Lance un pilote S3.1A BTC public D1/H1/M1,
  quatre grammaires × deux losses =
  **24 fits réels**, 40 mises à jour, une
  graine ; [workflow #40299287171](https://github.com/goldaj/trame-chartist-research/actions/runs/40299287171),
  trois jobs réussis et rapports SHA
  dans `research/token_grammar/S3_1_REAL_PILOT_RESULTS_20261026.md`.
  Le premier run avait échoué sur une assertion
  d'intégrité erronée exigeant deux SHA initiaux,
  corrigée : tous les bras de même width/depth/seed
  DOIVENT partir des mêmes poids.
- Corrige **une erreur arithmétique de planification
  de campagne** détectée avant publication
  du résultat final : quatre grammaires ×2
  objectifs ×2 largeurs ×2 profondeurs ×3
  seeds ×3 horizons font **288**, NON 192,
  soit 96 fits par horizon. Retire l'ancien
  workflow mal nommé 192, crée le nouveau
  `.github/workflows/trame-s3-predictive-288.yml`,
  et corrige la validation des 96/288 fits.
- [Run #40300156418](https://github.com/goldaj/trame-chartist-research/actions/runs/40300156418)
  lancé sur les trois historiques BTC publics
  originaux; **ne pas prétendre réussite totale
  sans vérifier les 3 jobs + job agrégateur**.
  Les résultats seront sur les labels DEV
  2022–2025 uniquement, 2026 strictement réservé.
- Documentation Codex dans
  `docs/CODEX_S3_1_HANDOFF_20261026.md`,
  `AGENTS.md`, protocole, PR et issue #20.
  Aucun modèle en prod, aucun trade, aucune
  transaction/frais simulés, pas d'edge prouvé.


### 26/10/2026 — clôture S3.1A 288 fits BTC réels (assistant, résumé non verbatim)
- Le run [#40300156418](https://github.com/goldaj/trame-chartist-research/actions/runs/40300156418)
  a **réussi 4/4 jobs**, dont D1/H1/M1
  (96 modèles chacun) et agrégation finale
  sur **288 fits /72 groupes appariés**.
- Trois graines, 200 optimizer updates,
  deux losses, deux widths/depths,
  quatre grammaires **décodées en scalaires**,
  Bitstamp SPOT 2012+/H1/M1 ; dev
  2022–25, **2026 toujours non ouvert**.
- Rapports de résultats et SHA256 dans
  `research/token_grammar/S3_1A_REAL_288_RESULTS_20261026.md`.
  Les cinq rapports complets (JSON D1/H1/M1,
  panel JSON, tableau MD) sont également
  regroupés en archive téléchargeable
  depuis la conversation ; leur contenu
  est reproductible via TRAME/GitHub Actions.
- Analyse : H1 Joint G2 améliore
  modestement BA et MAE du prix,
  réduit le biais monoclasse (0/12 vs 6/12)
  mais dégrade **l'erreur d'amplitude** ;
  ailleurs les effets sont faibles,
  variables ou contradictoires.
  Brier skill proche de zéro.
  Pas de preuve de gain conjoint ou PnL.
- Consigne Codex et issue #20 à actualiser
  vers S3.1B : **embeddings catégoriels
  réellement appris**, coût/paramètres
  appariés, protocole distinct ;
  nouveau modèle non traité dans S3.1A.


## 26/10/2026 — Reprise après crash, S3.1B embeddings (texte utilisateur VERBATIM)
**Utilisateur** :
> t'as crash, continue

**Assistant, description factuelle NON verbatim des actions effectivement réalisées :**
- Reprise à la clôture de **S3.1A**, [288 modèles réels](https://github.com/goldaj/trame-chartist-research/actions/runs/40300156418) et PR #24, pas de prétendu résultat non vérifié.
- Crée branche `chatgpt/trame-s3-learned-embeddings-20261026`,
  **[PR #25](https://github.com/goldaj/trame-chartist-research/pull/25)** DRAFT
  empilée sur PR #24 S3.1A.
- **Avant tout test BTC S3.1B**, préenregistre
  `research/token_grammar/S3_1B_PROTOCOL_20261026.md` :
  G1 signée fixe/G2 quantiles magnitude TRAIN-only,
  trois bras `decoded`, `embedding_ordered`
  et `embedding_random`. Les tables `nn.Embedding(11,1)`
  apprenables ajoutent **+11 paramètres** vs
  `decoded`; ordered-v-random égalise
  exactement capacité et architecture.
  Cibles, split, mini-lots, backbone initial
  SHA, normalisation TRAIN, objectifs maintenus.
- Implémente `learned_embeddings.py`,
  `learned_embeddings_panel.py`, tests
  `test_learned_embeddings.py` et `test_learned_embeddings_panel.py`.
  Vérifie sur fixtures artificielles que
  l'embedding ordonné donne exactement
  les mêmes sorties que decoded **avant**
  entraînement, et que decoded reproduit
  S3.1A après mêmes mises à jour.
  Le branchement temporel refuse dev 2026
  et les quantiles G2 sont calculés sur
  TRAIN uniquement. CI publique verte.
- Pilote réel **36 fits** D1/H1/M1 sur Bitstamp
  source publique, [Actions #40305840861](https://github.com/goldaj/trame-chartist-research/actions/runs/40305840861)
  **3 jobs réussis**, 40 updates 1 seed :
  notes + hashes et tableau
  `research/token_grammar/S3_1B_REAL_PILOT_RESULTS_20261026.md`.
  Ordered semble parfois légèrement améliorer
  l'accuracy directionnelle mais pas
  systématiquement le montant ; random
  provoque souvent une sortie monoclasse.
- Corrige **avant la campagne complète** une
  erreur du produit cartésien de paramètres :
  3 horizons ×2 grammaires ×3 bras ×2 losses
  ×2 widths ×2 depths ×3 seeds = **432 fits**
  (144 par horizon), et non « 216 ».
  Corrige le protocole, handoff Codex,
  PR et contrôles correspondants.
- Lance la véritable campagne **432 fits**
  [GitHub Actions #40306642813](https://github.com/goldaj/trame-chartist-research/actions/runs/40306642813) :
  **4 jobs sur 4 réussis** (D1/H1/M1 + panel),
  200 mises à jour, trois graines,
  144 groupes appariés trois bras.
  Archive les résultats scientifiques détaillés
  dans `research/token_grammar/S3_1B_REAL_432_RESULTS_20261026.md`
  (SHA256 des cinq rapports et limites).
  Une archive contenant les cinq fichiers
  JSON/MD est créée dans la conversation.
- Conclusion : **pas de supériorité robuste**
  des embeddings scalaire appris sur les
  centres numériques fixes en direction
  ET amplitude ; random augmente fortement
  le collapse monoclasse (H1 G2 Joint 11/12
  random vs 0/12 ordered et decoded).
  Scores BA proches du hasard et dev 2022–25
  trop sollicité pour être une validation
  indépendante. Test 2026 jamais utilisé.
- Actualise Codex (`AGENTS.md`,
  `docs/CODEX_S3_1B_HANDOFF_20261026.md`),
  PR #25, backlog issue #20.
  Priorité future **S3.1C** : audit de
  convergence et fonctions de perte
  avant augmentation lourde d'embeddings.
  Aucun ordre/compte/clé Hyperliquid,
  aucun PnL composé, frais toujours ignorés
  à la demande propriétaire.


### 26/10/2026 — Reprise automatique S3.1C après clôture des embeddings
**Utilisateur (demande déclenchante de ce tour, verbatim)** :
> t'as crash, continue

**Assistant, synthèse des actions réellement engagées (pas un verbatim de réponse)** :
- Après la conclusion S3.1B 432 fits réels [#40306642813](https://github.com/goldaj/trame-chartist-research/actions/runs/40306642813),
  constate qu'aucune grammaire apprise ne
  produit d'edge en direction et amplitude,
  l'initialisation random déclenchant
  souvent un modèle presque monoclasse.
  Clôture PR #25 avec rapport complet
  `research/token_grammar/S3_1B_REAL_432_RESULTS_20261026.md`,
  Codex `AGENTS.md`, issue #20,
  historique et archive ZIP des cinq
  rapports complets disponible en conversation.
- Décide comme chercheur ET ingénieur
  de diagnostiquer d'abord **la convergence
  du train** avant d'augmenter à nouveau
  taille et profondeur des réseaux.
- Crée **PR #26** branche
  `chatgpt/trame-s3-training-dynamics-20261026`,
  enfant PR #25. Préenregistre
  `research/token_grammar/S3_1C_CONVERGENCE_PROTOCOL_20261026.md`
  **avant la moindre mesure BTC réelle S3.1C**.
- Contrôle causal fort : aucun usage du
  DEV EXTERNE 2022–2025 pour régler la
  durée d'entraînement. Seuls les
  exemples historiquement TRAIN (<2022)
  sont employés. Deux réservoirs distincts
  et RNG indépendants :
  TRAIN cible disponible avant 2020,
  MONITOR interne 2020–2021,
  labels 2026 toujours gelés.
  Le cas limite label disponible
  exactement au 1er janvier 2022
  est exclu du moniteur.
- Implémente `convergence.py` (27
  trajectoires = 3 horizons×3 bras×3
  graines; 3 checkpoints du même
  optimiseur 200/800/2000 updates =
  81 observations internes, pas 81
  entraînements indépendants),
  `convergence_panel.py`,
  `test_convergence.py` et
  `test_convergence_panel.py`.
  Variables : loss train vs monitor,
  grad norm avant clipping, BA direction,
  %UP, monoclasse, MAE USD/bps,
  erreur amplitude bps et Brier prior
  train-only. CI synthétique réussie.
- Lance vrai workflow public
  [#40309653884](https://github.com/goldaj/trame-chartist-research/actions/runs/40309653884),
  trois jobs D1/H1/M1 et panel.
  **Au moment de la première rédaction,
  D1 et H1 ont réussi, M1 restait à
  vérifier.** Ne jamais inférer la
  réussite du job restant.
- Premiers chiffres monitor interne
  (pas une validation indépendante) :
  D1 G2 decoded BA 53.20% après 200
  steps →52.24% à 2000, MAE prix
  280.78→282.70 bps (dégradation) ;
  H1 49.02→51.93% BA et MAE prix
  54.80→54.61 bps (léger mieux).
  Le Brier H1 reste négatif. La
  durée idéale n'est pas universelle.
- Codex passation dans
  `docs/CODEX_S3_1C_HANDOFF_20261026.md`
  et rappel `AGENTS.md`.
  Aucun nouveau prix sensible, trade,
  clé, wallet, ordre Hyperliquid ou
  PnL capitalisé ; frais de simulation
  ignorés selon la consigne utilisateur.


### 26 octobre 2026 — S3.1C vrai diagnostic d'optimisation terminé (assistant, non verbatim)
- Le workflow GitHub Actions
  [#40309653884](https://github.com/goldaj/trame-chartist-research/actions/runs/40309653884)
  a **réussi 4 jobs sur 4** : D1,
  H1, M1 et agrégateur final.
- **27 trajectoires** de modèles
  entraînées chacune pour 2000
  optimizer updates et observées aux
  checkpoints 200,800,2000
  (**81 observations internes**).
  Ne pas qualifier les checkpoints
  de 81 entraînements distincts.
- Source authentique BTC Bitstamp
  public contrôlée SHA, jamais de
  simulation Hyperliquid ou PnL.
  Aucune réutilisation des cibles
  dev externe 2022–25 pour choisir
  les budgets, 2026 jamais ouvert.
  Deux réservoirs indépendants :
  TRAIN avant 2020 (D1 2876,
  H1/M1 4096), MONITOR 2020–21
  (D1 731, H1/M1 1024).
- **Résultats précis et SHA des
  cinq rapports** sont consignés
  dans `research/token_grammar/S3_1C_REAL_81_RESULTS_20261026.md`
  et archive ZIP jointe à la
  conversation pour éviter la seule
  dépendance aux artifacts GitHub.
  Code exécuté SHA
  `e0dae968998cb7f19c37b9f819e1de5d7524dd27`.
- Résultats résumés :
  D1 G2 decoded 53.20% BA /
  280.78bps MAE à 200 updates,
  52.24% /282.70bps à 2000
  (dégradation) ; H1 49.02%
  →51.93% BA, 54.80→54.61bps
  (amélioration modeste).
  M1 52.06%→53.02% BA,
  8.599→8.368bps MAE prix,
  MAIS amplitude 6.998→7.319bps
  (dégradation). Random mono
  H1 passe de 2/3 à 0/3,
  alors que D1 reste 2/3.
  Les gradients diminuent en
  moyenne et Brier skill est
  très proche du prior, souvent
  négatif.
- Décision recherche/ingénierie :
  aucune durée d'entraînement
  optimale universelle ; sous-
  entraînement n'explique qu'une
  partie des sorties monoclasse.
  **NO-GO** sur modèle de trading
  rentable; suite S3.1D = étudier
  séparément les objectifs direction,
  erreur du prix et magnitude,
  avec mêmes cohortes et en
  conservant 2026 comme test.
- `AGENTS.md`, Codex handoff,
  PR #26, issue #20 et historique
  à jour. Aucun compte, wallet,
  ordre réel ni clé publié ; les
  frais restent exclus par
  instruction de l'utilisateur.


## 2026-10-26 — Reprise après crash et correction de doublon S3.1C (VERBATIM utilisateur)
> t'as crash, reprends

**Assistant, synthèse NON verbatim des opérations constatables :**
- Se replace à S3.1C.1 : préenregistrement convergence
  200/800/2000 sur TRAIN<2020, MONITOR2020–21, dev
  2022–25 et holdout 2026 exclus.
- Introduit expérimentalement un second lecteur,
  runner/panel et deux CI de convergence, puis constate
  par lecture GitHub que **PR #26 S3.1C est DÉJÀ
  TERMINÉE** et vérifie les **4 jobs succès**
  [Actions #40309653884](https://github.com/goldaj/trame-chartist-research/actions/runs/40309653884).
  27 véritables trajectoires et 81 checkpoints
  déjà consignés dans
  `research/token_grammar/S3_1C_REAL_81_RESULTS_20261026.md`.
  Ne pas republier des résultats artificiels ou
  créer des versions concurrentes.
- **Supprime 8 fichiers de duplication**
  non nécessaires et leurs workflows sur
  PR #26 ; conserve l'implémentation canonique
  `research/token_grammar/convergence.py`
  et le rapport déjà vérifié. Améliore
  `stream.iter_cases(stop_labels_before)` et
  `read_bars(stop_before)` pour ne pas
  parcourir les bougies 2022–2025 du tout,
  et réutilise le mode `stop_labels_before`
  dans `convergence.collect_internal`.
  Ajoute un test régression du coupe-circuit.
  Le code de référence du run historique
  #40309653884 est antérieur à ce hardening,
  ses résultats n'ont pas été remplacés.
- **Prend S3.1D comme prochaine vraie étape** :
  branche `chatgpt/trame-s3-objective-ablation-20261026`,
  PR #27 DRAFT enfant de PR #26.
  **Avant essai réel**, préenregistre
  `research/token_grammar/S3_1D_LOSS_PROTOCOL_20261026.md`
  : isoler 5 losses direction/amplitude à
  backbone, cibles, données et réconciliation
  identiques. Cinq variantes Huber+BCE de poids
  0.25/0.5/1.0, et bonus d'erreur magnitude
  0.25/1.0, en toujours JOINT pour ne pas
  laisser la tête de direction non entraînée.
- Code `loss_ablation.py`,
  `loss_ablation_panel.py` et deux tests.
  CI de fixtures [réussie](https://github.com/goldaj/trame-chartist-research/actions/runs/40312632397).
- Un premier smoke réel D1/H1/M1 [#40312632612](https://github.com/goldaj/trame-chartist-research/actions/runs/40312632612)
  a échoué **avant entraînement** sur
  double déclaration CLI `--checkpoints`,
  sans produire de résultat BTC.
  Corrige la CLI, ajoute test `--help` en CI,
  relance smoke [#40312924527](https://github.com/goldaj/trame-chartist-research/actions/runs/40312924527)
  et campagne scientifique complète
  [#40313075915](https://github.com/goldaj/trame-chartist-research/actions/runs/40313075915).
  **Leurs conclusions doivent être vérifiées**
  avant toute affirmation de résultat ;
  45 trajectoires = D1/H1/M1×5 pertes×3
  seeds, observées à 200/800/2000 updates
  sur monitor INTERNE 2020–21 :
  135 observations non indépendantes.
- Documentation Codex `docs/CODEX_S3_1D_HANDOFF_20261026.md`
  et `AGENTS.md`. Respect du gel
  2022–25/2026, pas de profits inventés,
  aucun trade Hyperliquid, frais ignorés.


### 26/10/2026 — nouvelle reprise après crash : S3.1D finalisée
**Utilisateur (verbatim)** :
> t'as crash, continue

**Assistant, travaux réellement effectués (résumé NON verbatim) :**
- Vérifie que la vraie étude S3.1D [#40313075915](https://github.com/goldaj/trame-chartist-research/actions/runs/40313075915)
  est bien **terminée SUCCESS 4/4**, 3 horizons BTC
  spot Bitstamp D1/H1/M1 + agrégation.
  Code source réellement exécuté :
  SHA `5726cb99c0bcfef59509bf2b4884a7e1bf7036cc`.
- Récupère depuis les artefacts GitHub les JSON
  individuels D1/H1/M1 (15 trajectoires et
  45 observations par horizon), le panel complet
  135 lignes et son Markdown. **Contrôle**
  SHA256 des fichiers et cohérence
  45 trajectoires, 135 checkpoints ;
  consolide une archive ZIP avec MANIFEST.
  Le calcul des deltas appariés par seed
  vérifie qu'aucune variante de loss
  ne bat la référence sur sens+prix final+
  magnitude sur toutes les 3 graines.
- **Résultat clé** au checkpoint 2000 :
  augmenter le poids de l'amplitude à 1
  améliore son erreur de 16,4% (D1),
  21,3% (H1), 16,9% (M1), mais DÉGRADE
  le MAE du prix final de 5,9%, 9,8%
  et 7,1% et la BA de 0,88, 1,71
  et 0,59 points respectivement.
  La référence a même un MAE prix
  supérieur à la persistance simple
  aux trois horizons à 2000 updates.
  Pas d'edge prouvé, Brier faible.
- Crée
  `research/token_grammar/S3_1D_REAL_135_RESULTS_20261026.md`
  avec 15 combinaisons horizon/loss à
  2000 updates, détails scientifiques,
  SHA256 des 5 rapports, liens vers
  artifacts et question suivante.
- Met à jour
  `docs/CODEX_S3_1D_HANDOFF_20261026.md`,
  `AGENTS.md`, la description de PR #27
  et le backlog issue #20.
- **Propose S3.1E** : mesurer le
  désaccord entre sortie de régression
  signée `mu` et probabilité de hausse
  issue du logit, puis tester une
  loss alignée sur le prix reconstruit
  réellement utilisé, en gardant
  architecture/données/graines fixes.
  Préenregistrer protocole AVANT tout
  résultat réel, ne pas consulter
  2022–25/2026 pour sélection.
- Aucun PnL cumulé, aucun ordre réel
  Hyperliquid ni clé/secret, frais
  volontairement ignorés.



## 26/10/2026 — lancement S3.1E, hypothèse de cohérence deux têtes (assistant, NON verbatim)
Suite à S3.1D 45 trajectoires/135 observations
D1/H1/M1 réellement achevées (Actions #40313075915),
une différence importante apparaît entre
**loss retour signé de l'IA** et la règle
d'inférence `hard_sign(logit)*abs(mu)`.
Augmenter le poids de l'erreur amplitude
favorise cette métrique mais détériore
souvent prix final/BA, y compris contre
la persistance simple. Les cinq vrais
JSON/MD S3.1D et leur SHA sont consignés
dans `research/token_grammar/S3_1D_REAL_135_RESULTS_20261026.md`.

- Crée branche
  `chatgpt/trame-s3-reconciliation-loss-20261026`
  et [PR #28 DRAFT](https://github.com/goldaj/trame-chartist-research/pull/28)
  fille de la PR #27, sans merge.
- **AVANT essais BTC réels** préenregistre
  `research/token_grammar/S3_1E_RECONCILIATION_PROTOCOL_20261026.md`
  : 3 pertes identiques à la référence
  hormis ajout 0,25 /1.00 SmoothL1
  sur surrogate `tanh(logit/2)*sqrt(mu²+1e-12)`.
  Le surrogate différentiable SOFT n'est
  PAS le prix HARD réellement prédit ;
  tous les résultats économiques/BA
  doivent scorer la règle HARD existante.
- Crée `reconciliation_loss.py`,
  `reconciliation_panel.py`,
  `test_reconciliation_loss.py`,
  `test_reconciliation_panel.py`.
  Matrice fixée : trois horizons ×trois
  losses ×trois graines = 27 trajectoires
  réelles, 2000 steps par modèle, checkpoints
  200/800/2000 = 81 observations NON
  indépendantes.
- Tests synthétiques
  [Actions #40318703540](https://github.com/goldaj/trame-chartist-research/actions/runs/40318703540)
  réussis. Pilotes ingénierie à 40 updates
  [#40318703968](https://github.com/goldaj/trame-chartist-research/actions/runs/40318703968)
  **3/3 jobs réussis**.
- Lance vraie étude
  [Actions #40318969005](https://github.com/goldaj/trame-chartist-research/actions/runs/40318969005)
  et développe passation Codex
  `docs/CODEX_S3_1E_HANDOFF_20261026.md`,
  `AGENTS.md`. **Vérifier le run complet
  avant toute revendication** de résultat.
- Même TRAIN avant 2020 et MONITOR 2020–21,
  externe DEV 2022–25 ET 2026 restent
  non utilisés pour sélectionner.
  Pas de frais sur demande, ni PnL cumulatif,
  ni compte/trade Hyperliquid.


### 26/10/2026 — S3.1E BTC RÉELLE achevée (assistant, résumé non verbatim)
- [GitHub Actions #40318969005](https://github.com/goldaj/trame-chartist-research/actions/runs/40318969005)
  **4/4 jobs SUCCESS** D1/H1/M1 et panel,
  code Git SHA
  `73b56883dd09b3ad533aeeb4546eb1d402f2c003`.
  27 trajectoires réellement entraînées,
  81 checkpoints 200/800/2000 dépendants.
- Les cinq rapports détaillés JSON/MD
  sont récupérés depuis GitHub Actions,
  identifiés par SHA256 dans
  `research/token_grammar/S3_1E_REAL_81_RESULTS_20261026.md`
  et une archive ZIP avec manifeste
  `trame_s3_1e_27_81_resultats.zip`
  est créée dans la conversation.
- Analyse : vs `legacy`, la nouvelle
  loss de réconciliation différentiable
  améliore parfois BA OU magnitude,
  mais **pas** de supériorité conjointe
  du sens et MAE prix dur. Exemple
  D1 BA 52,24→52,83 mais MAE prix
  282,704→285,563 bps et Brier pire ;
  H1 BA 51,93→50,52 et prix
  54,611→54,945 ; M1 BA 53,02→52,73
  et prix 8,368→8,398.
- Le taux de désaccord `sign(mu)`
  vs `sign(logit)` sur `legacy`
  à 2000 updates est descriptivement
  D1 7,9%, H1 19,0%, M1 26,7%.
  Le soft proxy peut avoir un MAE
  inférieur au hard, mais n'est PAS
  la sortie du modèle réellement servi.
- **NO-GO** trade/edge ; même la
  persistance reste légèrement meilleure
  en MAE prix. Dev 2022–25 déjà utilisé
  par d'anciennes expériences n'est
  pas rouvert, monitor 2020–21 reste
  exploratoire, 2026 gelé. Aucun
  PnL composé/frais/transactions.
- Met à jour le rapport, Codex
  `docs/CODEX_S3_1E_HANDOFF_20261026.md`,
  `AGENTS.md`, PR #28 et issue #20.
  Prochaine expérience projetée S3.1F :
  comparer **à poids de modèle identiques**
  les règles d'inférence hard joint,
  direct mu et soft joint. Protocole
  à écrire avant résultats réels.

## 26 octobre 2026 — reprise après crash et expérimentation S3.1F
**Utilisateur, VERBATIM** :
> t'as crash, continue

**Assistant, opérations vérifiables (résumé NON verbatim)** :
- Reprend immédiatement après la création de
  `research/token_grammar/inference_ablation.py`
  et `test_inference_ablation.py`.
- Le protocole S3.1F **avait été préenregistré**
  dans `research/token_grammar/S3_1F_INFERENCE_PROTOCOL_20261026.md`
  avant tout essai BTC réel, sur la branche
  `chatgpt/trame-s3-postprocess-ablation-20261026`,
  fille de #28 S3.1E.
- Termine `research/token_grammar/inference_panel.py`,
  ajoute `test_inference_panel.py` :
  **9 vrais modèles**, 27 checkpoints,
  81 évaluations dépendantes des 3 règles.
  Tests de falsification refusant modèle,
  SHA init ou tête probabiliste différents
  sous prétexte de règle post-traitement.
- CI synthétique
  [#40326446195](https://github.com/goldaj/trame-chartist-research/actions/runs/40326446195)
  réussie ; comparateur legacy vs S3.1E
  sur même seed/past/targets exactement.
- Pilote sur vrais historiques BTC spot
  D1/H1/M1 [#40326446278](https://github.com/goldaj/trame-chartist-research/actions/runs/40326446278)
  **3/3 jobs réussis**, un modèle par
  horizon, 10/20/40 updates, moteur
  hard historique parfaitement répliqué.
- Ouvre [PR #29 DRAFT](https://github.com/goldaj/trame-chartist-research/pull/29)
  fille de PR #28, sans merge auto ;
  documente `docs/CODEX_S3_1F_HANDOFF_20261026.md`,
  `AGENTS.md`.
- Lance campagne vraie
  [GitHub Actions #40326818917](https://github.com/goldaj/trame-chartist-research/actions/runs/40326818917)
  3 horizons ×3 graines à 2000 steps,
  checkpoints 200/800/2000, 3 règles
  à poids constants. Exiger 4/4 jobs
  et panel complet avant conclure.
- Causalité et données : TRAIN labels <2020,
  MONITOR interne 2020–21 seulement,
  dev externe 2022–25 non utilisé,
  holdout 2026 réservé, quantiles/scale
  train-only, tous artefacts SHA vérifiables.
  Pas de trading, pas de PnL cumulé,
  frais ignorés selon utilisateur.
