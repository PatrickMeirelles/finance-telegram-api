import multiprocessing

# Configurações básicas
bind = "0.0.0.0:8000"
workers = 1  # Usando apenas 1 worker para o bot do Telegram
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5

# Configurações de logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"

# Configurações de segurança
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configurações de performance
max_requests = 1000
max_requests_jitter = 50
worker_connections = 1000 