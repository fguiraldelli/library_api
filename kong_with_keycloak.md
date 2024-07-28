To configure Kong to work with Keycloak, you typically need to set up OAuth 2.0 authentication. Kong provides a plugin for OAuth 2.0, which can be used to integrate with Keycloak. Here are the steps to configure Kong with Keycloak in `kong.yml`:

### Step 1: Set Up Keycloak

1. **Create a Realm**: Create a new realm in Keycloak if you don't have one already.
2. **Create a Client**: Create a new client in the realm. Set the client protocol to "openid-connect" and configure the client settings such as redirect URIs.
3. **Create a User**: Create a user in the realm and set a password.

### Step 2: Configure Kong

In your `kong.yml`, you'll need to configure a service and a route, and then apply the OAuth 2.0 plugin. Here's an example `kong.yml` configuration:

```yaml
_format_version: "3.0"
_transform: true

services:
  - name: book-service
    url: http://book-service:9001
    plugins:
      - name: oauth2
        config:
          name: keycloak-oauth
          scopes: email, profile
          token_expiration: 36000
          enable_authorization_code: true
          enable_implicit_grant: true
          enable_password_grant: true
          enable_client_credentials: true
          provision_key: EowN6j7J7tpZlLcieF8JjBpD1Ig=  # You'll need to set this
          client_id: user-cli # Keycloak client ID
          client_secret: zxiVm1tei3vGpmDgS0mqWEkTEIOWddct # Keycloak client secret
          site: http://localhost:8080/auth/realms/library # Keycloak site

    routes:
      - name: book-route
        paths:
          - /books

  - name: loan-service
    url: http://loan-service:9002
    plugins:
      - name: oauth2
        config:
          name: keycloak-oauth
          scopes: email, profile
          token_expiration: 36000
          enable_authorization_code: true
          enable_implicit_grant: true
          enable_password_grant: true
          enable_client_credentials: true
          provision_key: EuoPMD+3kftY+dxLjwaX2SxOpzs=  # You'll need to set this
          client_id: user-cli # Keycloak client ID
          client_secret: zxiVm1tei3vGpmDgS0mqWEkTEIOWddct # Keycloak client secret
          site: http://localhost:8080/auth/realms/library # Keycloak site

    routes:
      - name: loan-route
        paths:
          - /loans
```

### Step 3: Apply the Configuration

1. **Apply the configuration to Kong**:

   ```sh
   kong config db_import kong.yml
   ```

2. **Restart Kong** to make sure the new configuration is loaded:

   ```sh
   kong restart
   ```

### Step 4: Use the OAuth 2.0 Flow

1. **Get an Access Token**:
   - You will need to interact with Keycloak to get an access token. This typically involves directing the user to Keycloak's authorization endpoint, where they can log in and authorize the application. Keycloak will then redirect back to your application with an authorization code, which you can exchange for an access token.

2. **Access the Protected Resource**:
   - Once you have the access token, you can use it to access the protected resources in your services.

   ```sh
   curl --location --request GET 'http://localhost:8000/books' \
   --header 'Authorization: Bearer <access_token>'
   ```

### Summary

1. **Set Up Keycloak**: Create a realm, client, and user.
2. **Configure Kong**: Add the OAuth 2.0 plugin and configure it with Keycloak settings in `kong.yml`.
3. **Apply the Configuration**: Import the configuration into Kong and restart Kong.
4. **Use the OAuth 2.0 Flow**: Get an access token from Keycloak and use it to access protected resources.

By following these steps, you can integrate Kong with Keycloak using OAuth 2.0 authentication.
