import asyncio

import bleak
from jsonrpc import JSONRPCResponseManager, dispatcher
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

# The event loop is needed to run the coroutine
loop = asyncio.get_event_loop()

# The scanner object is used to discover BLE devices
scanner = bleak.BleakScanner()


@Request.application
def application(request):
    """
    The Werkzeug HTTP server will call this function whenever a request is
    received. The request is a JSON-RPC request, which is parsed and
    dispatched to the appropriate method.

       :param request: The HTTP request object
       :return: A JSON response
    """

    # Functions that can be called by JSON RPC requests
    def get_executed_coroutine_discover():
        """
        BleakScanner.discover() is a coroutine, so we need to run it in an event
        loop.

           :return: The only result of the coroutine, a list of BLEDevice
              objects address as strings.
        """
        result = loop.run_until_complete(asyncio.gather(scanner.discover()))[0]
        # turn all BLEDevice objects into dictionaries
        return [device.address for device in result]

    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["scan"] = get_executed_coroutine_discover

    # JSON RPC 2.0 handler
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype="application/json")


if __name__ == "__main__":
    run_simple("localhost", 4000, application)
