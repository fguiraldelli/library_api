O erro `KeyError: 'ContainerConfig'` indica que há um problema na configuração do contêiner para o serviço `book-service` no seu `docker-compose.yml`. Este problema pode ser causado por várias razões, como uma configuração inválida, um problema com os volumes, ou uma incompatibilidade com a versão do Docker Compose que você está usando.

Vamos verificar algumas configurações e tentar resolver o problema.

### Verificar `docker-compose.yml`

Primeiro, certifique-se de que a configuração do `docker-compose.yml` para o `book-service` está correta e não há problemas com a definição dos volumes ou outras configurações.

Aqui está um exemplo de como a configuração do `book-service` deve ser:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

  book-service:
    build:
      context: ./book-service
    environment:
      DATABASE_URL: postgresql://user:password@postgres/appdb
    depends_on:
      - postgres
    networks:
      - app-network

networks:
  app-network:

volumes:
  postgres_data:
```

Certifique-se de que o diretório `./book-service` contém um `Dockerfile` válido e que todas as dependências estão corretamente configuradas.

### Atualizar Docker Compose

Certifique-se de que você está usando a versão mais recente do Docker Compose. Você pode atualizar o Docker Compose usando os seguintes comandos:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

### Reconstruir e Reiniciar o Serviço

Vamos tentar reconstruir e reiniciar o serviço `book-service` novamente:

```bash
# Parar o serviço atual
docker-compose stop book-service

# Remover o contêiner atual (se necessário)
docker-compose rm -f book-service

# Reconstruir a imagem do book-service
docker-compose build book-service

# Reiniciar apenas o book-service
docker-compose up -d --no-deps --force-recreate book-service
```

### Verificar Logs e Status

Verifique os logs do serviço `book-service` para ver se ele foi iniciado corretamente:

```bash
docker-compose logs -f book-service
```

Verifique o status dos serviços para garantir que todos estão em execução:

```bash
docker-compose ps
```

### Conclusão

Se os passos acima não resolverem o problema, por favor, forneça o conteúdo completo do seu `docker-compose.yml` para uma análise mais detalhada. Isso ajudará a identificar qualquer problema específico na configuração que possa estar causando o erro.
