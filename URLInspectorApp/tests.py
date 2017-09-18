from django.test import TestCase
from URLInspectorApp.templatetags.ui_utils import truncate_chars_middle


class UIUtilsTest(TestCase):
    def test_truncate_middle(self):
        expected = {
            ("sunnyday", 4): "suay",
            ("wonderful", 3): "wol",
            ("magician", 5): "magan",
            ("dinosaur", 7): "dinoaur",
            ("greek god", 5): "greod",
            ("all of it", 20): "all of it",
            ("none of it", 0): "",
            # Edge cases below
            ("", 0): "",
            ("", 44): "",
            ("willnotbecomputed", -1): "",
            (False, 5): "False",    # Since the @stringfilter decorator was used, False is turned into "False"
            (0, 4): "0",
        }

        for input, output in expected.items():
            shortened = truncate_chars_middle(*input, sep="")

            self.assertEqual(shortened, output)
