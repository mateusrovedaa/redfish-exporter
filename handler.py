"""
This module contains the handler classes for the Falcon web server.
"""

import logging
import os
import traceback

import falcon
from prometheus_client.exposition import CONTENT_TYPE_LATEST
from prometheus_client.exposition import generate_latest

from collector import RedfishMetricsCollector


class WelcomePage:
    """
    Create the Welcome page for the API.
    """

    def on_get(self, req, resp):
        """
        Define the GET method for the API.
        """

        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.text = """
        <h1>Redfish Exporter</h1>
        <h2>Prometheus Exporter for redfish API based servers monitoring</h2>
        <ul>
            <li>Use <a href="/redfish">/redfish</a> to retrieve health metrics.</li>
            <li>Use <a href="/firmware">/firmware</a> to retrieve firmware version metrics.</li>
        </ul>
        """

class MetricsHandler:
    """
    Metrics Handler for the Falcon API.
    """

    def __init__(self, config, metrics_type):
        self._config = config
        self.metrics_type = metrics_type

    def on_get(self, req, resp):
        """
        Define the GET method for the API.
        """
        target = req.get_param("target")
        if not target:
            logging.error("No target parameter provided!")
            raise falcon.HTTPMissingParam("target")

        resp.set_header("Content-Type", CONTENT_TYPE_LATEST)

        host = target

        usr = self._config.get("username")
        pwd = self._config.get("password")

        if not usr or not pwd:
            msg = (
                f"Target {target}: "
                f"no user/password found in environment"
            )
            logging.error(msg)
            raise falcon.HTTPInvalidParam(msg, "")

        logging.debug("Target %s: Using user %s", target, usr)

        with RedfishMetricsCollector(
            self._config,
            target=target,
            host=host,
            usr=usr,
            pwd=pwd,
            metrics_type=self.metrics_type
        ) as registry:

            # open a session with the remote board
            registry.get_session()

            try:
                # collect the actual metrics
                resp.text = generate_latest(registry)
                resp.status = falcon.HTTP_200

            except Exception as err:
                message = f"Exception: {traceback.format_exc()}"
                logging.error("Target %s: %s", target, message)
                raise falcon.HTTPBadRequest(description=message)
