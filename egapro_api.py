from csv import DictReader
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Array, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

# Read the index-egalite-fh.csv file and store it in a dictionary
egapro_data = {}

with open("index-egalite-fh-utf8.csv") as csv_file:
    reader = DictReader(csv_file, delimiter=";", quotechar='"')
    for row in reader:
        if egapro_data.get(row["SIREN"]) is None:
            egapro_data[row["SIREN"]] = row
        elif egapro_data[row["SIREN"]]["Année"] < row["Année"]:
            egapro_data[row["SIREN"]].update(row)


# Define the data model for the response
class EgaProData(ComplexModel):
    SIREN = Unicode
    Année = Unicode
    Index = Unicode
    # Add other fields from the CSV as necessary


class ResponseData(ComplexModel):
    data = EgaProData
    error = Unicode


class EgaProService(ServiceBase):
    @rpc(Integer, _returns=ResponseData)
    def get_data(ctx, siren):
        """
        Return the EgaPro data for a given SIREN number.
        A 404 is returned if the SIREN is not found.

        :param siren: SIREN number as integer
        :return: The corresponding data as a SOAP response
        """
        response = egapro_data.get(str(siren))

        if response is None:
            return ResponseData(error="SIREN not found")
        else:
            data = EgaProData(**response)
            return ResponseData(data=data)


application = Application([EgaProService],
                          'spyne.examples.egapro',
                          in_protocol=Soap11(),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()
