import pytest
import requests
import os
from util4tests import run_single_test, log
from yaml4parms import read


def _testfile_path(*relative):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *relative)


def _wget(url, fname):
    r = requests.get(url)
    open(fname, 'wb').write(r.content)


@pytest.fixture
def pema_params():
    src = "https://raw.githubusercontent.com/marc-portier/pema/ARMS/analysis_directory/parameters_structured.tsv"
    tgt = _testfile_path('tmp', 'pema', 'parameters.tsv')
    os.makedirs(os.path.dirname(tgt), exist_ok=True)
    try:
        _wget(src, tgt)
    except requests.exceptions.ConnectionError:
        pass
    return tgt


@pytest.fixture
def local_test():
     return _testfile_path('in', 'local.txt')


def test_local(local_test):
    log.debug(f"now testing input from {local_test}")
    parms = read(local_test)
    assert parms is not None, 'reading the local file should not fail'
    assert {'text', 'count', 'measurement'}.issubset(set(parms)), "we expect a crucial set of params to be defined"
    assert parms['text']['title'] is not None, "parameter 'text' should have a 'title'"

    assert parms.as_json() is not None 
    assert parms.as_html() is not None


def test_pema_params(pema_params):
    log.debug(f"testing input from {pema_params}")
    parms = read(pema_params)
    assert parms is not None, 'reading the local file should not fail'


if __name__ == "__main__":
    run_single_test(__file__)
