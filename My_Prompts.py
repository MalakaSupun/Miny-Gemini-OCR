from langchain.prompts import ChatPromptTemplate

def create_ocr_prompt() -> ChatPromptTemplate:
    system_prompt = "Perform Optical Character Recognition (OCR) on the following image data. The output should be the extracted text formatted in Markdown."
    image_payload = [{"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,{image_data}"}}]
    return ChatPromptTemplate.from_messages([("system", system_prompt), ("user", image_payload)])
