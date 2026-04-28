from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseVerifier(ABC):
    """
    Abstract base class for all verifiers in Mythos-Safe.
    Ensures consistent interface across code, math, and cyber verifiers.
    """

    @abstractmethod
    def verify(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        """
        Core verification method.
        
        Returns:
            dict with at least:
            - "reward": float between 0.0 and 1.0
            - "details": dict with detailed metrics
        """
        pass

    def __call__(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        """Make verifier callable for convenience."""
        return self.verify(prompt, response, **kwargs)