import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def build_features(df):
    print("Columns in CSV:", df.columns.tolist())
    print("First row:", df.iloc[0].to_dict())

    # Normalize column names to lowercase with no spaces
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Try to find the team column
    team_col = None
    for candidate in ["team", "squad", "club", "team_name"]:
        if candidate in df.columns:
            team_col = candidate
            break
    if not team_col:
        raise ValueError(f"Can't find team column. Columns are: {df.columns.tolist()}")

    # Try to find the result column
    result_col = None
    for candidate in ["result", "outcome", "res"]:
        if candidate in df.columns:
            result_col = candidate
            break
    if not result_col:
        raise ValueError(f"Can't find result column. Columns are: {df.columns.tolist()}")

    # Map column names flexibly
    col = {
        "team":          team_col,
        "result":        result_col,
        "home":          next((c for c in df.columns if c in ["home", "h_a", "venue"]), None),
        "xg_for":        next((c for c in df.columns if "xg_for" in c or c == "xg"), None),
        "xg_against":    next((c for c in df.columns if "xg_against" in c or c == "xga"), None),
        "goals_for":     next((c for c in df.columns if "goals_for" in c or c in ["scored", "gf"]), None),
        "goals_against": next((c for c in df.columns if "goals_against" in c or c in ["missed", "ga"]), None),
    }
    print("Column mapping:", col)

    features = []
    for team in df[col["team"]].unique():
        team_df = df[df[col["team"]] == team].copy().reset_index(drop=True)
        if len(team_df) < 6:
            continue
        for i in range(5, len(team_df)):
            last5   = team_df.iloc[i-5:i]
            current = team_df.iloc[i]

            is_home = 1 if col["home"] and str(current[col["home"]]).lower() in ["h", "home"] else 0

            xg_for   = float(last5[col["xg_for"]].mean())   if col["xg_for"]   else 1.5
            xg_ag    = float(last5[col["xg_against"]].mean()) if col["xg_against"] else 1.5
            gf       = float(last5[col["goals_for"]].mean())  if col["goals_for"]  else 1.2
            ga       = float(last5[col["goals_against"]].mean()) if col["goals_against"] else 1.2
            wins     = int((last5[col["result"]] == "W").sum())
            draws    = int((last5[col["result"]] == "D").sum())

            features.append({
                "is_home":      is_home,
                "avg_xg_for":   round(xg_for, 3),
                "avg_xg_ag":    round(xg_ag,  3),
                "avg_goals_for": round(gf,    3),
                "avg_goals_ag": round(ga,     3),
                "wins_last5":   wins,
                "draws_last5":  draws,
                "result":       current[col["result"]],
            })

    return pd.DataFrame(features)


def train():
    csv_path = BASE_DIR / "data/xg_with_form.csv"
    if not csv_path.exists():
        csv_path = BASE_DIR / "data/xg_per_match.csv"
        print("Using xg_per_match.csv (no form column)")

    df = pd.read_csv(csv_path)
    feat_df = build_features(df)

    if len(feat_df) < 20:
        print(f"Not enough data to train — only {len(feat_df)} rows. Need at least 20.")
        return

    print(f"\nBuilt {len(feat_df)} feature rows")
    print("Result distribution:\n", feat_df["result"].value_counts())

    le = LabelEncoder()
    y  = le.fit_transform(feat_df["result"])
    X  = feat_df.drop("result", axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = XGBClassifier(n_estimators=100, max_depth=4,
                          learning_rate=0.1, use_label_encoder=False,
                          eval_metric="mlogloss")
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print("\nClassification report:")
    print(classification_report(y_test, preds, target_names=le.classes_))

    (BASE_DIR / "ml").mkdir(exist_ok=True)
    with open(BASE_DIR / "ml/model.pkl", "wb") as f:
        pickle.dump((model, le), f)
    print("Model saved to ml/model.pkl")


if __name__ == "__main__":
    train()