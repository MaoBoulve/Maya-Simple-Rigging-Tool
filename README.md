
# Overview
This tool is a simple rigging helper tool for Maya. It automates common rigging and control setup tasks.

Metadata modules provided courtesy of Micah Zahm

**Skeleton Joint Setup**
  - Save & Load Rig Templates from a JSON file
  - Mirror rig across XY/YZ/ZX planes

**Rig Control Setup**
  - Create and auto-rename controls on top of joints
  - Constrain controls on joints
  - Mirror control hierarchy across XY/YZ/ZX planes

**Weight Painting Tasks**
  - Flood mesh with weight paint from a joint
  - Flood vertex with weight paint value from a joint

# Setup

1. Place 'Maya-Simple-Rigging-Tool' folder into Maya scripts directory.

Default Maya script directory is at **C:\Users\\[Username]\Documents\maya\scripts**

![img_1.png](img_1.png)

2. Open Maya script editor

![img.png](img.png)

3. Edit filepath in following code block, then paste into a **Python** script editor

'''    

    import sys

    # rename [User directory name] to user account Maya files is installed under
    sys.path.append('/Users/[User directory name]/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Metadata')
    sys.path.append('/Users/[User directory name]/Documents/maya/scripts/Maya-Simple-Rigging-Tool/QtInterface')
    sys.path.append('/Users/[User directory name]/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Rigging')
    
    # initial import
    import rigging_user_commands
    
    # Main tool
    rigging_user_commands.open_tool()

'''
    
![img_3.png](img_3.png)

4. Create a Toolbar Button for ease of use by middle-click dragging script text

![img_2.png](img_2.png)