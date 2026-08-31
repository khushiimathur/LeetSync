from leetcode_client import LeetCodeClient
from repository_manager import RepositoryManager
from git_manager import GitManager
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs/sync.log"
)


def main():
    client = LeetCodeClient()
    repository = RepositoryManager()
    git = GitManager()


    solution = client.get_daily_solution()
    logger.info("Solution extracted")
    if solution is None:
            logger.info("No accepted submission found for today's problem.")
            return

    path = repository.save_solution(solution)
    if path is None:
        logger.warning("Solution already synced.")
        return
    
    try:
        git.add_changes(path)
        git.commit(f"Added solution for {solution['date']}")
        git.push()
    except Exception:
        logger.exception("Git push failed")
        return
    logger.info("Solution pushed to Github")

if __name__ == "__main__":
    logger.info("Starting Leetsync")
    main()