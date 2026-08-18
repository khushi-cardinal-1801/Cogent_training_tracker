from arq.connections import RedisSettings


async def product_created(ctx, product_data):
    print("================================")
    print("ARQ WORKER STARTED")
    print("================================")

    print("Product received:")
    print(product_data)

    print("Background task completed")

    return "Product processed successfully"


class WorkerSettings:
    functions = [product_created]

    redis_settings = RedisSettings(
        host="localhost",
        port=6379
    )