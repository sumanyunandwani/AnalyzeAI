"""
Backend/services/api/utility/prodels/get_podel.py
This module defines a singleton class to manage Podels from a YAML file.
It provides methods to read the YAML file and retrieve Podel nodes based on tags.
"""
from dataclasses import dataclass
from typing import Optional, List
import asyncio
import logging
import os
import yaml
from core.custom_logger import CustomLogger

@dataclass
class PodelNode:
    """
    Represents a node in the Podel linked list.
    """
    prev: Optional["PodelNode"] = None
    next: Optional["PodelNode"] = None
    prompt: str = ""
    need_history: bool = True
    need_answer: Optional[str] = None
    error_message_dict: Optional[dict] = None

class Podel:
    """
    Singleton class to manage SQL Podels from a YAML file.

    Returns:
        Podel: The singleton instance of Podel.
    """
    _instance = None
    _lock = asyncio.Lock()  # Lock for thread-safe singleton instantiation

    @classmethod
    async def get_instance(cls) -> "Podel":
        """
        Asynchronous singleton enforcement to get the instance of Podel.

        Returns:
            Podel: The singleton instance of Podel.
        """
        if cls._instance is None:
            async with cls._lock:
                if cls._instance is None:  # Double-check
                    cls._instance = cls()
        return cls._instance

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or CustomLogger.setup_logger(__name__)
        self._yml_file_path = os.path.join(
            os.path.dirname(__file__), "podel.yml"
        )
        self.podels = self._get_all_podels()

    def _get_all_podels(self) -> List[PodelNode]:
        """
        Reads the YAML file and returns a list of PodelNode instances.
        """
        with open(self._yml_file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        podels = {}

        for tag, list_of_prompts_dict in data.get('podels', {}).items():

            _head = None

            for prompt_dict in list_of_prompts_dict:
                self.logger.debug(f"Prompt Dict: {prompt_dict}")
                prompt = prompt_dict.get('prompt', '')
                need_history = prompt_dict.get('need_history', True)
                need_answer = prompt_dict.get('need_answer', None)
                error_message_dict = prompt_dict.get('error_message', None)
                node = PodelNode(
                    prompt=prompt,
                    need_history=need_history,
                    need_answer=need_answer,
                    error_message_dict=error_message_dict
                )
                if _head is None:
                    _head = node
                    podels[tag] = _head
                else:
                    node.prev = _head
                    _head.next = node
                    _head = node

        return podels

    def get_podel(self, tag: str) -> Optional[PodelNode]:
        """
        Returns the head of the Podel linked list for the given tag.
        
        Args:
            tag (str): The tag for which to retrieve the Podel.
        
        Returns:
            Optional[PodelNode]: The head of the Podel linked list or None if not found.
        """
        self.logger.debug("Retrieving Podel for tag: %s", tag)
        self.logger.debug("Available Podels: %s", list(self.podels.keys()))
        self.logger.info("Podel gathered for tag: %s is %s", tag, self.podels.get(tag, None))
        return self.podels.get(tag, None)
