import pymupdf
from app.parsers.base_parser import BaseResumeParser 

class PDFResumeParser(BaseResumeParser):


    async def extract_text(
            self,
            *,
            file_bytes: bytes
    ) -> str:

        try:
            document = pymupdf.open(
                stream=file_bytes,
                filetype="pdf"
            )

        except Exception as exc:
            raise ValueError(
                "The uploaded file is not a valid pdf."
            ) from exc


        try:
            text_parts: list[str] = [""]

            for page in document:
                page_text = page.get_text()

                if page_text:
                    text_parts.append(page_text)

            return "\n".join(text_parts)

        finally:
            document.close()