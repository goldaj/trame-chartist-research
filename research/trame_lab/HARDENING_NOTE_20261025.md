# TRAME Research Lab — hardening pass 8.2 / 8.6

**2026-10-25 | branche** `chatgpt/trame-lab-hardening-20261025`  
**Parent** `chatgpt/trame-research-lab-v01-20261025`  
**Statut** : modifications publiées ; leur validation CI doit être vérifiée sur le commit final.

## Objectif et périmètre

Améliorer le produit offline synthétique **sans** changer ses expériences, leurs
seeds, le mini-modèle, les données, les partitions réservées, la tête P1-B0
ou le benchmark. Aucun accès réseau, aucune donnée réelle, aucun ordre.

## Baby step 8.2a — accessibilité de la restitution

Dans `research/trame_lab/cli.py`, les quatre valeurs NLL ont
maintenant un rendu **textuel et tabulaire sémantique**, avec
`<caption>`, `<th scope="col">`, `<th scope="row">`, sans dépendre
d'une couleur ni de la taille des barres SVG. Le SVG conserve son rôle
graphique mais est caché aux technologies d'assistance pour éviter une
représentation doublée. Un lien d'évitement au contenu devient visible
au focus clavier, et le tableau reçoit une mise en forme sobre.

Test automatique du contrat HTML dans `test_cli.py`. Il prouve la
présence des éléments, **pas** leur rendu sur un lecteur d'écran.
**Audit visuel réel navigateur, lecteur d'écran et contrastes : NON FAIT**
(8.2b). Aucune certification WCAG revendiquée.

## Baby step 8.6a — garde-fous d'entrée et de restitution

- `--steps` est refusé avant entraînement hors plage 1–200.
- L'appel programmatique `run_lab(train_steps=...)` applique la même
  limite, avec exclusion explicite de `bool` et `float`.
- Le rendu refuse des compteurs non positifs, NLL non finies,
  quantiles synthétiques incohérents, CRPS négatif et comparaisons
  appariées non identifiées comme **fabriquées intentionnellement**.
- Les tests construisent exclusivement des payloads fictifs ;
  aucune série financière ni partition réservée n'est lue.

### Vérifications de reproduction

Depuis la racine du dépôt, avec les dépendances du laboratoire v0.1 :

```bash
python -m unittest discover -s research/trame_lab -p 'test_*.py' -v
python -m research.trame_lab.cli --steps 5 --output trame_research_lab.html
```

Le second appel produit `trame_research_lab.html` et
`trame_research_lab.json`. Le programme refuse l'écrasement implicite.
Ne pas versionner les rapports locaux ni les traiter comme preuves
de capacité prédictive sur marchés.

## Non-réalisé / risques résiduels

- Aucune démonstration sur navigateur réel ou technologies d'assistance.
- Les deux fichiers HTML et JSON ne sont pas encore une transaction
  de système de fichiers atomique. Une panne disque après écriture
  du JSON peut laisser une paire incomplète. Un correctif mérite un
  test d'injection de panne avant de revendiquer cette propriété.
- Reproductibilité CPU dépendante de la version exacte des dépendances,
  de la plateforme et des fonctions déterministes disponibles.
- Les étapes financières 5–7 restent **No-Go**.
- Avant toute fusion, vérifier les PR empilées et les checks du HEAD.

## Pour Codex

1. Lire `AGENTS.md` et `docs/CHATGPT_PROJECT_HISTORY.md`.
2. Conserver **séparées** les branches de PR #2–#6 et le parent v0.1 ;
   cette branche est une continuation de v0.1, pas un correctif direct
   de `main`.
3. Confirmer la CI, faire l'audit 8.2b sur navigateur, puis examiner
   l'atomicité des rapports avec tests de panne avant d'annoncer 8.6
   entièrement terminée.
4. Ne pas ouvrir de corpus financier non qualifié et ne pas exploiter
   le test synthétique réservé pour ajuster le modèle.
