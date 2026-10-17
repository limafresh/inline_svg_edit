import inkex
from lxml import html, etree

class SvgFromHtmlInput(inkex.InputExtension):
    def add_arguments(self, parser):
        parser.add_argument("--svg_id", type=str, help="id attribute of <svg></svg> element in HTML")

    def load(self, stream):
        svg_id = self.options.svg_id

        if not svg_id:
            raise inkex.AbortExtension("SVG id is not specified")

        try:
            html_tree = html.parse(stream)
        except Exception as e:
            raise inkex.AbortExtension(f"Failed to parse the HTML file: {e}")

        html_root = html_tree.getroot()

        try:
            svg = html_root.get_element_by_id(svg_id)
        except KeyError as e:
            raise inkex.AbortExtension(f"SVG not found: {e}")

        svg_string = etree.tostring(svg, encoding="unicode")

        self.document = inkex.load_svg(svg_string)

        return self.document

SvgFromHtmlInput().run()
