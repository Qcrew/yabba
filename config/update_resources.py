""" """

from qcore.helpers import Stage
from qcore.modes import *
from qcore.pulses import *

from config.experiment_config import MODES_CONFIG

if __name__ == "__main__":
    """ """

    # configpath must be the path to the modes config file
    # remote = True means the Stage will connect with the Server and stage instruments
    # for remote = True to work, please run setup_server.bat first

    # NOTE adding digital markers to test RF switch to RR

    with Stage(configpath=MODES_CONFIG, remote=True) as stage:
        # RETRIEVE INSTRUMENTS AND MODES
        lo_cav, lo_qubit, lo_rr = stage.get("lo_cav", "lo_qubit", "lo_rr")
        cav, qubit, qubitEF, rr = stage.get("cav", "qubit", "qubitEF", "rr")

        # CONFIGURE THE RR PROPERTIES AND OPERATIONS
        lo_rr.frequency = 7.465806e9 - 0.01e6
        lo_rr.power = 15.0
        lo_rr.output = True

        rr.configure(
            name="rr",
            lo_name="lo_rr",
            ports={"I": 3, "Q": 4, "out": 1},
            int_freq=50e6,
            tof=272,
        )

        rr.operations = [
            ConstantPulse(
                name="rr_constant_pulse",
                length=1000,
                I_ampx=0.4,
            ),
            GaussianPulse(
                name="rr_gaussian_pulse",
                sigma=100,
                chop=6,
                I_ampx=1.0,
                Q_ampx=0.0,
            ),
            ConstantReadoutPulse(
                name="rr_readout_pulse",
                length=2000,  # 2000,
                I_ampx=0.25,
                pad=600,
                digital_marker=DigitalWaveform("ADC_ON"),
                # threshold= 0.0004282540982746491,
                # weights="C:/Users/qcrew/Desktop/qcrew/qcrew/config/weights/20230720_142024_opt_weights.npz",
            ),
        ]

        # CONFIGURE THE QUBIT PROPERTIES AND OPERATIONS
        lo_qubit.frequency = 4.6871e9
        lo_qubit.power = 15.0
        lo_qubit.output = True

        qubit.configure(
            name="qubit",
            lo_name="lo_qubit",
            ports={"I": 1, "Q": 2},
            int_freq=79.6e6,
        )

        qubit.operations = [
            ConstantPulse(
                name="qubit_constant_pulse",
                length=1000,
                I_ampx=0.032,
            ),
            ConstantPulse(
                name="qubit_constant_pi_pulse",
                length=52,
                I_ampx=0.595,
            ),
            ConstantPulse(
                name="qubit_constant_pi2_pulse",
                length=52,
                I_ampx=0.595 / 2,
            ),
            ConstantPulse(
                name="qubit_constant_selective_pi_pulse",
                length=1000,
                I_ampx=0.032,
            ),
            ConstantPulse(
                name="qubit_constant_very_selective_pi_pulse",
                length=4000,
                I_ampx=0.008,
            ),
            GaussianPulse(
                name="qubit_gaussian_pulse",
                sigma=200,
                chop=4,
                I_ampx=0.032,
                Q_ampx=0.0,
            ),
            RampedConstantPulse(
                name="qubit_cos_ramp_pulse",
                ramp=10,
                rampfn="cos",
                length=20,
                I_ampx=1.4,
            ),
        ]

        qubitEF.configure(
            name="qubitEF",
            lo_name="lo_qubit",
            ports={"I": 1, "Q": 2},
            # int_freq=-191.11e6,
            # int_freq=-88.20e6,
            # int_freq=-125.45e6,
            int_freq=-127e6,
        )

        qubitEF.operations = [
            ConstantPulse(
                name="qubitEF_constant_pulse",
                length=500,
                I_ampx=0.0496,
            ),
            ConstantPulse(
                name="qubitEF_constant_pi_pulse",
                length=52,
                I_ampx=0.467,
            ),
            GaussianPulse(
                name="qubitEF_gaussian_pulse",
                sigma=200,
                chop=4,
                I_ampx=0.032,
                Q_ampx=0.0,
            ),
            RampedConstantPulse(
                name="qubitEF_cos_ramp_pulse",
                ramp=10,
                rampfn="cos",
                length=20,
                I_ampx=1.4,
            ),
        ]

        # CONFIGURE THE CAVITY PROPERTIES AND OPERATIONS
        lo_cav.frequency = 6.0e9
        lo_cav.power = 15.0
        lo_cav.output = True

        cav.configure(
            name="cav",
            lo_name="lo_cav",
            ports={"I": 7, "Q": 8},
            int_freq=71.64e6,
        )

        cav.operations = [
            ConstantPulse(
                name="cavity_constant_pulse",
                length=1000,
                I_ampx=0.2,
            ),
            GaussianPulse(
                name="cavity_gaussian_pulse",
                sigma=200,
                chop=4,
                I_ampx=0.032,
                Q_ampx=0.0,
            ),
        ]
