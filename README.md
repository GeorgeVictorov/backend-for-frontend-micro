# backend-for-frontend-micro

This project is an example implementation of the Backend-for-Frontend (BFF) pattern.

The BFF service acts as an intermediary between the frontend and multiple backend microservices, aggregating data and
optimizing API responses.

## Structure

- **BFF Service** 
- **Cart Service** 
- **Favorites Service** 
- **Inventory Service** 
- **Products Service** 
- **User Service** *(Not Implemented)*

## Communication

All services communicate via REST APIs.

## Technologies Used

- **[aiohttp](https://docs.aiohttp.org/en/stable/)** - Asynchronous HTTP Client/Server
- **[asyncpg](https://pypi.org/project/asyncpg/)** - Database interface library designed specifically for PostgreSQL
- **[asyncio](https://docs.python.org/3/library/asyncio.html)** - Standard Python library for asynchronous programming

## Response example

```json
{
  "cart_items": 3,
  "favorite_items": 3,
  "products": [
    {
      "product_id": 1,
      "inventory": 3
    },
    {
      "product_id": 4,
      "inventory": null
    },
    {
      "product_id": 3,
      "inventory": null
    },
    {
      "product_id": 2,
      "inventory": null
    },
    {
      "product_id": 5,
      "inventory": null
    }
  ]
}
```