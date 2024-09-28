import click

from api import create_app
from api.main.bloom_filter_manager import BloomFilterManager

application = create_app()


@application.cli.command("load")
@click.argument("file")
def load(file: str) -> None:
    """
    Load data into the bloom filter.
    """
    manager = BloomFilterManager()
    manager.new_filter(file=file)

    manager.write_filter_to_file()