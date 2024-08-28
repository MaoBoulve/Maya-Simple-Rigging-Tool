import sys

# rename [User directory name] to user account Maya files is installed under
sys.path.append('/Users/cmendoza/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Metadata')
sys.path.append('/Users/cmendoza/Documents/maya/scripts/Maya-Simple-Rigging-Tool/QtInterface')
sys.path.append('/Users/cmendoza/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Validator')
sys.path.append('/Users/cmendoza/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Rigging')

# initial import
import rigging_tasks
import simple_rigging_tool_widget
import importlib
import qt_maya_widget_base

# reimport
importlib.reload(rigging_tasks)
importlib.reload(simple_rigging_tool_widget)
importlib.reload(qt_maya_widget_base)

# main testing
# rigging_tasks.test()

rig_widget = simple_rigging_tool_widget.SimpleRigToolWindowWidget()
rig_widget.show()