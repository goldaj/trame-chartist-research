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
- **Expérience construite** : 15 configurations de stress, 14 contrôles,
  amélioration de NLL sur une loi bimodale artificielle avec corrections
  entraînées, rejouabilité de 20 pas et score CRPS sur prix fictifs.
- Aucun accès aux données de marchés réservées, téléchargement,
  ordre, déploiement, modèle GPT entraîné ou prétention de prévision.
  Fichiers de protocole gelés et sources `main` inchangés.
- Les résultats numériques ont été exécutés localement sur fixtures
  artificielles. La CI GitHub sur branche vérifie et archive les
  rapports ; vérifier son verdict pour le HEAD avant fusion.
