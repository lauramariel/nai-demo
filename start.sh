if [ "$1" = "local" ]; then
	docker compose  --profile local build
	docker compose --profile local up -d
	echo "access at http://localhost:8000/"
elif [ "$1" = "prod" ]; then
	docker compose  --profile prod build
	docker compose --profile prod up -d
else
	echo "Error: Please specify 'local' or 'prod' as the argument."
	exit 1
fi