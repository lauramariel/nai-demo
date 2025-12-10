if [ "$1" = "local" ]; then
	docker compose  build
	docker compose up -d
	echo "access at http://localhost:8000/"
elif [ "$1" = "prod" ]; then
	docker compose -f docker-compose.prod.yaml build
	docker compose -f docker-compose.prod.yaml up -d
else
	echo "Error: Please specify 'local' or 'prod' as the argument."
	exit 1
fi