include .makerc

meta_ai_schema.json:
	python3 -m sgqlc.introspection --header "x-hasura-admin-secret:${HASURA_ADMIN_SECRET}" ${HASURA_ENDPOINT} meta_ai_schema.json

meta_ai_graphql_schema.py: meta_ai_schema.json
	sgqlc-codegen schema meta_ai_schema.json meta_ai_graphql_schema.py

schema:
	make meta_ai_graphql_schema.py

clean:
	rm -f meta_ai_schema.json
	rm -f meta_ai_graphql_schema.py