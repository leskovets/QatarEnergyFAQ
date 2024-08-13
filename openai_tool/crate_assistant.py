from config import client
from openai_tool.promts import prompt_1


async def create_assistant() -> str:

    assistant = await client.beta.assistants.create(
        name="assistant",
        instructions=prompt_1['faq']['prompt'],
        model="gpt-4o",
        tools=[{"type": "file_search"}]
    )

    vector_store = await client.beta.vector_stores.create(name="Anxiety")

    with open("openai_tool/files/QatarEnergy.docx", 'rb') as file:

        await client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=[file]
        )

    await client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    return assistant.id
