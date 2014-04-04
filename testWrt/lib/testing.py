
import logging

LOG = logging.getLogger('test')

def assert_stderrlines(streams):
    errlines = None
    if len(streams) == 3:
        errlines = streams[2].readlines()
    else:
        errlines = streams[1]

    if errlines:
        LOG.critical("Stderr output:")
        LOG.critical(errlines)
        assert False

def assert_stdoutlines(streams):
    outlines = None
    if len(streams) == 3:
        outlines = streams[1].readlines()
    else:
        outlines = streams[0]

    if outlines:
        LOG.critical("Stdout output:")
        LOG.critical(outlines)
        assert False
