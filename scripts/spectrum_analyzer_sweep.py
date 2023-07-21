""" """

import matplotlib.pyplot as plt
from qm import qua

from qcore.instruments import QM
from qcore.pulses import ConstantPulse
from qcore import Stage

from config.experiment_config import (
    QUBIT,
    QUBITEF,
    RR,
    CAV,
    LO_RR,
    LO_QUBIT,
    LO_CAV,
    SA,
)


def get_sweep(mode, lo, sa, **kwargs):
    pulse = ConstantPulse("spectrum_analysis_constant_pulse")
    mode.add_operations(pulse)
    qm = QM(modes=(mode,), oscillators=(lo,))
    sa.configure(**kwargs)

    def get_qua_program(mode):
        with qua.program() as play_constant_pulse:
            with qua.infinite_loop_():
                mode.play(pulse, ampx=1.0)
        return play_constant_pulse

    job = qm.execute(get_qua_program(mode))  # play IF to mode
    freqs, amps = sa.sweep()  # get, plot, show sweep
    plt.plot(freqs, amps)
    job.halt()
    plt.show()


if __name__ == "__main__":
    mode = CAV
    mode_lo = LO_CAV

    sweep_parameters = {  # set sweep parameters
        "center": mode_lo.frequency,  # 1e9,
        "span": 400e6,
        "rbw": 250e3,
        "ref_power": 0,
    }
    get_sweep(mode, mode_lo, SA, **sweep_parameters)
