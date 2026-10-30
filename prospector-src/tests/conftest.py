import os, shutil, tempfile, pathlib
_TMP = tempfile.mkdtemp(prefix="prospector-test-")
os.environ["PROSPECTOR_HOME"] = _TMP
import pytest

@pytest.fixture(autouse=True)
def clean_home():
    for sub in ("data", "out"):
        shutil.rmtree(pathlib.Path(_TMP) / sub, ignore_errors=True)
    yield
