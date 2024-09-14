import logging


def configure_logging(level=logging.INFO):
    """Configure logging
    :param level: Logging level
    """
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s: %(levelname)-7s - %(message)s",
    )
    return


LOGGER = logging.getLogger()
configure_logging()
