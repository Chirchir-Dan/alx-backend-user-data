#!/usr/bin/env python3
"""
This module contains a function to obfuscate specific fields in log messages.
"""

import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Replaces the values of specified fields in a log message with a redaction string.

    Args:
        fields (List[str]): List of field names to obfuscate.
        redaction (str): The string to replace each field's value with.
        message (str): The original log message.
        separator (str): The character that separates fields in the message.

    Returns:
        str: The log message with specified fields obfuscated.
    """
    pattern = f'({"|".join(fields)})=([^;{separator}]+)'
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
