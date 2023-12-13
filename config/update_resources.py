""" """

from qcore.helpers import Stage
from qcore.modes import *
from qcore.pulses import *
import os
import numpy as np
import scipy as sc

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
        sa = stage.get("sa")
        # CONFIGURE THE RR PROPERTIES AND OPERATIONS
        lo_rr.frequency = 7.5651e9 + 0.2e6 - 0.40e6
        lo_rr.power = 15.0
        lo_rr.output = True

        rr.configure(
            name="rr",
            lo_name="lo_rr",
            ports={"I": 3, "Q": 4, "out": 1},
            int_freq=50e6,
            tof=282,
        )

        rr.operations = [
            ConstantReadoutPulse(
                name="rr_readout_pulse",
                length=1500,  # 2000,
                I_ampx=0.3,
                pad=900,
                digital_marker=DigitalWaveform("ADC_ON"),
                threshold=0.0001440406944069628,
                weights="C://Users//qcrew//Desktop//qcrew//qcrew//config//weights//20230801_184026_opt_weights.npz",
                has_optimized_weights=True,
            ),
        ]

        # CONFIGURE THE QUBIT PROPERTIES AND OPERATIONS
        lo_qubit.frequency = 5.1e9
        lo_qubit.power = 15.0
        lo_qubit.output = True

        qubit_factor = 374

        qubit.configure(
            name="qubit",
            lo_name="lo_qubit",
            ports={"I": 1, "Q": 2},
            # int_freq=177.3065e6,
            int_freq=177.3565e6,
        )

        # # assign directory
        # # directory = 'C:\Users\qcrew\Documents\yabba\waves'
        # folder_path = "C://Users//qcrew//Documents//yabba//waves"
        # all_vacuum_rabi_files = [x for x in os.listdir(folder_path) if "q_" in x]

        # # iterate over files in
        # # that directory
        # for filename in os.listdir(directory):
        #     f = os.path.join(directory, filename)
        #     # checking if it is a file
        #     curr = np.load(f)

        qubit.operations = [
            ConstantPulse(
                name="test",
                length=25,
                I_ampx=1.0,
            ),
            GaussianPulse(
                name="qubit_gaussian_short_pi_pulse",
                sigma=30,
                chop=4,
                I_ampx=1.13,
                Q_ampx=-0.028,
            ),
            GaussianPulse(
                name="qubit_gaussian_short_pi2_pulse",
                sigma=30,
                chop=4,
                I_ampx=0.56,
                Q_ampx=-0.028,
            ),
            GaussianPulse(
                name="qubit_gaussian_sel_pi_pulse",
                sigma=800,
                chop=4,
                I_ampx=0.042,
                Q_ampx=0.0,
            ),
            GaussianPulse(
                name="qubit_gaussian_sel_pi2_pulse",
                sigma=800,
                chop=4,
                I_ampx=0.021,
                Q_ampx=0.0,
            ),
            NumericalPulse(
                path=r"C:\Users\qcrew\Documents\yabba\waves\c_coh_1.npz",
                name="qubit_grape_pi_pulse",
                I_ampx=qubit_factor,
                Q_ampx=qubit_factor,
                pad=5000,
            ),
        ]

        qubitEF.configure(
            name="qubitEF",
            lo_name="lo_qubit",
            ports={"I": 1, "Q": 2},
            int_freq=1.739e6,
        )

        qubitEF.operations = [
            GaussianPulse(
                name="qubitEF_gaussian_short_pi_pulse",
                sigma=20,
                chop=4,
                I_ampx=0.694,
                Q_ampx=0.0,
            ),
        ]

        # CONFIGURE THE CAVITY PROPERTIES AND OPERATIONS
        lo_cav.frequency = 4.5e9
        lo_cav.power = 15.0
        lo_cav.output = True
        cavity_factor = 479

        cav.configure(
            name="cav",
            lo_name="lo_cav",
            ports={"I": 5, "Q": 6},
            int_freq=89.54e6,
        )

        cav.operations = [
            GaussianPulse(
                name="cavity_gaussian_coherent_1",
                sigma=27,
                chop=4,
                I_ampx=1.0,
                Q_ampx=0.0,
                drag=0.0,
            ),
            GaussianPulse(
                name="cavity_coherent_1",
                sigma=27,
                chop=4,
                I_ampx=1.0,
            ),
            GaussianPulse(
                name="cavity_coherent_1_long",
                sigma=52,
                chop=4,
                I_ampx=0.515,
            ),
            GaussianPulse(
                name="cavity_coherent_1_longer",
                sigma=80,
                chop=4,
                I_ampx=0.335,
            ),
            GaussianPulse(
                name="cavity_coherent_alot",
                sigma=500,
                chop=4,
                I_ampx=1.0,
            ),
            # NumericalPulse(
            #     path = r"C:\Users\qcrew\Documents\yabba\waves",
            #     name="c_coh_1.npz",
            #     I_ampx=cavity_factor,
            #     Q_ampx = cavity_factor,
            # ),
        ]
