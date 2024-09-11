import sys

# rename [User directory name] to user account Maya files is installed under
sys.path.append('/Users/ceeja/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Metadata')
sys.path.append('/Users/ceeja/Documents/maya/scripts/Maya-Simple-Rigging-Tool/QtInterface')
sys.path.append('/Users/ceeja/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Rigging')

# initial import
import rigging_user_commands
import skeleton_tab_widget
import rig_control_tab_widget
import simple_rigging_tool_widget
import rigging_system_commands
import rigging_tasks
import importlib

# reimport
importlib.reload(rigging_user_commands)
importlib.reload(skeleton_tab_widget)
importlib.reload(rig_control_tab_widget)
importlib.reload(simple_rigging_tool_widget)
importlib.reload(rigging_system_commands)
importlib.reload(rigging_tasks)

# main testing

# rigging_tasks.TDD_test_task()
rigging_user_commands.open_simple_rig_tool()