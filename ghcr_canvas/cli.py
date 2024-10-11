import argparse
from ghcr_canvas import merger, renamer

def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(prog='ghcr_canvas', description="GitHub Classroom Canvas Utilities")
    subparsers = parser.add_subparsers(dest='command', help='Available subcommands')

    parser_1 = subparsers.add_parser('rename', help='Run repo renamer', parents=[renamer.get_parser()])
    parser_1.set_defaults(func=renamer.main)

    parser_2 = subparsers.add_parser('merge', help='Run roster merger', parents=[merger.get_parser()])
    parser_2.set_defaults(func=merger.main)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func(args)

if __name__ == "__main__":
    main()
