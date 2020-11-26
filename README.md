[![Build Status](https://github.com/dmartin35/pronosfoot/workflows/CI/badge.svg)](https://github.com/dmartin35/pronosfoot/actions)

# pronosfoot
Site web perso de pronos entre amis pour la Ligue 1


Présentation
------------
Ce site est un "vieux" projet né 2010, pour remplacer les fichiers excel envoyés par mails entre copains,
avec mise à jour auto des calendrier & resultats issus du site officiel de la LFP.
Le site fournit aussi les côtes des matches issues du site officiel FDJ.

Conçu initialement avec django 1.0.2 & python 2.5, ce projet est maintenant porté sur django 1.10 & python 3.4+.
Nouveau design utilisant material design, pour rajeunir le visuel & mode adaptif pour tous les écrans.

Crons
-----
```bash
pronosfoot@ssh:~$ crontab -l
# m h  dom mon dow   command
0 23 * * * ~/.python/venv/pronosfoot/bin/python ~/pronosfoot/manage.py daily
0 12 * * * ~/.python/venv/pronosfoot/bin/python ~/pronosfoot/manage.py reminder
0 0 * * * ~/.python/venv/pronosfoot/bin/python ~/pronosfoot/manage.py clearexpiredsessions
```
