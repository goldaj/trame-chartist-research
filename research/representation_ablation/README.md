# S2b : test « représentation seule » avant les grammaires S3

Le protocole [S2b préenregistré](PROTOCOL_20261026.md) complète S2
sans modifier les résultats historiques S1/S2. Il distingue l'arrondi
des rendements de la modification des objectifs de loss.

## Dimensions
- Deux **entrées** : `continuous_bps` et `legacy_quantized_bps`
  (code historique entier ×10 bps).
- Deux objectifs inchangés de S2 : Huber et Huber+0,5 BCE direction.
- Deux largeurs : 16 et 32, deux profondeurs : 1 et 2.
- Trois horizons BTC indépendants : D1, H1, M1 ; trois graines.
- Matrice complète souhaitée : **144 fits**, mais **aucun run BTC réel
  S2b n'a encore été exécuté**. Smoke/CI : données INVENTÉES seulement.

## Méthode appariée
Même `Case` et même **vraie** cible continue pour les deux entrées.
Les anciennes prédictions S1 étaient sur une cible quantifiée ;
S2b garde volontairement la vraie cible pour n'isoler que l'entrée.

Les deux entrées ont chacune un écart-type calculé **sur TRAIN seul**.
L'échelle des **cibles**, `std(continuous_train_past_bps)`, est
**commune aux deux bras**. La séquence des indices de mini-lots
est identique par graine, et le SHA256 des poids initialisés
est conservé pour chaque entraînement afin de vérifier
la parité des initialisations.

Les résultats comprennent précision de sens équilibrée/brute,
taux de hausses prédites, MAE USD, MAE ancrée bps,
erreur d'amplitude absolue bps, couverture, Brier skill
par rapport au prior train-only (uniquement joint),
et temps CPU. Ne pas confondre différence d'amplitude
et PnL réel. Frais non simulés à la demande du propriétaire.

## Tests artificiels (publics)
~~~bash
python -m unittest research.representation_ablation.test_ablation research.representation_ablation.test_panel -v
~~~
Ces tests doivent passer sous `.github/workflows/trame-s2b-representation.yml`
sans token GitHub ni donnée BTC réelle.

## Exécution potentielle sur environnement privé **déjà autorisé**
**Aucun workflow privé n'a été créé**, car une tentative précédente
pour S2 a été rejetée par des contrôles de sécurité ; ne pas contourner.

Après validation des autorisations nécessaires et contrôle des données
locales épinglées (release privée dans le cache), les commandes
de recherche seraient :
~~~bash
python -m research.representation_ablation.runner --interval D1 --output /tmp/s2b_D1.json
python -m research.representation_ablation.runner --interval H1 --output /tmp/s2b_H1.json
python -m research.representation_ablation.runner --interval M1 --output /tmp/s2b_M1.json
python -m research.representation_ablation.panel \
  --inputs /tmp/s2b_D1.json /tmp/s2b_H1.json /tmp/s2b_M1.json \
  --output /tmp/s2b_panel.json --markdown /tmp/s2b_panel.md
~~~
Le runner refuse les labels 2026 et exige une version de code Git
traçable pour tout résultat étiqueté BTC réel.

## Pour Codex
Lire `AGENTS.md`, `docs/CODEX_S2_HANDOFF_20261026.md`,
`research/continuous_direction/PROTOCOL_20261026.md`,
`research/token_grammar/ROADMAP_20261026.md`.
Branches empilées : **S2b sur PR #19 (S2), elle-même sur
PR #18 (D1), #17 (scaling), #14 (A7)**.
Ne fusionner aucune PR automatiquement. S3 issue
[#20](https://github.com/goldaj/trame-chartist-research/issues/20)
continue d'exister ; les grammaires signées, patches
et VQ ne sont pas implicitement validées par S2b.
