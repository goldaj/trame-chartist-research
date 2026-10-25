# A5 — hybrides et alternatives sans survente

**Statut : exploration indépendante de la validation GPU A4.**
Objectif : tester si la combinaison de deux mécanismes déjà connus
apporte un signal nouveau **après** contrôle des ressources, plutôt que
de baptiser un modèle hybride de nom prestigieux.

## Hypothèses pré-déclarées

H1 : un bras attention causale + GRU peut rendre de meilleurs scores
sur une tâche fabriquée que les mêmes témoins séparés ;
H0 : ses gains apparents tiennent à la capacité, au compute et
à l'aléa. Ne pas « valider » H1 avec trois graines exploratoires.
H2 : les véritables hybrides SSM + attention pourront être testés
après A4.4 (GPU Mamba opérationnel). Le GRU ne représente pas
une implementation SSM sélective.

## Sous-tâches

- [x] **A5.1** : hypothèses, témoins et objectifs mesurables.
- [ ] **A5.2** : contrat modulaire des vrais hybrides SSM/attention
  (API, dépendances, masque, causalité, interface probabiliste),
  sans simuler des kernels Mamba ; attente d'A4.4 pour validation.
- [ ] **A5.3** : implémenter un témoin hybride CPU attention GQA
  causale + GRU, avec même tête BASE que les autres.
- [ ] **A5.4** : expériences synthétiques appariées, causalité,
  rétropropagation, même mini-lots, mesures de paramètres,
  temps et trois graines au moins.
- [ ] **A5.5** : ablations, rapport Go/No-Go, exclusion de toute
  déclaration de supériorité financière. Une étude compute-fair
  définitive ne pourra pas réutiliser aveuglément des proxies A3c.

## Critères d'admissibilité

- Même `x`, mêmes `y`, mêmes partitions train/dev, jamais le
  test réservé avant gel et validation préalable.
- `output_distribution` et fonctions de perte identiques,
  variantes modifiées de manière isolée.
- Chaque hybride annonce s'il est **véritablement** SSM+attention
  ou seulement attention+GRU ; noms non interchangeables.
- Paramètres, coût d'optimisation et FLOPs réels comparés ou
  absence de parité explicitement signalée.
- Baselines classiques incluses lors des campagnes financières.
- Aucun historique BTC privé requis en CI CPU.

## Risques déjà connus

Le petit jeu AR(1) artificiel et le prototype 20 tokens
ont une dépendance principalement locale. Ils sont
insuffisants pour départager les capacités à longue
mémoire, extrapolation, volatilité et dérive des marchés.
Une éventuelle meilleure NLL sur ce jeu ne présage
ni performance Bitcoin ni avantage économique.
