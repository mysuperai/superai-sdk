ifndef folder
folder=$(CURDIR)
$(warning Var not defined. Using test model in local directory)
endif

ifndef mode
mode=cpu
endif

seldon_substring=
ifdef seldon
seldon_substring=-seldon
endif


init:
	echo "MODEL_NAME=Model" > environment
	if [ ${seldon_substring} = '-seldon' ]; then echo "SELDON_MODE=true" >> environment && echo "SERVICE_TYPE=MODEL" >> environment; fi

build: init
	s2i build -E environment -v ~/.aws:/root/.aws --incremental=True . 185169359328.dkr.ecr.us-east-1.amazonaws.com/superai-model-s2i-python3711-${mode}${seldon_substring}:1 test-model-py3-${mode}${seldon_substring}:0.1

run:
	docker rm -f "test_predictor"
	docker run --name "test_predictor" -p 5000:5000 -p 80:8080 -p 8081:8081 -v $(folder):/opt/ml/model test-model-py3-${mode}${seldon_substring}:0.1

run_d:
	docker rm -f "test_predictor"
	docker run --name "test_predictor" --rm -d -p 5000:5000 -p 80:8080 -p 8081:8081 -p 9000:9000 -v $(folder):/opt/ml/model test-model-py3-${mode}${seldon_substring}:0.1

clean:
	docker rm -f "test_predictor"

.PHONY: test build run_d

test: build run_d
	sleep 4
	curl -d '{"my_image": {"image_url": "https://c1.staticflickr.com/3/2829/8987621878_94d0ebe159_b.jpg"}}' -H 'Content-Type: application/json' http://localhost/invocations
	docker rm -f "test_predictor"

seldon-core-microservice-test:
	export MNT_PATH=$(shell pwd)
	seldon-core-microservice Model --service-type MODEL --log-level DEBUG

test-seldon-core-microservice:
	curl -X POST http://localhost:9000/api/v1.0/predictions -H 'Content-Type: application/json' -d '{"data": {"image_url": "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png"}}'

# run using `make seldon=true folder=$(pwd) test-seldon`
test-seldon: init build run_d
	sleep 4
	curl -d '{"my_image": {"image_url": "https://c1.staticflickr.com/3/2829/8987621878_94d0ebe159_b.jpg"}}' -H 'Content-Type: application/json' http://localhost:9000/api/v1.0/predictions
	docker rm -f "test_predictor"
