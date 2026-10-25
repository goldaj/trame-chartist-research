# TRAME BTC/USD Bitstamp H1 & M1 - nouveau référentiel

Décision utilisateur du 25 octobre 2026 : abandonner la précédente
tentative de copie des trois snapshots D1. Les nouveaux historiques de
référence sont les archives Bitstamp H1/M1 de 2012 à juin 2026.
Les accepter telles quelles pour la recherche sans audit supplémentaire
de provenance, et préserver strictement leurs octets d'origine.

## Liens des fichiers exacts

Dépôt privé goldaj/hyperliquid-btc-pilot, GitHub Actions run
40208291215 (succès du 25 octobre 2026).

- H1, environ 2,7 Mo, artifact ID 12604202171 :
  https://github.com/goldaj/hyperliquid-btc-pilot/actions/runs/40208291215/artifacts/12604202171
- M1, environ 110 Mo, artifact ID 12604092598 :
  https://github.com/goldaj/hyperliquid-btc-pilot/actions/runs/40208291215/artifacts/12604092598

Les artifacts sont conservés jusqu'au 23 janvier 2027 selon GitHub.
Leur copie directe entre dépôts privé/public par connecteur n'est
pas permise ici. Aucun fichier de prix réel n'est présent dans cette
branche TRAME. Copier les deux ZIP manuellement, puis décompresser
UNIQUEMENT l'enveloppe ZIP, sans modifier les fichiers gzip.

Répertoire de destination : research/btc_h1_m1/raw/

Contenu attendu :
- BTCUSD_bitstamp_hourly_2012-2026.csv.gz
- BTCUSD_bitstamp_1min_2012.csv.gz
- ... un fichier par année jusqu'à ...
- BTCUSD_bitstamp_1min_2026.csv.gz

## Copie PowerShell rapide

Depuis la racine du dépôt TRAME local et après avoir téléchargé les
archives dans votre dossier Téléchargements :

~~~powershell
$dest = "research\btc_h1_m1\raw"
New-Item -ItemType Directory -Force $dest | Out-Null
Expand-Archive -Path "$env:USERPROFILE\Downloads\bitstamp-2012-2026-hourly-pinned.zip" -DestinationPath $dest
Expand-Archive -Path "$env:USERPROFILE\Downloads\bitstamp-2012-2026-minute-pinned.zip" -DestinationPath $dest
~~~

Adapter les noms des ZIP si GitHub les a renommés. Le lecteur attend
les seize fichiers gzip directement dans raw/. Ne pas extraire .csv.gz.

## Utiliser le nouveau référentiel

Dans un environnement Python 3.12 + NumPy/SciPy/PyTorch du Research Lab :

~~~powershell
python -c "from research.btc_h1_m1.stream import limited_preview; print(limited_preview('H1'))"
python -c "from research.btc_h1_m1.stream import limited_preview; print(limited_preview('M1'))"
python -m research.btc_h1_m1.experiment --interval H1 --steps 40 --output btc_h1_dev.json
python -m research.btc_h1_m1.experiment --interval M1 --steps 40 --output btc_m1_dev.json
~~~

Les fichiers sont lus en streaming sans tout charger en mémoire.
L'échantillonnage déterministe retient jusqu'à 4096 observations train
et 1024 de développement par granularité, puis compare trois
architectures sur les mêmes exemples et les mêmes mini-lots.

H1 et M1 prédisent des horizons différents (prochaine heure contre
prochaine minute) : leurs scores NLL ne sont pas directement équivalents.

## Règles de recherche

- train : prix dont la cible clôture avant le 1er janvier 2022 UTC ;
- développement : cibles de 2022 à fin 2025 ;
- 2026 : quarantaine, aucune cible utilisée pour entraîner ou mesurer ;
- bougies à volume nul et ruptures de chronologie : exclues du
  contexte, sans imputation silencieuse ;
- trois bras : Transformer classique, mini-GPT modernisé, GRU ;
  comparaison exploratoire et non égalisée en FLOPs ;
- persistance comme témoin sur prix natifs ;
- pas d'exécution de trading, ni financement/perp Hyperliquid,
  ni accès API, ni ordres ;
- les données réelles n'ont PAS été copiées et les scores réels
  n'ont donc PAS été exécutés par l'assistant à cette étape.

## Passation Codex

Lire AGENTS.md et docs/CHATGPT_PROJECT_HISTORY.md puis stream.py,
experiment.py et test_history.py.

Branche : chatgpt/btc-h1-m1-20261025, sur la branche
chatgpt/trame-multi-architecture-20261025 (PR #8).
L'ancienne branche D1 chatgpt/btc-history-bridge-20261025 n'est
pas intégrée dans cette nouvelle branche ; ne pas la merger
par erreur. Les trois CSV D1 qu'elle prévoyait ne sont pas livrés.

Tests CI sur petites archives gzip fabriquées, sans aucun prix réel.
Dès la copie locale des 16 fichiers, faire tourner la comparaison
réelle H1 et M1 et archiver les JSON hors des protocoles gelés.

Le propriétaire accepte les archives pour ses recherches sans nouvel
audit de provenance ; cette préférence ne constitue pas une preuve
de droits de redistribution consentis par tous les tiers éventuels.
