# Copy and paste this whole text into Maya's python script editor

# Place Maya-Simple-Rigging-Tool folders into C:\Users\[user]\Documents\maya\scripts\
# Edit filepaths then copy the following code into a Maya Python script and run.

# To add the code as a shelf button:
# Select all script text, then Middle-click drag the code up to shelf

import sys

# rename [User directory name] to user account Maya files is installed under
sys.path.append('/Users/[User directory name]/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Metadata')
sys.path.append('/Users/[User directory name]/Documents/maya/scripts/Maya-Simple-Rigging-Tool/QtInterface')
sys.path.append('/Users/[User directory name]/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Rigging')

# initial import
import rigging_user_commands

# Main tool
rigging_user_commands.open_tool()
