set -e

# TODO для корректного создания схем в Postgres прописать свой вариант
export VARIANT=v2
export SCRIPT_PATH=/docker-entrypoint-initdb.d/
export PGPASSWORD=test
psql --u program services -f "$SCRIPT_PATH/schemes/schema-$VARIANT.sql"
