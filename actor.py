import logging
import block
import blockchain


class Actor:
    
    actorCount = 0
    
    def __init__(self,name):
        self.name = name
        # actorCount = actorCount + 1
        return

def test():

    LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}

    # if len(sys.argv) > 1:
    # level_name = sys.argv[1]
    level_name = 'operations'
    level = LEVELS.get(level_name, logging.NOTSET)
    logging.basicConfig(level=level)
    print 'Start operations log file'
    print (logging.getLoggerClass().root.handlers[0].baseFilename)

    LOG_FILENAME = 'example.log'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
    logging.debug('This message should go to the log file')

    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical error message')

    chain = blockchain.Blockchain()
    logging.info('Blockchain initialized')
    
    white = Actor('White')
    logging.info('White Actor Created')
    
    
    red = Actor('Red')
    logging.info('Red Actor Created')

    blue = []
    blue_strategic = Actor('Blue/Strategic' )
    blue.append(blue_strategic)
    blue_operational = Actor('Blue/Operational')
    blue.append(blue_operational)
    blue_tactical = Actor('Blue/Tactical')
    blue.append(blue_tactical)
    logging.info('Blue Strategic, Operational and Tactical Actors Created')

    return 1

test()

