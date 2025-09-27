"""
Arkiver - Universal Data Extraction System
==========================================

A modular, configurable data extraction and categorization system.
"""

__version__ = "2.0.0"
__author__ = "MightyPrytanis"

from .core import DataExtractor
from .config import Config
from .extractors import ConversationExtractor
from .processors import KeywordProcessor
from .outputs import TextFileOutput

__all__ = [
    "DataExtractor",
    "Config", 
    "ConversationExtractor",
    "KeywordProcessor",
    "TextFileOutput"
]