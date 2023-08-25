# if .makerc exists, include it to load credentials
ifneq ("$(wildcard .makerc)","")
	include .makerc
endif

ifdef LOCAL
	# get hasura port using docker client
	HASURA_PORT=$(shell eval docker port meta-ai_hasura_1 8080 | grep -o "\:[0-9]*" | cut -d ":" -f 2)
	# If not found try spelling with all dashes
	ifeq ("$(HASURA_PORT)","")
		HASURA_PORT=$(shell eval docker port meta-ai-hasura-1 8080 | grep -o "\:[0-9]*" | cut -d ":" -f 2)
	endif
	HASURA_ENDPOINT="http://localhost:${HASURA_PORT}/v1/graphql"
	HASURA_ADMIN_SECRET="myadminsecretkey"
endif

meta_ai_schema.json:
	@echo "Local=${LOCAL}"
	@echo "HASURA_ENDPOINT=${HASURA_ENDPOINT}"
	python3 -m sgqlc.introspection --header "x-hasura-admin-secret:${HASURA_ADMIN_SECRET}" ${HASURA_ENDPOINT} meta_ai_schema.json

meta_ai_graphql_schema.py: meta_ai_schema.json
	sgqlc-codegen schema meta_ai_schema.json  meta_ai_graphql_schema.py

format: meta_ai_graphql_schema.py
	black meta_ai_graphql_schema.py
	isort meta_ai_graphql_schema.py

patch_schema: meta_ai_graphql_schema.py
	python patch_schema.py

schema: clean meta_ai_graphql_schema.py patch_schema format
	@echo "Local ${LOCAL}"

clean:
	rm -f meta_ai_schema.json
	rm -f meta_ai_graphql_schema.py