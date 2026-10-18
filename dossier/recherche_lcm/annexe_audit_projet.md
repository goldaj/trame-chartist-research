## Audit du contexte et provenance de cette étude

### Périmètre et dates

Recherche documentaire principale le 13 octobre 2026, complétée et finalisée le 14 octobre en heure de Paris. Les heures techniques ci-dessous sont conservées en UTC, avec leur équivalent parisien lorsqu'utile. Les informations d'exploitation sont des instantanés, pas une surveillance continue. Cette étude ne réalise ni diagnostic complet du compte ni certification du bon fonctionnement du trading.

Le dossier a été créé dans l'espace documentaire de cette conversation. Le dépôt de développement existant et le serveur ont été consultés en lecture seule. Aucun fichier du bot, paramètre de stratégie, service, ordre, permission de trading ou déploiement n'a été changé. Aucune donnée du holdout réservé n'a été ouverte. Aucun achat, location de GPU ou entraînement n'a été lancé.

### Trois états de code à ne pas confondre

Le dépôt privé identifié est `goldaj/hyperliquid-btc-pilot`. La branche GitHub par défaut observée est `codex/development`. La copie locale effectivement utilisée par le projet se trouve dans `C:/Users/golda/Documents/trading_bot_hyperliquid_6_astra`. L'espace documentaire courant n'est pas cette copie : son dépôt Git initial ne possédait pas de HEAD exploitable.

À la consultation du 13 octobre, `git ls-remote` indiquait développement `68ca04b9b4ebaa26a92b11d75a1d13e62b7cb429` et production `89620745d4c540b68518c3756dc92fc99ace4732`. Le HEAD local était `f5a6846544e7dac8a5a375fb6b4bf4046b9c28d5`, avec des modifications non committées, notamment autour du compte et du dashboard. Ces fichiers de travail ne sont pas assimilés à du code déployé. Les métadonnées ne constituent pas une vérification exhaustive des différences.

Sur le serveur, le lien nommé `current` résolvait vers la release `626b6e9`, tandis que `WorkingDirectory` du service live indiquait la release `8962074`. C'est la configuration du service qui renseigne son répertoire de travail ; le seul nom `current` ne prouve pas le code exécuté. Aucun redémarrage ni changement de lien n'a été effectué pour cette étude.

### Ressources et état observés

Lecture distante du 13 octobre à **18:05:30 UTC**, soit **20:05:30 à Paris** : 2 vCPU, mémoire totale affichée 3 819 Mio, mémoire disponible 1 610 Mio, swap utilisé 413 Mio sur 2 047 Mio, disque système de 38 Gio avec environ 27 Gio disponibles. Aucun accélérateur de calcul n'était exposé dans l'inventaire PCI consulté. Cela ne décrit pas les possibilités d'une future infrastructure.

Le service live était déclaré `active/running`, avec environ 107 Mio de mémoire courante et un compteur de redémarrages à 1. Les timers de capture et d'observation d'exécution étaient actifs en attente. Le groupe systemd du bot affichait un plafond mémoire de 1 Gio et une quote-part CPU correspondant à un CPU. Un service actif ne prouve ni la fraîcheur de toutes ses données ni la correction de sa comptabilité.

Les répertoires publics de recherche contenaient 241 fichiers de captures marché et 257 fichiers liés à l'observation d'exécution ; tailles respectives environ 7,6 Mio et 1,1 Mio. Le répertoire de nouvelles pesait environ 5,2 Mio. Ce sont des comptes de fichiers, pas des comptes de décisions admissibles, de bougies uniques ou d'observations statistiquement indépendantes. Les contenus économiques réservés n'ont pas été évalués.

Les contraintes historiques prévoient un serveur partagé avec d'autres services et un bot léger. Elles expliquent pourquoi un entraînement de fondation n'a pas sa place sur cette machine actuelle. L'utilisateur a explicitement précisé que l'infrastructure entière peut changer : ces constats ne bornent donc pas la conception de TRAME.

### Documents du projet utilisés

`AGENTS.md`, `OBJECTIF.md`, `AVANCEMENT.md`, `docs/server-constraints.txt`, `docs/architecture.md`, `docs/research-prospective.md`, `docs/research-execution-observation.md`, `docs/research-replay-model.md`, `docs/campaign007-preregistration.md`, `pyproject.toml` et un extrait de `src/hlbot/research_capture.py` ont servi à comprendre le contexte. Le README distant et les références Git ont été consultés via GitHub et Git. Les documents locaux peuvent inclure du travail non publié ; leur statut est conservé.

Les éléments utiles sont la collecte publique horodatée, le moteur de replay explicite sur ses limites, la séparation du signataire et les campagnes préenregistrées. La capture de 169 bougies horaires contient un historique recouvrant largement les captures voisines. Sa quote d'exécution postérieure ne doit pas devenir une entrée connue au moment de la capture initiale.

La campagne 007 décrite dans les fichiers réserve le 14 octobre 00:00 UTC au 9 décembre 00:00 UTC 2026 à une comparaison déjà définie. TRAME devra réserver son protocole et sa période séparément. Le présent dossier ne change ni cette campagne ni le holdout 002.

### Échantillon réel inspecté pour le langage

Une seule petite archive de prix a été téléchargée pour l'illustration du document 02, depuis Binance Vision : BTCUSDT spot, 1h, mars 2020. Aucun téléchargement massif ni constitution du corpus d'entraînement n'a été réalisé. L'empreinte vérifiée est `cc36c481c31ef93115d96b5a7045ec2ef737e5339546d6688cb1f677526c6787`.

Le contrôle a constaté 743 ouvertures uniques et un intervalle manquant à 10:00 UTC le 4 mars. Les transformations de la bougie du 12 mars à 12:00 UTC sont des calculs descriptifs, pas un test prédictif. Le manifeste local conserve l'URL, les nombres sources, la correspondance CHECKSUM et l'avertissement sur la disponibilité historique non attestée.

Attribution des nombres et de leur transcription transformée : Binance Vision ; conditions consultées au 14 octobre 2026, CC-BY-NC-SA-4.0 assorties des conditions du fournisseur. L'extrait et ses transformations sont présentés pour recherche personnelle hors production. Les références du document 02 permettent de consulter la source et les conditions. Aucun droit de production sur ce corpus n'est présumé.

### Révisions effectivement réalisées

La reformulation initiale a distingué recherche, conception et opérations de trading. La première révision a retiré OVH du rôle de contrainte architecturale après la précision de l'utilisateur. La deuxième a placé la conversion des courbes en langage au centre du dossier. La troisième a ouvert un atlas d'hypothèses inhabituelles et imposé pour chacune un test. La quatrième a renforcé le corpus réel multi-marchés et remplacé le nom LCM par TRAME.

La revue bibliographique a retiré les revendications trop générales de nouveauté après identification de Kronos, KiT et des modèles événementiels. La relecture technique par un agent distinct a précisé le sens d'intégration du flow matching, la différence entre horloge d'événements et calendrier, et la nécessité d'un modèle d'exécution distinct des bougies.

Une seconde relecture de l'atlas a vérifié numériquement les transformations et entraîné quatre corrections : échelles de normalisation en génération ; impossibilité de reconstruire le chemin intrapalier à partir de seuls franchissements ; tokenisation BPE du préfixe disponible uniquement ; séparation du bénéfice d'une représentation et de celui d'une information supplémentaire. Ces échanges logiciels sont réels ; les personas du document 05 sont fictifs.

### Ce qui n'a pas été établi

Ni corpus mondial déjà acquis, ni benchmark reproduit, ni gain statistique du projet, ni budget définitif, ni licence universelle de tous les poids, ni rentabilité de TRAME. La revue est approfondie mais ciblée, pas une recherche systématique exhaustive de toutes les publications et brevets. La nouveauté éventuelle reste à démontrer. Les sources récentes et pages de licences devront être figées par version au début d'une implémentation.
