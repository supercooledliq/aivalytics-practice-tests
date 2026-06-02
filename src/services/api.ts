import type { PracticeTestCardData } from "../types/practiceTest";
import type {
  AnswerReviewRow,
  LiveQuestion,
  ResultBreakdown,
  SelectionItem,
  TestSummary,
} from "../types/testFlow";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";
type ApiRequestOptions = Parameters<typeof fetch>[1];

interface PracticeTestsResponse {
  tests: PracticeTestCardData[];
}

export interface SelectionDataResponse {
  subjects: SelectionItem[];
  topics: SelectionItem[];
  subtopics: SelectionItem[];
  selectedTest: TestSummary;
}

export interface Recommendation {
  label: string;
  title: string;
  description: string;
}

export interface WeakArea {
  topic: string;
  accuracy: number;
}

export interface TestAttempt {
  id: string;
  userId: string;
  testId: string;
  status: "IN_PROGRESS" | "SUBMITTED";
  currentQuestion: number;
  answeredCount: number;
}

export interface AttemptQuestionsResponse {
  attempt: TestAttempt;
  question: LiveQuestion;
  totalQuestions: number;
  markedQuestions: number[];
}

export interface AttemptResultResponse {
  attemptId: string;
  title: string;
  overallScore: number;
  correct: number;
  incorrect: number;
  skipped: number;
  timeTaken: string;
  percentile: string;
  breakdown: ResultBreakdown[];
  answerReview: AnswerReviewRow[];
}

async function request<T>(path: string, options?: ApiRequestOptions): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const api = {
  getPracticeTests: () => request<PracticeTestsResponse>("/practice-tests"),
  getSelectionData: () => request<SelectionDataResponse>("/practice-tests/selection-data"),
  getRecommendations: (userId: string) =>
    request<{ recommendations: Recommendation[] }>(`/users/${userId}/recommendations`),
  getWeakAreas: (userId: string) =>
    request<{ weakAreas: WeakArea[] }>(`/users/${userId}/weak-areas`),
  startAttempt: () =>
    request<TestAttempt>("/test-attempts", {
      method: "POST",
      body: JSON.stringify({
        userId: "demo-user",
        testId: "prime-factors",
        subjectId: "quant",
        topicId: "number-systems",
        subtopicId: "prime-factors",
      }),
    }),
  getAttemptQuestions: (attemptId: string) =>
    request<AttemptQuestionsResponse>(`/test-attempts/${attemptId}/questions`),
  saveAnswer: (attemptId: string, questionId: number, optionId: string | null, status = "answered") =>
    request(`/test-attempts/${attemptId}/answers/${questionId}`, {
      method: "PATCH",
      body: JSON.stringify({ optionId, status }),
    }),
  submitAttempt: (attemptId: string) =>
    request<{ attemptId: string; status: string; resultUrl: string }>(
      `/test-attempts/${attemptId}/submit`,
      { method: "POST" },
    ),
  getAttemptResult: (attemptId: string) =>
    request<AttemptResultResponse>(`/test-attempts/${attemptId}/result`),
};
