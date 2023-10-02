import re
from pathlib import Path
from typing import Sequence

locale_pattern = re.compile(r"l10n.format_value\(\s*?\"([^\"]*)\"")


def extract(path: Path = Path()) -> Sequence[str]:
    locales = []

    for i in sorted(path.iterdir()):
        if i.is_dir():
            for locale in extract(i):
                if locale not in locales:
                    locales.append(locale)

        elif i.suffix == ".py":
            with i.open("r") as f:
                text = f.read()
                locales += re.findall(locale_pattern, text)

    return locales


def write_locale(file_path: Path, locales: Sequence[str]):
    with file_path.open("w") as f:
        f.write("\n".join(f"{x} = " for x in locales))


if __name__ == "__main__":
    locale_list = extract()
    write_locale(Path("locales", "tgbot.ftl.temp"), locale_list)
