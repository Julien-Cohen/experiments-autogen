from dataclasses import dataclass

from bdi.bdi_data import *
from bdi.bdi_component import *


# Message Protocol


@dataclass
class Message:
    initial_description: str
    current_list: str
    atomic_requirement_tentative: str = None
    validation: str = None


# Topics

cut_request_topic_type = "CUT"
correctness_validation_request_topic_type = "CORRECTNESS_VALIDATION_REQ"
non_redundancy_validation_request_topic_type = "NON_REDUNDANCY_VALIDATION_REQ"
satisfiability_validation_request_topic_type = "SATISFIABILITY_VALIDATION_REQ"
validation_result_topic_type = "VALIDATION_RES"
init_topic_type = "INIT"


# Belief tags
spec_tag = "SPEC"
req_list_tag = "REQ_LIST"

# validation tags
correctness_validated = "CORRECT"
correctness_invalidated = "INCORRECT"
non_redundancy_validated = "NOT_REDUNDANT"
non_redundancy_invalidated = "REDUNDANT"
satisfiability_validated = "SATISFIABLE"
satisfiability_invalidated = "NOT_SATISFIABLE"


def message__bdi_observe_message(d: BDIComponent, m: Message):
    d.update_belief(m.initial_description, spec_tag)
    d.update_belief(m.current_list, req_list_tag)
