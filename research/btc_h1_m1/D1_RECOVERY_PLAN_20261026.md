# TRAME A7-D1 : réintégration des données journalières (26 octobre 2026)

## Pourquoi le daily manquait
La release privée canonique contient trois CSV D1 depuis juillet 2010,
mais `stream.py`, `experiment.py`, `statistical_baselines.py`,
`regime_analysis.py` et le nouvel exécuteur de scaling acceptaient seulement
H1/M1. Le module `daily.py` existait déjà pour de la lecture descriptive ;
il n'était pas intégré aux expériences sur modèles. Aucune conversion de
cours ne justifie la perte de D1. **Cette PR corrige le raccordement.**

## Classement scientifique des trois segments de la même release
1. 2010-07-18 → 2011-08-17 : **prix de clôture INDICATIFS**,
   sans OHLCV, volume ou preuve de liquidité. `daily.read_daily` les rend
   disponibles pour études descriptives de très long terme ; ils ne
   peuvent rejoindre sans hypothèses supplémentaires l'expérience
   homogène Bitstamp qui exige des vrais volumes.
2. 2011-08-18 → 2011-12-31 : D1 **Bitstamp OHLCV** au schéma `date_utc`.
   Les volumes à zéro provoquent une rupture du contexte exploitable.
3. 2012-01-01 → 2026-06-30 : D1 **Bitstamp OHLCV** au schéma
   `datetime_utc`. Les barres 2026 ne sont ni passées au modèle ni
   utilisées pour choisir les hyperparamètres.

La cohorte principale D1 utilise exclusivement les deux segments
Bitstamp OHLCV réels, sans fabriquer de pseudo-bougies indicatives.
Pour la comparaison strictement *calendaire* D1/H1/M1 il faut
isoler le support 2012–2025 et déclarer explicitement les années
supplémentaires D1 ; les erreurs USD et la NLL ne sont PAS
commensurables entre horizons (1 jour / 1 heure / 1 minute).
On utilise même code, split chronologique et règles de mesure,
pas le même prix/candle échantillonné.

## Étapes rétablies, ordre des sous-tâches
- **D1.1** Audit de la release des trois fichiers, schémas, grades,
  périodes et nécessité d'observer le close à J+1 : vérifié.
- **D1.2** Lecteur unique `daily.py` branché dans `stream.read_bars`
  et `iter_cases("D1")` ; anciennes clôtures indicatives exclues de
  l'OHLCV, absence de lookahead.
- **D1.3** Généralisation du pipeline A7 :
  `experiment` (3 architectures), `statistical_baselines`
  (persistance + Ridge), `regime_analysis` (années/régimes).
- **D1.4** Généralisation du scaling S1 : mêmes cinq tailles × trois
  profondeurs × trois familles, 3 seeds, NLL/MAE/direction/magnitude ;
  270 entraînements deviennent **405** à trois horizons.
- **D1.5** Tests synthétiques `test_d1_parity.py`, CI et vérification
  de la branche courante, aucune utilisation de prix privés en CI.
- **D1.6** Campagne réelle **D1** sur le runner privé, après canary ;
  calculer également témoins/régimes/3 architectures/direction et
  archiver rapports agrégés, commit SHA, journal et seeds.
- **D1.7** Reconstituer le tableau comparatif D1/H1/M1 :
  réutiliser les sorties originales H1/M1 identifiées par SHA ou
  réexécuter le protocole harmonisé direction/amplitude (les résultats
  H1/M1 anciens **n'ont pas** la justesse directionnelle). Comparer
  par horizon et année/régime, pas valeur absolue NLL.
- **D1.8** Reprendre S1 scaling et campagnes de convergence ;
  ne jamais inférer de supériorité de l'architecture après
  seulement 40 mises à jour ou un petit échantillon.

## Direction et amplitude, modification de protocole utilisateur
L'utilisateur souhaite ignorer les frais ; le rapport comporte :
`direction_accuracy_all`, `direction_accuracy_when_signaled`
et **couverture**, balanced accuracy hausse/baisse, MAE USD, MAE bps,
erreur d'amplitude bps, calibration par groupes d'amplitudes prédites
et score moyen brut par bougie échantillonnée.
Le score brut n'est pas le rendement composé du portefeuille :
aucun carnet/entrée-sortie ou décision humaine n'est simulé.

## Runbooks sans accès privé implicite
~~~bash
python -m unittest research.btc_h1_m1.test_d1_parity -v
python -m research.scaling_study.runner --interval D1 --plan-only
python -m research.btc_h1_m1.release_store --resolution D1 --download
python -m research.btc_h1_m1.statistical_baselines --interval D1 --output /tmp/d1_baselines.json
python -m research.btc_h1_m1.regime_analysis --interval D1 --output /tmp/d1_regimes.json
python -m research.btc_h1_m1.experiment --interval D1 --steps 40 --output /tmp/d1_models.json
python -m research.scaling_study.runner --interval D1 --targets 2400 --depths 1 --architectures modern_gpt_style_mini --steps 2 --seeds 20261026 --output /tmp/d1_scaling_canary.json
~~~
**Exécuter les commandes réelles seulement avec les trois CSV épinglés et
une authentification GitHub valide** ; aucune donnée ni secret brut dans
TRAME public. Les workflows du dépôt privé peuvent épingler le SHA public
et conserver seulement des rapports agrégés privés. Rien ne déclenche
Hyperliquid ni n'utilise 2026.
