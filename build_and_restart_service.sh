#/bin/bash

set -e

# Parar o serviço atual
docker-compose stop $1

# Remover o contêiner atual (se necessário)
docker-compose rm -f $1

# Reconstruir a imagem do serviço
docker-compose build $1

# Reiniciar apenas o serviço
docker-compose up -d --no-deps --force-recreate $1

#Ver processos rodando
docker-compose ps