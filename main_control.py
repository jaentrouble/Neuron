from common.constants import *
from common.models import experiment_model as emodel
MODEL = emodel.dopa_test_1

MODEL.ctl_model(**MODEL.ctl_kwargs)