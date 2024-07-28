# Use a imagem base do Kong
FROM kong:3.4

# Garanta que estamos executando comandos como root
USER root

# Instale sudo
RUN apt-get update && apt-get install -y sudo && apt-get clean

# Crie um usuário com privilégios de sudo
RUN useradd -m -s /bin/bash kongadmin && echo "kongadmin:password" | chpasswd && adduser kongadmin sudo

# Permita sudo sem senha para o novo usuário (opcional)
RUN echo "kongadmin ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Instale curl
RUN apt-get update && apt-get install -y curl && apt-get clean

# Install dependencies
RUN apt-get update && apt-get install -y git unzip && apt-get clean

# Install lua-resty-openidc
RUN luarocks install lua-resty-openidc

RUN luarocks install kong-oidc-v3

COPY kong/kong.yml /usr/local/kong/declarative/kong.yml
RUN cp /etc/kong/kong.conf.default /etc/kong/kong.conf

ENV KONG_DATABASE=off
ENV KONG_DECLARATIVE_CONFIG=/usr/local/kong/declarative/kong.yml
ENV KONG_LOG_LEVEL=debug
ENV PORT=8000
EXPOSE 8000

#Revertendo para o usuário padrão do Kong se necessário
# USER kong

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["kong", "docker-start", "--vv"]



