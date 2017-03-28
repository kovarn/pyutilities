import logging
import multiprocessing
import sys
import threading
import traceback


# author zzzeek: http://stackoverflow.com/a/894284/7070842
class MultiProcessingLog(logging.Handler):
    """
    A wrapper around a base handler (FileHandler or RotatingFileHandler)
    that receives log records only in the parent process (where the instance
    is created). This solves the problem of writing to a single log file
    from multiple processes.
    """

    def __init__(self, base_handler: logging.Handler):
        super().__init__()

        self._handler = base_handler
        self.queue = multiprocessing.Queue(-1)

        t = threading.Thread(target=self.receive)
        t.daemon = True
        t.start()

    def setFormatter(self, fmt):
        super().setFormatter(fmt)
        self._handler.setFormatter(fmt)

    def receive(self):
        while True:
            # noinspection PyBroadException
            try:
                record = self.queue.get()
                self._handler.emit(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except:
                traceback.print_exc(file=sys.stderr)

    def send(self, s):
        self.queue.put_nowait(s)

    def _format_record(self, record):
        # ensure that exc_info and args
        # have been stringified.  Removes any chance of
        # unpickleable things inside and possibly reduces
        # message size sent over the pipe
        if record.args:
            record.msg = record.msg % record.args
            record.args = None
        if record.exc_info:
            dummy = self.format(record)
            record.exc_info = None

        return record

    def emit(self, record):
        # noinspection PyBroadException
        try:
            s = self._format_record(record)
            self.send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        self._handler.close()
        super().close()
