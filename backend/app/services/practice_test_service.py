from pydantic import ValidationError
from postgrest.exceptions import APIError

from app.core.supabase import get_supabase_client
from app.schemas.practice_test import (
    PracticeTest,
    PracticeTestsResponse,
    SelectionDataResponse,
    SelectionItem,
    TestSummary,
)
from app.services.mock_data import PRACTICE_TESTS, SELECTED_TEST, SUBJECTS, SUBTOPICS, TOPICS


class PracticeTestService:
    def list_practice_tests(self) -> PracticeTestsResponse:
        client = get_supabase_client()

        if client:
            try:
                response = client.table("practice_tests").select("*").order("created_at").execute()
                rows = response.data or []
                if rows:
                    return PracticeTestsResponse(
                        tests=[PracticeTest.model_validate(row) for row in rows]
                    )
            except APIError:
                pass
            except ValidationError:
                pass

            try:
                response = (
                    client.table("tests")
                    .select("id,title,duration_minutes,is_active,settings,created_at")
                    .order("created_at")
                    .execute()
                )
                rows = response.data or []
                if rows:
                    return PracticeTestsResponse(
                        tests=[PracticeTest.model_validate(self._map_existing_test(row)) for row in rows]
                    )
            except APIError:
                pass
            except ValidationError:
                pass

        return PracticeTestsResponse(
            tests=[PracticeTest.model_validate(test) for test in PRACTICE_TESTS]
        )

    def get_selection_data(self) -> SelectionDataResponse:
        client = get_supabase_client()

        if client:
            try:
                subjects = client.table("subjects").select("*").order("sort_order").execute().data or []
                topics = client.table("topics").select("*").order("sort_order").execute().data or []
                subtopics = client.table("subtopics").select("*").order("sort_order").execute().data or []
                summaries = client.table("test_summaries").select("*").limit(1).execute().data or []

                if subjects and topics and subtopics and summaries:
                    return SelectionDataResponse(
                        subjects=[SelectionItem.model_validate(item) for item in subjects],
                        topics=[SelectionItem.model_validate(item) for item in topics],
                        subtopics=[SelectionItem.model_validate(item) for item in subtopics],
                        selected_test=TestSummary.model_validate(summaries[0]),
                    )
            except APIError:
                pass
            except ValidationError:
                pass

            try:
                subjects = client.table("subjects").select("*").order("sort_order").execute().data or []
                topics = client.table("topics").select("*").order("sort_order").execute().data or []
                subtopics = client.table("subtopics").select("*").order("sort_order").execute().data or []
                tests = (
                    client.table("tests")
                    .select("title,subject_id,topic_id,duration_minutes,settings,created_at")
                    .order("created_at")
                    .limit(1)
                    .execute()
                    .data
                    or []
                )

                if subjects and topics and subtopics:
                    return SelectionDataResponse(
                        subjects=[
                            SelectionItem.model_validate(self._map_existing_selection_item(item))
                            for item in subjects
                        ],
                        topics=[
                            SelectionItem.model_validate(self._map_existing_selection_item(item))
                            for item in topics
                        ],
                        subtopics=[
                            SelectionItem.model_validate(self._map_existing_selection_item(item))
                            for item in subtopics
                        ],
                        selected_test=TestSummary.model_validate(
                            self._map_existing_summary(tests[0], subjects, topics, subtopics)
                            if tests
                            else SELECTED_TEST
                        ),
                    )
            except APIError:
                pass
            except ValidationError:
                pass

        return SelectionDataResponse(
            subjects=[SelectionItem.model_validate(item) for item in SUBJECTS],
            topics=[SelectionItem.model_validate(item) for item in TOPICS],
            subtopics=[SelectionItem.model_validate(item) for item in SUBTOPICS],
            selected_test=TestSummary.model_validate(SELECTED_TEST),
        )

    def _map_existing_test(self, row: dict) -> dict:
        settings = row.get("settings") or {}
        difficulty = settings.get("difficulty", "Medium")
        if difficulty not in {"Easy", "Medium", "Hard"}:
            difficulty = "Medium"

        return {
            "id": str(row["id"]),
            "title": row["title"],
            "category": settings.get("category", "Practice Test"),
            "status": "Not Started" if row.get("is_active", True) else "Completed",
            "questions": settings.get("questions", 0),
            "duration": row.get("duration_minutes") or settings.get("duration", 0),
            "difficulty": difficulty,
            "is_premium": settings.get("is_premium", False),
        }

    def _map_existing_selection_item(self, row: dict) -> dict:
        return {
            "id": str(row["id"]),
            "title": row.get("title") or row.get("name") or row.get("slug") or str(row["id"]),
            "progress": row.get("progress", 0),
            "average": row.get("average", "N/A"),
            "questions": row.get("questions", 0),
            "badge": row.get("badge"),
        }

    def _map_existing_summary(
        self,
        test: dict,
        subjects: list[dict],
        topics: list[dict],
        subtopics: list[dict],
    ) -> dict:
        settings = test.get("settings") or {}
        subject = self._find_name(subjects, test.get("subject_id"), "Practice")
        topic = self._find_name(topics, test.get("topic_id"), "General")
        subtopic = self._first_name(subtopics, "Mixed Practice")

        difficulty = settings.get("difficulty", "Medium")
        if difficulty not in {"Easy", "Medium", "Hard"}:
            difficulty = "Medium"

        question_count = settings.get("questions", 0)

        return {
            "subject": subject,
            "topic": topic,
            "subtopic": subtopic,
            "title": test["title"],
            "questions": question_count,
            "duration": test.get("duration_minutes") or 0,
            "total_marks": question_count,
            "difficulty": difficulty,
            "passing_score": settings.get("passing_score", "40%"),
            "attempts_allowed": settings.get("attempts_allowed", 3),
            "best_score": settings.get("best_score", "N/A"),
        }

    def _find_name(self, rows: list[dict], row_id: str | None, fallback: str) -> str:
        for row in rows:
            if str(row.get("id")) == str(row_id):
                return row.get("title") or row.get("name") or row.get("slug") or fallback
        return fallback

    def _first_name(self, rows: list[dict], fallback: str) -> str:
        if not rows:
            return fallback

        row = rows[0]
        return row.get("title") or row.get("name") or row.get("slug") or fallback


practice_test_service = PracticeTestService()
