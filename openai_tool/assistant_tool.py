from config import client


async def get_answer_from_assistant(question: str, chat_id: int, tread_id: str, assistant_id: str) -> str:

    message = await client.beta.threads.messages.create(
        thread_id=tread_id,
        role="user",
        content=question,
    )

    run = await client.beta.threads.runs.create_and_poll(
        thread_id=tread_id,
        assistant_id=assistant_id,
    )

    messages = list(await client.beta.threads.messages.list(thread_id=tread_id, run_id=run.id))

    messages = messages[0][1]

    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(annotation.text, '')
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = await client.files.retrieve(file_citation.file_id)
            citations.append(f" [{cited_file.filename}]")

    return message_content.value
