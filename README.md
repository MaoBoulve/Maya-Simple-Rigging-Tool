This tool is a generic game asset validator for Maya. It allows a user to tag assets as part of Prop, Animation, and Character groups and validate for common asset requirements (detailed below).

Metadata modules provided courtesy of Micah Zahm

**Character Validation Checks**
  - Character Mesh only using valid list of materials
  - Character Mesh Hierarchy only consists of mesh shape objects
  - Character Mesh rigged with skin binding influence only coming from tagged rig joints
  - Rig Hierarchy consists of only joint objects
  - Rig Hierarchy consists of no keyed frames in specified timeframe

**Animation Validation Checks**
  - Rig Hierarchy consists of only joint objects
  - Rig keyed for specified transform attributes, no floating point keys, in specified timeframe

**Prop Validation Checks**
  - Mesh only using valid list of materials
  - Mesh Hierarchy only consists of mesh shape objects
  - Mesh Node connections to prop has no rig influence
  - Mesh has no keyed attributes in specified timeframe
  - Collision Meshes are present, searching with user defined prefix

Following code block should be copied into the Maya script editor and run.

'''
    
    # Place Metadata, QInterface, and Validator folders into .../Documents/maya/scripts/ folder
    # Edit filepaths then copy the following code into a Maya Python script and run.
    # To add the code as a shelf button: Hit Ctrl + A, then Middle Click-dragging the code up to shelf
    
    
    import sys

    # rename [User directory name] to user account Maya files is installed under
    sys.path.append('/Users/[User directory name]/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Metadata')
    sys.path.append('/Users/[User directory name]/Documents/maya/scripts/Maya-Simple-Rigging-Tool/QtInterface')
    sys.path.append('/Users/[User directory name]/Documents/maya/scripts/Maya-Simple-Rigging-Tool/Rigging')
    
    # initial import
    import rigging_user_commands
    
    # Main tool
    rigging_user_commands.open_simple_rig_tool()


'''