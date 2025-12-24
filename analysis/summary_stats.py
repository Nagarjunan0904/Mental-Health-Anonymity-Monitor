import pandas as pd

def main():
    df = pd.read_csv("data/mham_annotated_sample.csv")

    
    df["text"] = df["text"].fillna("").astype(str)

    
    df["post_length"] = df["text"].str.len()

    rows = []
    for platform in ["4chan", "reddit"]:
        sub = df[df["source"] == platform]

        total_posts = len(sub)
        mean_toxicity = sub["toxicity"].mean()
        mean_sentiment = sub["sentiment_polarity"].mean()
        mean_subjectivity = sub["sentiment_subjectivity"].mean()
        avg_post_length = sub["post_length"].mean()

        rows.append({
            "platform": platform,
            "total_posts": total_posts,
            "mean_toxicity": mean_toxicity,
            "mean_sentiment_polarity": mean_sentiment,
            "mean_sentiment_subjectivity": mean_subjectivity,
            "avg_post_length": avg_post_length
        })

    out = pd.DataFrame(rows)
    out.to_csv("data/summary_stats_table.csv", index=False)
    print("Saved summary table to data/summary_stats_table.csv")
    print(out)

if __name__ == "__main__":
    main()
