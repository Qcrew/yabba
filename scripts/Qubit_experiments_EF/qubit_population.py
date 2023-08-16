""" """

from config.experiment_config import FOLDER, N, FREQ, I, Q, MAG, PHASE, RR

from qcore import Experiment, qua, Sweep


class QubitPopulation(Experiment):
    """Qubit thermal population"""

    ############################# DEFINE PRIMARY DATASETS ##############################
    # these Datasets form the "raw" experimental data and will be streamed by the OPX
    # they must be specified at experiment runtime

    primary_datasets = ["I", "Q"]

    ############################## DEFINE PRIMARY SWEEPS ###############################
    # these Sweeps are uniquely associated with the Experiment subclass
    # these Sweeps must be specified at experiment runtime

    primary_sweeps = ["qubitEF_pulse_amplitude"]

    ############################ DEFINE THE PULSE SEQUENCE #############################
    # ensure that you import 'qua' from 'qcore' and not from 'qm' library
    # attributes accessed via 'self' must be defined in 'if __name__ == "__main__"' code

    def sequence(self):
        """QUA sequence that defines this Experiment subclass"""

        self.qubit.play(self.qubit_pi_pulse, ampx=self.qubitGE_pulse_amplitude)
        qua.align(self.qubit, self.qubitEF)
        self.qubitEF.play(self.qubitEF_pi_pulse, ampx=self.qubitEF_pulse_amplitude)
        qua.align(self.qubitEF, self.qubit)
        self.qubit.play(self.qubit_pi_pulse)
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
        "qubitEF": "qubitEF",
        "resonator": "rr",
    }

    ################################### PULSE MAP ######################################
    # key: name of the Pulse as defined by the Experiment subclass
    # value: name of the Pulse as defined by the user in modes.yml

    pulses = {
        "qubit_pi_pulse": "qubit_gaussian_pi_pulse",
        "qubitEF_pi_pulse": "qubitEF_gaussian_pi_pulse",
        "readout_pulse": "rr_readout_pulse",
    }

    ############################## CONTROL PARAMETERS ##################################

    parameters = {
        "wait_time": 500e3,
        "ro_ampx": 1,
    }

    ######################## SWEEP (INDEPENDENT) VARIABLES #############################
    # must include an outermost averaging Sweep named "N"
    # must include all primary sweeps defined by the Experiment subclass

    # set number of repetitions for this Experiment run
    N.num = 1000

    # set the qubit amplitude sweep for this Experiment run
    QD_AMPX = Sweep(name="qubitEF_pulse_amplitude", start=-1.8, stop=1.8, num=201)
    QD_AMPY = Sweep(name="qubitGE_pulse_amplitude", points=[0.0, 1.0])
    sweeps = [N, QD_AMPY, QD_AMPX]
    
    

    ######################## DATASET (DEPENDENT) VARIABLES #############################
    # must include all primary datasets defined by the Experiment subclass
    I.fitfn = "sine "
    PHASE.datafn_args = {"delay": 2.792e-7, "freq": RR.int_freq}
    Q.plot,  MAG.plot = False, False
    datasets = [I, Q, MAG, PHASE]

    ######################## INITIALIZE AND RUN EXPERIMENT #############################

    expt = QubitPopulation(FOLDER, modes, pulses, sweeps, datasets, **parameters)
    expt.run()
