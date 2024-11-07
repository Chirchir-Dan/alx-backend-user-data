#!/usr/bin/env python3
"""
This module contains a function to obfuscate specific fields in log messages.
"""

import logging
import re
from typing import List, Tuple

PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter with specific fields to redact.

        Args:
            fields (List[str]): List of field names to be
            redacted in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record by filtering out sensitive fields.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log message with specified fields redacted.
        """
        original_message = super().format(record)
        return filter_datum(
                self.fields, self.REDACTION, original_message, self.SEPARATOR)


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """
    Replaces the values of specified fields in a log message with
    a redaction string.

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


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger with a custom formatter to handle sensitive
    information obfuscation.

    Returns:
        logging.Logger: Configured logger for user data.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger
