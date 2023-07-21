""" Readout integration weights training for single-shot readout """

import datetime
from pathlib import Path

from qcore import Stage
from qcore.instruments import QM
from qcore.scripts.readout_training import ReadoutTrainer

from config.experiment_config import MODES_CONFIG, FOLDER

if __name__ == "__main__":
    """ """

    with Stage(configpath=MODES_CONFIG, remote=True) as stage:

        rr, qubit = stage.get("rr", "qubit")
        lo_rr, lo_qubit = stage.get("lo_rr", "lo_qubit")

        qm = QM(modes=(rr, qubit), oscillators=(lo_rr, lo_qubit))

        # Save file with today's date
        date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_weights.npz")
        file_path = Path(FOLDER) / "config/weights" / date_str

        params = {
            "reps": 1000,
            "wait_time": 20000,  # ns
            "readout_pulse": "rr_readout_pulse",  # pulse name used to readout
            "qubit_pi_pulse": "qubit_constant_pi_pulse",  # pulse name used to excite qubit
            "weights_file_path": file_path,
        }

        ro_trainer = ReadoutTrainer(rr, qubit, qm, **params)
        ro_trainer.train_weights()

        ## Make sure to run this script every time the readout pulse is changed!!
