""""
CH4ESE - Conversion Helper 4 Easy Serialization of EXI
Copyright 2024, Battelle Energy Alliance, LLC
"""

import logging

logger = None


def create_logger(verbose):
    """creates a global logger and sets the mode based on the verbose flag"""
    global logger
    logger = logging.getLogger("CH4ESE Logger")
    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    logger.info("CH4ESE Logger Created")
