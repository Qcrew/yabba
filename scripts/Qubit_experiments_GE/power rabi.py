""" """
from config.experiment_config import FOLDER, N, FREQ, I, Q, MAG, PHASE, RR
from qcore import Experiment, qua, Sweep
from qm import qua as qm_qua
from qcore.libs.qua_macros import QuaVariable
from qcore import Dataset


class Rabi(Experiment):
    """Power Rabi"""

    ############################# DEFINE PRIMARY DATASETS ##############################
    # these Datasets form the "raw" experimental data and will be streamed by the OPX
    # they must be specified at experiment runtime
    primary_datasets = ["I", "Q", "SINGLE_SHOT"]

    ############################## DEFINE PRIMARY SWEEPS ###############################
    # these Sweeps are uniquely associated with the Experiment subclass
    # these Sweeps must be specified at experiment runtime
    primary_sweeps = ["qubit_pulse_amplitude"]

    ############################ DEFINE THE PULSE SEQUENCE #############################
    # ensure that you import 'qua' from 'qcore' and not from 'qm' library
    # attributes accessed via 'self' must be defined in 'if __name__ == "__main__"' code
    def sequence(self):
        """QUA sequence that defines this Experiment subclass"""
        # qua.reset_frame(self.qubit)
        print("HI")
        self.qubit.play(self.qubit_drive, ampx=self.qubit_pulse_amplitude)
        self.qubit.play(self.qubit_drive, ampx=self.qubit_pulse_amplitude)
        self.qubit.play(self.qubit_drive, ampx=self.qubit_pulse_amplitude)
        qua.align(self.qubit, self.resonator)
        self.resonator.measure(self.readout_pulse, (self.I, self.Q), ampx=self.ro_ampx)
        qua.wait(self.wait_time, self.resonator)
        if self.plot_single_shot:  # assign state to G or E
            qm_qua.assign(
                self.SINGLE_SHOT,
                qm_qua.Cast.to_fixed(self.I < 144e-6),
            )


if __name__ == "__main__":
    """ """

    #################################### MODE MAP ######################################
    # key: name of the Mode as defined by the Experiment subclass
    # value: name of the Mode as defined by the user in modes.yml
    modes = {
        "qubit": "qubit",
        "resonator": "rr",
    }

    ################################### PULSE MAP ######################################
    # key: name of the Pulse as defined by the Experiment subclass
    # value: name of the Pulse as defined by the user in modes.yml
    pulses = {
        "qubit_drive": "qubit_gaussian_short_pi_pulse",
        "readout_pulse": "rr_readout_pulse",
    }

    ############################## CONTROL PARAMETERS ##################################
    parameters = {
        "wait_time": 500_000,
        "ro_ampx": 1,
        "plot_single_shot": True,
    }

    ######################## SWEEP (INDEPENDENT) VARIABLES #############################
    # must include an outermost averaging Sweep named "N"
    # must include all primary sweeps defined by the Experiment subclass

    # set number of repetitions for this Experiment run
    N.num = 200

    # set the qubit amplitude sweep for this Experiment run
    QD_AMPX = Sweep(
        name="qubit_pulse_amplitude",
        start=-1.2,
        stop=1.2,
        num=201,
    )

    sweeps = [N, QD_AMPX]

    ######################## DATASET (DEPENDENT) VARIABLES #############################
    # must include all primary datasets defined by the Experiment subclass
    I.fitfn, Q.fitfn, MAG.fitfn = "sine", "sine", "sine"
    PHASE.datafn_args = {"delay": 2.792e-7, "freq": RR.int_freq}

    SINGLE_SHOT = Dataset(
        name="SINGLE_SHOT",
        save=True,
        plot=True,
    )

    datasets = [I, Q, SINGLE_SHOT]

    ######################## INITIALIZE AND RUN EXPERIMENT #############################
    expt = Rabi(FOLDER, modes, pulses, sweeps, datasets, **parameters)
    expt.run()
