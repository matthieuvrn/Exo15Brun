from csv import DictReader
from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable
from spyne.protocol.json import JsonDocument
from spyne.protocol.http import HttpRpc
from spyne.server.wsgi import WsgiApplication

# Lecture du fichier index-egalite-fh.csv et stockage dans un dictionnaire
egapro_data = {}

with open("index-egalite-fh-utf8.csv", encoding="utf-8") as csv_file:
    reader = DictReader(csv_file, delimiter=";", quotechar='"')
    for row in reader:
        if egapro_data.get(row["SIREN"]) is None:
            egapro_data[row["SIREN"]] = row
        elif egapro_data[row["SIREN"]]["Année"] < row["Année"]:
            egapro_data[row["SIREN"]].update(row)


class EgaProService(ServiceBase):
    @rpc(Integer, _returns=Unicode)
    def get_data(ctx, siren):
        """
        Retourne les données EgaPro pour un numéro SIREN donné.
        Un message d'erreur est retourné si le SIREN n'est pas trouvé.

        :param siren: numéro SIREN en entier
        :return: Les données correspondantes sous forme de chaîne JSON
        """
        response = egapro_data.get(str(siren))

        if response is None:
            return '{"error": "SIREN not found"}'
        else:
            return str(response)


application = Application([EgaProService],
                          tns='spyne.examples.egapro',
                          in_protocol=HttpRpc(validator='soft'),
                          out_protocol=JsonDocument())

wsgi_application = WsgiApplication(application)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    server = make_server('127.0.0.1', 8001, wsgi_application)
    print("En écoute sur le port 8000...")
    server.serve_forever()