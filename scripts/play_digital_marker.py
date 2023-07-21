""" test rf switch """

from pathlib import Path
import time

from qcore import Experiment, Stage
from qcore.modes import Qubit, RFSwitch
from qcore.pulses import ConstantPulse, DigitalWaveform
from qcore.instruments import QM
from qcore.libs.qua_macros import wait

from qm import qua


def sequence(mode_, pulse_, lo_):
    """QUA sequence that defines this Experiment subclass"""

    with qua.program() as play_digital_marker:
        with qua.infinite_loop_():
            mode_.play(pulse_)
            wait(10000, mode_)

    qm = QM(modes=(mode_,), oscillators=(lo_,))
    import pprint

    pprint.pp(qm.get_config())
    job = qm.execute(play_digital_marker)


if __name__ == "__main__":
    """ """

    configpath = Path.cwd()

    with Stage(configpath=configpath, remote=True) as stage:
        qubit, lo_qubit = stage.get("qubit", "lo_cav")

        rf_switch = RFSwitch(name="qubit_rf_switch", port=5, delay=0, buffer=0)

        test_pulse = ConstantPulse(
            name="qubit_constant_pulse",
            length=1000,
            I_ampx=1.0,
            digital_marker=DigitalWaveform(name="rf_switch_on", samples=[(1, 0)]),
        )

        qubit.configure(
            lo_name="lo_cav",
            ports={"I": 5, "Q": 6},
            int_freq=50e6,
            rf_switch=rf_switch,
            operations=[test_pulse],
        )

    sequence(qubit, test_pulse, lo_qubit)
