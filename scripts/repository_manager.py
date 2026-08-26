from pathlib import Path
import json
import re

class RepositoryManager:
    LANGUAGE_EXTENSIONS = {
        "cpp": ".cpp",
        "python": ".py",
        "java": ".java",
    }   
    def __init__(self, solutions_dir="solutions"):
        self.solutions_dir = Path(solutions_dir)

    def slugify_title(self, title):
        title = title.lower()
        title = re.sub(r"[^a-z0-9\s-]", "", title)

    # replace whitespace with -
        title = re.sub(r"\s+", "-", title)
        return title

    def get_solution_directory(self, solution):
        year, month, day = solution["date"].split("-")
        slug = self.slugify_title(solution["title"])
        return self.solutions_dir / year / month / f"{day}-{slug}"

    def create_solution_directory(self, solution):
        dir_path = self.get_solution_directory(solution)

        # create directory
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    def write_solution_file(self, solution, sol_dir):
        extension = self.LANGUAGE_EXTENSIONS[solution["language"].lower()]
        file_path = sol_dir / f"solution{extension}"
        
        # write solution["code"]
        file_path.write_text(solution["code"])

    def write_metadata_file(self, solution, sol_dir):
        file_path = sol_dir / f"metadata.json"
        metadata = {
            "date": solution["date"],
            "title": solution["title"],
            "slug": self.slugify_title(solution["title"]),
            "submission_id": solution["submission_id"],
            "difficulty": solution["difficulty"],
            "language":solution["language"],
            "runtime": solution["runtime"],
            "memory": solution["memory"],
            "leetcode_url": solution["leetcode_url"],
        }
        mtdta = json.dumps(metadata)
        file_path.write_text(mtdta)



    def save_solution(self, solution):
        sol_dir = self.create_solution_directory(solution)
        #create solution file
        self.write_solution_file(solution, sol_dir)
        self.write_metadata_file(solution, sol_dir)
       
        return sol_dir



    

