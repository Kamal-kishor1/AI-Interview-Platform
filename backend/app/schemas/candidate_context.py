from pydantic import BaseModel, Field


class ProjectContext(BaseModel):

    # structured information about one candidate project.

    name: str
    description: str | None = None
    technologies: list[str] = Field(default_factory=list)


class ExperienceContext(BaseModel):

    # structured information about one work/internship experience

    role: str | None = None
    company: str | None = None
    description: str | None = None
    technologies: list[str] = Field(default_factory=list)


class CandidateContext(BaseModel):

    # structured context extracted from a candidate's resume

    skills: list[str] = Field(default_factory=list)

    projects: list[ProjectContext] = Field(default_factory=list)

    experience: list[ExperienceContext] = Field(default_factory=list)

    resume_text: str


class CandidateContextExtraction(BaseModel):

    # this is used for llm output response

    skills: list[str] = Field(default_factory=list)
    projects: list[ProjectContext] = Field(default_factory=list)
    experience: list[ExperienceContext] = Field(default_factory=list)
