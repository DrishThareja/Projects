import tempfile
import unittest
from pathlib import Path

import pandas as pd

from recommender import NetflixRecommender, jaccard, to_set

COLUMNS = ["title", "type", "release_year", "listed_in", "director", "cast"]
ROWS = [
    ("Space Quest", "Movie", 2020, "Sci-Fi, Adventure", "A Rao", "X, Y"),
    ("Galaxy Wars", "Movie", 2019, "Sci-Fi, Adventure", "B Das", "X"),
    ("Star Show", "TV Show", 2021, "Sci-Fi, Drama", "", "P, Q"),
    ("Cook Along", "TV Show", 2018, "Reality, Food", "", "Chef M"),
    ("Space Quest", "Movie", 2020, "Sci-Fi, Adventure", "A Rao", "X, Y"),  # duplicate row
]


class TestRecommender(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        path = Path(self.tmp.name) / "titles.csv"
        pd.DataFrame(ROWS, columns=COLUMNS).to_csv(path, index=False)
        self.rec = NetflixRecommender(path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_returns_requested_count(self):
        self.assertEqual(len(self.rec.recommend("Space Quest", n=2)), 2)

    def test_excludes_input_title(self):
        out = self.rec.recommend("Space Quest", n=3)
        self.assertNotIn("Space Quest", out["title"].values)

    def test_similar_title_ranks_above_unrelated(self):
        titles = self.rec.recommend("Space Quest", n=3)["title"].tolist()
        self.assertLess(titles.index("Galaxy Wars"), titles.index("Cook Along"))

    def test_lookup_is_case_insensitive(self):
        self.assertEqual(len(self.rec.recommend("space quest", n=1)), 1)

    def test_type_filter(self):
        out = self.rec.recommend("Space Quest", n=5, content_type="TV Show")
        self.assertEqual(set(out["type"]), {"TV Show"})

    def test_unknown_title_raises(self):
        with self.assertRaises(ValueError):
            self.rec.recommend("Space Quet")

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            NetflixRecommender("nope.csv")

    def test_jaccard_helper(self):
        self.assertEqual(jaccard(to_set("a, b"), to_set("b, c")), 1 / 3)
        self.assertEqual(jaccard(set(), set()), 0.0)


if __name__ == "__main__":
    unittest.main()
