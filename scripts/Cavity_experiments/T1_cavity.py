""" """

from config.experiment_config import FOLDER, N, I, Q, MAG, PHASE, RR
from qcore import Experiment, qua, Sweep


class CavityT1(Experiment):
    """Cavity T1"""

    ############################# DEFINE PRIMARY DATASETS ##############################
    # these Datasets form the "raw" experimental data and will be streamed by the OPX
    # they must be specified at experiment runtime

    primary_datasets = ["I", "Q"]

    ############################## DEFINE PRIMARY SWEEPS ###############################
    # these Sweeps are uniquely associated with the Experiment subclass
    # these Sweeps must be specified at experiment runtime

    primary_sweeps = ["time_delay"]

    ############################ DEFINE THE PULSE SEQUENCE #############################
    # ensure that you import 'qua' from 'qcore' and not from 'qm' library
    # attributes accessed via 'self' must be defined in 'if __name__ == "__main__"' code

    def sequence(self):
        """QUA sequence that defines this Experiment subclass"""
        self.cavity.play(self.cavity_drive)
        qua.wait(self.time_delay, self.cavity)
        qua.align(self.cavity, self.qubit)
        self.qubit.play(self.qubit_pulse)
        qua.align(self.qubit, self.resonator)
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
        "cavity_drive": "cavity_coherent_1",
        "qubit_pulse": "qubit_gaussian_pi_sel_pulse2",
        "readout_pulse": "rr_readout_pulse",
    }

    ############################## CONTROL PARAMETERS ##################################

    parameters = {
        "wait_time": 5000e3,
        "ro_ampx": 1,
    }

    ######################## SWEEP (INDEPENDENT) VARIABLES #############################
    # must include an outermost averaging Sweep named "N"
    # must include all primary sweeps defined by the Experiment subclass

    # set number of repetitions for this Experiment run
    N.num = 5000

    # set the qubit frequency sweep for this Experiment run

    DEL = Sweep(
        name="time_delay", 
        start=10, 
        stop=6000e3, 
        num=101, 
        dtype=int)
    sweeps = [N, DEL]

    ######################## DATASET (DEPENDENT) VARIABLES #############################
    # must include all primary datasets defined by the Experiment subclass
    I.fitfn, PHASE.fitfn = 'cohstate_decay', 'cohstate_decay'
    PHASE.datafn_args = {"delay": 2.792e-7, "freq": RR.int_freq}
    Q.plot, MAG.plot = False, False
    datasets = [I, Q, MAG, PHASE]

    ######################## INITIALIZE AND RUN EXPERIMENT #############################

    expt = CavityT1(FOLDER, modes, pulses, sweeps, datasets, **parameters)
    expt.run()
