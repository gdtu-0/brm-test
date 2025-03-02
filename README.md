# brm-test

This repo is a test project intended to compare performance of different db and search engines in a real business case of applying user-defined transformation rules to accounting transactional data.

## Source data

### Transactional accounting data

A dataset of roughly 450 000 records (~48 Mb) of accounting data was generated. For security reasons this dataset is not included in repo files.

![Image](/.images/src_accounting_data.png)

### Transformation rules

User-defined transformation rules are defined in table format. The strucutre containes several src* fields for data selection and trg* fields for mapping selected data to target analytics. Enumerations, masks and exceptions are supported. Transformation rules table contains around 31 000 records (11 Mb).
For security reasons transformation rules are not included in repo files.

![Image](/.images/src_mapping_rules.png)

### Parsing user-defined rules

Workflow includes parsing user-defined transformation rules to SQL WHERE conditions. This is an exaple of generated WHERE condition:

```sql
WHERE (account LIKE '05307%')
    AND (
        (corr_account LIKE '01%' OR corr_account LIKE '02%' OR corr_account LIKE '06%' OR corr_account LIKE '07%' OR corr_account LIKE '08%' OR corr_account LIKE '10%' OR corr_account LIKE '15%' OR corr_account LIKE '16%' OR corr_account LIKE '97%')
        AND corr_account <> '9720000100'
        AND (corr_account NOT LIKE '086%' AND corr_account NOT LIKE '975%' AND corr_account NOT LIKE '08803%' AND corr_account NOT LIKE '06107%' AND corr_account NOT LIKE '06207%' AND corr_account NOT LIKE '06400%')
    )
```

## Workflow

General worflow is implemented using Dagster. First it loads source data and mapping files from local folder, then applies mapping in different db and engines.

![Image](/.images/workflow.png)

### DB and engines

1. PostgreSQL

PostgreSQL is used without any optimizations.

2. Clickhouse

Fields in data table are defined with LowCardinality option to boost select performance.

3. Opensearch

Fields in Opensearch index are defined as keyword becasue full-featured text search is not needed for this task. Opensearch SQL interface is used for querying data.

4. DuckDB

DuckDB is used without any optimizations.

All the tesing was done in docker environment is single-instance mode.

## Results

Opensearch was not able to handle most diverse where conditions due to memory limitations for statement parsing.
Clickhouse is about 2x faster then PostgreSQL in this type of queries. DuckDB shows slightly better performance then Clickhouse, but in cluster scenarios Clickhose is expected to show better performance.

Average task duration in seconds is shown below.

![Image](/.images/results.png)
