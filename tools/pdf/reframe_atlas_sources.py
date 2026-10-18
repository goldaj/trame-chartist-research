from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[2]; D=ROOT/'dossier/recherche_lcm'
p=D/'02_atlas_des_langages.md'; s=p.read_text(encoding='utf-8')
s=s.replace('ce petit exemple n\'est pas un corpus autorisé pour le futur bot de production.','cet exemple reste limité à la recherche personnelle. Il ne définit pas le corpus multi-marchés visé.')
s=s.replace("La chart ressemble à l'originale, mais une différence de cet ordre peut modifier un résultat après frais.","La chart ressemble à l'originale, mais la différence peut être plus grande qu'une variation que nous cherchons à prévoir.")
s=s.replace('les unités économiques','les unités de prix').replace("L'échelle économique disparaît","L'échelle absolue disparaît").replace('sens économique des crans','amplitude physique des crans').replace('niveaux économiquement importants','petits écarts de prix et des extrêmes').replace('faible lien avec la décision','faible lien avec la cible future')
s=s.replace("un long et un short n'ont pas toujours les mêmes coûts et contraintes ; le temps inversé peut fabriquer une liquidité irréaliste.","hausses et baisses peuvent présenter des dynamiques et des queues différentes ; inverser le temps peut détruire les dépendances temporelles et la chronologie des événements.")
s=s.replace("son intérêt persiste après les coûts si l'on en fait une stratégie",'son information prédictive se retrouve sur des actifs et périodes réservés')
s=s.replace('sans alpha directionnel','sans prédictivité directionnelle').replace('scores décodés, calibration, reconstruction et éventuelle décision après coûts','scores de prévision décodés, calibration, reconstruction et transfert entre marchés')
s=s.replace("La deuxième ronde oppose les deux meilleurs choix à une génération continue de trajectoires et à un modèle préentraîné existant. La troisième teste au plus deux extensions : langues parallèles et contexte entre actifs.","Les rondes suivantes comparent continu, discret et hybride à plusieurs tailles de GPT et volumes de données. Une faible performance initiale ne suffit pas à éliminer une famille : on étudie sa courbe de progression et ses pertes d'information. Les langues parallèles et le contexte entre actifs sont des axes distincts.")
s=s.replace("Un candidat est écarté si son avantage vient d'une information future, d'une comparaison de budget inégale, d'une résolution économique inadéquate ou d'un effet non reproduit.","Un résultat est invalidé si son avantage vient d'une information future ou d'une comparaison inégale. Une résolution inadéquate ou un effet non reproduit motive un diagnostic et une nouvelle version de l'expérience ; cela ne réfute pas tous les modèles possibles de cette famille.")
s=s.replace('la reconstruction en prix et les décisions sous coûts','la reconstruction en prix et la prévision hors échantillon')
s=s.replace('## 1 La question essentielle',"**Mise à jour scientifique 2, 14 octobre 2026. L'exemple historique reste une démonstration de conversion. Le document 07 ajoute une mesure réelle de distorsion ; le document 08 ouvre la comparaison GPT et marché latent.**\n\n## 1 La question essentielle")
s+='''

## 11 Nouvelle piste : un langage à précision progressive

La comparaison réelle du document 07 montre un piège : des quantiles par champ peuvent bien restituer la majorité des petites variations et beaucoup moins bien certains mouvements rares. Cette observation ne réfute pas les vocabulaires appris. Elle indique que le débit alloué aux queues et la représentation des valeurs hors plage doivent être des paramètres explicites.

Une piste hybride représente chaque coordonnée par un signe, une classe d'ordre de grandeur, un code de forme et un résidu. Une autre réserve un symbole d'échappement aux extrêmes, suivi d'une amplitude continue. Une troisième utilise plusieurs couches de précision, où l'on ne termine le mot qu'après un nombre maximal de raffinements. Ces langages sont des propositions nouvelles pour l'expérience suivante, pas des mécanismes déjà entraînés ou validés.

Le coût doit inclure les échelles, l'ancre, la durée, le codebook et les résidus. Une faible erreur obtenue avec cinq nombres continus supplémentaires par bougie n'est pas une compression gratuite. On cherchera un front précision/débit, puis un front prévision/calcul, à plusieurs tailles de modèle. La reconstruction isolée ne suffit pas à choisir le meilleur langage prédictif.

Le niveau zéro d'une mèche, l'absence de transaction et l'absence de mesure restent des états différents. Un token rare ne doit pas servir indistinctement pour une crise réelle, une valeur impossible et une panne de source. Ces distinctions sont sémantiques avant d'être architecturales.
'''
p.write_text(s,encoding='utf-8')

p=D/'06_etat_art_sources_audit.md'; s=p.read_text(encoding='utf-8').split('## Audit du contexte et provenance de cette étude')[0]
s=s.replace('sans backtest exécuté et sans modification du bot','sans expérience prédictive exécutée').replace('## Conclusion exploitable','## Conclusion scientifique')
s=s.replace('Hyperliquid et OVH sont des contextes d’application, pas des frontières du modèle. ','')
s=s.replace('Aucun résultat publié consulté n’établit qu’un modèle de chandeliers sera rentable sur notre bot et notre marché.','Aucun résultat publié consulté ne prouve à lui seul la prévisibilité de tous les prix dans tous les régimes.')
s=s.replace('Ne pas non plus importer mécaniquement l’AGPL dans l’ensemble du bot sans examen des composants effectivement réutilisés.','Les licences des composants effectivement réutilisés devront être examinées séparément.')
s=s.replace('pour Hyperliquid','sur notre futur corpus multi-marchés').replace('n’est transposé à Hyperliquid','n’est transposé à notre expérience scientifique').replace('dans le bot de production','dans un système autonome hors du périmètre autorisé')
s=s.replace('avec tâches correspondant au bot','avec cibles et horizons correspondant à la question scientifique')
s=re.sub(r'\*\*Séparer trois espaces\.\*\*[^\n]+',"**Séparer trois espaces.** L'espace observable contient les informations réellement disponibles. L'espace latent les représente. L'espace de sortie contient la distribution des prix futurs. Une reconstruction précise n'établit pas que le latent prédit bien ; une information perdue peut être sans importance pour une cible et indispensable pour une autre.",s)
s=s.replace(' Pour l’utilité économique : comparer une règle de décision fixée avec frais, funding, spread, slippage, délais et limites de taille. Un gain de loss sans avantage économique peut néanmoins justifier un outil de risque ; il ne justifie pas une promesse d’alpha.',' Les scores de direction, dispersion et trajectoire sont publiés séparément. Un score de token favorable ne garantit pas une meilleure prévision des prix.')
s=s.replace('La prévision de rendement, la volatilité, la liquidité, l’exécution et la simulation constituent différentes évaluations de cette représentation. La rentabilité d’un bot est une validation possible parmi celles-ci, pas la définition complète du modèle fondation.','La prévision des accroissements de prix, de la dispersion et des trajectoires constitue différentes évaluations de cette représentation.')
s=s.replace('ou à Hyperliquid','à un marché particulier').replace('leur recouvrement précis avec Hyperliquid','leur recouvrement avec nos futurs tests').replace('la rentabilité reste une hypothèse ouverte','la prévisibilité et le transfert restent des hypothèses ouvertes')
s=s.replace('Le plafond pertinent n’est donc pas la capacité du serveur OVH, mais la frontière empirique entre information disponible, biais de représentation, capacité du modèle et coût acceptable. Une infrastructure nouvelle est légitime si cette frontière mesurée la justifie.','La frontière à étudier relie information disponible, biais de représentation, capacité, diversité et calcul. Une faible performance locale ne suffit pas à en déduire un plafond universel.')
s=s.replace('## 8. Corpus réel : cinq voies d’acquisition vérifiées au-delà d’Hyperliquid','## 8. Corpus réel : voies d’acquisition multi-marchés')
s=s.replace('aucun abonnement, achat, téléchargement massif ni transfert des données du projet n’a été réalisé. Ce catalogue établit des voies d’accès, pas un inventaire déjà acquis.','aucun abonnement ni achat n’a été effectué. Ce catalogue décrit des voies d’accès ; le document 07 distingue désormais les petites collectes réellement acquises et auditées.')
s=re.sub(r'\*\*Point matériel sur les archives Binance\.\*\*[^\n]+',"**Droits du corpus témoin.** Les conditions Binance Vision consultées le 14 octobre 2026 prévoient la recherche personnelle hors production et encadrent séparément les autres usages. Les données dérivées conservent attribution et conditions applicables ; l'utilisation ici est descriptive et scientifique. [Conditions primaires](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md).",s)
s=s.replace('garantie d’un gain de trading net sur nos données','garantie de prévision généralisable sur nos données')
s=s.replace('Ces petites expériences servent à choisir le langage et à estimer une loi de progression','Ces petites expériences servent à qualifier les erreurs, comparer plusieurs régimes d’échelle et estimer une loi de progression')
s+='''

## 10 Mise à jour du 14 octobre : marché latent, GPT et échelle

Le cadrage actif porte sur la prévision scientifique multi-marchés. L'ancienne annexe d'exploitation est conservée uniquement dans la version 1 archivée. Le papier 01 et le document 08 distinguent partage de grammaire, information croisée et état commun partiel. Aucun modèle prédictif n'a été entraîné pour cette mise à jour.

TimesFM-3, annoncé le 31 août 2026, constitue une antériorité importante pour l'attention entre séries dans un Transformer temporel. Les mécanismes et les limites des sorties marginales sont analysés au document 08. L'annonce est une source primaire des auteurs, pas une reproduction indépendante. [Annonce technique](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/).

Les travaux d'Edwards et de Yao motivent une mesure des effets d'échelle. Leurs résultats ne constituent pas une loi universelle des prix financiers ; les détails et restrictions sont discutés dans le document 05. [Edwards et al.](https://arxiv.org/abs/2405.13867v2), [Yao et al.](https://arxiv.org/abs/2410.12360v3).

La notion de facteur partagé possède une longue histoire économétrique. Stock et Watson proposent de résumer un grand nombre de prédicteurs par des composantes avant de prévoir une série. Cette référence empêche de présenter le seul « Marché commun » comme une idée nouvelle. Notre programme ajoute des questions sur les langues, les masques et le transfert. [Article des auteurs](https://www.princeton.edu/~mwatson/papers/Stock_Watson_JASA_2002.pdf).

Le catalogue NYSE Daily TAQ annonce une histoire remontant à 1993, ce qui ouvre une voie de recherche pour les épisodes de 2000 et de 2008, sous conditions d'accès à établir. Il n'atteste pas une qualité uniforme de chaque variable à la seconde sur toute cette période. Les données BCE constituent une voie distincte pour les références quotidiennes de devises. [NYSE](https://www.nyse.com/data-products/catalog/daily-taq), [BCE : séries de référence](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html).

Les nouveaux manifestes locaux documentent les observations effectivement reçues. Les sources synthétiques mentionnées dans certains modèles de la littérature n'ont pas été substituées aux observations réelles des mesures TRAME. Les petits exemples artificiels des tests de calcul sont identifiés comme tels.
'''
p.write_text(s,encoding='utf-8')

p=D/'08_marche_latent_et_gpt.md'; s=p.read_text(encoding='utf-8')
blocks=re.findall(r'\\\[\s*.*?\\\]',s,flags=re.S)
repls=['`P[a,t] = G[a](z[t], u[a,t], m[a,t]) + epsilon[a,t]`.','`p_theta({P[a,t+h]} pour a et h | F[t])`, où F[t] contient les observations effectivement disponibles au plus tard à t.']
assert len(blocks)==2
for a,b in zip(blocks,repls): s=s.replace(a,b)
p.write_text(s,encoding='utf-8')
print('02, 06 and math layout 08 updated')
