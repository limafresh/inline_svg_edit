import inkex
from html.parser import HTMLParser
import svg_string_tools

class UpdateInlineSvg(inkex.EffectExtension):
    def add_arguments(self, parser):
        parser.add_argument("--html_path", type=str, help="Path to the HTML file")
        parser.add_argument("--indent_type", type=str, help="Indent type (space or tab)")
        parser.add_argument("--number_of_indents", type=int, help="Number of indents in SVG code")
        parser.add_argument("--optimize_svg", type=inkex.Boolean, help="SVG optimization")

    def effect(self):
        with open(self.options.html_path, "r", encoding="utf-8") as f:
            html_string = f.read()

        svg_id = self.svg.get_id()
        if not svg_id:
            raise inkex.AbortExtension("Current SVG has not id")

        try:
            parser = Parser(html_string, svg_id)
            parser.feed(html_string)
        except StopParsing:
            pass

        if parser.start_abs_pos is None or parser.end_abs_pos is None:
            raise inkex.AbortExtension("Current inline SVG not found")
        current_inline_svg: str = html_string[parser.start_abs_pos:parser.end_abs_pos]

        svg_string = svg_string_tools.get_proper_svg_string(
            self.svg,
            self.options.indent_type,
            self.options.number_of_indents,
            self.options.optimize_svg,
        )

        indent = self.get_start_line_indent(html_string, parser.start_pos)
        indented_svg_string = self.get_indented_string(svg_string, indent)

        new_html_string = html_string.replace(current_inline_svg, indented_svg_string)

        with open(self.options.html_path, "w", encoding="utf-8") as f:
            f.write(new_html_string)

    def get_start_line_indent(self, text: str, pos: tuple[int, int]) -> str:
        line, column = pos

        lines: list[str] = text.splitlines(keepends=True)

        target_line: str = lines[line - 1]
        indent = target_line[:column]

        return indent

    def get_indented_string(self, string: str, indent: str) -> str:
        lines: list[str] = string.splitlines()

        indented_lines = [lines[0]]

        for line in lines[1:]:
            indented_lines.append(indent + line)

        indented_string = "\n".join(indented_lines)

        return indented_string

class Parser(HTMLParser):
    def __init__(self, html_string: str, element_id: str):
        super().__init__()

        self.tag = "svg"

        self.html_string = html_string
        self.element_id = element_id

        self.found = False
        self.depth = 0

        self.start_abs_pos, self.end_abs_pos = None, None
        self.start_pos = None

    def handle_starttag(self, tag, attrs):
        if not self.found and tag == self.tag and dict(attrs).get("id") == self.element_id:
            self.found = True
            self.depth = 1

            self.start_abs_pos = self.find_absolute_pos(self.getpos())
            self.start_pos = self.getpos()

            return

        if self.found and tag == self.tag:
            self.depth += 1

    def handle_endtag(self, tag):
        if self.found and tag == self.tag:
            self.depth -= 1
            if self.depth == 0:
                self.end_abs_pos = self.find_absolute_pos(self.getpos()) + len("</svg>")

                raise StopParsing()

    def find_absolute_pos(self, pos: tuple[int, int]) -> int:
        line, column = pos

        all_lines: list[str] = self.html_string.splitlines(keepends=True)

        previous_lines: list[str] = all_lines[:line - 1]
        previous_lines_length: int = sum(map(len, previous_lines))

        absolute_pos = previous_lines_length + column

        return absolute_pos

class StopParsing(Exception):
    pass

UpdateInlineSvg().run()
