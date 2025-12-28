firestore:
	gcloud emulators firestore start --host-port=127.0.0.1:8082
	
config:
	gcloud config set project hf-hifivechat-dev

auth:	
	gcloud auth application-default login

build:
	docker-compose up --build

up:
	docker-compose up

secret:
	gcloud secrets versions access latest --secret="sa-key-sa-cloud-run-dev" --project="hf-hifivechat-dev" > src/credentials/application_default_credentials.json