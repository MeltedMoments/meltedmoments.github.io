# logger.py
import logging

# Add an extra logging level, VERBOSE
# Ref: https://www.programcreek.com/python/?project_name=dwavesystems%2Fdwave-hybrid
def _add_logger_level(levelname:str, level:int, *, func_name=None):
    """
    Adds a custom logging level to the standard library logging module.

    Args:
        levelname (str): Name of the new level (e.g., 'VERBOSE').
        level (int): Numeric value of the level (e.g., 5).
        func_name (str, optional): Function name to call the logger (defaults to levelname.lower()).
    """
    func_name = func_name or levelname.lower()

    setattr(logging, levelname, level)
    logging.addLevelName(level, levelname)

    def log_for_level(self, message, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)

    setattr(logging.Logger, func_name, log_for_level)

_add_logger_level("VERBOSE", 5)

log = logging.getLogger(__name__)

# Set up default logging configuration, by checking *this* module's logger
if not log.hasHandlers():       
    logging.basicConfig(
        level = logging.DEBUG,
        format = "%(asctime)s [%(levelname).4s] %(message)s"
    )


def reconfigure_logging(loglevel=logging.INFO, logfile=None, format=None):
    """
    Reconfigure the logger at runtime. Call this function to change the default logging.

    Args:
        loglevel (int): The logging level to set (e.g., logging.DEBUG, logging.INFO).
        logfile (str): The file to log to. If None, logs to stdout.
        format (str): The format of the log messages.

    """
    format = format or "%(asctime)s [%(levelname).4s] %(message)s"

    # Remove old handlers from the root logger
    log = logging.getLogger()
    for handler in log.handlers[:]:
        log.removeHandler(handler)

    # New handler
    if logfile:
        handler = logging.FileHandler(logfile)
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(logging.Formatter(format))
    log.addHandler(handler)
    log.setLevel(loglevel)



# # Define this stuff first, then the logger can be used in the rest of the file
# """
#     Add an extra logging level, VERBOSE
#     Ref: https://www.programcreek.com/python/?project_name=dwavesystems%2Fdwave-hybrid
# """

# _func_prototype = "def {logger_func_name}(self, message, *args, **kwargs):\n" \
#                   "    if self.isEnabledFor({levelname}):\n" \
#                   "        self._log({levelname}, message, args, **kwargs)"
# def _add_logger_level(levelname, level, *, func_name = None):
#     """
#     :type levelname: str
#         The reference name of the level, e.g. DEBUG, WARNING, etc
#     :type level: int
#         Numeric logging level
#     :type func_name: str
#         The name of the logger function to log to a level, e.g. "info" for log.info(...)
#     """
#     func_name = func_name or levelname.lower()

#     setattr(logging, levelname, level)
#     logging.addLevelName(level, levelname)

#     exec(_func_prototype.format(logger_func_name=func_name, levelname=levelname), logging.__dict__, locals())
#     setattr(logging.Logger, func_name, eval(func_name))

# _add_logger_level("VERBOSE", 5)

# log = logging.getLogger(__name__)
