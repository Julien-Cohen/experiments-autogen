from dataclasses import dataclass

from bdi_routed_agent import BDIRoutedAgent


# Message Protocol


@dataclass
class Message:
    initial_description: str
    current_list: str
    atomic_requirement_tentative: str = None
    validation: str = None


# Topics

cut_request_topic_type = "CUT"
validation_request_topic_type = "VALIDATION_REQ"
validation_result_topic_type = "VALIDATION_RES"
init_topic_type = "INIT"


from bdi_data import *

# Belief tags
spec_tag = "SPEC"
req_list_tag = "REQ_LIST"


def bdi_observe_message(d: BDIRoutedAgent, m: Message):
    d.update_belief(m.initial_description, spec_tag)
    d.update_belief(m.current_list, req_list_tag)


def message__bdi_observe_message(d: BDIRoutedAgent, m: Message):
    bdi_observe_message(d, m)
