import logging as lg


lg.basicConfig(filemode='w+', filename='GameTweak.log', format='%(levelname)s | %(message)s')

def error(msg: str) -> None:
    lg.error(msg)

def info(msg: str) -> None:
    lg.info(msg)

def debug(msg: str) -> None:
    lg.debug(msg)

def warning(msg: str) -> None:
    lg.warning(msg)