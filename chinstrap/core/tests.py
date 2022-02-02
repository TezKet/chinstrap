import io
import os
import sys
import glob
import pytest
from pytezos import ContractInterface
from chinstrap.core import ligo, smartpy
from chinstrap.Helpers import ensureCurrentDirectoryIsChinstrapProject


class Tests:
    def __init__(self, args, config, chinstrapPath) -> None:
        self.config = config
        ensureCurrentDirectoryIsChinstrapProject()

        if config.compiler.lang == "smartpy":
            self.compile = smartpy.SmartPy(args, config, chinstrapPath)

        elif "ligo" in config.compiler.lang:
            self.compile = ligo.Ligo(args, config, chinstrapPath)

    def runAllTests(self):
        return self.compile.runAllTests()

    def runTest(self, test):
        if self.config.compiler.test == "pytest":
            return runSinglePyTest(test)

        return self.compile.runSingleTest(test)


def runPyTests():
    tests = glob.iglob("./tests/*.py")
    for test in tests:
        runSinglePyTest(test)


def runSinglePyTest(file):
    stdoutOrig = sys.stdout
    stdoutTemp = io.StringIO()
    sys.stdout = stdoutTemp

    res = pytest.main(["--co", "-x", "-q", f"{file}"])
    sys.stdout = stdoutOrig
    if "no tests collected" in stdoutTemp.getvalue():
        return 0

    else:
        msg = f"Running tests on <ansigreen>{file}</ansigreen>"
        print(msg)
        res = pytest.main(["--no-header", f"{file}"])
        if res.value:
            return 1

    return 0


def getContractInterface(contractName):
    # get contract interface.
    if os.path.exists(
        f"./build/contracts/{contractName.lower()}/step_000_cont_0_contract.tz"
    ):
        return ContractInterface.from_file(
            f"./build/contracts/{contractName.lower()}/step_000_cont_0_contract.tz"
        )

    # try to build if doesn't exist
    else:
        raise BaseException("Please compile the contracts")
