""" Readout integration weights training for single-shot readout """

from qcore import Stage
from qcore.instruments import QM
from qcore.scripts.readout_training import ReadoutTrainer

from config.experiment_config import MODES_CONFIG

if __name__ == "__main__":
    """ """

    with Stage(configpath=MODES_CONFIG, remote=True) as stage:

        rr, qubit = stage.get("rr", "qubit")
        lo_rr, lo_qubit = stage.get("lo_rr", "lo_qubit")

        qm = QM(modes=(rr, qubit), oscillators=(lo_rr, lo_qubit))
        params = {
            "reps": 1000,
            "wait_time": 20000,  # ns
            "readout_pulse": "rr_readout_pulse",  # pulse name used to readout
            "qubit_pi_pulse": "qubit_constant_pi_pulse",  # pulse name used to excite qubit
        }

        ro_trainer = ReadoutTrainer(rr, qubit, qm, **params)
        threshold, data = ro_trainer.calculate_threshold()
