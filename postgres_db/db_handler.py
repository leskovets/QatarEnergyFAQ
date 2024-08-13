from postgres_db.database import Clients, session_factory


async def add_new_client(client_name: str, assistant_id: str, chat_id: int) -> None:
    client = Clients(
        client_name=client_name,
        assistant_id=assistant_id,
        chat_id=chat_id
    )
    async with session_factory() as session:
        session.add(client)
        await session.commit()


async def get_client(chat_id: int) -> Clients:
    async with session_factory() as session:
        client = await session.get(Clients, chat_id)
    return client
