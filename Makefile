build:
	pip install -r hello_world/requirements.txt
	sam build --use-container
invoke: build
	sam local invoke
deploy: build
	terraform init
	terraform apply -var-file=secrets.tfvars
graph: main.tf
	terraform graph | dot -Tsvg > graph.svg
