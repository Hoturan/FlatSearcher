""" Logging init to be shared across the different functions """
import logging


if logging.getLogger().hasHandlers():
    # The Lambda environment pre-configures a handler logging to stderr.
    # If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    LOGGER = logging.getLogger().setLevel(logging.INFO)
else:
    LOGGER = logging.basicConfig(level=logging.INFO)
