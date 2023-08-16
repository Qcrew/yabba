""" """

from config.experiment_config import FOLDER, N, FREQ, I, Q, MAG, PHASE, RR

from qcore import Experiment, qua, Sweep


class ALLXY(Experiment):
    """ALLXY"""

    ############################# DEFINE PRIMARY DATASETS ##############################
    # these Datasets form the "raw" experimental data and will be streamed by the OPX
    # they must be specified at experiment runtime

    primary_datasets = ["I", "Q"]

    ############################## DEFINE PRIMARY SWEEPS ###############################
    # these Sweeps are uniquely associated with the Experiment subclass
    # these Sweeps must be specified at experiment runtime

    primary_sweeps = ["qubit_pulse_amplitude"]

    ############################ DEFINE THE PULSE SEQUENCE #############################
    # ensure that you import 'qua' from 'qcore' and not from 'qm' library
    # attributes accessed via 'self' must be defined in 'if __name__ == "__main__"' code


    self.gate_list = [
        ("idle", 0.00, "idle", 0.00, "IdId"),
        (self.qubit_pi_op, 0.00, self.qubit_pi_op, 0.00, "XpXp"),
        (self.qubit_pi_op, 0.25, self.qubit_pi_op, 0.25, "YpYp"),
        (self.qubit_pi_op, 0.00, self.qubit_pi_op, 0.25, "XpYp"),
        (self.qubit_pi_op, 0.25, self.qubit_pi_op, 0.00, "YpXp"),
        (self.qubit_pi2_op, 0.00, "idle", 0.00, "X9Id"),
        (self.qubit_pi2_op, 0.25, "idle", 0.00, "Y9Id"),
        (self.qubit_pi2_op, 0.00, self.qubit_pi2_op, 0.25, "X9Y9"),
        (self.qubit_pi2_op, 0.25, self.qubit_pi2_op, 0.00, "Y9X9"),
        (self.qubit_pi2_op, 0.00, self.qubit_pi_op, 0.25, "X9Yp"),
        (self.qubit_pi2_op, 0.25, self.qubit_pi_op, 0.00, "Y9Xp"),
        (self.qubit_pi_op, 0.00, self.qubit_pi2_op, 0.25, "XpY9"),
        (self.qubit_pi_op, 0.25, self.qubit_pi2_op, 0.00, "YpX9"),
        (self.qubit_pi2_op, 0.00, self.qubit_pi_op, 0.00, "X9Xp"),
        (self.qubit_pi_op, 0.00, self.qubit_pi2_op, 0.00, "XpX9"),
        (self.qubit_pi2_op, 0.25, self.qubit_pi_op, 0.25, "Y9Yp"),
        (self.qubit_pi_op, 0.25, self.qubit_pi2_op, 0.25, "YpY9"),
        (self.qubit_pi_op, 0.00, "idle", 0.00, "XpId"),
        (self.qubit_pi_op, 0.25, "idle", 0.00, "YpId"),
        (self.qubit_pi2_op, 0.00, self.qubit_pi2_op, 0.00, "X9X9"),
        (self.qubit_pi2_op, 0.25, self.qubit_pi2_op, 0.25, "Y9Y9"),
    ]


        # Assign one sweep value for each time QUA_stream_results method is executed in
        # the pulse sequence. Is used for plotting with correct labels.
        self.internal_sweep = [x[4] for x in self.gate_list]  # select gate names

        super().__init__(**other_params)  # Passes other parameters to parent





    def sequence(self):
        """QUA sequence that defines this Experiment subclass"""
        
        for gate_pair in self.gate_list:
            gate1_rot, gate1_axis, gate2_rot, gate2_axis, _ = gate_pair
            
            # qua.reset_frame(self.qubit.name)
            # Play the first gate
            if gate1_rot != "idle":
                self.qubit.play(gate1_rot, phase=gate1_axis)
            # Play the second gate
            if gate2_rot != "idle":
                self.qubit.play(gate2_rot, phase=gate2_axis)
                
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
    N.num = 50000

    # set the qubit amplitude sweep for this Experiment run
    # QD_AMPX = Sweep(name="qubit_pulse_amplitude", start=-1.2, stop=1.2, num=401)
    sweeps = [N]

    ######################## DATASET (DEPENDENT) VARIABLES #############################
    # must include all primary datasets defined by the Experiment subclass
    I.fitfn, Q.fitfn, MAG.fitfn = "sine", "sine", "sine"

    PHASE.datafn_args = {"delay": 2.792e-7, "freq": RR.int_freq}
    # PHASE.plot = False
    datasets = [I, Q, MAG, PHASE]

    ######################## INITIALIZE AND RUN EXPERIMENT #############################

    expt = ALLXY(FOLDER, modes, pulses, sweeps, datasets, **parameters)
    expt.run()
