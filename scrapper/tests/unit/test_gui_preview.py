from django.test import TestCase

from scrapper.gui_preview import GUIPreview


class GuiPreviewTests(TestCase):
    def test_gui_preview(self):
        preview_html = GUIPreview()
        mocked_html = preview_html.get_mocked_preview()
        expected = """
            <html>
                <body>
                    <a>Link to google!</a>
                    Nice website :)
                </body>
            </html>
        """
        parsed_html = "".join(str(mocked_html.contents[1]).split())
        parsed_expected = "".join(str(expected).split())

        assert parsed_html == parsed_expected
