from pydantic import BaseModel
from datetime import datetime

class SubmissionCreateResponse(BaseModel):
    submission_id: int
    message: str = "Submission received. Processing started."

class SubmissionResult(BaseModel):
    submission_id: int
    status: str
    converted_code: str | None = None
    success_rate: float | None = None
    image_path: str
    submitted_at: datetime
    score: int | None = None
    accuracy: float | None = None
    execution_time: float | None = None
    is_correct: bool | None = None

    class Config:
        from_attributes = True