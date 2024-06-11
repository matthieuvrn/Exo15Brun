import os
from csv import DictReader
from flask import Flask, jsonify, abort
from flasgger import Swagger, swag_from

# Initialiser l'application Flask
application = Flask(__name__)
swagger = Swagger(application)

# Chemin vers le fichier CSV
csv_file_path = os.path.join(os.path.dirname(__file__), "index-egalite-fh-utf8.csv")

# Lire le fichier CSV et stocker les données dans un dictionnaire
egapro_data = {}

if not os.path.exists(csv_file_path):
    print(f"Error: The file {csv_file_path} does not exist.")
    exit(1)

with open(csv_file_path, encoding='utf-8') as csv_file:
    reader = DictReader(csv_file, delimiter=";", quotechar='"')

    for row in reader:
        siren = row.get("SIREN")
        annee = row.get("Année")

        if not siren or not annee:
            continue

        if egapro_data.get(siren) is None:
            egapro_data[siren] = row
        elif egapro_data[siren].get("Année", "") < annee:
            egapro_data[siren].update(row)


@application.route("/siren/<siren>")
@swag_from({
    'parameters': [
        {
            'name': 'siren',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'SIREN number as integer'
        }
    ],
    'responses': {
        200: {
            'description': 'EgaPro data for the given SIREN number',
            'schema': {
                'type': 'object',
                'properties': {
                    'SIREN': {'type': 'string'},
                    'Année': {'type': 'string'},
                    'other_fields': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'SIREN not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def siren(siren: int):
    """
    Retourne les données EgaPro pour un numéro de SIREN donné.
    Une erreur 404 est retournée si le SIREN n'est pas trouvé.
    """
    response = egapro_data.get(siren)

    if response is None:
        response = {"error": "SIREN not found"}
        status = 404
    else:
        status = 200
    return jsonify(response), status


if __name__ == "__main__":
    application.run(debug=True)
