
from pydantic import BaseModel, ConfigDict, Field, EmailStr

class ResumeAnalysisData(BaseModel):
    
    file_name: str | None = None
    file_size: int | None = None
    file_type: str | None = None
    content: str | None = None

class ResumeAnalysisResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    success: bool = False
    data: ResumeAnalysisData


class PersonalInfo(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    location: str | None = None
    linkedin: str | None = None
    github: str | None = None
    portfolio: str | None = None

class Education(BaseModel):
    institution: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: str | None = None

class Experience(BaseModel):
    company: str | None = None
    position: str | None = None
    location: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: str | None = None
    achievements: list[str] = Field(default_factory=list)

class Project(BaseModel):
    name: str | None = None
    description: str | None = None
    technologies: list[str] = Field(default_factory=list)
    url: str | None = None

class Certification(BaseModel):
    name: str | None = None
    issuer: str | None = None
    date: str | None = None
    credential_url: str | None = None


class ResumeProfile(BaseModel):
    personal_info: PersonalInfo = Field(
        default_factory=PersonalInfo
    )

    summary: str | None = None

    skills: list[str] = Field(
        default_factory=list
    )

    education: list[Education] = Field(
        default_factory=list
    )

    experience: list[Experience] = Field(
        default_factory=list
    )

    projects: list[Project] = Field(
        default_factory=list
    )

    certifications: list[Certification] = Field(
        default_factory=list
    )

    publications: list[str] = Field(
        default_factory=list
    )

    achievements: list[str] = Field(
        default_factory=list
    )

    languages: list[str] = Field(
        default_factory=list
    )
