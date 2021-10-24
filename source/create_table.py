from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
table_id = "egen-training-kck.training_capstone.userLogs"
schema = [
    bigquery.SchemaField("remote_addr", "STRING"),
    bigquery.SchemaField("timelocal", "STRING"),
    bigquery.SchemaField("request_type", "STRING"),
    bigquery.SchemaField("status", "STRING"),
    bigquery.SchemaField("body_bytes_sent", "STRING"),
    bigquery.SchemaField("http_referer", "STRING"),
    bigquery.SchemaField("http_user_agent", "STRING"),
]

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)  # Make an API request.
print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)