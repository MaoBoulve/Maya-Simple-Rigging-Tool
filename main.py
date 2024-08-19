import sys

# rename [User directory name] to user account Maya files is installed under
sys.path.append('/Users/cmendoza/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Metadata')
sys.path.append('/Users/cmendoza/Documents/maya/scripts/Maya-Simple-Rigging-Tool/QtInterface')
sys.path.append('/Users/cmendoza/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Validator')
sys.path.append('/Users/cmendoza/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Rigging')

# initial import
import rigging_tasks
import importlib

# reimport
importlib.reload(rigging_tasks)

# main testing
rigging_tasks.test()

