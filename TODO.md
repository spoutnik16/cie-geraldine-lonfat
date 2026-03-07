# TODO — Site Compagnie Géraldine Lonfat

## En cours — Purge photos

Photos récupérées depuis Dropbox, réorganisées par spectacle dans `static/images/shows/<slug>/`.
**46 nouvelles photos à trier** via `photo_tagger.html` (identifier les bannis).

### État des photos par spectacle

| Spectacle | Total | Anciennes OK | Nouvelles à trier | Notes |
|-----------|-------|-------------|-------------------|-------|
| Teruel | 6 | 3 + 3 (4k) | 0 | OK |
| Pazzi | 7 | 1 + 1 (4k) | 5 presse | Dossier "CLAUDE JPEG PETITES" dans Dropbox = 20+ photos en rab si besoin |
| Shabbath | **0** | 0 | 0 | **Aucune source trouvée** — demander à Géraldine |
| Kaos | 13 | 1 + 1 (4k) | 11 | |
| L'Oubli des Anges | 18 | 1 + 1 (4k) | 16 | |
| J'ai Hâte d'Aimer | 13 | 1 | 12 | |
| Les Hérétiques | 2 | 1 + 1 (4k) | 0 | OK |
| Traces | 4 | 4 | 0 | OK |
| Vive la vie | 1 | 0 | 1 (visuel/affiche) | **Pas de photos de spectacle** dans Dropbox (que des articles scannés) |
| Noces de Joie | 7 | 3 + 4 (4k) | 0 | OK |
| ACDMS | 0 | 0 | 0 | Photos dispo dans `D:/Dropbox/GERALDINE/Au creux de mon silence/PHOTOS/` (pas encore copiées) |
| X-elles | 0 | 0 | 0 | Rien dispo |

### Prochaine étape
1. Mettre à jour `photo_tagger.html` avec les 46 nouvelles photos uniquement
2. Trier (identifier bannis sur les photos)
3. Supprimer les photos avec bannis
4. Mettre à jour `shows_extra.json` avec les galeries finales
5. Mettre à jour les chemins dans le template (nouvelle structure en sous-dossiers)
6. Rebuild

### Sources Dropbox pour photos supplémentaires
- Pazzi extras : `D:/Dropbox/1 INTERFACE/1 INTERFACE/1 association/1 Compagnie/1 spectacles/6 Pazzi/6 photos/PAZZI CLAUDE JPEG PETITES/` (~20+ photos)
- ACDMS : `D:/Dropbox/GERALDINE/Au creux de mon silence/PHOTOS/` (4 pro + sélection Roger Fusciardi 24+ photos)
- Shabbath & VLV : **aucune source identifiée** — à chercher avec Géraldine

## Prioritaire
- [ ] **Trier les 46 nouvelles photos** (outil photo_tagger.html)
- [ ] Trouver des photos pour Shabbath et Vive la vie
- [ ] Copier les photos ACDMS depuis Dropbox
- [ ] Ajouter une photo de Géraldine pour la page Parcours
- [ ] Refaire les meta descriptions de chaque page (SEO)
- [ ] Vérifier/corriger l'adresse email de contact
- [ ] Ajouter les infos des spectacles "Au creux de mon silence" et "X-elles" (descriptions, distributions)

## Design
- [ ] Choisir une police de caractères définitive
- [ ] Choisir les couleurs définitives
- [ ] Hero image pour la page d'accueil
- [ ] Favicon

## Contenu
- [ ] Ajouter les 4 spectacles pré-Teruel : Palosanto (1995), Circum Vitae, Tempora (~1999), Histoire d'elle
  - Palosanto documenté via arsenic.ch (description, distribution, dates)
  - Chercher des archives web pour les 3 autres
  - Demander à Géraldine les infos manquantes (dates, descriptions, photos)
- [ ] Compléter les descriptions manquantes des spectacles
- [ ] Ajouter les liens vers la presse / articles
- [ ] Page ou section vidéos / bandes-annonces

## Technique
- [ ] Mettre à jour build.py et templates pour la nouvelle structure en sous-dossiers (`shows/<slug>/`)
- [ ] Acheter le nom de domaine — **geraldinelonfat.fr** (dispo sur Gandi)
- [ ] Créer le repo GitHub et configurer GitHub Pages
- [ ] Configurer le domaine custom + HTTPS
- [ ] Tester sur mobile
