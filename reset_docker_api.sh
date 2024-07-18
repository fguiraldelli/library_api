docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls -q)
# docker rmi $(docker images -a -q)
docker system prune -f
docker network create app-network
# docker-compose build
# docker-compose up -d