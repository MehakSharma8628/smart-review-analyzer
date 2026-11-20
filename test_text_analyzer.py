
import unittest

from text_analyzer import (
    extract_keywords,
    detect_entities,
    analyze_sentiment,
    summarize
)


class TestAnalyzer(unittest.TestCase):

    def test_keywords_remove_stopwords(self):
        words = [
            w for w, _ in extract_keywords(
                "The pizza and the pasta. The pizza is great."
            )
        ]

        self.assertIn("pizza", words)
        self.assertNotIn("the", words)

    def test_entities(self):
        entities = dict(
            detect_entities(
                "Mail me at a@b.com about the $50 deal in March 2026. "
                "Ask Ravi Kumar."
            )
        )

        self.assertEqual(entities.get("a@b.com"), "Email")
        self.assertEqual(entities.get("$50"), "Money")
        self.assertEqual(
            entities.get("Ravi Kumar"),
            "Name/Place/Org"
        )

    def test_positive_sentiment(self):
        result = analyze_sentiment(
            "The food was excellent and delicious."
        )

        self.assertEqual(result[0], "positive")

    def test_negative_sentiment(self):
        result = analyze_sentiment(
            "The service was terrible and slow."
        )

        self.assertEqual(result[0], "negative")

    def test_negation(self):
        result = analyze_sentiment(
            "The food was not good."
        )

        self.assertEqual(result[0], "negative")

    def test_summary_length(self):
        text = (
            "One is here. Two is here. "
            "Three is here. Four is here."
        )

        summary = summarize(text, 2)

        self.assertLessEqual(
            len(summary.split(". ")),
            2
        )


if __name__ == "__main__":
    unittest.main()
