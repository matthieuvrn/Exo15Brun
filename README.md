# EgaPro Data Distribution Services
Ce projet fournit des services de distribution de données pour l'Index EgaPro. Il inclut des API pour la distribution via JSON-RPC, REST et SOAP.

## Description
Ce projet a été développé dans le cadre d'un cours pour créer une architecture de services distribuant les données de l'Index EgaPro. Le projet est structuré pour fournir les données via trois types de services :

RPC (Remote Procedure Call)
API REST (Representational State Transfer)
API SOAP (Simple Object Access Protocol)
Chaque étudiant a été responsable du développement d'un de ces services, et l'architecture a été documentée de manière exhaustive.

## Diagramme de Séquence
Le diagramme de séquence suivant illustre l'interaction entre les différentes composantes de notre architecture de services.
![diagram_sequence](https://github.com/matthieuvrn/Exo15Brun/assets/148461115/bde9d474-0fc1-43e8-80a1-c8efbe1a7a77)

## API REST (documentation)
L'API REST permet d'accéder aux données de l'Index EgaPro via des appels HTTP. Les données sont retournées au format JSON.

Exemple de requete : 127.0.0.1:5000/apidocs

![image](https://github.com/matthieuvrn/Exo15Brun/assets/148461115/e1fe0539-12a8-4040-9a17-5266615dfa7e)

![image](https://github.com/matthieuvrn/Exo15Brun/assets/148461115/ae0031ca-c44d-4394-b042-89272ca7c01c)

![image](https://github.com/matthieuvrn/Exo15Brun/assets/148461115/16879022-793d-42fa-80a4-44fefd8e3fd6)

## API SOAP (documentation)
L'API SOAP permet d'accéder aux données via des messages XML envoyés sur HTTP.

Exemple de requete : 127.0.0.1:8000/?wsdl

![image](https://github.com/matthieuvrn/Exo15Brun/assets/148461115/aab4af0f-172c-4f7e-b5aa-167ff3b38ce7)

## API RPC
L'API RPC permet d'appeler des fonctions distantes pour obtenir les données de l'Index EgaPro.

Exemple de requete : http://127.0.0.1:5000/siren/423492792

![image](https://github.com/matthieuvrn/Exo15Brun/assets/148461115/19dc2e40-5850-4eff-9674-ec217b12a3fe)

