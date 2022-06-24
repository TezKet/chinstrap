from logging import StreamHandler
import os
import pytezos
from mnemonic import Mnemonic
from chinstrap import helpers


class InitChinstrap:
    def __init__(self, chinstrapPath, name, path, force, with_samples, create_account) -> None:
        self.name = name
        self.path = path
        self.chinstrapPath = chinstrapPath

        if not helpers.isChinstrapProject(path):
            with open(f"{path}/.chinstrap", "a"):
                os.utime(f"{path}/.chinstrap", None)

        if helpers.checkToCreateDir(f"{path}/contracts", force):
            self.initContracts()

        if helpers.checkToCreateDir(f"{path}/originations", force):
            self.initOriginations()

        if helpers.checkToCreateDir(f"{path}/tests", force):
            self.initTests()

        if helpers.checkToCreateFile(f"{path}/chinstrap-config.yml", force):
            self.initConfig()

        if with_samples:
            helpers.copyFile(
                f"{self.chinstrapPath}/core/sources/contracts/SampleContract.py",
                f"{self.path}/contracts/SampleContract.py",
            )
        
            helpers.copyFile(
                f"{self.chinstrapPath}/core/sources/originations/1_samplecontract_origination.py",
                f"{self.path}/originations/1_samplecontract_origination.py",
            )  

            helpers.copyFile(
                f"{self.chinstrapPath}/core/sources/tests/samplecontractPytest.py",
                f"{self.path}/tests/samplecontract.pytest.py",
            )

            helpers.copyFile(
                f"{self.chinstrapPath}/core/sources/tests/sampleContractSmartPy.py",
                f"{self.path}/tests/sampleContract.smartpy.py",
            )

        if create_account:
            self.generateAccount()
            
        msg = "\n<ansigreen>✔</ansigreen> Initialization successful. Happy hacking 🐧"
        helpers.printFormatted(msg)

    def initContracts(self):
        helpers.mkdir(f"{self.path}/contracts")

    def initOriginations(self):
        """
        create origination scripts
        """
        helpers.mkdir(f"{self.path}/originations")

    def initTests(self):
        """
        create pytezos test scripts
        """
        helpers.mkdir(f"{self.path}/tests")

    def initConfig(self):
        config = """chinstrap:
# Networks define how Chinstrap connect to Tezos.
  network:
    development:
      host: http://localhost:20000

      # You need to configure accounts with private key,
      # to sign your transactions before they're sent to a remote public node
      accounts:
        - privateKeyFile: ./.secret

    # hangzhounet:
    #   host: https://hangzhounet.smartpy.io:443
    #   accounts:
    #     - privateKeyFile: ./.secret

    # ithacanet:
    #   host: https://ithacanet.smartpy.io:443
    #   accounts:
    #     - privateKeyFile: ./.secret

    # mainnet:
    #   host: https://mainnet.smartpy.io:443
    #   accounts:
    #     - privateKeyFile: ./.secret

  compiler:
    # Compiler configuration
    # lang: smartpy, cameligo, pascaligo, reasonligo, jsligo
    lang: smartpy

    # test: smartpy, pytest, smartpy, cameligo, pascaligo, reasonligo, jsligo
    test: smartpy
"""
        helpers.copyFile(
            f"{self.chinstrapPath}/core/sources/chinstrap-config.yml",
            f"{self.path}/chinstrap-config.yml",
        )

    def generateAccount(self):
        # default configuration taken from Pytezos
        curve    = b'ed'
        strength = 128
        language = "english"

        mnemonic = Mnemonic(language).generate(strength)
        key = pytezos.Key.from_mnemonic(mnemonic, '', curve=curve)
        esk = key.secret_key(passphrase=''.encode())
    
        with open(f"{self.path}/.secret","w") as f:
            f.write(esk)
        
        with open(f"{self.path}/.mnemonic","w") as f:
            f.write(mnemonic)