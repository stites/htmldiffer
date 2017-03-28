import unittest
import re
from diff import *

html_a = """
<html>
    <head class="this-is-a-class">
        <script src="some_js.js"></script>
    </head>
    <body>
      <div>
         test <b> test</b> foo
      </div>
      <div>
         del
      </div>
    </body>
</html>
"""

class TestDiffMethods(unittest.TestCase):
    def test_html2list(self):
        html_list = html2list(html_a)
        self.assertEqual(html_list[1], "</head>")
        self.assertFalse("</head>" in html_list[2])
        self.assertTrue('class="this-is-a-class"' in html_list[0])

        """test if the two strings are functionally the same"""
        new_html_string = "".join(html_list)
        rx = re.compile('\n|\t|\r|\s{2}')
        original_html_string = html_a
        original_html_string = rx.sub('', original_html_string)

        # TODO: make sure that a space before text does not make a difference in html, ever
        self.assertTrue("test <b>" in new_html_string)
        self.assertFalse("<div> test " in new_html_string)
        self.assertTrue("<div>test " in new_html_string)

        new_html_list = html2list(new_html_string)
        self.assertEqual(new_html_list, html_list)

def main():
    unittest.main()

if __name__ == '__main__':
    main()