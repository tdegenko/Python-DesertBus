import pathlib
import urllib.parse
import urllib.request

import desertbus.constants


def url_opener(
    user_agent: str = desertbus.constants.USER_AGENT,
) -> urllib.request.OpenerDirector:
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-agent", user_agent)]
    return opener


def build_db_url(
    path_parts: list[str], parameters: dict[str, str | list[str]] | None = None
):
    split_url = urllib.parse.urlsplit(desertbus.constants.BASE_URL)._asdict()
    split_url["path"] = pathlib.PurePosixPath(split_url["path"], *path_parts).as_posix()
    if parameters is not None:
        split_url["query"] = urllib.parse.urlencode(parameters)

    return urllib.parse.urlunsplit(urllib.parse.SplitResult(**split_url))
