import re
from pathlib import Path


def read_text_from_file(path: Path) -> str | None:
    """Reads text from a file at the given path."""
    try:
        return path.read_text()
    except FileNotFoundError:
        print(f"File not found at path: {path}")
        return None


def split_articles_into_files(text: str, output_dir: Path) -> None:
    """Splits articles into separate files in the given output directory."""
    article_pattern = re.compile(r"Статья ([\d\.]+)")
    chunks = re.split(r"(Статья [^\n]+)", text)[1:]
    articles = ["".join(chunks[i : i + 2]) for i in range(0, len(chunks), 2)]

    for article in articles:
        article_number = (
            article_pattern.search(article).group(1).replace(".", "_").rstrip("_")
        )
        output_file = output_dir / f"{article_number}.txt"
        output_file.write_text(article, encoding="utf-8")


if __name__ == "__main__":
    file_path = Path("../documents/44fz/44fz.txt").resolve()
    text = read_text_from_file(file_path)
    output_dir = Path("../documents/44fz/articles").resolve()
    split_articles_into_files(text, output_dir)
    print("Done splitting articles.")
