""" """

from config.experiment_config import FOLDER, N, I, Q, MAG, PHASE, RR
from qcore import Experiment, qua, Sweep


class QubitT1(Experiment):
    """Qubit T1"""

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
        factor = qua.declare(qua.fixed)
        qua.assign(factor, self.detuning * 4 * 1e-9)
        qua.reset_frame(self.qubit)
        
        
        self.qubit.play(self.qubit_drive)
        qua.wait(self.time_delay, self.qubit)
        
        qua.assign(self.phase, qua.Cast.mul_fixed_by_int(factor, self.time_delay))
        self.qubit.play(self.qubit_drive, phase=self.phase)
        
        qua.align(self.qubit, self.resonator)
        self.resonator.measure(self.readout_pulse, (self.I, self.Q), ampx=self.ro_ampx)
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
        "qubit_drive": "qubit_constant_pi_pulse",
        "readout_pulse": "rr_readout_pulse",
    }

    ############################## CONTROL PARAMETERS ##################################

    parameters = {
        "wait_time": 100000,
        "ro_ampx": 1,
    }

    ######################## SWEEP (INDEPENDENT) VARIABLES #############################
    # must include an outermost averaging Sweep named "N"
    # must include all primary sweeps defined by the Experiment subclass

    # set number of repetitions for this Experiment run
    N.num = 50000

    # set the qubit frequency sweep for this Experiment run

    DEL = Sweep(name="time_delay", start=10, stop=120000, step=1000, dtype=int)
    sweeps = [N, DEL]

    ######################## DATASET (DEPENDENT) VARIABLES #############################
    # must include all primary datasets defined by the Experiment subclass

    MAG.axes = sweeps[1:]
    PHASE.axes = sweeps[1:]
    PHASE.datafn_args = {"delay": 2.792e-7, "freq": RR.int_freq}
    PHASE.plot = False
    datasets = [I, Q, MAG, PHASE]

    ######################## INITIALIZE AND RUN EXPERIMENT #############################

    expt = QubitT1(FOLDER, modes, pulses, sweeps, datasets, **parameters)
    expt.run()
