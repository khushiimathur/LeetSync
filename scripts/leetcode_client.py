import requests
import os
from dotenv import load_dotenv

load_dotenv()

class LeetCodeClient:
    GRAPHQL_URL = "https://leetcode.com/graphql"

    def __init__(self):
        self.session = requests.Session()
        self.session.cookies.set(
            "LEETCODE_SESSION",
            os.getenv("LEETCODE_SESSION")
        )

        self.session.cookies.set(
            "csrftoken",
            os.getenv("LEETCODE_CSRF_TOKEN")
        )   


   
    def _query(self, query, variables=None, operation_name=None):
        response = self.session.post(
            self.GRAPHQL_URL,
            json={
                "query": query,
                "variables": variables or {},
                "operationName": operation_name
            }
        )

        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            raise RuntimeError(
                f"LeetCode GraphQL error: {data['errors']}"
            )

        return data["data"]

    def get_daily_problem(self):
        query = """
        query questionOfToday {
            activeDailyCodingChallengeQuestion {
                date
                link
                question {
                    questionFrontendId
                    title
                    titleSlug
                    difficulty
                }
            }
        }
        """

        data = self._query(
            query=query,
            operation_name="questionOfToday"
        )

        return data["activeDailyCodingChallengeQuestion"]

    def get_submissions(self, question_slug, limit=20):
        query = """
        query submissions(
            $offset: Int!,
            $limit: Int!,
            $lastKey: String,
            $questionSlug: String!
        ) {
            submissionList(
                offset: $offset,
                limit: $limit,
                lastKey: $lastKey,
                questionSlug: $questionSlug
            ) {
                submissions {
                    id
                    statusDisplay
                    lang
                    runtime
                    timestamp
                    url
                    isPending
                    memory
                }
            }
        }
        """

        variables = {
            "offset": 0,
            "limit": limit,
            "lastKey": "",
            "questionSlug": question_slug
        }

        data = self._query(
            query=query,
            variables=variables,
            operation_name="submissions"
        )

        submissions = data["submissionList"]["submissions"]

        return submissions or []

    def get_submission_details(self, submission_id):
        query = """
        query submissionDetails($submissionId: Int!) {
            submissionDetails(submissionId: $submissionId) {
                code
                lang {
                    name
                }
                runtime
                memory
                statusDisplay
            }
        }
        """

        variables = {
            "submissionId": int(submission_id)
        }

        data = self._query(
            query=query,
            variables=variables,
            operation_name="submissionDetails"
        )

        return data["submissionDetails"]

    def get_daily_solution(self):
        problem = self.get_daily_problem()

        slug = problem["question"]["titleSlug"]

        submissions = self.get_submissions(slug)

        accepted = [
            submission
            for submission in submissions
            if submission["statusDisplay"] == "Accepted"
        ]

        if not accepted:
            return None

        latest_submission = max(
            accepted,
            key=lambda submission: int(submission["timestamp"])
        )

        details = self.get_submission_details(
            latest_submission["id"]
        )

        return {
            "date": problem["date"],
            "title": problem["question"]["title"],
            "slug": slug,
            "difficulty": problem["question"]["difficulty"],
            "problem_id": problem["question"]["questionFrontendId"],
            "submission_id": latest_submission["id"],
            "language": details["lang"]["name"],
            "code": details["code"],
            "runtime": details["runtime"],
            "memory": details["memory"],
            "status": details["statusDisplay"],
            "leetcode_url": problem["link"],
        }