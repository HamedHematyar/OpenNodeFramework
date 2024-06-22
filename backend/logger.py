import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(name)s %(module)s:%(funcName)s:%(lineno)d %(message)s",
)

logger = logging.getLogger(__name__)
