# P1-B0 0.2 : qualification documentaire

Voir le chapitre 13, édition 2.4. `freeze.json` scelle le candidat, le protocole et le script avant le nouvel audit de cibles. Il ne constitue pas une préinscription externe. Les choix restent discutables ; les données d'ajustement avaient déjà été explorées.

`target_audit_report.json` : 304 920 présentations, 15 360 cotations cibles distinctes, partition 1999-2009 exclusivement. Aucun modèle ou score prédictif. Les scripts refusent d'écraser leurs rapports.

`design_report.json` : identités rationnelles, inventaire de paramètres et quatre illustrations math.erfc. Aucune tête complète, normalisation différentiable ou simulation de trajectoires implémentée. SciPy/mpmath absents du runtime ; leur documentation n'est pas un test exécuté.

Le champ hérité `arithmetic_recurrence_check` du candidat 0.2 désigne le contrôle historique `../20261015/design_checks.json`. Les contrôles nouveaux sont dans `design_report.json`. Le candidat 0.1 et le plan original restent inchangés dans 20261015. Le nouveau statut est dans `progress.json`.

Le candidat utilise S=64 par défaut. La sensibilité déclarée S=256 doit changer le biais initial en log((8-.25)/(256-8)) pour garder sigma initial égal à huit. Ce complément explicite figure au chapitre 13 ; aucune exécution de modèle n'a suivi. Les très faibles bornes de masse hors dictionnaire limitent la portée générale de la tête.

Ne pas relancer les scripts de préparation ou d'audit sur les rapports existants. Toute modification doit être versionnée et sa position chronologique par rapport aux lectures de données indiquée.
