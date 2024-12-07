from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

model = GigaChat(
    credentials="ключ_авторизации(будем подключать позже)",
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    streaming=False,
    verify_ssl_certs=False,
)

messages = [
    SystemMessage(
        content='Тебе присылают список блюд, которые нужно приготовить, и список продуктов. Для каждого блюда найди \
        классический рецепт этого блюда и напиши полный список продуктов, которые нужны для приготовления. Объедини все \
        продукты для блюд и из данного пользователем списка в один. Результат верни в формате JSON-списка без каких-либо\
        пояснений, например, ["продукт1", "продукт2", "продукт3"]. Не дублируй продукты.'
    )
]

user_input = input()
messages.append(HumanMessage(content=user_input))
res = model.invoke(messages)
messages.append(res)
print(res.content)

# Пока в формате классического ввода-вывода, подключать к боту будем по мере появления бота :)
