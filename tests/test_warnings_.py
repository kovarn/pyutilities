import logging
import warnings
from io import StringIO

import pytest as pytest

from utils import warnings_


@pytest.fixture
def logger():
    logger = logging.getLogger(__name__)

    stream = StringIO()

    ch = logging.StreamHandler(stream)
    ch.setLevel(logging.DEBUG)
    ch_formatter = logging.Formatter('%(name)s: %(levelname)s | %(message)s')
    ch.setFormatter(ch_formatter)
    logger.addHandler(ch)
    yield logger
    logger.removeHandler(ch)


@pytest.mark.usefixtures('logger')
class TestWarningsLog:
    def test_set_warnings_handlers_from(self, logger: logging.Logger):
        warnings_.set_warnings_handlers_from(logger)

        wlogger = logging.getLogger("py.warnings")
        # print(wlogger.handlers)
        assert wlogger.handlers
        assert len(wlogger.handlers) == len(logger.handlers)

        logging.captureWarnings(True)
        warnings.warn("Testing warnings")
        logging.captureWarnings(False)

        stream_value = logger.handlers[0].stream.getvalue()
        # print(stream_value)
        assert stream_value.startswith('py.warnings: WARNING |')

    def test_warnings_to_log_without_categories(self, logger: logging.Logger):
        warnings_.set_warnings_handlers_from(logger)

        with warnings_.warnings_to_log():
            warnings.warn("This should be logged as WARNING")
        stream_value = logger.handlers[0].stream.getvalue()
        print(stream_value)
        assert stream_value.startswith('py.warnings: WARNING |')

    def test_warnings_to_log_match_category_action_debug(self, logger: logging.Logger):
        warnings_.set_warnings_handlers_from(logger)

        with warnings_.warnings_to_log(UserWarning, action='debug'):
            warnings.warn("This should be logged as DEBUG")
        stream_value = logger.handlers[0].stream.getvalue()
        print(stream_value)
        assert stream_value.startswith('py.warnings: DEBUG |')

    def test_warnings_to_log_not_match_category_action_debug(self, logger: logging.Logger):
        warnings_.set_warnings_handlers_from(logger)
        with warnings_.warnings_to_log(DeprecationWarning, action='debug'):
            warnings.warn("This should be logged as Warning")
        stream_value = logger.handlers[0].stream.getvalue()
        print(stream_value)
        assert stream_value.startswith('py.warnings: WARNING |')

    def test_warnings_to_log_match_category_subclass_action_debug(self, logger: logging.Logger):
        warnings_.set_warnings_handlers_from(logger)

        with warnings_.warnings_to_log(Warning, action='debug'):
            warnings.warn("This should be logged as DEBUG")
        stream_value = logger.handlers[0].stream.getvalue()
        print(stream_value)
        assert stream_value.startswith('py.warnings: DEBUG |')

    def test_warnings_to_log_match_category_multiple_action_debug(self, logger: logging.Logger):
        warnings_.set_warnings_handlers_from(logger)

        with warnings_.warnings_to_log(DeprecationWarning, UserWarning, action='debug'):
            warnings.warn("This should be logged as DEBUG")
        stream_value = logger.handlers[0].stream.getvalue()
        print(stream_value)
        assert stream_value.startswith('py.warnings: DEBUG |')

    def test_warnings_to_log_match_msg_action_debug(self, logger: logging.Logger):
        warnings_.set_warnings_handlers_from(logger)
        with warnings_.warnings_to_log("should match", action='debug'):
            warnings.warn("This should match")
        stream_value = logger.handlers[0].stream.getvalue()
        print(stream_value)
        assert stream_value.startswith('py.warnings: DEBUG |')

    def test_warnings_to_log_not_match_msg_action_debug(self, logger: logging.Logger):
        warnings_.set_warnings_handlers_from(logger)
        with warnings_.warnings_to_log("should match", action='debug'):
            warnings.warn("This doesn't match")
        stream_value = logger.handlers[0].stream.getvalue()
        print(stream_value)
        assert stream_value.startswith('py.warnings: WARNING |')

    def test_warnings_to_log_match_category_action_ignore(self, logger: logging.Logger):
        warnings_.set_warnings_handlers_from(logger)

        with warnings_.warnings_to_log(UserWarning, action='ignore'):
            warnings.warn("This should be ignored")
        stream_value = logger.handlers[0].stream.getvalue()
        print(stream_value)
        assert stream_value == ''

    def test_warnings_to_log_not_match_category_action_ignore(self, logger: logging.Logger):
        warnings_.set_warnings_handlers_from(logger)
        with warnings_.warnings_to_log(DeprecationWarning, action='ignore'):
            warnings.warn("This should be logged as Warning")
        stream_value = logger.handlers[0].stream.getvalue()
        print(stream_value)
        assert stream_value.startswith('py.warnings: WARNING |')

    def test_warnings_to_log_match_msg_action_ignore(self, logger: logging.Logger):
        warnings_.set_warnings_handlers_from(logger)
        with warnings_.warnings_to_log("should match", action='ignore'):
            warnings.warn("This should match and be ignored")
        stream_value = logger.handlers[0].stream.getvalue()
        print(stream_value)
        assert stream_value == ''

    def test_warnings_to_log_not_match_msg_action_ignore(self, logger: logging.Logger):
        warnings_.set_warnings_handlers_from(logger)
        with warnings_.warnings_to_log("should match", action='ignore'):
            warnings.warn("This doesn't match")
        stream_value = logger.handlers[0].stream.getvalue()
        print(stream_value)
        assert stream_value.startswith('py.warnings: WARNING |')
