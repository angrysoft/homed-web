"""
This type stub file was generated by pyright.
"""

from amqpstorm.connection import Connection

"""AMQPStorm Uri wrapper for Connection."""
LOGGER = ...

class UriConnection(Connection):
    """RabbitMQ Connection that takes a Uri string.

    e.g.
    ::

        import amqpstorm
        connection = amqpstorm.UriConnection(
            'amqp://guest:guest@localhost:5672/%2F?heartbeat=60'
        )

    Using a SSL Context:
    ::

        import ssl
        import amqpstorm
        ssl_options = {
            'context': ssl.create_default_context(cafile='ca_certificate.pem'),
            'server_hostname': 'rmq.eandersson.net'
        }
        connection = amqpstorm.UriConnection(
            'amqps://guest:guest@rmq.eandersson.net:5671/%2F?heartbeat=60',
            ssl_options=ssl_options
        )

    :param str uri: AMQP Connection string
    :param dict ssl_options: SSL kwargs
    :param dict client_properties: None or dict of client properties
    :param bool lazy: Lazy initialize the connection

    :raises TypeError: Raises on invalid uri.
    :raises ValueError: Raises on invalid uri.
    :raises AttributeError: Raises on invalid uri.
    :raises AMQPConnectionError: Raises if the connection
                                 encountered an error.
    """

    __slots__ = ...
    def __init__(
        self, uri, ssl_options=..., client_properties=..., lazy=...
    ) -> None: ...
