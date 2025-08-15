if [ "$1" = "local" ]; then
	docker compose  --profile local down
elif [ "$1" = "prod" ]; then
	docker compose  --profile prod down
else
	echo "Error: Please specify 'local' or 'prod' as the argument."
	exit 1
fi