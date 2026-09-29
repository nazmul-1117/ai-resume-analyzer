from abc import ABC, abstractmethod

class BaseResumeParser(ABC):

    @abstractmethod
    async def extract_text(
            self,
            *,
            file_bytes: bytes
    ) -> str:

        """
        Extract raw text from a resume file
        """

        raise NotImplementedError