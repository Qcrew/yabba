""" """
from config.experiment_config import FOLDER, N, FREQ, I, Q, MAG, PHASE, RR
from qcore import Experiment, qua, Sweep


class RamseyRevival(Experiment):
    """Ramsey revival"""

    ############################# DEFINE PRIMARY DATASETS ##############################
    # these Datasets form the "raw" experimental data and will be streamed by the OPX
    # they must be specified at experiment runtime
    primary_datasets = ["I", "Q"]

    ############################## DEFINE PRIMARY SWEEPS ###############################
    # these Sweeps are uniquely associated with the Experiment subclass
    # these Sweeps must be specified at experiment runtime
    primary_sweeps = ["delay"]

    ############################ DEFINE THE PULSE SEQUENCE #############################
    # ensure that you import 'qua' from 'qcore' and not from 'qm' library
    # attributes accessed via 'self' must be defined in 'if __name__ == "__main__"' code

    def sequence(self):
        """QUA sequence that defines this Experiment subclass"""
        # qua.update_frequency(self.cavity, self.cavity_frequency)
        self.cavity.play(self.cavity_pulse, ampx = self.cavity_ampx)
        qua.align(self.cavity, self.qubit)
        self.qubit.play(self.qubit_pulse)
        qua.wait(self.delay, self.qubit)
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
        "cavity_pulse": "cavity_gaussian_coherent_1",
        "qubit_pulse": "qubit_gaussian_short_pi_pulse",
        "readout_pulse": "rr_readout_pulse",
    }

    ############################## CONTROL PARAMETERS ##################################

    parameters = {
        "wait_time": 10e6,
        "ro_ampx": 1,
        "cavity_ampx": 1,
        "fetch_interval": 8,
    }

    ######################## SWEEP (INDEPENDENT) VARIABLES #############################
    # must include an outermost averaging Sweep named "N"
    # must include all primary sweeps defined by the Experiment subclass

    # set number of repetitions for this Experiment run
    N.num = 1000

    # set the qubit frequency sweep for this Experiment run
    DELAY = Sweep(
        name="delay",
        dtype=int,
        start=16,
        stop=2400,
        step=20,
    )

    sweeps = [N, DELAY]

    ######################## DATASET (DEPENDENT) VARIABLES #############################
    # must include all primary datasets defined by the Experiment subclass
    # MAG.fitfn = "gaussian"

    PHASE.datafn_args = {"delay": 2.792e-7, "freq": RR.int_freq}
    MAG.plot = False
    Q.plot = False
    PHASE.plot = False,
    I.fitfn = "gaussian"
    datasets = [I, Q, MAG, PHASE]

    ######################## INITIALIZE AND RUN EXPERIMENT #############################

    expt = RamseyRevival(FOLDER, modes, pulses, sweeps, datasets, **parameters)
    expt.run()
