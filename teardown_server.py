""" """

import time

import Pyro5.api as pyro
from qcore import logger, Server

if __name__ == "__main__":
    with pyro.Proxy(Server.URI) as server:
        logger.info("Tearing down the remote Server from an external script...")
        server.teardown()
    time.sleep(1)
    logger.info("Remote Server has been torn down by an external script!")
