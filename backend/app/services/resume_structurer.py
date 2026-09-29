import re

from app.schemas.resume_schema import (
    PersonalInfo,
    ResumeProfile,
    Education,
    Experience,
    Project,
    Certification,
)


class ResumeStructurer:
    """
    Converts extracted resume text into a structured ResumeProfile.
    """

    # ------------------------------------------------------------------
    # REGEX PATTERNS
    # ------------------------------------------------------------------

    EMAIL_PATTERN = re.compile(
        r"\b[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    PHONE_PATTERN = re.compile(
        r"(?<!\d)"
        r"(?:\+\d{1,3}[\s.-]?)?"
        r"(?:\(\d{3}\)|\d{3})"
        r"[\s.-]?"
        r"\d{3}"
        r"[\s.-]?"
        r"\d{4}"
        r"(?!\d)"
    )

    URL_PATTERN = re.compile(
        r"(?:https?://)?"
        r"(?:www\.)?"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
        r"(?:/[^\s|]+)?"
    )

    DATE_RANGE_PATTERN = re.compile(
        r"^("
        r"\d{1,2}/\d{1,2}/\d{4}"
        r"|"
        r"\d{4}"
        r"|"
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
        r"[a-z]*\.?\s+\d{4}"
        r"|"
        r"\d{1,2}\s+"
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
        r"[a-z]*\.?\s+\d{4}"
        r")"
        r"\s*[-–—]\s*"
        r"(Present|Current|Now|"
        r"\d{1,2}/\d{1,2}/\d{4}"
        r"|"
        r"\d{4}"
        r"|"
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
        r"[a-z]*\.?\s+\d{4}"
        r"|"
        r"\d{1,2}\s+"
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
        r"[a-z]*\.?\s+\d{4}"
        r")$",
        re.IGNORECASE,
    )

    YEAR_RANGE_PATTERN = re.compile(
        r"^(\d{4})\s*[-–—]\s*(\d{4}|Present|Current)$",
        re.IGNORECASE,
    )

    SECTION_ALIASES = {
        # Skills
        "SKILLS": "SKILLS",
        "TECHNICAL SKILLS": "SKILLS",
        "TECHNOLOGIES": "SKILLS",

        # Education
        "EDUCATION": "EDUCATION",
        "ACADEMIC BACKGROUND": "EDUCATION",

        # Experience
        "EXPERIENCE": "EXPERIENCE",
        "WORK EXPERIENCE": "EXPERIENCE",
        "PROFESSIONAL EXPERIENCE": "EXPERIENCE",
        "EMPLOYMENT": "EXPERIENCE",
        "EMPLOYMENT HISTORY": "EXPERIENCE",

        # Research
        "RESEARCH EXPERIENCE": "RESEARCH_EXPERIENCE",

        # Projects
        "PROJECTS": "PROJECTS",
        "PERSONAL PROJECTS": "PROJECTS",
        "ACADEMIC PROJECTS": "PROJECTS",
        "SELECTED PROJECTS": "PROJECTS",

        # Certifications
        "CERTIFICATIONS": "CERTIFICATIONS",
        "CERTIFICATION": "CERTIFICATIONS",
        "CERTIFICATES": "CERTIFICATIONS",
        "CERTIFICATE": "CERTIFICATIONS",

        # Publications
        "PUBLICATIONS": "PUBLICATIONS",
        "PUBLICATIONS AND PATENTS": "PUBLICATIONS",
        "PUBLICATIONS & PATENTS": "PUBLICATIONS",
        "PATENTS": "PUBLICATIONS",

        # Achievements
        "ACHIEVEMENTS": "ACHIEVEMENTS",
        "SCHOLASTIC ACHIEVEMENTS": "ACHIEVEMENTS",
        "AWARDS": "ACHIEVEMENTS",
        "HONORS": "ACHIEVEMENTS",
        "HONORS AND AWARDS": "ACHIEVEMENTS",

        # Languages
        "LANGUAGES": "LANGUAGES",

        # Summary
        "SUMMARY": "SUMMARY",
        "PROFESSIONAL SUMMARY": "SUMMARY",
        "PROFILE": "SUMMARY",
        "OBJECTIVE": "SUMMARY",
        "CAREER OBJECTIVE": "SUMMARY",
    }

    # ------------------------------------------------------------------
    # MAIN METHOD
    # ------------------------------------------------------------------

    def structure(self, text: str) -> ResumeProfile:
        """
        Convert raw resume text into ResumeProfile.
        """

        if not text or not text.strip():
            return ResumeProfile()

        sections = self._extract_sections(text)

        personal_info = self._extract_personal_info(text)

        summary = self._extract_summary(
            sections.get("SUMMARY", "")
        )

        skills = self._extract_skills(
            sections.get("SKILLS", "")
        )

        education = self._extract_education(
            sections.get("EDUCATION", "")
        )

        experience = self._extract_experience(
            sections.get("EXPERIENCE", "")
        )

        research_experience = self._extract_experience(
            sections.get("RESEARCH_EXPERIENCE", "")
        )

        experience.extend(research_experience)

        projects = self._extract_projects(
            sections.get("PROJECTS", "")
        )

        certifications = self._extract_certifications(
            sections.get("CERTIFICATIONS", "")
        )

        publications = self._extract_list_section(
            sections.get("PUBLICATIONS", "")
        )

        achievements = self._extract_list_section(
            sections.get("ACHIEVEMENTS", "")
        )

        languages = self._extract_languages(
            sections.get("LANGUAGES", "")
        )

        return ResumeProfile(
            personal_info=personal_info,
            summary=summary,
            skills=skills,
            education=education,
            experience=experience,
            projects=projects,
            certifications=certifications,
            publications=publications,
            achievements=achievements,
            languages=languages,
        )

    # ------------------------------------------------------------------
    # SECTION EXTRACTION
    # ------------------------------------------------------------------

    def _extract_sections(
        self,
        text: str,
    ) -> dict[str, str]:

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        sections: dict[str, list[str]] = {}

        current_section = None

        for line in lines:

            normalized = self._normalize_heading(line)

            section_name = self.SECTION_ALIASES.get(
                normalized
            )

            if section_name:
                current_section = section_name
                sections.setdefault(current_section, [])
                continue

            if current_section:
                sections[current_section].append(line)

        return {
            key: "\n".join(value)
            for key, value in sections.items()
        }

    @staticmethod
    def _normalize_heading(line: str) -> str:
        """
        Normalize headings such as:
        'EXPERIENCE'
        'Experience'
        'EXPERIENCE:'
        """

        line = line.strip()

        line = re.sub(
            r"^[•*\-–—]+\s*",
            "",
            line,
        )

        line = line.rstrip(":").strip()

        return re.sub(
            r"\s+",
            " ",
            line.upper(),
        )

    # ------------------------------------------------------------------
    # PERSONAL INFORMATION
    # ------------------------------------------------------------------

    def _extract_personal_info(
        self,
        text: str,
    ) -> PersonalInfo:

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        email_match = self.EMAIL_PATTERN.search(text)

        phone_match = self.PHONE_PATTERN.search(text)

        # Remove email from URL detection.
        text_without_email = self.EMAIL_PATTERN.sub(
            "",
            text,
        )

        # Remove phone number too.
        if phone_match:
            text_without_email = (
                text_without_email.replace(
                    phone_match.group(0),
                    "",
                )
            )

        urls = self.URL_PATTERN.findall(
            text_without_email
        )

        return PersonalInfo(
            name=self._extract_name(lines),

            email=(
                email_match.group(0)
                if email_match
                else None
            ),

            phone=(
                phone_match.group(0)
                if phone_match
                else None
            ),

            location=self._extract_location(lines),

            linkedin=self._find_link(
                urls,
                "linkedin",
            ),

            github=self._find_link(
                urls,
                "github",
            ),

            portfolio=self._find_portfolio(
                urls,
                [
                    "linkedin",
                    "github",
                ],
            ),
        )

    @staticmethod
    def _extract_name(
        lines: list[str],
    ) -> str | None:

        if not lines:
            return None

        first_line = lines[0]

        # Ignore obvious non-name lines.
        if (
            "@" in first_line
            or "http" in first_line.lower()
            or "linkedin" in first_line.lower()
            or "github" in first_line.lower()
            or re.search(r"\d{3,}", first_line)
        ):
            return None

        return first_line.strip()

    @staticmethod
    def _extract_location(
        lines: list[str],
    ) -> str | None:

        for line in lines[:10]:

            if "@" in line:
                continue

            if (
                "linkedin" in line.lower()
                or "github" in line.lower()
            ):
                continue

            parts = re.split(
                r"[|•]",
                line,
            )

            for part in parts:

                part = part.strip()

                if not part:
                    continue

                # City, State
                if re.fullmatch(
                    r"[A-Za-z .'-]+,\s*[A-Za-z .'-]+",
                    part,
                ):
                    return part

                # City, State, Country
                if re.fullmatch(
                    r"[A-Za-z .'-]+,\s*"
                    r"[A-Za-z .'-]+,\s*"
                    r"[A-Za-z .'-]+",
                    part,
                ):
                    return part

        return None

    @staticmethod
    def _find_link(
        urls: list[str],
        keyword: str,
    ) -> str | None:

        for url in urls:

            if keyword.lower() in url.lower():
                return url

        return None

    @staticmethod
    def _find_portfolio(
        urls: list[str],
        excluded: list[str],
    ) -> str | None:

        for url in urls:

            lower_url = url.lower()

            if any(
                keyword.lower() in lower_url
                for keyword in excluded
            ):
                continue

            return url

        return None

    # ------------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_summary(
        section: str,
    ) -> str | None:

        if not section:
            return None

        lines = [
            line.strip()
            for line in section.splitlines()
            if line.strip()
        ]

        if not lines:
            return None

        return " ".join(lines)

    # ------------------------------------------------------------------
    # SKILLS
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_skills(
        section: str,
    ) -> list[str]:

        if not section:
            return []

        skills = []

        category_labels = {
            "languages",
            "tools",
            "libraries",
            "programming",
            "frameworks",
            "devops",
            "cloud",
            "cloud providers",
            "databases",
            "database",
            "technologies",
            "technical skills",
        }

        for line in section.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.lower().rstrip(":") in category_labels:
                continue

            # Remove bullet.
            line = re.sub(
                r"^[•*\-–—]\s*",
                "",
                line,
            )

            if not line:
                continue

            # Handle comma / pipe / semicolon separated skills.
            parts = re.split(
                r"[,;|]",
                line,
            )

            for skill in parts:

                skill = skill.strip()

                if skill:
                    skills.append(skill)

        return ResumeStructurer._unique_preserve_order(
            skills
        )

    # ------------------------------------------------------------------
    # EDUCATION
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_education(
        section: str,
    ) -> list[Education]:

        if not section:
            return []

        lines = [
            line.strip()
            for line in section.splitlines()
            if line.strip()
        ]

        education = []

        current = Education()

        for line in lines:

            clean_line = re.sub(
                r"^[•*\-–—]\s*",
                "",
                line,
            ).strip()

            # Date range
            date_match = re.search(
                r"(\d{4})\s*[-–—]\s*(\d{4}|Present|Current)",
                clean_line,
                re.IGNORECASE,
            )

            if date_match:

                current.start_date = (
                    date_match.group(1)
                )

                current.end_date = (
                    date_match.group(2)
                )

                continue

            lower = clean_line.lower()

            # Degree
            degree_keywords = (
                "bachelor",
                "master",
                "b.tech",
                "m.tech",
                "b.sc",
                "m.sc",
                "b.e.",
                "m.e.",
                "phd",
                "doctor of",
                "associate",
                "diploma",
            )

            if any(
                keyword in lower
                for keyword in degree_keywords
            ):

                if "," in clean_line:

                    degree, field = (
                        clean_line.split(
                            ",",
                            1,
                        )
                    )

                    current.degree = (
                        degree.strip()
                    )

                    current.field_of_study = (
                        field.strip()
                    )

                else:

                    current.degree = clean_line

                continue

            # Institution
            institution_keywords = (
                "university",
                "institute",
                "college",
                "school",
                "academy",
            )

            if any(
                keyword in lower
                for keyword in institution_keywords
            ):

                current.institution = clean_line
                continue

            # Description
            if current.institution:
                if current.description:
                    current.description += (
                        " " + clean_line
                    )
                else:
                    current.description = clean_line

        if (
            current.degree
            or current.institution
        ):
            education.append(current)

        return education

    # ------------------------------------------------------------------
    # EXPERIENCE
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_experience(
        section: str,
    ) -> list[Experience]:

        if not section:
            return []

        lines = [
            line.strip()
            for line in section.splitlines()
            if line.strip()
        ]

        experiences = []

        date_pattern = re.compile(
            r"^("
            r"\d{1,2}/\d{1,2}/\d{4}"
            r"|"
            r"\d{4}"
            r"|"
            r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
            r"[a-z]*\.?\s+\d{4}"
            r")"
            r"\s*[-–—]\s*"
            r"(Present|Current|Now|"
            r"\d{1,2}/\d{1,2}/\d{4}"
            r"|"
            r"\d{4}"
            r"|"
            r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
            r"[a-z]*\.?\s+\d{4}"
            r")$",
            re.IGNORECASE,
        )

        i = 0

        while i < len(lines):

            date_match = date_pattern.match(
                lines[i]
            )

            if not date_match:
                i += 1
                continue

            start_date = (
                date_match.group(1)
            )

            end_date = (
                date_match.group(2)
            )

            # Most common format:
            #
            # Position
            # Date
            # Company
            # Location
            #
            position = (
                lines[i - 1]
                if i > 0
                else None
            )

            company = (
                lines[i + 1]
                if i + 1 < len(lines)
                else None
            )

            location = (
                lines[i + 2]
                if i + 2 < len(lines)
                else None
            )

            # Detect bullets after location.
            achievements = []

            j = i + 3

            current_bullet = None

            while j < len(lines):

                current_line = lines[j]

                # Next experience.
                if date_pattern.match(
                    current_line
                ):
                    break

                if current_line.startswith(
                    ("•", "*", "▪", "●", "◦")
                ):

                    if current_bullet:
                        achievements.append(
                            current_bullet
                        )

                    current_bullet = re.sub(
                        r"^[•*▪●◦]\s*",
                        "",
                        current_line,
                    ).strip()

                else:

                    # Continuation of previous bullet.
                    if current_bullet:
                        current_bullet += (
                            " " + current_line
                        )

                j += 1

            if current_bullet:
                achievements.append(
                    current_bullet
                )

            experiences.append(
                Experience(
                    company=company,
                    position=position,
                    location=location,
                    start_date=start_date,
                    end_date=end_date,
                    description=None,
                    achievements=achievements,
                )
            )

            i = j

        return experiences

    # ------------------------------------------------------------------
    # PROJECTS
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_projects(
        section: str,
    ) -> list[Project]:

        if not section:
            return []

        projects = []

        lines = [
            line.strip()
            for line in section.splitlines()
            if line.strip()
        ]

        current_project = None
        description_parts = []

        def save_current_project():

            nonlocal current_project
            nonlocal description_parts

            if not current_project:
                return

            description = " ".join(
                description_parts
            ).strip()

            projects.append(
                Project(
                    name=current_project,
                    description=description or None,
                    technologies=[],
                    url=None,
                )
            )

            current_project = None
            description_parts = []

        for line in lines:

            # Remove bullet.
            clean_line = re.sub(
                r"^[•*▪●◦]\s*",
                "",
                line,
            ).strip()

            if not clean_line:
                continue

            # Format:
            #
            # ScaleETL - Description
            #
            if " - " in clean_line:

                save_current_project()

                name, description = (
                    clean_line.split(
                        " - ",
                        1,
                    )
                )

                current_project = name.strip()

                description_parts = [
                    description.strip()
                ]

                continue

            # If the line starts with a bullet
            # and there is no " - ", consider it
            # a new project.
            if line.startswith(
                ("•", "*", "▪", "●", "◦")
            ):

                save_current_project()

                current_project = clean_line
                description_parts = []

                continue

            # Continuation line.
            if current_project:
                description_parts.append(
                    clean_line
                )

        save_current_project()

        return projects

    # ------------------------------------------------------------------
    # CERTIFICATIONS
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_certifications(
        section: str,
    ) -> list[Certification]:

        if not section:
            return []

        certifications = []

        lines = [
            line.strip()
            for line in section.splitlines()
            if line.strip()
        ]

        for line in lines:

            clean_line = re.sub(
                r"^[•*▪●◦]\s*",
                "",
                line,
            ).strip()

            if not clean_line:
                continue

            name = clean_line
            issuer = None
            date = None
            credential_url = None

            # Detect URL.
            url_match = ResumeStructurer.URL_PATTERN.search(
                clean_line
            )

            if url_match:
                credential_url = (
                    url_match.group(0)
                )

                name = (
                    clean_line
                    .replace(
                        credential_url,
                        "",
                    )
                    .strip(
                        " |-–—"
                    )
                )

            # Format:
            # Certificate Name - Issuer
            if " - " in name:

                parts = name.split(
                    " - ",
                    1,
                )

                name = parts[0].strip()
                issuer = parts[1].strip()

            # Try to extract date.
            date_match = re.search(
                r"\b(19|20)\d{2}\b",
                name,
            )

            if date_match:

                date = date_match.group(0)

                name = (
                    name[:date_match.start()]
                    +
                    name[date_match.end():]
                ).strip(
                    " ,|-–—"
                )

            certifications.append(
                Certification(
                    name=name,
                    issuer=issuer,
                    date=date,
                    credential_url=credential_url,
                )
            )

        return certifications

    # ------------------------------------------------------------------
    # GENERIC LIST SECTIONS
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_list_section(
        section: str,
    ) -> list[str]:

        if not section:
            return []

        items = []

        lines = [
            line.strip()
            for line in section.splitlines()
            if line.strip()
        ]

        current_item = None

        for line in lines:

            if line.startswith(
                ("•", "*", "▪", "●", "◦")
            ):

                if current_item:
                    items.append(
                        current_item
                    )

                current_item = re.sub(
                    r"^[•*▪●◦]\s*",
                    "",
                    line,
                ).strip()

            else:

                if current_item:
                    current_item += (
                        " " + line
                    )
                else:
                    current_item = line

        if current_item:
            items.append(current_item)

        return items

    # ------------------------------------------------------------------
    # LANGUAGES
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_languages(
        section: str,
    ) -> list[str]:

        if not section:
            return []

        languages = []

        for line in section.splitlines():

            line = re.sub(
                r"^[•*▪●◦]\s*",
                "",
                line.strip(),
            )

            if not line:
                continue

            parts = re.split(
                r"[,;|]",
                line,
            )

            for language in parts:

                language = language.strip()

                if language:
                    languages.append(
                        language
                    )

        return ResumeStructurer._unique_preserve_order(
            languages
        )

    # ------------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------------

    @staticmethod
    def _unique_preserve_order(
        items: list[str],
    ) -> list[str]:

        seen = set()
        result = []

        for item in items:

            key = item.lower()

            if key in seen:
                continue

            seen.add(key)
            result.append(item)

        return result