from pathlib import Path
import json, csv, math
ROOT=Path(__file__).resolve().parents[2]; D=ROOT/'dossier/recherche_lcm'; R=ROOT/'research/trame_poc0'
m=json.loads((R/'results/measurements.json').read_text()); audit=json.loads((R/'results/data_manifest.json').read_text()); ecb=json.loads((R/'ecb_exploratory/audit.json').read_text())
names={'continuous':'Continu float64','fixed':'Pas fixes','quantile64':'Quantiles 64','signs':'Signes / présence','adaptive':'Pas selon sigma passée'}
summary=[]
for tf,tfdata in m['timeframes'].items():
 for codec,assets in tfdata['codecs'].items():
  n=sum(a['bars'] for a in assets.values()); nt=sum(a['tail_bars'] for a in assets.values())
  summary.append({'timeframe':tf,'codec':codec,'bars':n,'mean':sum(a['bars']*a['ohlc_log_bps']['mean'] for a in assets.values())/n,'max':max(a['ohlc_log_bps']['max'] for a in assets.values()),'tail_n':nt,'tail_mean':sum(a['tail_bars']*a['tail_ohlc_log_bps'].get('mean',0) for a in assets.values())/nt,'invalid':sum(a['invalid_bars'] for a in assets.values())})
(R/'results/summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
rows='\n'.join('| '+ ' | '.join([r['timeframe'],names[r['codec']],f"{r['mean']:.4f}",f"{r['tail_mean']:.4f}",f"{r['max']:.4f}"])+ ' |' for r in summary)
assets='\n'.join(f"| {asset} | {m['timeframes']['1h']['codecs']['fixed'][asset]['bars']} | {m['timeframes']['1h']['codecs']['fixed'][asset]['ohlc_log_bps']['mean']:.3f} | {m['timeframes']['1h']['codecs']['quantile64'][asset]['ohlc_log_bps']['mean']:.3f} | {m['timeframes']['1h']['codecs']['quantile64'][asset]['ohlc_log_bps']['max']:.3f} |" for asset in audit['started_from'] and ['BTCUSDT','ETHUSDT','BNBUSDT','ADAUSDT','XRPUSDT','LTCUSDT','EOSUSDT','TRXUSDT'])
body=f'''# Première mesure des langages et extension du corpus réel

**Rapport du 14 octobre 2026, version scientifique 2. Les nombres ci-dessous sont issus d'observations réelles. Ils mesurent reconstruction et qualité des données, pas prévision du prix futur.**

## 1 Rôle exact de cette expérience

POC0 est un appareil de mesure pour la conversion des courbes en représentations. Il prend une bougie déjà observée, l'encode, puis la reconstruit. L'expérience évalue la distorsion créée par le langage. Aucun GPT, RNN, modèle de trajectoire ou codebook neuronal n'a été entraîné. Aucun score prédictif n'a été calculé. Des paramètres de quantification ont été ajustés sur une période de calibration passée.

Le corpus horaire témoin était choisi avant le recadrage multi-marchés approfondi. Il sert à qualifier les calculs et ne constitue ni le corpus cible ni une preuve de transfert. Une seconde acquisition ajoute maintenant une histoire réelle de devises de 1999 à 2020 ; elle fait l'objet d'un audit, sans lui appliquer artificiellement une géométrie de bougie absente.

## 2 Protocole gelé, puis amendement explicite

La version initiale a été gelée le {audit['started_from']['amends']['frozen_at_utc']}. L'acquisition s'est arrêtée sur une bougie dont l'heure de fermeture ne correspondait pas à une heure complète. Des archives déjà reçues ont alors été inspectées uniquement pour ce contrôle de durée ; aucune métrique de représentation n'avait encore été produite.

La version 1.1 a été gelée le {audit['started_from']['frozen_at_utc']}. Elle exclut les bougies se terminant avant la fin de leur heure du comparatif à durée fixe, les conserve dans le brut et les signale. Les timestamps hors de l'intervalle prévu restent rejetés. L'amendement ajoute aussi une lecture des bornes de dates depuis le protocole et le contrôle de finitude des reconstructions. La version précédente, son code et ses empreintes sont conservés.

La période janvier–août 2021 ajuste les vocabulaires et les seuils ; septembre–octobre 2021 fournit la mesure de développement. Les archives de novembre–décembre 2021 pour les huit paires n'ont pas été téléchargées. Ce découpage historique n'est pas une validation prospective. Les futures expériences pourront réserver d'autres périodes sans présenter celles déjà examinées comme vierges.

Empreinte SHA-256 du protocole actif : `{audit['started_from']['protocol_sha256']}`. Empreinte du programme d'analyse : `{audit['started_from']['analysis_sha256']}`. Le protocole et le journal d'amendement sont dans research/trame_poc0 ; les résultats complets sont dans son sous-dossier results.

## 3 Corpus horaire réellement reçu

Quatre-vingts archives mensuelles ont été reçues et leur empreinte vérifiée contre le CHECKSUM publié. Elles concernent BTCUSDT, ETHUSDT, BNBUSDT, ADAUSDT, XRPUSDT, LTCUSDT, EOSUSDT et TRXUSDT, sur janvier–octobre 2021. Source : [Binance Vision, documentation primaire](https://github.com/binance/binance-public-data). Les manifestes donnent chaque URL, date de réception, taille et empreinte.

- {audit['source_observations']:,} lignes sources ; {audit['missing_hours']} créneaux horaires absents par rapport au calendrier continu, comptés sur les huit séries.
- {audit['early_close_excluded']} lignes se terminant avant la fin de leur heure, conservées mais exclues du comparatif.
- {audit['observations']:,} bougies horaires complètes admises ; {sum(a['bytes'] for a in audit['archives']):,} octets d'archives ZIP.
- Aucun remplissage des trous. Un trou réinitialise le contexte. L'agrégation H4 exige exactement quatre parents H1 complets, alignés en UTC.

Les heures absentes et les trois fermetures anticipées par actif se retrouvent sur plusieurs séries. Il ne faut pas compter ces répétitions comme des incidents indépendants ni attribuer leur cause sans preuve. Par exemple, une ligne du 11 février 2021 à 03:00 UTC se termine après 2 454 774 ms ; une autre du 25 avril à 04:00 UTC après 58 147 ms. Le checksum était pourtant correct : intégrité de transfert et qualité du calendrier sont deux contrôles différents.

La géométrie exige un précédent prix et des échelles calculées sur le passé strict. Chaque segment exige 65 bougies de contexte avant la première mesure. En H1 : {m['timeframes']['1h']['usable_train']:,} observations de calibration, {m['timeframes']['1h']['usable_dev']:,} de développement et {m['timeframes']['1h']['warmup_excluded_total']:,} exclues pour l'amorçage du contexte. En H4 : {m['timeframes']['4h']['usable_train']:,}, {m['timeframes']['4h']['usable_dev']:,} et {m['timeframes']['4h']['warmup_excluded_total']:,} respectivement. Les exclusions après des trous peuvent retirer des épisodes agités : l'échantillon admis n'est pas présumé sans biais. H4 provient de H1 : les deux résolutions ne sont pas deux corpus indépendants.

## 4 Cinq représentations comparées

Chaque bougie positive est transformée en g=ln(O/C_précédent), b=ln(C/O), u=ln(H/max(O,C)), d=ln(min(O,C)/L) et v=ln(1+V/V_ref). V_ref est la médiane des 64 volumes strictement précédents, avec plancher 10^-12. Sigma est l'écart-type population de 64 rendements de clôture strictement passés, avec plancher 10^-6. Ces références sont observées et fournies à la reconstruction.

| Langage | Règle exacte | Statut |
|---|---|---|
| Continu | Cinq coordonnées float64 | Contrôle numérique presque identique, pas un vainqueur de compression |
| Pas fixes | Arrondi au plus proche, égalités vers pair ; pas 0,001 sur g,b,u,d et 0,05 sur v | Entiers sans vocabulaire borné |
| Quantiles 64 | Zéro explicite ; au plus 63 classes non nulles par champ ; médiane d'apprentissage par classe | Vocabulaire fini empirique, non neuronal, séparé H1/H4 |
| Signes / présence | Signe de g et b ; présence ou absence de u,d,v ; amplitude médiane de calibration | Contrôle volontairement destructeur |
| Adaptatif | Pas 0,1 sigma passée sur g,b,u,d ; pas 0,05 sur v | Entiers non bornés ; échelle fournie comme information auxiliaire |

Les quantiles sont ajustés sur janvier–août uniquement, en regroupant les huit actifs pour chaque résolution. Les frontières dupliquées sont fusionnées ; les classes extérieures sont ouvertes et les zéros restent exacts. Un code de classe ne conserve pas la distance à son représentant. Le programme mesure séparément les sorties du support de calibration.

Les 64 observations passées représentent 64 heures en H1 et 256 heures en H4. La comparaison entre ces résolutions ne contrôle donc pas la durée physique de normalisation ; elle n'a pas été conçue pour estimer le seul effet de la fréquence. Une prochaine expérience devra fixer cet axe séparément.

## 5 Résultats descriptifs

L'erreur est `10 000 × abs(ln(prix_reconstruit/prix_observé))`. Un point de base logarithmique vaut 0,0001 en logarithme. Ce n'est pas exactement un point de base de variation simple pour les grands écarts. La moyenne ci-dessous regroupe O,H,L,C et toutes les bougies admises de développement, avec pondération par leur nombre.

La colonne « queue » sélectionne les bougies dont le corps absolu dépasse le 99e percentile de calibration de leur résolution, sans sélectionner les erreurs après coup. Elle contient seulement {summary[0]['tail_n']} bougies en H1 et {next(r['tail_n'] for r in summary if r['timeframe']=='4h')} en H4, potentiellement corrélées entre actifs. Ces très petits effectifs décrivent cet échantillon ; ils ne permettent pas une généralisation statistique sur les crises ni une comparaison prédictive.

| Résolution | Langage | Moyenne log-bps | Moyenne queue log-bps | Maximum log-bps |
|---|---|---:|---:|---:|
{rows}

<!-- pocfigure -->

La branche continue restitue les prix à l'arrondi numérique près. Les prix de toutes les branches respectent ici les contraintes OHLC : c'est en grande partie une propriété du décodeur géométrique, pas une découverte empirique sur la prévisibilité.

**Constat majeur : moyenne et extrêmes conduisent à des lectures différentes.** En H1, les quantiles sont légèrement meilleurs en moyenne que les pas fixes (2,282 contre 2,568 log-bps), mais leur moyenne sur les corps extrêmes atteint environ 200 log-bps, contre environ 2,98 pour les pas fixes. Le maximum des quantiles dépasse 2 456 log-bps. L'espace des grandes amplitudes est trop grossièrement représenté par certaines classes terminales. Cette observation concerne ce quantificateur marginal précis ; elle ne condamne pas un vocabulaire hiérarchique appris.

L'absence de borne de vocabulaire donne aux pas fixes une propriété différente : l'erreur locale est bornée par 5 log-bps pour O, 10 pour C, et 15 pour H/L, hors erreur numérique. Ces bornes résultent de la somme des arrondis de g, b et des mèches. Il serait incorrect de déclarer ce langage globalement supérieur sans compter son débit et comparer ses capacités prédictives.

### Décomposition H1 par actif

| Actif témoin | Bougies dev | Moyenne fixe | Moyenne quantiles | Maximum quantiles |
|---|---:|---:|---:|---:|
{assets}

Toutes les erreurs de ce tableau sont en log-bps. La granularité de la source et les actifs de cette expérience ne définissent pas les futurs marchés d'entraînement. Une répétition sur actions, or ou devises ne peut pas être revendiquée à partir de ces chiffres.

## 6 Autres diagnostics conservés

Les résultats JSON détaillent erreurs de clôture, quantiles d'erreur par actif, volumes, support de calibration, occupation des codes et dérive cumulative. La dérive réutilise les échelles observées et une ancre vraie au début de chaque segment de développement : c'est une dérive conditionnelle du codec, pas une trajectoire future générée. Pour une génération réelle, les échelles futures devraient être figées ou mises à jour sur le chemin généré selon une règle annoncée.

Un diagnostic séparé repère des paliers sur les seules clôtures, avec seuil de 0,005 logarithmique, soit environ +0,50125 % pour un palier montant. Il agrège les multiples franchissements visibles à une clôture, conserve durée et résidu, et marque l'attente finale comme censurée. Il ne reconstruit pas l'ordre des mouvements intrabougie et ne traite pas les paliers comme des horizons calendaires fixes.

Les informations latérales ne sont pas comptabilisées en bits dans ce premier rapport. Le continu, les entiers non bornés et les quantiles ne disposent donc pas du même débit démontré. Une comparaison débit-distortion reste à construire. La fréquence des tuples inconnus ne prouve ni nouveauté économique ni difficulté prédictive.

## 7 Extension réelle hors du corpus horaire : devises BCE

Une requête bornée à 1999–2020 a reçu {ecb['total_rows']:,} lignes pour AUD, CAD, CHF, GBP, JPY et USD contre EUR. Elle contient {ecb['valid_rows']:,} valeurs numériques, soit 5 632 par devise, du 4 janvier 1999 au 31 décembre 2020. Les 372 entrées explicitement vides portent le statut H de non-publication ; elles ne sont pas remplacées par des prix. Le contrôle ne trouve aucun doublon de clé série-date. L'empreinte du brut est `{ecb['raw_sha256']}`.

Sur les 5 740 dates du lundi au vendredi de la période demandée, 108 n'ont pas de valeur numérique : 62 sont explicitement marquées H et 46 n'ont aucune ligne. Ces 46 dates ne sont pas toutes certifiées individuellement par un calendrier historique dans cet audit. Les H s'arrêtent en 2012 ; le changement de représentation des absences ne doit pas devenir un faux signal de régime.

Cette acquisition apporte une vraie profondeur historique comprenant les années 2000, 2008 et 2020. Elle ne démontre aucune capacité à prévoir les événements de ces périodes. Les séries partagent l'EUR comme dénominateur : six devises ne sont pas six expériences indépendantes et une partie de leurs relations est mécanique. Aucun cours postérieur à 2020 n'a été reçu dans cette requête.

Ce sont des références quotidiennes, pas des transactions ni des bougies avec hauts, bas et volumes. Leur disponibilité ne doit pas être assimilée au début de la date civile. La publication habituelle a été déplacée vers 16:00 CET à partir du 1er juillet 2016 ; la documentation antérieure indique environ 14:30. Le fichier actuel ne prouve pas la version exacte ni l'heure de réception historique de chaque ligne. [BCE : séries](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html), [changement de publication](https://www.ecb.europa.eu/press/pr/date/2015/html/pr151207.en.html).

L'audit et les comptages annuels sont conservés dans research/trame_poc0/ecb_exploratory. Ils n'ont pas servi à ajuster les cinq codecs OHLCV. Ils préparent une branche de recherche distincte, avec masque de modalité et une convention de disponibilité adaptée. [Politique de réutilisation des statistiques BCE](https://www.ecb.europa.eu/stats/ecb_statistics/governance_and_quality_framework/html/usage_policy.en.html).

## 8 Vérification et portée scientifique

Neuf contrôles de calcul ont réussi : intégrité et périmètre d'archive ; schéma et doublons ; exclusion tracée des bougies partielles ; agrégation à quatre parents ; invariance au futur ; réinitialisation après trou ; reconstruction et bornes d'arrondi ; traitement des zéros ; paliers et censure. Les petits exemples construits pour ces contrôles ne font pas partie des observations utilisées dans les tableaux.

Les premières revues entre agents logiciels ont vérifié disponibilité des sources et absence de fuite dans les références passées. Elles ont conduit à expliciter coût des informations auxiliaires, durée différente de sigma selon la résolution et limites des trajectoires reconstruites. Ce n'est pas une revue par des chercheurs humains indépendants.

La conclusion autorisée est que l'appareil de mesure fonctionne sur deux types de données réelles et qu'un quantificateur simple peut perdre fortement les extrêmes malgré une bonne moyenne. La conclusion non établie est qu'un langage, un GPT ou un état latent commun prédit les prix. Les prochaines comparaisons doivent étudier information latérale, précision progressive et corpus multi-marchés, puis tester la prévision à plusieurs échelles de modèle selon le protocole scientifique.
'''
for value in [audit['source_observations'],audit['observations'],sum(a['bytes'] for a in audit['archives']),ecb['total_rows'],ecb['valid_rows']]+[m['timeframes'][tf][key] for tf in ['1h','4h'] for key in ['usable_train','usable_dev','warmup_excluded_total']]:
    body=body.replace(f'{value:,}',f'{value:,}'.replace(',',' '))
(D/'07_premieres_mesures_reelles.md').write_text(body,encoding='utf-8')

import sys
sys.path.insert(0,str(ROOT/'tmp/pdfs/chart_deps'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
fig,axes=plt.subplots(1,2,figsize=(10,3.65),layout='constrained')
colors=['#294b67','#c58a36','#96485a','#438778']
for ax,tf in zip(axes,['1h','4h']):
 vals=[r for r in summary if r['timeframe']==tf and r['codec']!='continuous']; x=np.arange(4)
 ax.bar(x-.18,[r['mean'] for r in vals],.34,color=colors,label='Toutes les bougies',alpha=.95)
 ax.bar(x+.18,[r['tail_mean'] for r in vals],.34,facecolor='white',edgecolor=colors,hatch='///',label='Corps extrêmes')
 ax.set_xticks(x,['Fixe','Quantiles','Signes','Adaptatif']);ax.set_yscale('log');ax.set_ylim(1,1500);ax.set_title('Résolution '+tf.upper(),fontweight='bold');ax.set_ylabel('Erreur OHLC moyenne (log-bps)');ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
 ax.spines[['top','right']].set_visible(False)
axes[0].legend(fontsize=8,loc='upper left')
fig.suptitle('Reconstruction : une bonne moyenne peut masquer les extrêmes',fontsize=12)
fig.savefig(R/'results/reconstruction_errors.png',dpi=180)
fig.savefig(R/'results/reconstruction_errors.svg')
plt.close(fig)
print('REPORT',len(body.split()),'words; figure and summary generated')
