"""
This type stub file was generated by pyright.
"""

"""AMQPStorm Exception."""
AMQP_ERROR_MAPPING = ...

class AMQPError(IOError):
    """General AMQP Error.

    Exceptions raised by AMQPStorm are mapped based to the
    AMQP 0.9.1 specifications (when applicable).

    e.g.
    ::

        except AMQPChannelError as why:
            if why.error_code == 312:
                self.channel.queue.declare(queue_name)
    """

    _documentation = ...
    _error_code = ...
    _error_type = ...
    @property
    def documentation(self):  # -> str | bytes:
        """AMQP Documentation string."""
        ...
    @property
    def error_code(self):  # -> None:
        """AMQP Error Code - A 3-digit reply code."""
        ...
    @property
    def error_type(self):  # -> str | None:
        """AMQP Error Type e.g. NOT-FOUND."""
        ...
    def __init__(self, *args, **kwargs) -> None: ...

class AMQPConnectionError(AMQPError):
    """AMQP Connection Error."""

    ...

class AMQPChannelError(AMQPError):
    """AMQP Channel Error."""

    ...

class AMQPMessageError(AMQPChannelError):
    """AMQP Message Error."""

    ...

class AMQPInvalidArgument(AMQPError):
    """AMQP Argument Error."""

    ...
