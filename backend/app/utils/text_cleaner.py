import re

class TextCleaner:

    @classmethod
    def clean(
                self,
                *,
                raw_text: str
        ) -> str:
    
            text: str = raw_text.strip()
            
            # Normalzie line breaks
            text = text.replace("\r\n", "\n")
            text = text.replace("\r", "\n")
    
            # replace multiple line breaks
            text = re.sub(
                # r"[^a-z0-9+#./\-\s]",
                r"\n+",
                "\n",
                text,
            )
    
            text = re.sub(
                r"[ \t]+",
                " ",
                text,
            )
    
            return text.strip()