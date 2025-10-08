from dataclasses import dataclass

# Message Protocol

@dataclass
class Message:
    desire: str = None
    options : str = None
    intention : str = None
    validation: str = None


# Topics

desire_topic_type = "DESIRE"
option_topic_type = "OPTIONS"
intention_topic_type = "INTENTION"
validated_topic_type = "VALIDATED"