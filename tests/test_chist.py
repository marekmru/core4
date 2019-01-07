import datetime
import logging
import os

import pytest

import core4.logger.mixin
import core4.script.chist
import core4.service.setup
import core4.util.tool

ASSET_FOLDER = 'asset'
MONGO_URL = 'mongodb://core:654321@localhost:27017'
MONGO_DATABASE = 'core4test'


def asset(*filename, exists=True):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, ASSET_FOLDER, *filename)
    if not exists or os.path.exists(filename):
        return filename
    raise FileNotFoundError(filename)


@pytest.fixture(autouse=True)
def reset(tmpdir):
    logging.shutdown()
    # logging mixin (setup complete)
    core4.logger.mixin.CoreLoggerMixin.completed = False
    # setup
    os.environ["CORE4_CONFIG"] = asset("config/empty.yaml")
    os.environ["CORE4_OPTION_folder__root"] = str(tmpdir)
    core4.logger.mixin.logon()
    yield
    # run @once methods
    for i, j in core4.service.setup.CoreSetup.__dict__.items():
        if callable(j):
            if "has_run" in j.__dict__:
                j.has_run = False
    # singletons
    core4.util.tool.Singleton._instances = {}
    # os environment
    dels = []
    for k in os.environ:
        if k.startswith('CORE4_'):
            dels.append(k)
    for k in dels:
        del os.environ[k]


def test_parse_datetime():
    assert (core4.script.chist.parse_range("2018-01-31 12:34:56")
            == datetime.datetime(2018, 1, 31, 11, 34, 56))
    assert (core4.script.chist.parse_range("2018-01-31 12:34")
            == datetime.datetime(2018, 1, 31, 11, 34, 0))
    assert (core4.script.chist.parse_range("2018-01-31T12:34")
            == datetime.datetime(2018, 1, 31, 11, 34, 0))
    assert (core4.script.chist.parse_range("2018-01-31 12")
            == datetime.datetime(2018, 1, 31, 11, 0, 0))
    assert (core4.script.chist.parse_range("2018-01-31")
            == datetime.datetime(2018, 1, 31))
    assert (core4.script.chist.parse_range("2018 01 31")
            == datetime.datetime(2018, 1, 31))
    assert (core4.script.chist.parse_range("2018/01/31")
            == datetime.datetime(2018, 1, 31))


def test_parse_time():
    assert (core4.script.chist.parse_time(
        "12:33:44", now=datetime.datetime(2018, 1, 31, 13, 00))
            == datetime.datetime(2018, 1, 31, 11, 33, 44))
    assert (core4.script.chist.parse_time(
        "12:33:44", now=datetime.datetime(2018, 1, 31, 12, 00))
            == datetime.datetime(2018, 1, 30, 11, 33, 44))

def test_parse_delta():
    assert (core4.script.chist.parse_delta(
        "1h", now=datetime.datetime(2018, 12, 31, 0, 30))
            == datetime.datetime(2018, 12, 30, 22, 30))
    assert (core4.script.chist.parse_delta(
        "1d", now=datetime.datetime(2018, 12, 31, 0, 30))
            == datetime.datetime(2018, 12, 29, 23, 30))
    assert (core4.script.chist.parse_delta(
        "2w", now=datetime.datetime(2018, 12, 31, 0, 30))
            == datetime.datetime(2018, 12, 16, 23, 30))
    assert (core4.script.chist.parse_delta(
        "1m", now=datetime.datetime(2018, 12, 31, 0, 30))
            == datetime.datetime(2018, 11, 30, 23, 30))

