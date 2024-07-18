## Comands used

Commands used in the project

# Create network

- docker network create app-network

# Erase all volumes

- docker volume rm $(docker volume ls -q --filter dangling=true)

# Delete all images

- docker rmi -f $(docker images -aq)

# Reset all docker variables and erase all
 
- docker system prune -af