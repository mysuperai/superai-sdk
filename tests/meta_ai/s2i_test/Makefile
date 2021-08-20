ifndef mode
mode=cpu
endif

build:
	s2i build -E environment -v ~/.aws:/root/.aws --incremental=True . superai-model-s2i-python3711-${mode}:1 test-model-py3-${mode}:0.1

run:
	docker rm -f "test_predictor"
	docker run --name "test_predictor" -p 5000:5000 -p 80:8080 -p 8081:8081 -v $(folder):/opt/ml/model test-model-py3-${mode}:0.1

run_d:
	docker rm -f "test_predictor"
	docker run --name "test_predictor" --rm -d -p 5000:5000 -p 80:8080 -p 8081:8081 -v $(folder):/opt/ml/model test-model-py3-${mode}:0.1

clean:
	docker rm -f "test_predictor"

.PHONY: test build run_d

test: build run_d
	sleep 4
	curl -d '{"my_image": {"image_url": "https://c1.staticflickr.com/3/2829/8987621878_94d0ebe159_b.jpg"}}' -H 'Content-Type: application/json' http://localhost/invocations
	docker rm -f "test_predictor"