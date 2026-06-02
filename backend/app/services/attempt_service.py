from uuid import uuid4

from app.schemas.analytics import AttemptResult
from app.schemas.attempt import (
    AttemptQuestionsResponse,
    SaveAnswerRequest,
    SaveAnswerResponse,
    StartAttemptRequest,
    SubmitAttemptResponse,
    TestAttempt,
)
from app.services.mock_data import ANSWER_REVIEW, LIVE_QUESTION, RESULT_BREAKDOWN, SELECTED_TEST

ATTEMPTS: dict[str, dict] = {}
ANSWERS: dict[tuple[str, int], dict] = {}


class AttemptService:
    def start_attempt(self, payload: StartAttemptRequest) -> TestAttempt:
        attempt_id = str(uuid4())
        attempt = {
            "id": attempt_id,
            "user_id": payload.userId,
            "test_id": payload.testId,
            "status": "IN_PROGRESS",
            "current_question": 12,
            "answered_count": 11,
        }
        ATTEMPTS[attempt_id] = attempt
        return TestAttempt.model_validate(attempt)

    def get_questions(self, attempt_id: str) -> AttemptQuestionsResponse:
        attempt = ATTEMPTS.get(
            attempt_id,
            {
                "id": attempt_id,
                "user_id": "demo-user",
                "test_id": "prime-factors",
                "status": "IN_PROGRESS",
                "current_question": 12,
                "answered_count": 12,
            },
        )

        return AttemptQuestionsResponse(
            attempt=TestAttempt.model_validate(attempt),
            question=LIVE_QUESTION,
            total_questions=SELECTED_TEST["questions"],
            marked_questions=[15, 22],
        )

    def save_answer(
        self,
        attempt_id: str,
        question_id: int,
        payload: SaveAnswerRequest,
    ) -> SaveAnswerResponse:
        answer = {
            "attempt_id": attempt_id,
            "question_id": question_id,
            "option_id": payload.optionId,
            "status": payload.status,
        }
        ANSWERS[(attempt_id, question_id)] = answer

        if attempt_id in ATTEMPTS and payload.status == "answered":
            ATTEMPTS[attempt_id]["answered_count"] = max(
                ATTEMPTS[attempt_id]["answered_count"],
                question_id,
            )

        return SaveAnswerResponse.model_validate(answer)

    def submit_attempt(self, attempt_id: str) -> SubmitAttemptResponse:
        if attempt_id in ATTEMPTS:
            ATTEMPTS[attempt_id]["status"] = "SUBMITTED"

        return SubmitAttemptResponse(
            attempt_id=attempt_id,
            status="SUBMITTED",
            result_url=f"/practice-tests/results?attemptId={attempt_id}",
        )

    def get_result(self, attempt_id: str) -> AttemptResult:
        return AttemptResult(
            attempt_id=attempt_id,
            title=SELECTED_TEST["title"],
            overall_score=78,
            correct=24,
            incorrect=4,
            skipped=2,
            time_taken="38:15",
            percentile="92nd",
            breakdown=RESULT_BREAKDOWN,
            answer_review=ANSWER_REVIEW,
        )


attempt_service = AttemptService()
