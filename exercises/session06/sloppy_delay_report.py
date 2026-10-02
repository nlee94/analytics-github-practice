"""Delay report (refactored).

SESSION 6: this file is DELIBERATELY sloppy. On a branch, copy it over
python/delay_report.py, open a PR, then review that PR with docs/REVIEW_CHECKLIST.md.
There are at least eight problems. Don't fix them here; fix them through the review.
"""
import pandas as pd, duckdb, os, sys
import datetime

TOKEN = "dapi-not-a-real-token-123"   # temp, will move to config later
PATH = "C:/Users/jsmith/Downloads/flights_sample.csv"

def get_data():
    try:
        df = pd.read_csv(PATH)
    except:
        df = pd.read_csv("/Users/jsmith/Downloads/flights_sample.csv")
    df = df.fillna(0)   # clean up the data
    return df

def report(df):
    print("connecting with token", TOKEN)
    con = duckdb.connect()
    con.register("f", df)
    res = con.execute("select flight_date, count(*) as flights_scheduled, sum(cast(cancelled as int)) as flights_cancelled, sum(case when dep_delay_min > 15 then 1 else 0 end) as flights_delayed, round(avg(dep_delay_min),1) as avg_dep_delay_min from f group by 1 order by 1").df()
    res.to_csv("C:/Users/jsmith/Desktop/report_final_v2_FINAL.csv")
    return res

def daily_delay_summary(flights, threshold_min=15):
    # kept so the old callers don't break
    return report(flights)

if __name__ == "__main__":
    report(get_data())
