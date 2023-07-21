""" 
NOTE this script must be on the same folder level as a yml config file named 'instruments.yml' and the .bat scripts 'setup_stage.bat' and 'teardown_stage.bat' in order for the remote stage to be setup, served, and torn down successfully
"""


from pathlib import Path

from qcore import Server

if __name__ == "__main__":
    """
    Initialize a Server with a yml config file specifying Instruments to be served remotely. This initialization is a blocking call which serves the Instruments on a remote stage until the stage is torn down.
    """

    instruments_config = Path(__file__).resolve().parent / "config/instruments.yml"
    server = Server(instruments_config)
    server.serve()
