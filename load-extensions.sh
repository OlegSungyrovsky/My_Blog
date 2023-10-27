#!/bin/sh

# You could probably do this fancier and have an array of extensions
# to create, but this is mostly an illustration of what can be done

psql -U $POSTGRES_USER $POSTGRES_DB  <<EOF
CREATE EXTENSION pg_trgm;
EOF