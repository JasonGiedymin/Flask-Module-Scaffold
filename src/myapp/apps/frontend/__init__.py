from myapp import utils

## Required
module_name = utils.getFinalName(__name__)
module = utils.getModule(__name__, static_path="/frontend/static")

import views
import views.morepages