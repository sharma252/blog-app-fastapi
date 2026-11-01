from slugify import slugify


def generate_slug(title: str) -> str:
    return slugify(title)
