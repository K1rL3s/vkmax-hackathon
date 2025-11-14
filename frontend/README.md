# Мини-приложение для max

## Запуск

### Предварительные действия:

```bash
# Генерация api через swagger документацию

pnpm run openapi:install
pnpm run openapi:gen
```

### Локальный запуск:

```bash
pnpm install
pnpm run dev
```

### В контейнере

```bash
docker build . -t maxhack-frontend --build-arg VITE_API_URL=http://localhost:7001
docker run -p "7002:80" max/frontend
```

Приложение будет доступно по адрессу http://localhost:7002
