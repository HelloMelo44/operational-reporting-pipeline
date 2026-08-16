from pathlib import Path
import logging

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "service_tickets_raw.csv"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "service_tickets_clean.csv"
LOG_FILE_PATH = BASE_DIR / "logs" / "pipeline.log"

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


def configure_logging() -> None:
    LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE_PATH,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def load_raw_data() -> pd.DataFrame:
    logging.info("Loading raw data from %s", RAW_DATA_PATH)
    return pd.read_csv(RAW_DATA_PATH)


def validate_columns(df: pd.DataFrame) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        logging.error("Missing required columns: %s", missing_columns)
        raise ValueError(f"Missing required columns: {missing_columns}")

    logging.info("Column validation passed")


def clean_ticket_data(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Cleaning ticket data")

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

    logging.info("Ticket data cleaning completed")

    return cleaned_df


def save_processed_data(df: pd.DataFrame) -> None:
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    logging.info("Processed data saved to %s", PROCESSED_DATA_PATH)


def main() -> None:
    configure_logging()
    logging.info("Pipeline started")

    raw_df = load_raw_data()
    validate_columns(raw_df)

    cleaned_df = clean_ticket_data(raw_df)
    save_processed_data(cleaned_df)

    logging.info("Raw rows loaded: %s", len(raw_df))
    logging.info("Processed rows saved: %s", len(cleaned_df))
    logging.info("Pipeline completed successfully")

    print(f"Raw rows loaded: {len(raw_df)}")
    print(f"Processed rows saved: {len(cleaned_df)}")
    print(f"Output file: {PROCESSED_DATA_PATH}")
    print(f"Log file: {LOG_FILE_PATH}")


if __name__ == "__main__":
    main()