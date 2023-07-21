""" Calibrate DC offset for optimized readout """

from qcore import Stage
from qcore.instruments import QM
from qm import qua
import numpy as np

from config.experiment_config import MODES_CONFIG

def get_qua_program(rr, dc_offset_op):

    with qua.program() as cal_dc:

        adc = qua.declare_stream(adc_trace=True)
        qua.reset_phase(rr.name)
        qua.measure(dc_offset_op, rr.name, adc)

        with qua.stream_processing():
            adc.input1().save("adc")

    return cal_dc


if __name__ == "__main__":
    """ """

    with Stage(configpath=MODES_CONFIG, remote=True) as stage:

        rr, lo_rr = stage.get("rr", "lo_rr")
        
        dc_offset_pulse_name = "rr_readout_pulse"

        # Reset DC offset of readout mode to be calibrated
        to_update = {"out": 0.0}
        rr.mixer_offsets = {**rr.mixer_offsets, **to_update}

        qm = QM(modes=(rr,), oscillators=(lo_rr,))

        # Execute script
        job = qm.execute(get_qua_program(rr, dc_offset_pulse_name))

        handle = job.result_handles
        handle.wait_for_all_values()
        adc_avg = np.mean(handle.get("adc").fetch_all())
        dc_offset = -adc_avg * (2 ** -12)

        # Update DC offset of readout mode to be calibrated
        to_update = {"out": dc_offset}
        rr.mixer_offsets = {**rr.mixer_offsets, **to_update}
