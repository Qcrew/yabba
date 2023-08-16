""" """
from config.experiment_config import FOLDER, N, FREQ, I, Q, MAG, PHASE, RR
from qcore import Experiment, qua, Sweep


class DisplacementCal(Experiment):
    """Cavity spectroscopy"""

    ############################# DEFINE PRIMARY DATASETS ##############################
    # these Datasets form the "raw" experimental data and will be streamed by the OPX
    # they must be specified at experiment runtime
    primary_datasets = ["I", "Q"]

    ############################## DEFINE PRIMARY SWEEPS ###############################
    # these Sweeps are uniquely associated with the Experiment subclass
    # these Sweeps must be specified at experiment runtime
    primary_sweeps = ["cavity_drive_amplitude"]

    ############################ DEFINE THE PULSE SEQUENCE #############################
    # ensure that you import 'qua' from 'qcore' and not from 'qm' library
    # attributes accessed via 'self' must be defined in 'if __name__ == "__main__"' code
    def sequence(self):
        """QUA sequence that defines this Experiment subclass"""
        
        self.cavity.play(
            self.cavity_drive, ampx=self.cavity_drive_amplitude
        )  # play displacement to cavity
        qua.align(self.cavity, self.qubit)  # align all modes
        self.qubit.play(self.qubit_drive)  # play qubit pulse
        qua.align(self.qubit, self.resonator)  # align all modes
        self.resonator.measure(self.readout_pulse, (self.I, self.Q), ampx=self.ro_ampx)
        qua.wait(self.wait_time, self.resonator)


if __name__ == "__main__":
    """ """

    #################################### MODE MAP ######################################
    # key: name of the Mode as defined by the Experiment subclass
    # value: name of the Mode as defined by the user in modes.yml
    modes = {
        "cavity": "cav",
        "qubit": "qubit",
        "resonator": "rr",
    }

    ################################### PULSE MAP ######################################
    # key: name of the Pulse as defined by the Experiment subclass
    # value: name of the Pulse as defined by the user in modes.yml
    pulses = {
        "cavity_drive": "cavity_gaussian_coherent_1",
        "qubit_drive": "qubit_gaussian_sel_pi_pulse",
        "readout_pulse": "rr_readout_pulse",
    }

    ############################## CONTROL PARAMETERS ##################################
    parameters = {
        "wait_time": 10e6,
        "ro_ampx": 1,
    }

    ######################## SWEEP (INDEPENDENT) VARIABLES #############################
    # must include an outermost averaging Sweep named "N"
    # must include all primary sweeps defined by the Experiment subclass

    # set number of repetitions for this Experiment run
    N.num = 2000
    QD_AMPX = Sweep(name="cavity_drive_amplitude", start=0, stop=1.8, step=0.02)
    sweeps = [N, QD_AMPX]

    ######################## DATASET (DEPENDENT) VARIABLES #############################
    # must include all primary datasets defined by the Experiment subclass
    I.fitfn = "displacement_cal"
    PHASE.datafn_args = {"delay": 2.792e-7, "freq": RR.int_freq}
    Q.plot, MAG.plot = False, False
    datasets = [I, Q, MAG, PHASE]

    ######################## INITIALIZE AND RUN EXPERIMENT #############################
    expt = DisplacementCal(FOLDER, modes, pulses, sweeps, datasets, **parameters)
    expt.run()
