build:
	sam build --use-container
invoke: build
	sam local invoke
deploy: build
	sam deploy