# Databricks notebook source
# MAGIC %md
# MAGIC # Explore departure delays (practice notebook)
# MAGIC
# MAGIC This file is a Databricks notebook stored in **source format**: a plain `.py` file
# MAGIC where `# COMMAND ----------` separates cells and `# MAGIC` prefixes markdown and
# MAGIC `%sql` cells. Databricks renders it as a notebook; GitHub shows a readable diff;
# MAGIC and no cell output is ever committed. The first line is what tells Databricks
# MAGIC this is a notebook.

# COMMAND ----------

import pandas as pd

# In a Databricks Git folder the working directory is this notebook's folder, so
# paths relative to the repo just work. No hard-coded workspace or DBFS paths.
flights_pd = pd.read_csv("../data/sample/flights_sample.csv")
flights_pd.head()

# COMMAND ----------

# `spark` and `display` are injected by Databricks at runtime. pyproject.toml tells
# ruff to ignore "undefined name" for this folder for exactly that reason.
flights = spark.createDataFrame(flights_pd)
flights.createOrReplaceTempView("flights")
display(flights.limit(10))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     origin,
# MAGIC     COUNT(*) AS flights,
# MAGIC     ROUND(AVG(dep_delay_min), 1) AS avg_dep_delay_min
# MAGIC FROM flights
# MAGIC WHERE NOT cancelled
# MAGIC GROUP BY origin
# MAGIC ORDER BY avg_dep_delay_min DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercise (Session 8)
# MAGIC
# MAGIC 1. On a branch, change the query above to group by `aircraft_type` instead of `origin`.
# MAGIC 2. Commit and push from the Databricks Git dialog, open the PR on GitHub, merge, pull.
# MAGIC 3. Look at the PR diff: three changed lines, no JSON, no outputs.
