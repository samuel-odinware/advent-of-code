import pathlib
from typing import Annotated, Any

import httpx
import markdownify
import nbformat
import pydantic
import typer
from bs4 import BeautifulSoup, ResultSet
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class AdventOfCodeSettings(BaseSettings):
    """Advent of Code setting."""

    TOKEN: str
    URL: pydantic.HttpUrl = "https://adventofcode.com"
    YEAR: int = 2024

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AOC_",
        case_sensitive=True,
        extra="ignore",
    )


class Challenge(pydantic.BaseModel):
    number: int
    instructions: str


settings = AdventOfCodeSettings()
INSTRUCTION_PATH_TEMPLATE = """import pathlib

INPUT_PATH = pathlib.Path("{file_path}")
"""


def parse_articles_from_html(html: str | bytes) -> ResultSet[Any]:
    page_soup = BeautifulSoup(html, "html.parser")
    h2_tag = page_soup.h2
    h1_tag = page_soup.new_tag("h1")
    h1_tag.string = h2_tag.string
    page_soup.h2.replace_with(h1_tag)

    return page_soup.findAll("article")


def convert_html_results_to_markdown(articles: ResultSet[Any]) -> list[Challenge]:
    if len(articles) == 0:
        raise ValueError("No instruction were found for the given day.")
    output = []
    for index, article in enumerate(articles, start=1):
        output.append(
            Challenge(
                number=index,
                instructions=markdownify.MarkdownConverter().convert_soup(article),
            )
        )

    return output


def write_notebook_file(instructions: str, path: pathlib.Path) -> None:
    notebook = nbformat.v4.new_notebook()
    notebook["cells"].append(
        nbformat.v4.new_markdown_cell(instructions),
    )
    notebook["cells"].append(
        nbformat.v4.new_code_cell(
            INSTRUCTION_PATH_TEMPLATE.format(
                file_path=f"{path.parent.as_posix()}/input.txt"
            )
        ),
    )
    notebook["cells"].append(
        nbformat.v4.new_code_cell("def main() -> None:\n\tpass"),
    )
    notebook["cells"].append(
        nbformat.v4.new_code_cell("def test_main() -> None:\n\tpass"),
    )
    notebook["cells"].append(
        nbformat.v4.new_code_cell("%%timeit\n\nmain()"),
    )
    notebook["cells"].append(
        nbformat.v4.new_code_cell("%%memit\n\nmain()"),
    )
    notebook["cells"].append(
        nbformat.v4.new_code_cell("%%pyinstrument\n\nmain()"),
    )

    nbformat.write(notebook, path)


def request_instruction_data(day: int):
    try:
        response = httpx.get(
            f"{settings.URL}{settings.YEAR}/day/{day}",
            cookies={"session": settings.TOKEN},
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.error(exc)
        raise exc
    except httpx.RequestError as exc:
        logger.error(exc)
        raise exc
    return response.text


def request_input_data(day: int):
    try:
        response = httpx.get(
            f"{settings.URL}{settings.YEAR}/day/{day}/input",
            cookies={"session": settings.TOKEN},
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.error(exc)
        raise exc
    except httpx.RequestError as exc:
        logger.error(exc)
        raise exc
    return response.text


def main(day: Annotated[int, typer.Argument(help="Advent of Code day to create.")]):
    root_path = pathlib.Path().cwd()
    day_path = root_path.joinpath(f"day_{day:02}")
    day_path.mkdir(mode=0o775, exist_ok=True)
    challenges = convert_html_results_to_markdown(
        articles=parse_articles_from_html(
            html=request_instruction_data(day=day),
        ),
    )
    for challenge in challenges:
        challenge_path = day_path.joinpath(f"challenge_{challenge.number:02}.ipynb")
        if challenge_path.exists():
            logger.info(
                f"SKIP: File already exists for day {day} challenge {challenge.number}."
            )
            continue
        write_notebook_file(instructions=challenge.instructions, path=challenge_path)
    input_file = day_path.joinpath("input.txt")
    if not input_file.exists():
        input_file.write_text(request_input_data(day=day))


if __name__ == "__main__":
    typer.run(main)
