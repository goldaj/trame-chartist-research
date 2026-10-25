# BTC/USD historique : bibliothèque privée commune à TRAME

**Décision définitive courante : 25 octobre 2026.**

L'unique source de vérité est la **release versionnée du dépôt privé
goldaj/btc-historical-data**. Ni le dépôt du bot Hyperliquid ni ses
artefacts Actions éphémères ne doivent être utilisés comme référence
primaire. TRAME public contient seulement le lecteur et les résultats,
**pas les archives de prix**.

- Dépôt : https://github.com/goldaj/btc-historical-data
- Release : https://github.com/goldaj/btc-historical-data/releases/tag/btcusd-bitstamp-2010-2026-reference-v1
- Tag exact : btcusd-bitstamp-2010-2026-reference-v1
- 21 assets publiés : 3 CSV journaliers, 1 gzip H1, 15 gzip M1, un
  MANIFEST.json et un SHA256SUMS.txt.
- Référence immuable par tag, jusqu'à publication explicite d'une
  nouvelle version. Ne pas suivre la dernière release sans accord.

## Consigne du propriétaire

Utiliser ces historiques **tels quels**, sans réexaminer
leur provenance ni solliciter une nouvelle validation. Les conserver
sous leur format et leur nom d'origine. Les opérations de recherche
continuent à respecter les plages temporelles réservées, les trous,
les volumes nuls et les limites liées à la résolution des bougies.
La provenance n'est pas requalifiée ici.

## État courant de la recherche

La pause historique du 25 octobre est levée pour TRAME,
voir [le tableau de bord actif](../../docs/CODEX_EXECUTION_BOARD_20261025.md).
La priorité actuelle reste **A3c/A4**, et les campagnes sur
cours réels restent **non exécutées**. Les commandes de téléchargement
et les exemples ci-dessous ne s'exécutent que si une campagne
autorisée en a besoin ; aucune nouvelle vérification de provenance
des fichiers BTC n'est demandée.

## Accéder aux données sans alourdir TRAME

Le dépôt privé nécessite l'authentification GitHub pour
accéder à ses assets. Une lecture distante octet par octet serait
inutilement coûteuse ; le lecteur passe par **un cache local**,
à l'extérieur du clone Git TRAME :

- Par défaut : dossier personnel/.cache/trame/bitcoin/
  btcusd-bitstamp-2010-2026-reference-v1/
- Personnalisable avec la variable TRAME_BTC_CACHE_DIR.
- Aucune copie dans TRAME ou dans un commit public.
- Les octets gzip restent inchangés. Aucun recalcul préalable.
- Les téléchargements suivants sont ignorés si les fichiers
  attendus sont déjà présents avec leur taille prévue.
- La commande refuse les fichiers incomplets ou les symlinks ;
  elle ne réécrit pas silencieusement un asset.

Installer GitHub CLI une fois, puis se connecter :

~~~powershell
gh auth login
gh auth status
~~~

Depuis la racine d'un clone TRAME, la commande télécharge
uniquement les archives requises, **directement depuis la release
privée** :

~~~powershell
python -m research.btc_h1_m1.release_store --resolution H1 --download
python -m research.btc_h1_m1.release_store --resolution M1 --download
python -m research.btc_h1_m1.release_store --resolution D1 --download
~~~

Le mode ALL récupère tous les dix-neuf fichiers de prix :

~~~powershell
python -m research.btc_h1_m1.release_store --resolution ALL --download
~~~

L'accès ne fonctionne que sur les machines authentifiées disposant
d'un droit de lecture du dépôt privé. La CI publique de TRAME ne
reçoit aucun token privé et travaille uniquement avec des archives
fictives générées en mémoire/disque temporaire.

## Utilisation pour TRAME

Après récupération locale, aperçu sans nouveau téléchargement :

~~~powershell
python -c "from research.btc_h1_m1.stream import limited_preview; print(limited_preview('H1'))"
python -c "from research.btc_h1_m1.stream import limited_preview; print(limited_preview('M1'))"
~~~

Campagnes exploratoires (Python 3.12, NumPy, SciPy, PyTorch CPU) :

~~~powershell
python -m research.btc_h1_m1.experiment --interval H1 --steps 40 --output btc_h1_dev.json
python -m research.btc_h1_m1.experiment --interval M1 --steps 40 --output btc_m1_dev.json
~~~

Les fichiers H1/M1 sont lus **en streaming**, sans tout
décompresser en mémoire. Les partitions exploratoires utilisent
l'entraînement avant 2022 et le développement sur 2022–2025.
Les cibles 2026 ne sont pas utilisées dans ces expériences.
Une bougie zéro volume ou une discontinuité du calendrier rompt
le contexte d'entraînement.

**Attention** : des fenêtres H1 (prochaine heure) et M1
(prochaine minute) prédisent des horizons différents. Aucune
comparaison brute de NLL entre les deux n'est recevable.
Les trois architectures sont encore des prototypes de recherche
non égalisés en budget de calcul. Aucun backtest économique et
aucune preuve de performance réelle n'ont été produits ici.

Le corpus D1 remonte au 18 juillet 2010 ; les archives H1 et M1
commencent en 2012. Le téléchargeur gère également D1 pour
les analyses ultérieures des cycles de plus longue durée.
Ces prix historiques BTC/USD spot/indicatifs ne représentent
pas les conditions d'exécution sur les perpétuels Hyperliquid.

## Livraisons / passation Codex

Branche : chatgpt/btc-h1-m1-20261025, créée sur
chatgpt/trame-multi-architecture-20261025 (PR #8).
L'ancienne branche chatgpt/btc-history-bridge-20261025
est abandonnée et n'entre pas dans cette chaîne.

- release_store.py : inventaire exact de la release et acquisition
  à la demande par gh avec cache local, sans accès réseau implicite.
- stream.py : lecture séquentielle des archives H1/M1.
- experiment.py : comparaison exploratoire de trois backbones.
- test_release_store.py / test_history.py : tests sur fausses
  archives gzip et appels CLI simulés ; aucun prix réel utilisé.
- .github/workflows/trame-btc-h1-m1.yml : CI sans données privées.

Avant tout travail, lire AGENTS.md et docs/CHATGPT_PROJECT_HISTORY.md,
puis ce document. Toujours préserver la séparation des temps et
l'inventaire de la release. Aucune action de trading ou sur le bot.

L'usage recherche par l'utilisateur ne préjuge pas à lui seul de
droits externes ; aucune validation nouvelle de provenance n'est
demandée pour ce travail.
