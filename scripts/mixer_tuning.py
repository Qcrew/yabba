""" """

from qcore.helpers import Stage
from qcore.scripts.mixer_tuning import MixerTuner

from config.experiment_config import MODES_CONFIG

if __name__ == "__main__":
    """ """

    # Mixer tuning must be done within the Stage context if you want the mixer offsets to be saved in the modes config
    with Stage(configpath=MODES_CONFIG, remote=True) as stage:
        #################### RETRIEVE RESOURCES FROM THE STAGE #########################

        SA, QUBIT, QUBITEF, RR, CAV = stage.get("sa", "qubit", "qubitEF", "rr", "cav")

        ########### INITIALIZE THE MIXER TUNER WITH THE SPECTRUM ANALYZER ##############

        mixer_tuner = MixerTuner(SA)

        ############ SET THE MODE WHOSE LO OR SB LEAKAGE IS TO BE TUNED ################

        mode = CAV

        ########################### MINIMIZE LO LEAKAGE ################################

        # use brute force (BF) minimizer
        bf_params_lo = {
            # range of DC offsets you want to sweep to tune LO
            "offset_range": (-0.5, 0.5),  # (min = -0.5, max = 0.5)
            # number of DC offset sweep points in the given range i.e. decide step size
            "num_points": 21,
            # number of iterations of the minimization you want to run
            "num_iterations": 5,
            # after each iteration, the sweep range will be reduced by this factor
            "range_divider": 2,
            # if you want the full minimization traceback, set this to True
            "verbose": True,
            # if you want a plot that shows minimization summary, set this to True
            "plot": False,
        }

        # mixer_tuner.tune_lo(mode=mode, method="BF", **bf_params_lo)

        # user Nelder-Mead (NM) minimizer
        # mixer_tuner.tune_lo(mode=mode, method="NM")

        ########################### MINIMIZE SB LEAKAGE ################################

        # use brute force (BF) minimizer
        bf_params_sb = {
            # range of DC offsets you want to sweep to tune LO
            "offset_range": (-0.5, 0.5),  # (min = -0.5, max = 0.5)
            # number of DC offset sweep points in the given range i.e. decide step size
            "num_points": 21,
            # number of iterations of the minimization you want to run
            "num_iterations": 5,
            # after each iteration, the sweep range will be reduced by this factor
            "range_divider": 2,
            # if you want the full minimization traceback, set this to True
            "verbose": True,
            # if you want a plot that shows minimization summary, set this to True
            "plot": False,
        }

        # mixer_tuner.tune_sb(mode=mode, method="BF", **bf_params_lo)

        # user Nelder-Mead (NM) minimizer
        mixer_tuner.tune_sb(mode=mode, method="NM")
