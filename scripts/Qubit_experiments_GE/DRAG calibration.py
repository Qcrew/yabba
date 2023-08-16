""" """

from config.experiment_config import FOLDER, N, FREQ, I, Q, MAG, PHASE, RR

from qcore import Experiment, qua, Sweep


class DRAGcal(Experiment):
    """DRAG calibration"""

    ############################# DEFINE PRIMARY DATASETS ##############################
    # these Datasets form the "raw" experimental data and will be streamed by the OPX
    # they must be specified at experiment runtime

    primary_datasets = ["I", "Q"]

    ############################## DEFINE PRIMARY SWEEPS ###############################
    # these Sweeps are uniquely associated with the Experiment subclass
    # these Sweeps must be specified at experiment runtime

    primary_sweeps = ["drag"]

    ############################ DEFINE THE PULSE SEQUENCE #############################
    # ensure that you import 'qua' from 'qcore' and not from 'qm' library
    # attributes accessed via 'self' must be defined in 'if __name__ == "__main__"' code

    

    def sequence(self):
        """QUA sequence that defines this Experiment subclass"""

        # (self.qubit_pi_op, 0.25, self.qubit_pi2_op, 0.00, "YpX9"),  # YpX9
        # (self.qubit_pi_op, 0.00, self.qubit_pi2_op, 0.25, "XpY9"),  # XpY9

        # qua.reset_phase(self.qubit)
        self.qubit.play(self.qubit_pi_op, phase = self.pha)
        # AS SOON AS YOU SET THE PHASE AS A SWEEP, IT EXPLODES
        self.qubit.play(self.qubit_pi2_op, ampx=(1.0, 0.0, 0.0, self.drag), phase = 0.0)
        qua.align(self.qubit, self.resonator)
        self.resonator.measure(self.readout_pulse, (self.I, self.Q))
        qua.wait(self.wait_time, self.resonator)


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
        "qubit_pi_op": "qubit_gaussian_pi_pulse",
        "qubit_pi2_op": "qubit_gaussian_pi2_pulse",
        "readout_pulse": "rr_readout_pulse",
    }

    ############################## CONTROL PARAMETERS ##################################

    parameters = {
        "wait_time": 500_000,
        "ro_ampx": 1,
    }

    ######################## SWEEP (INDEPENDENT) VARIABLES #############################
    # must include an outermost averaging Sweep named "N"
    # must include all primary sweeps defined by the Experiment subclass

    # set number of repetitions for this Experiment run
    N.num = 100

    # set the qubit amplitude sweep for this Experiment run
    PHA = Sweep(name="pha", dtype = float,  start=0.0, stop=0.25, step = 0.1)
    # PHA2 = Sweep(name="phase2", start=-0.0, stop=0.25, step=0.25)
    DRAG = Sweep(name="drag", start=-0.2, stop=0.2, step=0.02)

    sweeps = [N, PHA, DRAG]

    ######################## DATASET (DEPENDENT) VARIABLES #############################
    # must include all primary datasets defined by the Experiment subclass
    I.fitfn, Q.fitfn, MAG.fitfn = "sine", "sine", "sine"

    PHASE.datafn_args = {"delay": 2.792e-7, "freq": RR.int_freq}
    # PHASE.plot = False
    datasets = [I, Q, MAG, PHASE]

    ######################## INITIALIZE AND RUN EXPERIMENT #############################

    expt = DRAGcal(FOLDER, modes, pulses, sweeps, datasets, **parameters)
    expt.run()
