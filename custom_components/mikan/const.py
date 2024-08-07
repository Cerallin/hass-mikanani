import logging
from datetime import timedelta

LOGGER = logging.getLogger(__package__)
DEFAULT_SCAN_INTERVAL = timedelta(hours=1)

DOMAIN = "mikanani"

ATTRIBUTION = "第三方蜜柑计划 ha 集成"

MIKAN_HOST = "https://mikanani.me"
