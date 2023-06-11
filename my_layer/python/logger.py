""" Logging init to be shared across the different functions """
import logging


if logging.getLogger().hasHandlers():
    # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logger = logging.getLogger().setLevel(logging.INFO)
else:
    logger = logging.basicConfig(level=logging.INFO)