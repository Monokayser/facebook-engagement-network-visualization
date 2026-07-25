# Data provenance and processing

## Source

**Facebook Live Sellers in Thailand**  
Author: Nassim Dehouche  
DOI: https://doi.org/10.24432/C5R60S  
Official source: https://archive.ics.uci.edu/dataset/488/facebook%2Blive%2Bsellers%2Bin%2Bthailand  
License: Creative Commons Attribution 4.0 International  
Downloaded: 2026-07-25

The official UCI archive was used because Kaggle credentials were unavailable. The documented Kaggle mirror was not the download source.

## Raw files

- `raw/facebook_live_sellers_uci.zip`: official UCI archive.
- `raw/Live_20210128.csv`: extracted raw CSV, 7,050 rows × 16 columns.
- SHA-256 of CSV: `ea6a31aab095b15d3fd0c24a63d5d59822f1dd34922b09295179ea9c464a8d5b`.

Download again with:

```powershell
Invoke-WebRequest `
  -Uri "https://archive.ics.uci.edu/static/public/488/facebook+live+sellers+in+thailand.zip" `
  -OutFile "data/raw/facebook_live_sellers_uci.zip"
Expand-Archive "data/raw/facebook_live_sellers_uci.zip" -DestinationPath "data/raw"
```

## Processed file

`processed/facebook_live_sellers_cleaned.csv` is created by `python main.py`. The workflow:

1. preserves the raw file;
2. removes four entirely empty placeholder columns;
3. checks full-row and `status_id` duplicates;
4. normalizes post types;
5. validates nonnegative integer counts;
6. parses timestamps;
7. creates zero-safe engagement ratios and temporal features;
8. flags upper-Tukey engagement outliers without deleting them;
9. validates the transformed table.

## Synthetic exercise data

Files under `generated/` are explicitly synthetic:

- `students.csv`, `courses.csv`, and `enrollments.csv`;
- `domain_graph_nodes.csv` and `domain_graph_edges.csv`.

They demonstrate graph construction and are not observations about real people, courses, or research communities.
