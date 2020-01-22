# Utilisation de Data Connect, l’API Linky

Data Connect est une API proposée par Enedis pour permettre à une application d’accéder aux données de consommation d’un utilisateur équipé d’un compteur Linky.

Son utilisation est gratuite, mais peut prendre plusieurs semaines à mettre en place. Cette page en donne un aperçu, la documentation officielle (bien plus détaillée) est disponible après inscription sur le site [Enedis DataHub](https://datahub-enedis.fr/data-connect/).

## Contribution

Ce dépôt est proposé par le collectif des [consometers](https://www.consometers.org/) pour partager notre expérience et échanger avec d’autres utilisateurs. N‘hésitez pas à ouvrir une [Issue](https://github.com/consometers/data-connect/issues) pour suggérer une modification ou échanger sur Data Connect.

## Utilisation

Data Connect permet à une application de :

- Recueillir le consentement de l’utilisateur à travers l’espace client Enedis.
- Accéder aux données de consommations d’un utilisateur équipé d’un compteur Linky.
- Accéder aux informations contractuelles du consommateur, comme son identité, ses coordonnées, le type de compteur ou la puissance souscrite.

Un certain nombre de limitations peuvent être trop contraignantes pour votre application. C‘est notamment le cas si vous voulez accéder à vos propres données de consommation, qui pourraient être récupérées plus simplement dans votre espace client Enedis. D’autres moyens sont proposée par Enedis pour [accéder aux données de mesure](https://www.enedis.fr/acceder-aux-donnees-de-mesure).

## Limitations

- L’utilisateur doit être équipé d’un compteur Linky, raccordé avec une puissance inférieure à 36 kVA.
- L’enregistrement d’une application nécessite un numéro de SIRET et la signature d’un contrat avec Enedis.
- L’application doit être développée en mode « bac à sable » et implémenter un parcours client conforme avant de pouvoir accéder à des données réelles.
- Il n’est pas possible de récupérer une consommation « instantanée », le pas de mesure le plus fin est de 30 min.
- Il n’est pour le moment pas possible d’accéder aux données de productions.
