build:
	pip install -r hello_world/requirements.txt
	sam build --use-container
invoke: build
	sam local invoke
deploy: build
	sam deploy