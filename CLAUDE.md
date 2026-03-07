# Site Web — Compagnie Géraldine Lonfat

## Architecture

Site statique généré par `build.py` (Python + Jinja2).

```
site-geraldine/
├── data/                # Données JSON (source de vérité)
│   ├── shows.json       # Spectacles, distributions
│   ├── events.json      # Événements, lieux, dates
│   └── bio.json         # Bio, prix, stats, cycles
├── templates/           # Templates Jinja2
│   ├── base.html        # Layout commun (nav + footer)
│   ├── index.html       # Page d'accueil
│   ├── spectacles.html  # Tous les spectacles
│   ├── parcours.html    # Biographie et prix
│   ├── calendrier.html  # Historique des représentations
│   └── contact.html     # Contact
├── static/
│   ├── css/style.css    # Feuille de style unique
│   └── images/          # Photos, affiches, miniatures
├── docs/                # Site généré (servi par GitHub Pages)
├── build.py             # Script de génération
├── TODO.md              # Tâches en cours
└── CLAUDE.md            # Ce fichier
```

## Workflow de mise à jour

1. Modifier les données dans `data/*.json` ou les templates dans `templates/`
2. Lancer `python build.py` pour regénérer le site
3. Vérifier le résultat dans `docs/index.html`
4. `git add . && git commit && git push`

## RÈGLE OBLIGATOIRE — Vérifier TODO.md avant chaque déploiement

**Avant tout `git push` ou toute action de déploiement, tu DOIS :**
1. Lire `TODO.md`
2. Vérifier s'il y a des tâches bloquantes pour le déploiement
3. Signaler à l'utilisateur les tâches en suspens
4. Ne déployer que si l'utilisateur confirme

## Données

### shows.json
Chaque spectacle a : `id`, `name`, `slug`, `category`, `description`, `short_description`, `miniature`, `companies`, `distributions`, `stats` (played, cancelled, countries).

### events.json
Chaque événement a : `show_id`, `show_name`, `venue`, `city`, `country`, `dates[]` (datetime ISO, cancelled bool).

### bio.json
Contient : `name`, `title`, `intro`, `bio_paragraphs[]`, `awards[]`, `cycles[]`, `stats`.

### Dates annulées
Le champ `cancelled: true` dans events.json indique une date annulée (COVID, etc.). Elles apparaissent barrées dans le calendrier mais ne sont pas comptées dans les stats.

## SEO — PRIORITÉ HAUTE

Le référencement est crucial pour ce site. À chaque modification de template ou de contenu, s'assurer que :
- Chaque page a une **meta description** unique et pertinente (150-160 caractères)
- Les balises `<title>` sont descriptives et contiennent les mots-clés importants (nom, spectacle, danse, théâtre)
- Les images ont des attributs `alt` descriptifs (pas vides, pas génériques)
- Le HTML est sémantique : `<article>`, `<section>`, `<nav>`, `<h1>`-`<h3>` bien hiérarchisés
- Les données structurées (JSON-LD / Schema.org) sont présentes : `Person`, `PerformingGroup`, `TheaterEvent`, etc.
- Les URLs sont propres et lisibles (slugs en français)
- Le site est rapide : images optimisées, CSS minimal, pas de JS inutile
- Domaine cible : **geraldinelonfat.fr**
- Mots-clés principaux : Géraldine Lonfat, chorégraphe, danse contemporaine, théâtre, compagnie, spectacles

## Conventions

- **Langue** : Français
- **Encoding** : UTF-8 partout
- **CSS** : Un seul fichier `style.css`, pas de framework, variables CSS pour les couleurs
- **Images** : Dans `static/images/`, formats JPG/WebP, optimisées
- **Photos spectacles** : Dans `static/images/shows/` (73 photos HD + 4K copiées du site Compagnie Interface)
- **Python** : Compatible Python 3.6+ (pas de f-strings walrus, pas de fromisoformat)

## Sources de données (site Compagnie Interface)

Le site original Compagnie Interface (`../`) contient du contenu riche réutilisable :

### Templates de spectacles
Dans `../templates/sites/compagnieinterface/spectacles/` : 12 templates Django avec :
- **Citations presse** (3-4 par spectacle) avec source, auteur, date
- **Processus de création** (200-500 mots) : récits d'immersion, méthodologie
- **URLs YouTube** des bandes-annonces (embed IDs)

Spectacles documentés : teruel, pazzi, shabbath, kaos, loubli-des-anges, jai-hate-daimer, les-heretiques, traces, vive-la-vie, noces-de-joie

### Photos HD (déjà copiées)
`static/images/shows/` contient 4 photos par spectacle + versions 4K :
- teruel1-4.jpg, pazzi1-4.jpg, shabbath1-4.jpg, kaos1-4.jpg
- loubli-des-anges1-4.jpg, jai-hate-daimer1-4.jpg (manque 1+3)
- les-heretiques1-4.jpg, traces1-4.jpg
- vive-la-vie1,2,4.jpg, noces-de-joie/ou-es-tu 1,2,4.jpg

### Pages HTML archivées
Dans `../temp/` : pages scrappées du site local (temp_teruel.html, temp_pazzi.html, etc.)

### Dropbox
`D:/Dropbox/GERALDINE/` contient les dossiers complets pour :
- **Au creux de mon silence** : affiche, photos, presse, prix Francine Delacrétaz
  - `PHOTOS/` : 4 photos pro (Copyright Claude Journu, Jim Planche, Maxime Lonfat)
  - `PHOTOS/sélection roger fusciardi/` : 24+ photos HD de Géraldine seule
  - `PHOTOS/photos presse/` : photos presse + sous-dossier presse avignon
  - `PHOTOS/Dominique Hugon - Générale/` : photos de la générale
  - `PHOTOS/Céline - Fillage/hq/` : photos du fillage
- **X-elles** (`X Elles/`) : dossier de présentation (PDF), CV Florence Alayrac, partitions, textes — pas de photos
- **Noces de Joie** (`noce de joie/`) : affiche, dossier présentation, 1 photo NB HD de Géraldine (TIF), vidéos
- **Photos à récupérer** :
  - VLV, ODA, JHA : dossiers PRESS à la racine de Dropbox (sélections de photos)
  - Pazzi, Kaos : `D:/Dropbox/interface/interface association/compagnie/spectacles/`
  - Shabbath : toujours aucune source identifiée

## Personnes à purger (OBLIGATOIRE)

Ces personnes ne doivent JAMAIS apparaître sur le site (ni nom, ni photo, ni mention) :

- **Thomas Laubacher** — texte, interprète
- **Ophélie** aka **Salomé** — (nom de famille à confirmer)
- **Johanna Rittiner Sermier** — musique, interprète
- **Stéphanie Boll** — chorégraphie
- **Alain Boll**
- **André Pignat** — cofondateur Compagnie Interface (scandale MeToo)
- **Gerda Pignat** — costumes
- **David Gaudin** — vidéo
- **Pierre Favre** — scénographie
- **Jean-Blaise Évéquoz** — peinture
- **Kim Salah** — costumes
- **Jean-Camille Sormain** — mise en scène
- **Xavier Loira** — interprète
- **Nico** — (nom de famille à confirmer)
- **Rémy** — (nom de famille à confirmer)
- **Marie Fournier** — interprète (L'Oubli des Anges)
- **Lionel Fournier** aka **Victor**
- **Marie Lanfroy** — interprète (Noces de Joie, Vive la vie) — PAS bannie, OK
- **Marc** — (nom de famille à confirmer)

Le mot "traître" est un terme interne — ne doit jamais apparaître sur le site ni dans les données publiques.

Les distributions ont été retirées de tous les spectacles sauf ACDMS et X-elles.
Un outil `photo_tagger.html` permet d'identifier les photos à supprimer (personnes visibles).

## Contexte

- Géraldine Lonfat = danseuse, chorégraphe, metteuse en scène
- A fondé la Compagnie Interface en 1990 (dissoute suite à scandale MeToo d'André Pignat)
- A créé la Compagnie Géraldine Lonfat pour continuer
- NE JAMAIS mentionner André Pignat ou le scandale sur le site
- Les spectacles anciens (Compagnie Interface) sont présentés comme son travail personnel
- ~928 représentations jouées, 88 annulées (COVID), 20 pays, 12 spectacles (+ 4 pré-Teruel à ajouter)

## Spectacles pré-Teruel (à ajouter)
4 spectacles avant Teruel (2003) pas encore dans le site :
- **Palosanto** (1995) — arsenic.ch/archives/palosanto — description et distribution connues
- **Circum Vitae** — dates et infos à chercher
- **Tempora** (~1999) — Prix d'encouragement de l'État du Valais 1999
- **Histoire d'elle** — dates et infos à chercher

## Utilisatrice

Géraldine est danseuse, pas informaticienne. Elle utilise Claude Code CLI pour faire ses modifications. Les instructions doivent être claires et les erreurs explicites.
