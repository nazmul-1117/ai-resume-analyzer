from fastapi import UploadFile

import pymupdf
import re

class ResumeService:

    def __init__(
            self
    ):
        pass

    async def analyze_resume(
            self,
            *,
            file: UploadFile | None = None
    ) -> str:

        if file is None:
            raise ValueError("File Not Found")

        if file.content_type != "application/pdf":
            raise ValueError("Please upload only pdf file")

        extracted_text = await self._extract_text(file=file)
        cleaned_text = self._clean_text(raw_text=extracted_text)

        return cleaned_text

    async def _extract_text(
            self,
            *,
            file: UploadFile
    ) -> str:

        pdf_bytes = await file.read()

        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        text = ""

        for page in document:
            text += page.get_text()

        return text


    def _clean_text(
            self,
            *,
            raw_text: str
    ) -> str:

        text: str = raw_text.lower().strip()
        text = text.replace("\n", " ")

        text = re.sub(
            r"[^a-z0-9+#./\-\s]",
            "",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()


    def _save_file(
            self,
            *,
            file: UploadFile
    ):
        ...

