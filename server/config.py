username = 'postgres'
password = 'cognitiveati'
host = 'telle-ai-database.cqh3eh5shl0r.us-east-2.rds.amazonaws.com'
port = 5432
prod_db = 'telle_ai_prod'

db_string = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(username, password, host, port, prod_db)

redis_host = 'telle-redis.telle.production'

redis_port = 6379

service_channel = 'telle_ai_chat'

