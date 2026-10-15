# L’effet prothèse — Projet de recherche de Sébastien Noguès

Site éditorial français présentant une recherche **à venir**, issue du cadrage version 3 :

**L’intelligence artificielle dans les organisations éducatives : l’hypothèse de l’« effet prothèse » à l’épreuve du travail réel.**

Usages, résistances et reconfigurations du pouvoir face au déploiement d’une IA générative à TBS Education.

Destination : **https://nogues.app/these/**. Dépôt demandé : **https://github.com/nogseb/these**.

## Structure

```text
site/
  index.html                       page publique, contenu complet en HTML
  assets/styles.css                identité responsive Bento
  assets/site.js                   navigation et exploration progressive
  assets/signe.svg                 favicon
  assets/partage.png                aperçu des liens partagés
  documents/synthese-projet.md      synthèse publique téléchargeable
  manus-routes.json                 manifeste de la page de prévisualisation
  sitemap.xml                      URL canonique indexable
  .htaccess                        règles propres au sous-dossier Apache
scripts/
  check_site.py                    validation sans dépendance tierce
.github/workflows/
  deploy-ovh.yml                    publication SFTP depuis GitHub Actions
```

Aucun framework, build, backend, compte, cookie, traceur d’audience ou service externe n’est nécessaire au fonctionnement du site. Les seuls liens externes sont des références ou liens de navigation. Aucun contenu d’enquête ou document privé n’est inclus dans le dépôt.

## Aperçu local

```bash
python3 -m http.server 3000 --bind 0.0.0.0 --directory site
```

La page est utilisable sans JavaScript : les trois dimensions sont alors toutes affichées, les hypothèses utilisent les composants natifs `details` et la navigation reste accessible. Le JavaScript ajoute le menu mobile, le repère de navigation et une exploration sélective des dimensions.

## Validation

```bash
python3 scripts/check_site.py
node --check site/assets/site.js
```

## Publication sur OVHcloud via GitHub

Le workflow publie `site/` **uniquement dans `www/these`** à chaque modification pertinente poussée sur `main`, ou manuellement depuis l’onglet Actions. Aucun fichier distant n’est supprimé. La racine `www/` et les autres projets ne sont pas modifiés.

### Prérequis du propriétaire

Les secrets sont propres à chaque dépôt. Leur présence dans `nogseb/nogues.app` ne les rend pas disponibles dans `nogseb/these`.

Dans [Settings → Secrets and variables → Actions de nogseb/these](https://github.com/nogseb/these/settings/secrets/actions), configurer :

| Secret | Contenu à fournir dans GitHub, jamais dans le code |
|---|---|
| `OVH_SFTP_HOST` | Nom du serveur SFTP de l’hébergement OVHcloud |
| `OVH_SFTP_USER` | Identifiant FTP/SFTP autorisé pour cet hébergement |
| `OVH_SFTP_PASSWORD` | Mot de passe de cet utilisateur |
| `OVH_SFTP_KNOWN_HOSTS` | Ligne OpenSSH `known_hosts` pour ce serveur, avec clé d’hôte vérifiée hors bande |

Le domaine et son certificat HTTPS existent déjà. Le compte SFTP doit être autorisé à écrire dans `www/these`. Ne pas créer de CNAME ou changer les DNS : le site est un sous-dossier du domaine, pas un nouveau domaine GitHub Pages.

Si les secrets sont absents, le workflow échoue explicitement **avant tout envoi**. Il ne signale jamais une publication réussie lorsqu’elle n’a pas eu lieu. Après leur configuration, lancer [Actions → Publier le projet de recherche sur nogues.app/these → Run workflow](https://github.com/nogseb/these/actions).

Le workflow reprend le mécanisme SFTP de l’hébergement existant, mais exige l’authentification du serveur SSH. Fournir une ligne `known_hosts` provenant d’une connexion déjà approuvée, ou comparer son empreinte avec celle confirmée par OVHcloud avant de la configurer. Ne pas faire confiance à une clé obtenue par `ssh-keyscan` sans comparaison indépendante. La ligne doit correspondre exactement au nom d’hôte renseigné dans `OVH_SFTP_HOST`, sur le port SFTP standard 22. Aucune clé inconnue ou modifiée n’est acceptée automatiquement.

Le workflow vérifie ensuite la page publique, l’image de partage et la synthèse. En cas d’erreur Apache, vérifier les directives autorisées par l’hébergement dans `site/.htaccess` sans modifier le `.htaccess` de la racine du domaine.

## Modifier le contenu

La page est dans `site/index.html`, la synthèse dans `site/documents/synthese-projet.md`. Maintenir les deux cohérentes. Ne pas annoncer comme confirmés l’encadrement, l’inscription, les autorisations d’accès ou les résultats. Les quatre années sont celles du cadrage V3 et restent indicatives.

Après modification des fichiers CSS/JS, mettre à jour leur paramètre de version dans `index.html` pour renouveler le cache. Garder les métadonnées de partage et le sitemap cohérents avec l’URL canonique.

## Références effectivement consultées

- [LaborIA Explorer — Synthèse générale, 17 mai 2024](https://www.laboria.ai/laboria-explorer-synthese-generale/).
- [Inria — Présentation des résultats de l’étude exploratoire du LaborIA](https://www.inria.fr/fr/impacts-intelligence-artificielle-travail-laboria).
- [Clark & Chalmers — The Extended Mind, 1998, texte sur le site de David Chalmers](https://consc.net/papers/extended.html).

Les noms des personnes pressenties et le cadrage proviennent de la version 3 retenue dans le projet de recherche. La version source interne et les échanges de préparation ne sont pas publiés.

Présentation personnelle de Sébastien Noguès, **non institutionnelle**.
