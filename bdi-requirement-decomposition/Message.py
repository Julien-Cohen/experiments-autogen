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
init_topic_type = "INIT"


from BDIData import *
# Belief tags
spec_tag = "SPEC"
req_list_tag = "REQ_LIST"

def bdi_eat_message(d: BDIData, m:Message):
    d.add_belief(m.initial_desription, spec_tag) #FIXME : the initial description never changes
    d.add_belief(m.current_list, req_list_tag)