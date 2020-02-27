from common.constants import *
from common.models import experiment_model as emodel
import rapidjson
import os
import numpy as np

MODEL = emodel.dopa_test_1

td_log, v_log, r_log = MODEL.ctl_model(**MODEL.ctl_kwargs)

with open(os.path.join(LOG_path, LOG_control_name), 'w') as logfile :
    rapidjson.dump({
        str(CTL_TD_LOG) : td_log.tolist(),
        str(CTL_V_LOG) : v_log.tolist(),
        str(CTL_R_LOG) : r_log.tolist(),
    }, logfile)