from myapp import utils

## Required
module_name = utils.getFinalName(__name__)
module = utils.getModule(__name__, subdomain=module_name)

import views
import views.morepages