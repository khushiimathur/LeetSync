from leetcode_client import LeetCodeClient
from repository_manager import RepositoryManager

def main():
    client = LeetCodeClient()
    repository = RepositoryManager()

    solution = client.get_daily_solution()
    repository.save_solution(solution)

    if solution is None:
        print("No accepted submission found for today's problem.")
        return

    print("Today's solution:")
    print("Title:", solution["title"])
    print("Language:", solution["language"])
    print("Submission:", solution["submission_id"])
    print("Runtime:", solution["runtime"])
    print("Memory:", solution["memory"])

    print("\nCode:")
    print(solution["code"])


if __name__ == "__main__":
    main()