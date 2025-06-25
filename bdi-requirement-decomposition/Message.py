from dataclasses import dataclass

# Message Protocol

@dataclass
class Message:
    initial_desription: str
    current_list : str
    atomic_requirement_tentative : str = None
    validation:str = None


# Topics

cut_request_topic_type = "CUT"
validation_request_topic_type = "VALIDATION_REQ"
validation_result_topic_type = "VALIDATION_RES"
addition_request_topic_type = "ADD"
init_topic_type = "INIT"