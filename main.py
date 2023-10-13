import logging
import logging.config
import os.path
import sys

import uvicorn

if not os.path.isfile(sys.argv[2]):
    print('Logging config file not found')
    raise FileNotFoundError('Logging config file not found')
logging.config.fileConfig(sys.argv[2], disable_existing_loggers=False)

from src.server.server import Server
from src.utils.config_provider import config_provider


class Main:
    def __init__(self):
        self.logger = logging.getLogger("Main")
        self.logger.info("Starting app...")
        self.server = Server()
        self.server.prepare_routers()
        self.logger.info("Initialized Server")
        app = self.server.app
        app.add_event_handler("shutdown", self.shutdown_handler)
        self.logger.info("App started!")

    def shutdown_handler(self):
        self.logger.info("Stopping app...")


if __name__ == "__main__":
    host = config_provider.get_config_value("server", "host")
    port = int(config_provider.get_config_value("server", "port"))
    main = Main()
    uvicorn.run(main.server.app, host=host, port=port, lifespan="on", log_config=None)
