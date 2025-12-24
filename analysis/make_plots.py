import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_toxicity_by_platform(df):
    sub = df.dropna(subset=["toxicity"])
    avg = sub.groupby("source")["toxicity"].mean().reset_index()

    plt.figure(figsize=(8, 5))
    sns.barplot(data=avg, x="source", y="toxicity")
    plt.title("Figure 1: Average Toxicity by Platform")
    plt.xlabel("Platform")
    plt.ylabel("Mean Toxicity (0–1)")
    plt.tight_layout()
    plt.savefig("fig1_toxicity_by_platform.png")
    plt.close()

def plot_sentiment_distribution(df):
    sub = df.dropna(subset=["sentiment_polarity"])

    plt.figure(figsize=(8, 5))
    sns.histplot(
        data=sub,
        x="sentiment_polarity",
        hue="source",
        kde=True,
        bins=40,
        element="step"
    )
    plt.title("Figure 2: Sentiment Distribution Across Platforms")
    plt.xlabel("Sentiment Polarity (-1 to +1)")
    plt.ylabel("Post Count")
    plt.tight_layout()
    plt.savefig("fig2_sentiment_distribution.png")
    plt.close()

def plot_post_length_distribution(df):
    df = df.copy()
    df["post_length"] = df["text"].fillna("").astype(str).str.len()

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="source", y="post_length")
    plt.title("Figure 3: Post Length Distribution Across Platforms")
    plt.xlabel("Platform")
    plt.ylabel("Post Length (characters)")
    plt.tight_layout()
    plt.savefig("fig3_post_length_distribution.png")
    plt.close()

def plot_keyword_freq(df):
    df = df.copy()
    df["text"] = df["text"].fillna("").astype(str).str.lower()
    keywords = ["help", "therapy", "alone", "suicide"]

    records = []
    for platform in ["4chan", "reddit"]:
        sub = df[df["source"] == platform]
        total_posts = len(sub)
        texts = sub["text"]
        for kw in keywords:
            count = texts.str.contains(kw).sum()
            per_1000 = (count / total_posts) * 1000 if total_posts > 0 else 0
            records.append(
                {"platform": platform, "keyword": kw, "per_1000": per_1000}
            )

    kdf = pd.DataFrame(records)

    plt.figure(figsize=(8, 5))
    sns.barplot(data=kdf, x="keyword", y="per_1000", hue="platform")
    plt.title("Figure 4: Keyword Frequency per 1000 Posts")
    plt.xlabel("Keyword")
    plt.ylabel("Occurrences per 1000 Posts")
    plt.tight_layout()
    plt.savefig("fig4_keyword_freq.png")
    plt.close()

def plot_sentiment_toxicity_heatmap(df):
    sub = df.dropna(subset=["sentiment_polarity", "toxicity"])

    plt.figure(figsize=(8, 6))
    plt.hexbin(
        sub["sentiment_polarity"],
        sub["toxicity"],
        gridsize=40
    )
    plt.colorbar(label="Post Count")
    plt.title("Figure 5: Sentiment vs Toxicity Density")
    plt.xlabel("Sentiment Polarity (-1 to +1)")
    plt.ylabel("Toxicity (0–1)")
    plt.tight_layout()
    plt.savefig("fig5_sentiment_vs_toxicity.png")
    plt.close()

def plot_temporal_toxicity(df):
    sub = df.dropna(subset=["toxicity", "created_utc"]).copy()
    sub["created_dt"] = pd.to_datetime(sub["created_utc"], unit="s", errors="coerce")
    sub = sub.dropna(subset=["created_dt"])
    sub["date"] = sub["created_dt"].dt.date

    grouped = (
        sub.groupby(["date", "source"])["toxicity"]
        .mean()
        .reset_index()
        .sort_values("date")
    )

    plt.figure(figsize=(10, 5))
    for platform in grouped["source"].unique():
        gsub = grouped[grouped["source"] == platform]
        plt.plot(gsub["date"], gsub["toxicity"], marker="o", label=platform)

    plt.title("Figure 6: Temporal Trend of Mean Toxicity")
    plt.xlabel("Date")
    plt.ylabel("Mean Toxicity (0–1)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig("fig6_temporal_toxicity.png")
    plt.close()

def main():
    df = pd.read_csv("data/mham_annotated_sample.csv")


    plot_toxicity_by_platform(df)
    plot_sentiment_distribution(df)
    plot_post_length_distribution(df)
    plot_keyword_freq(df)
    plot_sentiment_toxicity_heatmap(df)
    plot_temporal_toxicity(df)

    print("Saved figures: fig1_... to fig6_... in analysis/")

if __name__ == "__main__":
    main()
