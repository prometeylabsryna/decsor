from django.test import TestCase, override_settings
from django.utils import translation


class FaqTranslationTests(TestCase):
    def test_faq_answer_translates_to_english(self):
        with translation.override("en"):
            text = translation.gettext(
                "Без жодних проблем, за умови повної оплати товару та вартості доставки"
            )
        self.assertIn("No problem", text)
        self.assertNotIn("Без жодних", text)

    @override_settings(LANGUAGE_CODE="uk")
    def test_faq_page_english_prefix(self):
        response = self.client.get("/en/pro-kompaniyu/faq/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I live far from Kyiv")
        self.assertContains(response, "No problem at all")
