# TRAME S3.1A : pilote réel G0b/G0a/G1/G2
26 octobre 2026. **24 entraînements BTC/USD Bitstamp
SPOT réellement exécutés**, 3/3 jobs réussis :
[GitHub Actions #40299287171](https://github.com/goldaj/trame-chartist-research/actions/runs/40299287171).
**Pas de validation indépendante ni d'edge démontré.**

## Protocole réellement exécuté
D1/H1/M1 × 4 grammaires G0b/G0a/G1/G2 × 2 modes
Huber et Huber+0,5 BCE = 24 bras,
width16/depth1, 2 418 paramètres / réseau,
**une seule graine 20261026, 40 optimizer updates**,
train D1 3608, H1/M1 4096, dev 1024 par horizon.
Les quantiles G2 proviennent exclusivement
des 20 rendements passés dans TRAIN ;
normalisations input/target communes fit TRAIN.
2026 hors train/dev ; aucune transaction.

Les tokens G1/G2 sont **décodés en bps**
avant `ContinuousDirectionModel` : ce pilote
teste la représentation d'entrée,
**pas les embeddings discrets appris**.

## Justesse directionnelle ET précision du montant

| Résolution | Loss | Grammaire | BA sens % | MAE bps | Erreur amplitude bps | % sorties UP |
|---|---|---|---:|---:|---:|---:|
| D1 | Huber | G0b continu | 53,41 | 181,429 | 175,240 | 14,36 |
| D1 | Huber | G0a arrondi | 53,40 | 181,424 | 175,225 | 14,55 |
| D1 | Huber | G1 signée fixe | 50,00 | 181,797 | 178,140 | 0,00 |
| D1 | Huber | G2 quantiles train | 49,37 | 181,635 | 180,121 | 56,45 |
| D1 | Joint | G0b continu | 51,14 | 181,724 | 173,841 | 89,26 |
| D1 | Joint | G0a arrondi | 51,04 | 181,754 | 173,823 | 88,96 |
| D1 | Joint | G1 signée fixe | **52,83** | **181,478** | 176,297 | 66,80 |
| D1 | Joint | G2 quantiles train | 51,56 | 181,579 | 179,330 | 86,72 |
| H1 | Huber | G0b continu | 50,10 | 34,463 | 28,942 | 99,90 |
| H1 | Huber | G0a arrondi | 50,19 | 34,443 | 28,972 | 99,80 |
| H1 | Huber | G1 signée fixe | 50,00 | 34,914 | 27,979 | 100,00 |
| H1 | Huber | G2 quantiles train | 50,00 | 34,262 | 29,888 | 100,00 |
| H1 | Joint | G0b continu | 50,00 | 34,421 | 29,137 | 100,00 |
| H1 | Joint | G0a arrondi | 50,00 | 34,415 | 29,125 | 100,00 |
| H1 | Joint | G1 signée fixe | 50,00 | 34,615 | 28,690 | 100,00 |
| H1 | Joint | G2 quantiles train | 49,18 | 34,209 | 30,245 | 95,51 |
| M1 | Huber | G0b continu | 51,53 | 5,881 | 4,128 | 11,23 |
| M1 | Huber | G0a arrondi | **52,81** | 5,843 | 4,083 | 16,80 |
| M1 | Huber | G1 signée fixe | **52,81** | **5,839** | 4,112 | 16,80 |
| M1 | Huber | G2 quantiles train | 50,22 | 5,902 | 4,053 | 3,03 |
| M1 | Joint | G0b continu | 50,31 | 6,099 | 4,157 | 51,46 |
| M1 | Joint | G0a arrondi | 49,51 | 5,973 | 4,152 | 83,40 |
| M1 | Joint | G1 signée fixe | 49,67 | 5,890 | 4,224 | 60,94 |
| M1 | Joint | G2 quantiles train | **51,10** | 6,137 | 4,042 | 34,47 |

**À ne pas sur-interpréter :**
- Un score à 50% pour prédiction quasi
  toujours UP n'est pas une classification
  directionnelle exploitable ; regarder la
  dernière colonne.
- Sur D1 Joint, G1 améliore légèrement BA
  et MAE bps face au continu (52,83 vs
  51,14 ; 181,478 vs 181,724) mais son
  erreur d'AMPLITUDE ABSOLUE se dégrade
  de 173,841 à 176,297 bps. **Pas de
  victoire sur TOUS les critères.**
- H1 est toujours quasi monoclasse.
- Une seule graine/40 steps = simple
  canary d'ingénierie, pas une campagne
  crédible de sélection, encore moins un
  test indépendant. La cohorte D1 publique
  commence en 2012, à distinguer
  des anciens D1 2011H2 privés.
- Les biais de sampling sont conservés :
  1024 dates de développement par horizon,
  contextes recouvrants ; aucune
  croissance de portefeuille inférable.

## Artefacts sources et SHA-256
Rapports JSON des 3 jobs du run :
- D1 `D1_s3_4grammars_real_pilot.json`,
  SHA256 `996c322499d69ebc1c6284aeeded8974b52b174d03eb22ac3e79defd8b8f9eae`.
- H1 `H1_s3_4grammars_real_pilot.json`,
  SHA256 `55006674ea4f4cb4e6808d613f63b9e085daaf9728497706d4e4822b6a31e7eb`.
- M1 `M1_s3_4grammars_real_pilot.json`,
  SHA256 `19f309ea0477abd71c97c5efe28a6407d87d546c8ea1add862653b31658d3638`.

Modèle du run : Git SHA
`4119b1c2f8cae104696e677f40673cc8475ba1ae`.
Ces rapports sont entièrement agrégés,
pas de prix bruts ni d'identité trader.

## Étape suivante
Lancer la **matrice correcte 288 fits**
= 3×4×2×2×2×3 (96/horizon), 200 updates,
3 seeds, 2 widths/profondeurs.
Workflow `.github/workflows/trame-s3-predictive-288.yml`
et run public
[GitHub Actions #40300156418](https://github.com/goldaj/trame-chartist-research/actions/runs/40300156418).
**Vérifier son état avant de dire « 288 terminés ».**
Le premier workflow mal nommé 192,
run #40299704128, a été retiré
avant d'être considéré valide ;
sa matrice et ses assertions étaient
fausses. Le correctif a été fait avant
l'analyse du benchmark définitif.
