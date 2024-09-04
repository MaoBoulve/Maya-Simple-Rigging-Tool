import sys

# rename [User directory name] to user account Maya files is installed under
sys.path.append('/Users/cmendoza/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Metadata')
sys.path.append('/Users/cmendoza/Documents/maya/scripts/Maya-Simple-Rigging-Tool/QtInterface')
sys.path.append('/Users/cmendoza/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Rigging')

# initial import
import rigging_tasks
import rigging_user_commands
import simple_rigging_tool_widget
import importlib
import rigging_network_nodes

# reimport
importlib.reload(rigging_user_commands)
importlib.reload(rigging_tasks)
importlib.reload(simple_rigging_tool_widget)
importlib.reload(rigging_network_nodes)

# main testing

rigging_tasks.TDD_test_task()