This folder contains 3 scripts to:
    1. Calibrate the DC offset of the acquired readout pulse (`calibrate_dc_offset.py`)
    2. Get optimal integration weights for a given readout pulse (`integration_weights_training.py`)
    3. Calculate discrimination threshold between G and E states (`threshold_calculation.py`)

These three scripts must be ran IN THIS ORDER every time the length or amplitude of the readout pulse is adjusted or when the time of flight is changed.

The `time_diff_calculation.py` script calculates the time offset that is hardcoded on the ReadoutTrainer. This value is a parameter of the OPX and doesn't change with time.

To reset to constant integration weights, do the following in `update_resources.py` WITHIN the Stage context:

# NOTE `READOUT_PULSE` must be of ReadoutPulse class
from config.experiment_config import READOUT_PULSE

READOUT_PULSE.weights = (1.0, 0.0, 0.0, 1.0)
