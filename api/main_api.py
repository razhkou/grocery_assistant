from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from parser.edadealdo.py import parse_vers_0


def process(bot_inp, city):
    if bot_inp.type() != str:
        return "Введите текст."
    if len(bot_inp) < 2:
        return "Введите полный запрос."
    ai_ret = giga_proc(bot_inp)
    parse_ret = parse_vers_0(city, ai_ret)
    return parse_ret


def giga_proc(input_str):
    model = GigaChat(
        credentials="Njg4NzYwYmMtY2E3OC00OTlkLWFhOGMtYzExNTI1ZTA5ZmNmOjA0NDEyYTJiLWZhOGEtNGFhNy04ZTc1LTAzMTQ4OGMwZDE2NA==",
        scope="GIGACHAT_API_PERS",
        model="GigaChat",
        streaming=False,
        verify_ssl_certs=False,
    )

    messages = [
        SystemMessage(
            content='После слова "Запрос" перечислены блюда, для каждого из блюд найди \
        классический рецепт этого блюда и напиши полный список продуктов, которые нужны для приготовления в формате JSON-списка без каких-либо \
        пояснений, например, ["продукт1", "продукт2", "продукт3"]. После блюд перечислены продукты, которые нужно купить.\
        Добавь их в список. Не дублируй продукты. После слова "Предпочтения" будут написаны продукты, которые любит пользователь.\
        Если в твоем списке есть какие-то из них, то добавь уточнение предпочтений в свой список. Верни результат в виде одного общего списка \
        продуктов к поупке в формате ["продукт1", "продукт2", "продукт3"].'
        )
    ]
    user_input = input_str
    messages.append(HumanMessage(content=user_input))
    res = model.invoke(messages)
    messages.append(res)
    return res.content
