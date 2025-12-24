import pandas as pd
from textblob import TextBlob

def main():
    df = pd.read_csv("data/mham_with_toxicity_sample.csv")

    df["sentiment_polarity"] = None
    df["sentiment_subjectivity"] = None

    for i, row in df.iterrows():
        text = str(row["text"])
        if not text or text.strip() == "":
            continue

        blob = TextBlob(text)
        df.at[i, "sentiment_polarity"] = blob.sentiment.polarity
        df.at[i, "sentiment_subjectivity"] = blob.sentiment.subjectivity

        if i % 200 == 0:
            print("Processed", i, "rows...")

    df.to_csv("data/mham_annotated_sample.csv", index=False)
    print("Saved to data/mham_annotated_sample.csv")

if __name__ == "__main__":
    main()
