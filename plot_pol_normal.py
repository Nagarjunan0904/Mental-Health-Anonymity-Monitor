import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "mhams_pol_activity.db"

# Load entire table
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT is_thread, created_at FROM pol_activity", conn)
conn.close()

# Parse timestamps
df['created_at'] = pd.to_datetime(df['created_at'], utc=True)

# Filter date range (Nov 2 → Nov 15)
start = "2025-11-02"
end   = "2025-11-15 23:59:59"
df = df[(df['created_at'] >= start) & (df['created_at'] <= end)]

# THREADS
threads = df[df['is_thread'] == 1]
threads_daily = threads.groupby(threads['created_at'].dt.date).size()

plt.figure(figsize=(12,6))
threads_daily.plot(kind='bar')
plt.title("Daily Thread Count on /pol/ (Nov 2–15, 2025)")
plt.xlabel("Date")
plt.ylabel("Threads")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("figure7_pol_threads_daily.png", dpi=300)

# POSTS
posts = df[df['is_thread'] == 0]
posts_hourly = posts.groupby(posts['created_at'].dt.floor('h')).size()

plt.figure(figsize=(14,6))
posts_hourly.plot()
plt.title("Hourly Post Count on /pol/ (Nov 2–15, 2025)")
plt.xlabel("Date (Hourly)")
plt.ylabel("Posts")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("figure8_pol_posts_hourly.png", dpi=300)

print("Figures generated:")
print(" - figure7_pol_threads_daily.png")
print(" - figure8_pol_posts_hourly.png")