from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "service_tickets_clean.csv"
REPORTS_DIR = BASE_DIR / "reports"
QUALITY_REPORT_PATH = REPORTS_DIR / "data_quality_report.csv"

REPORTS_DIR.mkdir(exist_ok=True)


def load_processed_data() -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DATA_PATH)


def build_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    checks = [
        {
            "check_name": "total_rows",
            "result": len(df),
            "status": "info",
        },
        {
            "check_name": "duplicate_ticket_ids",
            "result": df["ticket_id"].duplicated().sum(),
            "status": "pass" if df["ticket_id"].duplicated().sum() == 0 else "review",
        },
        {
            "check_name": "unresolved_tickets",
            "result": int((df["is_resolved"] == False).sum()),
            "status": "info",
        },
        {
            "check_name": "sla_breached_tickets",
            "result": int(df["sla_breached"].sum()),
            "status": "info",
        },
        {
            "check_name": "reopened_tickets",
            "result": int(df["reopened_flag"].sum()),
            "status": "info",
        },
    ]

    for column in df.columns:
        missing_count = int(df[column].isna().sum())
        checks.append(
            {
                "check_name": f"missing_values_{column}",
                "result": missing_count,
                "status": "pass" if missing_count == 0 else "review",
            }
        )

    return pd.DataFrame(checks)


def main() -> None:
    df = load_processed_data()
    quality_report = build_quality_report(df)

    quality_report.to_csv(QUALITY_REPORT_PATH, index=False)

    print(f"Data quality report saved: {QUALITY_REPORT_PATH}")


if __name__ == "__main__":
    main()