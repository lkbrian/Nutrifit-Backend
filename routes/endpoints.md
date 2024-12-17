
# API ENDPOINTS

### Create Account
```bash
curl -X POST http://<your-server-url>/create-account \
  -H "Content-Type: application/json" \
  -d '{ \
        "email": "user@example.com", \
        "password": "yourPassword123" \
      }'
```

### Verify Account
```bash
curl -X POST http://<your-server-url>/verify-account \
  -H "Content-Type: application/json" \
  -d '{ \
        "token": "your_token" \
      }'
```

### Login
```bash
curl -X POST http://<your-server-url>/login \
  -H "Content-Type: application/json" \
  -d '{ \
        "email": "user@example.com", \
        "password": "yourPassword123" \
      }'
```

### Logout
```bash
curl -X DELETE http://<your-server-url>/logout \
  -H "Authorization: Bearer <your_jwt_token>"
```
