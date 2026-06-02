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
            response = client.table("practice_tests").select("*").order("created_at").execute()
            rows = response.data or []
            if rows:
                return PracticeTestsResponse(tests=[PracticeTest.model_validate(row) for row in rows])

        return PracticeTestsResponse(
            tests=[PracticeTest.model_validate(test) for test in PRACTICE_TESTS]
        )

    def get_selection_data(self) -> SelectionDataResponse:
        client = get_supabase_client()

        if client:
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

        return SelectionDataResponse(
            subjects=[SelectionItem.model_validate(item) for item in SUBJECTS],
            topics=[SelectionItem.model_validate(item) for item in TOPICS],
            subtopics=[SelectionItem.model_validate(item) for item in SUBTOPICS],
            selected_test=TestSummary.model_validate(SELECTED_TEST),
        )


practice_test_service = PracticeTestService()
