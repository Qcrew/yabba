""" """

from config.experiment_config import FOLDER, N, ADC, ADC_FFT, READOUT_PULSE

from qcore import Experiment, qua, Sweep


class TimeOfFlight(Experiment):
    """ """

    primary_datasets = ["adc"]

    primary_sweeps = []

    def sequence(self):
        """the QUA pulse sequence for a Time Of Flight experiment"""
        qua.reset_phase(self.resonator)
        self.resonator.measure(self.readout_pulse, stream=self.adc, ampx=self.ro_ampx)
        qua.wait(self.wait_time, self.resonator)


if __name__ == "__main__":
    """ """

    #################################### MODE MAP ######################################
    # key: name of the Mode as defined by the Experiment subclass
    # value: name of the Mode as defined by the user in modes.yml

    modes = {"resonator": "rr"}

    ################################### PULSE MAP ######################################
    # key: name of the Pulse as defined by the Experiment subclass
    # value: name of the Pulse as defined by the user in modes.yml

    pulses = {"readout_pulse": "rr_readout_pulse"}

    ############################## CONTROL PARAMETERS ##################################

    parameters = {
        "wait_time": 5000,
        "ro_ampx": 1.0,
        "fetch_interval": 4,
    }

    ######################## SWEEP (INDEPENDENT) VARIABLES #############################
    # must include an outermost averaging Sweep named "N"
    # must include all primary sweeps defined by the Experiment subclass

    # NOTE expts streaming raw adc data e.g. time of flight do not support >= 2D sweeps

    # set number of repetitions for this Experiment run
    N.num = 200
    sweeps = [N]

    ######################## DATASET (DEPENDENT) VARIABLES #############################
    # must include all primary datasets defined by the Experiment subclass

    # must initialize axes based on expected shape of raw data for ADC datasets
    ADC.initialize(axes=[N.num, READOUT_PULSE.total_length])

    freqs = Sweep(
        name="Frequency",
        start=0,
        stop=0.5,
        step=1 / READOUT_PULSE.total_length,
        units="GHz",
    )
    freqs.initialize()
    N.initialize()
    ADC_FFT.initialize(axes=[N, freqs])
    datasets = [ADC, ADC_FFT]

    ######################## INITIALIZE AND RUN EXPERIMENT #############################

    expt = TimeOfFlight(FOLDER, modes, pulses, sweeps, datasets, **parameters)
    expt.run()
