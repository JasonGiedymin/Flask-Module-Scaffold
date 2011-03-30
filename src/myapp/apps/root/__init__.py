from myapp import utils

## Required
module_name = utils.getFinalName(__name__)
module = utils.getModule(__name__)

import views
import views.morepages