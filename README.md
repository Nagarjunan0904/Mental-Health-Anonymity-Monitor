# Starfall Knight – Project 3  
**Interactive Dashboard for Mental Health Discourse Analysis**

The goal of Project 3 is to provide a **research-driven, interactive visualization tool** that allows users to explore how **platform anonymity influences toxic vs. empathetic expressions** in mental-health-related discussions on **4chan** and **Reddit**.

---

## Research Question

**How does the degree of anonymity influence the prevalence of toxic vs. empathetic expressions across 4chan and Reddit?**

This question is explored through three analyses:
1. Toxicity by platform
2. Sentiment distribution and sentiment–toxicity correlation
3. Keyword frequency comparison for mental-health-related terms

---

## Project Structure

```
mham/collector/
├── analysis/
│   ├── data/
│   │   ├── mham_posts_sample.csv
│   │   ├── mham_with_toxicity_sample.csv
│   │   └── mham_annotated_sample.csv
│   ├── annotate_toxicity_sample.py
│   ├── annotate_sentiment_sample.py
│   ├── make_plots.py
│   └── summary_stats.py
│
├── project3_dashboard/
│   ├── app.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── toxicity.html
│   │   ├── sentiment.html
│   │   └── keywords.html
│   └── static/
│       └── plots/
│
├── crawler_4chan.py
├── crawler_reddit.py
├── db.py
├── util.py
├── main.py
├── enrich_db_from_csv.py
└── requirements.txt
```
---

## What the Code Does

### Interactive Dashboard 
- Implemented using **Flask**
- Reads directly from the enriched SQLite database
- Provides three interactive views:
  1. **Toxicity by Platform**
     - Filters: platform, date range
  2. **Sentiment Analysis**
     - Filters: platform, date range
     - Plots:
       - Sentiment distribution
       - Sentiment vs. toxicity correlation
  3. **Keyword Frequency Analysis**
     - Filters: keyword, platform, date range
- All plots are generated dynamically and rendered as PNGs

---

## How to Run the Project

### 1. Set up a Python virtual environment
```bash
python3 -m venv p3env
source p3env/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Project 3 dashboard
```bash
cd project3_dashboard
python3 app.py
```
Open a browser and go to:
```
http://127.0.0.1:5000
```

---

## Dashboard Pages

| Route | Description |
|-------|-------------|
| `/toxicity` | Average toxicity comparison by platform |
| `/sentiment` | Sentiment distribution and sentiment–toxicity relationship |
| `/keywords` | Keyword frequency comparison across platforms |

Each page supports interactive filtering.

---

## Assumptions and Limitations

- Perspective API toxicity scores are available only for a subset of posts
- Sentiment analysis uses lexicon-based methods (TextBlob), which may miss sarcasm or contextual nuance
- Keyword analysis is limited to four predefined mental-health-related terms
- Cross-platform comparisons are affected by differences in moderation and post length

These limitations are discussed in detail in the Project 3 report.

---




