import io
import tokenize

import click
from colorama import init as init_colorama, Style


def display_tokens(source: str, show_newlines: bool = False):
    io_stream = io.StringIO(source)
    lines = source.split("\n")

    for token in tokenize.generate_tokens(io_stream.__next__):
        type_name = tokenize.tok_name[token.type]
        line_index = token.start[0]
        start_pos, end_pos = token.start[1], token.end[1]
        cur_line = lines[line_index - 1]

        token_info = " ".join(
            [
                "{:>5}:".format(line_index),
                "[{:^11}]".format(type_name),
                "| {:>3} - {:<3} |".format(start_pos, end_pos),
            ]
        )

        print(token_info, end=" ")

        prefix, highlighted, suffix = "", "", ""

        if type_name == "ENDMARKER":
            highlighted = "<EOF>"
        elif type_name in ("NEWLINE", "NL"):
            if show_newlines:
                prefix = cur_line
                highlighted = "\\n"
        elif type_name in ("INDENT", "DEDENT"):
            highlighted = ("=" * (end_pos - 2)) + "\u21d2 "
            suffix = cur_line[end_pos:]
        else:
            prefix = cur_line[:start_pos]
            highlighted = cur_line[start_pos:end_pos]
            suffix = cur_line[end_pos:]

        print(
            "".join(
                [
                    Style.DIM + prefix + Style.NORMAL,
                    Style.BRIGHT + highlighted + Style.NORMAL,
                    Style.DIM + suffix + Style.NORMAL,
                ]
            )
        )


@click.command()
@click.argument("source", type=click.File("r"))
@click.option("--nl/--no-nl", default=False)
def main(source, nl):
    """
    Visualize Python token stream produced by tokenize module.
    """
    init_colorama()
    display_tokens(source.read(), show_newlines=nl)


if __name__ == "__main__":
    main()
