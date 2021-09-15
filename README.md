# SnapDirecte
Snapchat bot to send EcoleDirecte's homework (and more, I hope) in DMs (or in group chat)

The rest will be in French, sorry.

#### Disclaimer
C'est mon premier "vrai" script en python, merci d'être indulgent à propos de la qualité du code ! Je suis conscient qu'elle n'est pas optimale, et travaille à l'améliorer.

## Fonctionnement
### 1. Récupération des données
La récupération des données du site d'EcoleDirecte se fait via des requêtes HTTP sur leur API. Une boucle assure au script d'être à jour en continu.

### 2. L'envoi sur SnapChat
Comme je n'ai pas vraiment envie de me démener à récupérer l'API privée de SnapChat, j'utilise PyAutoGUI combiné à BlueStacks pour ouvrir le groupe de la classe (ou le DM) puis envoyer le message.


## Mise en place
- Premièrement, il vous faut modifier les identifiants de connexion. Ça se passe ligne 12.
- Ensuite, il faut télécharger BlueStacks. (https://cloud.bluestacks.com/api/getdownloadnow?platform=win&win_version=10)
- Dans BlueStacks, connectez-vous sur le PlayStore et installez SnapChat. Vous verrez un raccourci apparaître sur le bureau.
**⚠️ Attention, la fenêtre d'accueil de SnapChat doit être visible sur le bureau lorsque vous exécutez le script !⚠️**

Ce n'est pas encore idéal, puisqu'il est nécessaire d'avoir 24h/24 son ordinateur "dédié" à la fenêtre de Snap'. Si vous voulez un VPS Windows, venez là :*https://discord.gg/Y5cCwHsgaS*


### ❗ Une erreur  ?
Ouvrez une issue !

### 💞 Un conseil ?
Faites une Pull Request ou bien contactez moi sur Discord (*MathiAs2Pique_#1717*) pour m'aider à développer cet outil


## *Roadmap*

[x] Prévenir lors des nouveaux devoirs
[] Résumé quotidien des devoirs
[] Prévenir lors de nouvelles notes
[] Message spécial lors des évaluations
[] Prévenir lors des nouveaux documents dans le Cloud
[] Des commandes ?
