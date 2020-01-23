# Utilisation de Data Connect, l’API Linky

Data Connect est une API proposée par Enedis pour permettre à une application d’accéder aux données de consommation d’un utilisateur équipé d’un compteur Linky.

Son utilisation est gratuite, mais peut prendre plusieurs semaines à mettre en place. Cette page en donne un aperçu, la documentation officielle (bien plus détaillée) est disponible après inscription sur le site [Enedis DataHub](https://datahub-enedis.fr/data-connect/).

## Contribution

Ce dépôt est proposé par le collectif des [consometers](https://www.consometers.org/) pour partager notre expérience et échanger avec d’autres utilisateurs. N’hésitez pas à ouvrir une [Issue](https://github.com/consometers/data-connect/issues) pour suggérer une modification ou échanger sur Data Connect.

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

## Recueil du consentement de l’utilisateur

### Envoi sur l’espace client Enedis

La première étape consiste à diriger l’utilisateur vers son espace client Enedis, selon un parcours défini, pour recueillir son consentement. Par exemple :

```
https://espace-client-particuliers.enedis.fr/group/espace-particuliers/consentement-linky/oauth2/authorize?client_id=ae632d42-91b8-4ce9-b0d4-8438ecd014a1&duration=P3Y&redirect_URI=https%3A%2F%2Fvotre-app.fr%2Fdataconnect%2Fredirect&response_type=code&state=abcd123
```

| Paramètre | Description |
| --- | --- |
| `client_id` | Identifiant de votre application, fourni lors son enregistrement.<br/>Ex. `ae632d42-91b8-4ce9-b0d4-8438ecd014a1`. |
| `redirect_URI` | Adresse vers laquelle l‘utilisateur sera redirigé après avoir exprimé son consentement.<br/>Ex. `https://votre-app.fr/dataconnect/redirect` |
| `state` | Sera ajouté à l’adresse de redirection maintenir l’état entre la requête et la redirection.<br/>Ex. `abcd123`. |
| `duration` | Durée pendant laquelle l’application souhaite accéder aux données du client, au format ISO 8601, ne peut excéder 3 ans.<br/>Ex. `P3Y`. |

Cette page affichera une demande de consentement.

### Redirection sur votre application

Une fois le consentement exprimé, l’utilisateur sera redirigé vers votre application :

```
https://votre-app.fr/dataconnect/redirect?code=ZS5454hkfa47w7wkAwqQ9GrtUWwooL&state=abcd123&usage_point_id=22516914714270
```

Vous permettant d’obtenir :

| Paramètre | Description |
| --- | --- |
| `code` | Permet de récupérer un `refresh_token` et un `access_token`. Valable 180 s.<br/>Ex. `ZS5454hkfa47w7wkAwqQ9GrtUWwooL`. |
| `state` | Valeur passée avant la redirection pour maintenir l’état.<br/>Ex. `abcd123`. |
| `usage_point_id` | Points de livraison (PRM ou PDL) identifiant le/les compteurs de l’utilisateur (non testé avec plusieurs identifiants).<br/>Ex.  `22516914714270`. |

## Authentification

L’accès aux données de l’utilisateur nécessite un `access_token`, valide 3 heures. Cet `access_token` devra être transmis en entête de chaque requête HTTP permettant d’accéder aux données de l’utilisateur :

```
Authorization: Bearer 7tT7xon48xnhxSWnBX5FzuoiEUWm2hApyf1lmqeDlHyU2oqcCv84xf
```

### Juste après le consentement

La première fois il sera obtenu à partir du  `code` récupéré après le consentement de l’utilisateur.

```
curl -d "grant_type=authorization_code&client_id=ae632d42-91b8-4ce9-b0d4-8438ecd014a1&client_secret=d7ee309e-8ae2-429c-96d0-d7ab99800a22&code=ZS5454hkfa47w7wkAwqQ9GrtUWwooL" -X POST "https://gw.prd.api.enedis.fr/v1/oauth2/token?redirect_uri=https%3A%2F%2Fvotre-app.fr%2Fdataconnect%2Fredirect"
```

| Paramètre | Description |
| --- | --- |
| `code` | Récupéré après le consentement de l’utilisateur.<br/>Ex. `ZS5454hkfa47w7wkAwqQ9GrtUWwooL`. |
| `client_id` | Identifiant de votre application.<br/>Ex. `ae632d42-91b8-4ce9-b0d4-8438ecd014a1`. |
| `client_secret` | Authentifie l’application, secret envoyé lors de l’enregistrement de votre application.<br/>Ex. `d7ee309e-8ae2-429c-96d0-d7ab99800a22`. |
| `redirect_uri` | Adresse de rediretion configurée pour votre application.<br/>Ex. `https://votre-app.fr/dataconnect/redirect`. |

```json
{
    "access_token": "7tT7xon48xnhxSWnBX5FzuoiEUWm2hApyf1lmqeDlHyU2oqcCv84xf",
    "token_type": "Bearer",
    "expires_in": 12600,
    "refresh_token": "2r9UcExfnH9WAnl6sM4T2rxYrYOW2sKjPcx8uWnrcgXvU3",
    "scope": "/v3/metering_data/daily_consumption.GET /v3/metering_data/consumption_load_curve.GET /v3/metering_data/consumption_max_power.GET",
    "refresh_token_issued_at": "1579681026182",
    "issued_at": "1579681026182"
}
```

### Les fois suivantes

Un `access_token` expiré sera renouvelé grâce au `refresh_token` :

```
curl -d "grant_type=refresh_token&client_id=ae632d42-91b8-4ce9-b0d4-8438ecd014a1&client_secret=d7ee309e-8ae2-429c-96d0-d7ab99800a22&refresh_token=2r9UcExfnH9WAnl6sM4T2rxYrYOW2sKjPcx8uWnrcgXvU3" -X POST "https://gw.prd.api.enedis.fr/v1/oauth2/token?redirect_uri=https%3A%2F%2Fvotre-app.fr%2Fdataconnect%2Fredirect"
```

## Accès aux données

### Courbe de charge

- Puissances moyennes de consommation sur des tranches de 30 minutes
- 7 jours consécutifs au maximum
- La valeur portant le numéro 1 correspond à la puissance moyenne mesurée entre minuit et minuit trente le premier jour.
- La valeur portant le numéro le plus élevé correspond à la puissance moyenne mesurée entre 23h30.

```
curl -H 'Accept: application/json' -H 'Authorization: Bearer 7tT7xon48xnhxSWnBX5FzuoiEUWm2hApyf1lmqeDlHyU2oqcCv84xf' 'https://gw.prd.api.enedis.fr/v3/metering_data/consumption_load_curve?start=2019-12-01&end=2019-12-05&usage_point_id=22516914714270'
```

| Paramètre | Description |
| --- | --- |
| `start` | Jour de début au format RFC 3339.<br/>Ex. `2019-12-01`. |
| `end` | Jour de fin au format RFC 3339.<br/>Ex. `2019-12-05`. |
| `usage_point_id` | Points de livraison (PRM ou PDL) identifiant le/les compteurs de l’utilisateur (non testé avec plusieurs identifiants).<br/>Ex.  `22516914714270`. |

```json
{
  "usage_point": [
    {
      "meter_reading": {
        "usage_point_id": "22516914714270",
        "start": "2019-12-01",
        "end": "2019-12-05",
        "reading_type": {
          "measurement_kind": "power",
          "interval_length": "1800",
          "unit": "W",
          "aggregate": "average"
        },
        "interval_reading": [
          {"rank": "49", "value": "200" },
          {"rank": "50", "value": "228" },
          …
          {"rank": "191", "value": "6384" },
          { "rank": "192", "value": "3664" }
        ]
      }
    }
  ]
}
```

## Dépannage

- [Description des erreurs](https://datahub-enedis.fr/data-connect/documentation/description-des-erreurs/) sur Enedis DataHub.
- Les problèmes que nous rencontrons sont documentés dans la section [Issues](https://github.com/consometers/data-connect/issues).

## Exemples

- [BeMyHomeSmart](https://github.com/gelleouet/smarthome-application/), par Gregory Elleouet, [utilise l’API](https://github.com/gelleouet/smarthome-application/search?q=DataConnect&unscoped_q=DataConnect) en production.
- [Exemple Python](examples/dataconnect.py), par Gautier Husson, utilisation de l’environnement bac à sable.
