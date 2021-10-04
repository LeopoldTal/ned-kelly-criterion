build:
	pip install -r hello_world/requirements.txt
	sam build --use-container
invoke: build
	sam local invoke
deploy: build
	terraform init
	terraform apply
graph: main.tf
	terraform graph | dot -Tsvg > graph.svg
