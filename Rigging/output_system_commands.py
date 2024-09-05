from rigging_network_nodes import OutputLog


def append_to_output_log(log_entry, log_target_object=""):
    OutputLog.add_to_output_log(log_entry, log_target_object)
    return

def get_current_output_log():
    output = OutputLog.get_output_log()

    return output

def clear_current_output_log():
    OutputLog.clear_output_log()

    return