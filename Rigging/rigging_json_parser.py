from json_file_parser import FileWriter, FileReader


class RiggingJSONDataManagement:
    __json_filename = "rigging_joint_bases.json"

    """
    Class for reading validation settings from json class, converting inputs to format usable by metadata system

    Assumes JSON file is in the Validator folder & is named validator_settings.json. Need to match parameter order
    of each settings metadata node.
    """

    @classmethod
    def get_joint_list(cls, list_name_query="list_name"):
        """

        """

        json_data = FileReader.get_json_data(cls.__json_filename)

        joint_list = []

        if json_data:
            joint_list = list(json_data[list_name_query])

        return joint_list

    @classmethod
    def add_joint_list_to_json_file(cls, joint_entry_list, list_name):
        """
        Adds a new entry to json file.
        :param joint_entry_list: List of entries in format [joint_name, [x,y,z] world position, parent_joint_name]
        :param list_name: Name of entry for getting list
        """

        FileWriter.write_json_value(entry_key=list_name, entry_value=joint_entry_list, json_filename=cls.__json_filename)

        return