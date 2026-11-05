# Netflix Content-Based Recommender

A command-line tool that recommends Netflix titles similar to one you already like, built with Python (OOP) and Pandas.

## Dataset
[Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) (Kaggle, ~8,800 titles).
Download `netflix_titles.csv` and place it in the `data/` folder. The CSV is not committed to this repo.

## How it works
1. **Load and clean** - drop duplicate titles, fill missing genre/director/cast values.
2. **Turn each title into two sets** - its genres, and its directors + cast members.
3. **Score similarity** - for each other title, compute the Jaccard score on genres and on people
   (Jaccard = items in common / total distinct items), then combine: 60% genres + 40% people.
4. **Rank** - sort by score (newer titles first on ties) and return the top N.

The logic lives in the `NetflixRecommender` class, so it can be reused or tested without the command line.

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
```bash
python recommender.py "Stranger Things"
python recommender.py "Inception" -n 10 --type Movie
```
Options: `-n` number of results (default 5), `--type Movie|"TV Show"`, `--data` path to the CSV.
Misspelled titles give suggestions (e.g. `Did you mean: [...]`).

## Sample output
<!-- Run the tool and paste your real output here -->

## Tests
```bash
python -m unittest -v
```
Tests cover result count, excluding the input title, ranking, case-insensitive lookup, the type filter, the similarity helper and error handling.

## Limitations and future work
- Uses only genres, directors and cast; it ignores the plot description.
- No user ratings, so this is content-based only.
- Possible next steps: use the description text (TF-IDF), add a simple web interface.

## Tech
Python, Pandas, argparse, unittest
