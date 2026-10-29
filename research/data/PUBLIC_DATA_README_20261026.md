# TRAME — données BTC/USD publiques, intégration reproductible
Import initial : 26 octobre 2026. **Source autorisée à être publiée par
l'utilisateur pour son projet de recherche** ; l'autorisation du
propriétaire de ce dépôt ne supprime pas les droits éventuels des
producteurs externes. Attributions et liens de licence conservés.

## Ce qui est effectivement versionné dans la branche
- `reference/btcusd-bitstamp-d1-2012-2026H1.csv` :
  **372 096 octets**, **5 295 bougies journalières OHLCV**
  du 01/01/2012 au 30/06/2026, vérifié à l'identique
  par Git blob SHA-1 `a8f2da91cb00fce75117ba5bf000384f240abd56`.
  Cet ensemble quotidien est issu du dépôt
  [BTC Cycle Data](https://github.com/alessiostomeo/btc-cycle-data/tree/b57f460fab1afb82705eb813cee2ef4afb1f6848)
  et de l'archive de recherche privée de référence.
  C'est une série préparée à partir du bloc original upstream,
  tronquée au 30 juin 2026. Ce fichier est **du spot BTC/USD
  Bitstamp**, pas un marché des perpétuels Hyperliquid.
- `reference/bitstamp_source_manifest.json` :
  16 archives gzip H1/M1, noms, longueurs et
  **Git blob SHA-1 originaux**, commit upstream
  `b57f460fab1afb82705eb813cee2ef4afb1f6848`.
- `public_data.py` : downloader autonome sans secret
  depuis l'upstream **public**, validation taille
  + Git SHA1 **identique**, SHA256 consignable,
  pas de remplacement d'un fichier déjà corrompu.
  H1/M1 ne sont PAS committés : leur taille cumulée
  est d'environ **113 Mo compressés** et ils sont
  stockés dans le cache hors dépôt Git après download
  sur une machine autorisée avec accès réseau.
- **Les fichiers M1/H1 compressés ne sont pas encore
  téléchargés dans le runtime de cette conversation** :
  ce runtime ne dispose pas d'un accès réseau brut
  utilisable vers raw.githubusercontent.com. Le
  connecteur GitHub valide des fichiers texte,
  pas un transfert complet de gzip. Ne pas revendiquer
  que les 16 fichiers ont été effectivement copiés.

## Attribution des producteurs et conditions
Historique Bitstamp 2012–2026 :
- Sources dérivées : [alessiostomeo/btc-cycle-data](https://github.com/alessiostomeo/btc-cycle-data),
  commit épinglé cité ci-dessus.
- Historique Bitstamp précurseur :
  [ff137/bitstamp-btcusd-minute-data](https://github.com/ff137/bitstamp-btcusd-minute-data),
  reprenant des données de
  [Zielak / mczielinski sur Kaggle](https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data).
- L'attribution enregistrée dans le dépôt de données
  d'origine indique **CC BY-SA 4.0** pour les segments
  anciens dérivés de Kaggle et **CC BY 4.0** pour
  les ajouts Bitstamp API ultérieurs.
  Respecter la licence effectivement applicable à
  chaque segment :
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
  et [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
  Le fichier journalier ici est **reformaté/limité
  temporellement** ; conserver les notices et, si
  nécessaire, les obligations de partage dans les
  mêmes conditions.
- **2010-07-18 → 2011-08-17** : clôtures **indicatives**
  de [viratsoft/btc-price-json](https://github.com/viratsoft/btc-price-json),
  source attribuée à CoinGecko, **sans licence
  de redistribution clairement confirmée ici**.
  Elles ne sont **pas** committées dans TRAME.
- **2011-08-18 → 2011-12-31** :
  [daniegitx1/btc-price-history](https://github.com/daniegitx1/btc-price-history).
  Les conditions de redistribution n'étant pas
  clairement établies, ces bougies ne sont **pas**
  reproduites dans TRAME.
  La prise en charge du cache **complet** D1 d'origine
  reste dans `research/btc_h1_m1/daily.py`.

## Utilisation dans TRAME
Depuis le clone TRAME, avec Python 3.12 :

~~~bash
# Référence D1 2012+ : copie locale instantanée, pas de réseau :
python -m research.data.public_data --resolution D1 --check-only

# Reconstituer H1 et M1 depuis les 16 sources gzip publiques :
python -m research.data.public_data --resolution H1
python -m research.data.public_data --resolution M1

# Vérifier l'identité locale déjà téléchargée, sans réseau :
python -m research.data.public_data --resolution ALL --check-only

# Les lecteurs A7/S1/S2 utilisent ensuite exactement le
# même cache DEFAULT_CACHE / TRAME_BTC_CACHE_DIR :
python -m research.btc_h1_m1.statistical_baselines --interval D1 --output /tmp/d1_public_baselines.json
~~~

Le D1 2012+ peut également être ouvert directement depuis
`research/data/reference/` dans les scripts acceptant un
dossier explicite, puisque le lecteur supporte désormais
les deux modes :
- **trois segments** D1 2010–2026H1 si ceux-ci sont
  déjà disponibles légalement et localement ;
- **un segment** vérifié D1 2012–2026H1 public.

**Attention comparabilité** : la cohorte « D1 2012+
seulement » omet les quelques exemples 2011H2. Elle
doit donc avoir un `cohort_id` différent des anciennes
statistiques D1 privées. Ne pas écrire qu'un résultat
ancien a été reproduit à l'identique si les cohortes
diffèrent. Aucune importation de D1 2010–2011
en OHLCV fictif.

## Sécurité et rigueur scientifique
- Même si les données historiques sont publiques, les
  **clés GitHub, identifiants, portefeuilles et
  secrets de trading** ne le sont pas.
- Le fichier journalier comprend des jours de 2026,
  mais **l'entraînement et le développement S1/S2
  n'ouvrent pas les cibles 2026** : gel chronologique
  toujours appliqué par le code.
- Séries BTC/USD spot, parfois zéro volume /
  bougies remplies artificiellement par l'amont,
  **pas** une simulation d'exécution de contrats
  perpétuels Hyperliquid.
- Les frais restent exclus des simulations selon
  la décision utilisateur. Aucun ordre réel.
- Les téléchargements restent dans `~/.cache/trame/`
  ou `TRAME_BTC_CACHE_DIR`, pas dans des commits
  Git de plusieurs centaines de Mo.
- Aucune exécution de S2/S2b sur cours réels
  n'est attestée par la simple disponibilité
  d'un fichier D1. Lancer/reproduire les
  entraînements reste une tâche distincte.
