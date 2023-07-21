""" """

from config.experiment_config import FOLDER, N, ADC, ADC_FFT, READOUT_PULSE, RR

from qcore import Experiment, qua, Dataset, Sweep


class TimeOfFlightDemod(Experiment):
    """ """

    primary_datasets = ["adc"]

    primary_sweeps = []

    def sequence(self):
        """the QUA pulse sequence for a Time Of Flight experiment"""
        self.qubit.play(self.qubit_drive, ampx=self.qd_ampx)
        qua.align(self.qubit, self.resonator)
        self.resonator.measure(self.readout_pulse, stream=self.adc, ampx=self.ro_ampx)
        qua.wait(self.wait_time, self.resonator)


if __name__ == "__main__":
    """ """

    #################################### MODE MAP ######################################
    # key: name of the Mode as defined by the Experiment subclass
    # value: name of the Mode as defined by the user in modes.yml

    modes = {
        "resonator": "rr",
        "qubit": "qubit",
    }

    ################################### PULSE MAP ######################################
    # key: name of the Pulse as defined by the Experiment subclass
    # value: name of the Pulse as defined by the user in modes.yml

    pulses = {
        "readout_pulse": "rr_readout_pulse",
        "qubit_drive": "qubit_constant_pi_pulse",
    }

    ############################## CONTROL PARAMETERS ##################################

    parameters = {
        "wait_time": 10000,
        "ro_ampx": 1.0,
        "qd_ampx": 1.0,
        "fetch_interval": 3,
    }

    ######################## SWEEP (INDEPENDENT) VARIABLES #############################
    # must include an outermost averaging Sweep named "N"
    # must include all primary sweeps defined by the Experiment subclass

    # NOTE expts streaming raw adc data e.g. time of flight do not support >= 2D sweeps

    # set number of repetitions for this Experiment run
    N.num = 800

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

    ADC_DEMOD = Dataset(
        name="adc_demod",
        plot=True,
        datafn="demod",
        datafn_args={"freq": RR.int_freq, "length": READOUT_PULSE.total_length},
        plot_args={"plot_type": "line", "plot_err": False},
    )
    ADC_DEMOD.initialize(axes=[2, READOUT_PULSE.total_length])  # 1: real, 2: imag
    datasets = [ADC, ADC_FFT, ADC_DEMOD]

    ######################## INITIALIZE AND RUN EXPERIMENT #############################

    expt = TimeOfFlightDemod(FOLDER, modes, pulses, sweeps, datasets, **parameters)
    expt.run()
