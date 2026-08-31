from scripts.repository_manager import RepositoryManager


def test_slugify_title():
    manager = RepositoryManager()

    result = manager.slugify_title(
        "Smallest Missing Multiple of K"
    )

    assert result == "smallest-missing-multiple-of-k"


def test_solution_directory():
    manager = RepositoryManager()

    solution = {
        "date": "2026-08-26",
        "title": "Smallest Missing Multiple of K"
    }

    path = manager.get_solution_directory(solution)

    assert str(path) == (
        "solutions/2026/08/26-smallest-missing-multiple-of-k"
    )