"""
This module is a Flask app that serves the EgaPro data, via a JSON API and JSON-RPC.
It reads the data from a CSV file, and serves it as a JSON object.
"""

from csv import DictReader
from flask import Flask, jsonify
from flask_jsonrpc import JSONRPC

# Read the index-egalite-fh.csv file and store it in a dictionary

egapro_data = {}

with open("index-egalite-fh-utf8.csv", encoding='utf-8') as csv_file:
    reader = DictReader(csv_file, delimiter=";", quotechar='"')
    for row in reader:
        siren = row.get("SIREN")
        annee = row.get("Année")
        if siren and annee:
            if egapro_data.get(siren) is None:
                egapro_data[siren] = row
            elif egapro_data[siren]["Année"] < annee:
                egapro_data[siren].update(row)

application = Flask(__name__)
jsonrpc = JSONRPC(application, '/api')

# Define the SIREN route taking a SIREN as a parameter and returning the
# corresponding data from the egapro_data dictionary
@application.route("/siren/<siren>")
def siren(siren: str):  # Changed to str to handle SIREN correctly
    """
    Return the EgaPro data for a given SIREN number.
    A 404 is return if the SIREN is not found.

    :param siren: SIREN number as string
    :return: The corresponding data as a JSON
    """
    response = egapro_data.get(siren)

    if response is None:
        response = {"error": "SIREN not found"}
        status = 404
    else:
        status = 200
    return jsonify(response), status

@jsonrpc.method('api.get_siren')
def get_siren_rpc(siren: str) -> dict:
    """
    Return the EgaPro data for a given SIREN number via RPC.
    A 404 is return if the SIREN is not found.

    :param siren: SIREN number as string
    :return: The corresponding data as a JSON
    """
    response = egapro_data.get(siren)

    if response is None:
        response = {"error": "SIREN not found"}
    return response

# A debug flask launcher
if __name__ == "__main__":
    application.run(debug=True)
