from dataclasses import dataclass
from enum import Enum


@dataclass
class MockMail:
    body: str = ''
    html: str = ''


class MockEnum(Enum):
    """Demo Enum for testing."""
    demo_1 = 1
    demo_2 = 2
    demo_3 = 3
    demo_4 = 4
