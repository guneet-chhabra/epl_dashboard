import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE_DIR / "data/xg_per_match.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["team", "date"]).reset_index(drop=True)

# Add form column manually without groupby dropping the team column
form_list = [""] * len(df)

for team in df["team"].unique():
    idx = df[df["team"] == team].index.tolist()
    results = df.loc[idx, "result"].tolist()
    for i, pos in enumerate(idx):
        start = max(0, i - 4)
        form_list[pos] = "".join(results[start:i + 1])

df["form"] = form_list

print("Columns after:", df.columns.tolist())
print(f"Rows: {len(df)}, Teams: {df['team'].nunique()}")
print(df[["team", "date", "result", "form"]].head(8))

df.to_csv(BASE_DIR / "data/xg_with_form.csv", index=False)
print("Saved xg_with_form.csv")