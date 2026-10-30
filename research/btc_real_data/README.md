# TRAME : référence BTC/USD D1 2010–2026 (jeu de l'utilisateur)

**25 octobre 2026 : nouvelle priorité.** Pour TRAME, l'histoire de
référence est le Bitcoin BTC/USD au long cours, **pas** celle du perp
Hyperliquid. Le propriétaire accepte explicitement les snapshots comme
tels, sans nouvelle enquête sur leur provenance.

## Trois fichiers attendus, inchangés

- raw/btcusd-indicative-close-d1-2010-2011.csv : 396 clôtures indicatives.
- raw/btcusd-bitstamp-d1-2011H2.csv : 136 bougies D1 OHLCV.
- raw/btcusd-bitstamp-d1-2012-2026H1.csv : 5295 bougies D1 OHLCV.

**Statut Git de cette branche : ces fichiers ne sont PAS présents.**
Ils sont dans le dépôt privé goldaj/hyperliquid-btc-pilot,
branche codex/chat-gpt6-btc-long-history-20261025, PR #3,
commit 826e0880d4cc9c96b7407ca503c1772225558ea9.
La tentative de copie privée-vers-publique via le connecteur a été
bloquée par un contrôle de sécurité. Le lecteur et les tests sont
présents, mais aucun entraînement TRAME sur les cours réels
n'est donc déclaré comme exécuté ici.

L'utilisateur autorise à diffuser les CSV dans ses propres projets.
Cette autorisation ne constitue pas en soi une licence de
redistribution accordée par les fournisseurs de données tiers.
Lors d'une copie publique, préserver les attributions et les
conditions éventuelles déjà recensées dans
research-data/ATTRIBUTION.md du dépôt d'origine.

### Installation manuelle locale (PowerShell)

Une fois les deux dépôts clonés avec les branches concernées :

~~~powershell
$bot = "C:\chemin\vers\hyperliquid-btc-pilot"
$trame = "C:\chemin\vers\trame-chartist-research"
New-Item -ItemType Directory -Force "$trame\research\btc_real_data\raw" | Out-Null
Copy-Item "$bot\research-data\btcusd-*.csv" "$trame\research\btc_real_data\raw\"
cd $trame
python -m research.btc_real_data.loader
python -m research.btc_real_data.experiment --steps 20 --output btc_development.json
~~~

L'exécutable est offline, sans ordre, clé de trading ou réseau.
Le JSON généré est une mesure exploratoire, pas un backtest PnL.

### Tester le logiciel sans les données privées

~~~bash
python -m unittest discover -s research/btc_real_data -p "test_*.py" -v
~~~

La CI reconstruit des fixtures artificielles de 5827 journées, avec
les mêmes trois schémas CSV, puis teste la préparation causale
et une très petite campagne d'apprentissage.

## Splits et prévention des fuites

| Groupe | Dates des cibles |
| --- | --- |
| Train | 2010 jusqu'au 31 décembre 2021, moins le contexte initial |
| Développement exploratoire | 1er janvier 2022 au 31 décembre 2025 |
| Quarantaine non évaluée | 1er janvier au 30 juin 2026 |

Chaque prédiction est le **rendement clôture-à-clôture D+1**,
à partir de 20 rendements antérieurs. Quantification fixe
floor(1000 × log(close[t]/close[t−1]) + 0,5), jamais
ajustée à partir du futur. Le programme ne calcule ni scores,
ni codes cibles de 2026.

Une décision au début du jour D+1 UTC peut utiliser la
clôture du jour D, mais pas la clôture de D+1 ; le programme
sépare decision_at_utc et label_available_at_utc.
Le millésime historique exact de publication n'est pas garanti :
c'est une hypothèse de clôture, explicitement reconnue.

Comparaison à trois bras : Transformer causal, mini GPT-style
et GRU, mêmes mini-lots/seeds, NLL gaussienne arrondie
et MAE des prix médians BTC/USD. Un témoin train-only
gaussien et la persistance sont également évalués.
Comparaison **exploratoire, non compute-fair** : pas de preuve
de gain financier, pas de simulation des frais/funding d'Hyperliquid.
Les jours 2010–2011 n'autorisent pas de faux OHLCV.

## Passation Codex

Lire AGENTS.md et docs/CHATGPT_PROJECT_HISTORY.md, puis loader.py,
experiment.py, les tests et cette note. Conserver la comparaison
multi-architectures et l'interdiction des données postérieures
à la partition de développement. La période 2026 a pu être
examinée dans d'autres travaux : ne jamais prétendre qu'elle
constitue à elle seule un holdout indépendant certifié.

Cette branche dépend de chatgpt/trame-multi-architecture-20261025
(PR #8). Aucune fusion automatique, aucun changement du bot.
