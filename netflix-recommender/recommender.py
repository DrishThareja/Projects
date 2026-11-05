"""Simple content-based recommender for the Kaggle 'Netflix Movies and TV Shows' dataset.

Two titles are 'similar' when they share genres, directors or cast members.
Similarity uses the Jaccard score: (items in common) / (total distinct items).

Usage:
    python recommender.py "Stranger Things" -n 5
    python recommender.py "Inception" --type Movie
"""
import argparse
import difflib
import sys
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["title", "type", "release_year", "listed_in", "director", "cast"]
GENRE_WEIGHT = 0.6   # genre match counts a bit more...
PEOPLE_WEIGHT = 0.4  # ...than director/cast match


def to_set(text):
    """'Drama, Comedy' -> {'drama', 'comedy'}"""
    return {part.strip().lower() for part in str(text).split(",") if part.strip()}


def jaccard(a, b):
    """Overlap between two sets: 0 = nothing in common, 1 = identical."""
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


class NetflixRecommender:
    """Recommends titles similar to a given title."""

    def __init__(self, csv_path):
        self.df = self._load(csv_path)
        self.genres = [to_set(g) for g in self.df["listed_in"]]
        self.people = [to_set(d + "," + c) for d, c in zip(self.df["director"], self.df["cast"])]

    @staticmethod
    def _load(csv_path):
        path = Path(csv_path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")
        df = pd.read_csv(path)
        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"Dataset is missing columns: {missing}")
        df = df.drop_duplicates(subset="title").reset_index(drop=True)
        for col in ["listed_in", "director", "cast"]:
            df[col] = df[col].fillna("")
        return df

    def _find_index(self, title):
        matches = self.df.index[self.df["title"].str.lower() == title.strip().lower()]
        if len(matches) == 0:
            close = difflib.get_close_matches(title, self.df["title"].tolist(), n=3)
            hint = f" Did you mean: {close}?" if close else ""
            raise ValueError(f"Title '{title}' not found.{hint}")
        return matches[0]

    def recommend(self, title, n=5, content_type=None):
        """Return a DataFrame of the n most similar titles (optionally only 'Movie' or 'TV Show')."""
        idx = self._find_index(title)
        scores = [
            GENRE_WEIGHT * jaccard(self.genres[idx], self.genres[j])
            + PEOPLE_WEIGHT * jaccard(self.people[idx], self.people[j])
            for j in range(len(self.df))
        ]
        result = self.df.assign(score=scores).drop(index=idx)
        if content_type:
            result = result[result["type"].str.lower() == content_type.lower()]
        result = result.sort_values(["score", "release_year"], ascending=[False, False]).head(n)
        return result[["title", "type", "release_year", "listed_in", "score"]].reset_index(drop=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Netflix content-based recommender")
    parser.add_argument("title", nargs="?", help="Title to find recommendations for (asked if left out)")
    parser.add_argument("-n", type=int, default=5, help="Number of recommendations (default 5)")
    parser.add_argument("--type", choices=["Movie", "TV Show"], help="Filter by content type")
    parser.add_argument("--data", help="Path to the CSV (default: real Kaggle file if present, else the sample)")
    args = parser.parse_args(argv)

    # Pick the dataset: use the real Kaggle file if it exists, otherwise the small sample.
    here = Path(__file__).resolve().parent
    real, sample = here / "data" / "netflix_titles.csv", here / "data" / "sample_titles.csv"
    data_path = args.data or (real if real.exists() else sample)
    example = "Stranger Things" if data_path == real else "Space Quest"
    print(f"Using dataset: {data_path}")

    title = args.title or input(f"Enter a title you like (e.g. {example}): ").strip()

    try:
        rec = NetflixRecommender(data_path)
        out = rec.recommend(title, n=args.n, content_type=args.type)
    except (FileNotFoundError, ValueError) as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    print(f"\nBecause you watched '{title}':\n")
    print(out.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
