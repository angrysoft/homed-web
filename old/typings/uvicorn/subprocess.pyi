"""
This type stub file was generated by pyright.
"""

import multiprocessing

"""
Some light wrappers around Python's multiprocessing, to deal with cleanly
starting child processes.
"""
spawn = multiprocessing.get_context("spawn")

def get_subprocess(config, target, sockets):
    """
    Called in the parent process, to instantiate a new child process instance.
    The child is not yet started at this point.

    * config - The Uvicorn configuration instance.
    * target - A callable that accepts a list of sockets. In practice this will
               be the `Server.run()` method.
    * sockets - A list of sockets to pass to the server. Sockets are bound once
                by the parent process, and then passed to the child processes.
    """
    ...

def subprocess_started(config, target, sockets, stdin_fileno):
    """
    Called when the child process starts.

    * config - The Uvicorn configuration instance.
    * target - A callable that accepts a list of sockets. In practice this will
               be the `Server.run()` method.
    * sockets - A list of sockets to pass to the server. Sockets are bound once
                by the parent process, and then passed to the child processes.
    * stdin_fileno - The file number of sys.stdin, so that it can be reattached
                     to the child process.
    """
    ...
