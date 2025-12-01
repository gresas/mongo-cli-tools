import sys
import logging
import argparse
from pathlib import Path
from settings.load_config import setup_logging
from tools.transfering import transfer_handler


logger = logging.getLogger(__name__)
sys.path.insert(0, str(Path(__file__).parent))


def create_parser():
    parser = argparse.ArgumentParser(
        description="News Transfer Tools - Transfer and manage news data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n  python cli.py transfer-all-news --source classification:58cc42ab1d172700103f3ee3 --dest classification:56ab81075d84bd022ce2f597" \
                "\n  python cli.py transfer-all-news --source tag:empreededorismo --dest classification:56ab81075d84bd022ce2f597"
                "\n  python cli.py validate --file data.json"
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    transfer_parser = subparsers.add_parser('transfer-all-news', help='News are filtered from a source rule and associated to a destination rule')
    transfer_parser.add_argument('--source', required=True, help='Source type chose for news filtering')
    transfer_parser.add_argument('--dest', required=True, help='Destination parameter to associate filtered news')
    transfer_parser.set_defaults(func=transfer_handler.command_handler)
    
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        args.func(args)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    setup_logging()
    main()
