import pandas as pd
from perspective_client import score_text
import time

def main():
    df = pd.read_csv("data/mham_posts_sample.csv")

    # Add new columns
    df["toxicity"] = None
    df["insult"] = None
    df["identity_attack"] = None
    df["is_toxic"] = None

    for i, row in df.iterrows():
        text = str(row["text"])

        try:
            scores = score_text(text)
            df.at[i, "toxicity"] = scores.get("toxicity")
            df.at[i, "insult"] = scores.get("insult")
            df.at[i, "identity_attack"] = scores.get("identity_attack")
            df.at[i, "is_toxic"] = 1 if (scores.get("toxicity", 0) >= 0.5) else 0
        except Exception as e:
            print(f"Error scoring row {i}: {e}")

        if i % 200 == 0:
            print("Scored", i, "rows...")

        time.sleep(1)  # to stay within rate limits

    df.to_csv("data/mham_with_toxicity_sample.csv", index=False)
    print("Saved to data/mham_with_toxicity_sample.csv")

if __name__ == "__main__":
    main()
