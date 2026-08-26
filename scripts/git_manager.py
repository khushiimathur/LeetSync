import subprocess


class GitManager:

    def __init__(self, repo_dir="."):
        self.repo_dir = repo_dir

    def _run_git(self, *args):
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo_dir,
            capture_output=True,
            text = True
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Git command failed: {result.stderr}"
            )

        return result

    def status(self):
        result = self._run_git("status", "--short")

        return result.stdout

    def add_changes(self):
        result = self._run_git("add", ".")
        return result.stdout

    def commit(self, message):
        result = self._run_git("commit", "-m", message)
        return result.stdout

    def push(self):
        result = self._run_git("push", "origin", "main")
        return result.stdout


if __name__ == "__main__":
    git = GitManager()

    print(git.status())
    print(git.add_changes())
    print(git.commit("Added git_manager.py"))
    print(git.push())