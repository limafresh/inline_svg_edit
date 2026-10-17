import inkex
import svg_string_tools

class CopySvgCode(inkex.EffectExtension):
    def add_arguments(self, parser):
        parser.add_argument("--indent_type", type=str, help="Indent type (space or tab)")
        parser.add_argument("--number_of_indents", type=int, help="Number of indents in SVG code")
        parser.add_argument("--optimize_svg", type=inkex.Boolean, help="SVG optimization")

    def effect(self):
        svg_string = svg_string_tools.get_proper_svg_string(
            self.svg,
            self.options.indent_type,
            self.options.number_of_indents,
            self.options.optimize_svg,
        )

        self.msg(svg_string)

CopySvgCode().run()
