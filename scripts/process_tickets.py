from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "service_tickets_raw.csv"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "service_tickets_clean.csv"

REQUIRED_COLUMNS = [
    "ticket_id",
    "created_date",
    "resolved_date",
    "department",
    "category",
    "priority",
    "status",
    "assigned_team",
    "customer_type",
    "resolution_hours",
    "sla_hours",
    "reopened",
]


def load_raw_data() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_PATH)


def validate_columns(df: pd.DataFrame) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def clean_ticket_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned_df = df.copy()

    cleaned_df["created_date"] = pd.to_datetime(cleaned_df["created_date"])
    cleaned_df["resolved_date"] = pd.to_datetime(cleaned_df["resolved_date"], errors="coerce")

    cleaned_df["resolution_hours"] = pd.to_numeric(
        cleaned_df["resolution_hours"], errors="coerce"
    )
    cleaned_df["sla_hours"] = pd.to_numeric(cleaned_df["sla_hours"], errors="coerce")

    cleaned_df["is_resolved"] = cleaned_df["status"].eq("Resolved")
    cleaned_df["sla_breached"] = cleaned_df["resolution_hours"] > cleaned_df["sla_hours"]

    cleaned_df["reopened_flag"] = cleaned_df["reopened"].eq("Yes")

    return cleaned_df


def save_processed_data(df: pd.DataFrame) -> None:
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)


def main() -> None:
    raw_df = load_raw_data()
    validate_columns(raw_df)

    cleaned_df = clean_ticket_data(raw_df)
    save_processed_data(cleaned_df)

    print(f"Raw rows loaded: {len(raw_df)}")
    print(f"Processed rows saved: {len(cleaned_df)}")
    print(f"Output file: {PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    main()