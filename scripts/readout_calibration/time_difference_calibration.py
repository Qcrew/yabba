""" """

from qcore import Stage
from qcore.instruments import QM
from qcore.scripts.time_difference_calibration import TimeDiffCalibrator

from config.experiment_config import MODES_CONFIG


if __name__ == "__main__":

    with Stage(configpath=MODES_CONFIG, remote=True) as stage:

        rr, qubit = stage.get("rr", "qubit")
        lo_rr, lo_qubit = stage.get(rr.lo_name, qubit.lo_name)

        qm = QM(modes=(rr, qubit), oscillators=(lo_rr, lo_qubit))
        old_config = qm.get_config()

        timediff = TimeDiffCalibrator(qm._qmm, old_config, rr.name, reps=1)
        timediff.calibrate(simulate=False)
