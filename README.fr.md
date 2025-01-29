# ULToICAL
[ [English](README.fr.md) | [Francais](README.fr.md) ]

[ [Supporter mon travail](https://ko-fi.com/totorocodesoften) ]


ULToICAL est un outil facile pour convertir votre EDT UL en format ICAL utilise par Google Agenda, le Calendrier Apple etc...
## Installation
Pour utiliser ULToICAL vous aurais besoin de `python>=3.10`

Commencer par faire

```bash
pip install .
```

Puis demarer le programme avec:

```bash
ultoical
```

## Obtenir le jeton UL (Facultatif)
Pour obtenir le jeton aller sur votre EDT et faites `CTRL + Maj + I`

Cliquez sur `Reseau/Network` sur la fenetre qui vient de s'ouvrir

Naviguer dans l'UL jusqu'a ce que vous voyez un `200 POST schedule json`

Cliquez dessus, allez dans `Requests` et copier le champ `authToken`