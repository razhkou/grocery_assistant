from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from parser.edadealdo import parse_vers_0


def process(bot_inp, city):
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
        классический рецепт и напиши полный список продуктов, которые нужны для приготовления всех перечисленных блюд в формате JSON-списка без каких-либо \
        пояснений, например, ["продукт1", "продукт2", "продукт3"]. После блюд перечислены продукты, которые нужно купить.\
        Добавь их в список. Не дублируй продукты. После слова "Предпочтения" будут написаны предпочтения по продуктам,\
        если в списке есть продукты, по которым есть предпочтения, то добавь уточнение предпочтений в свой список, например: ["продукт1", "продукт2 фирмы1"]". \
        Верни результат в виде одного общего списка всех нужных\
        продуктов к покупке в формате ["продукт1", "продукт2", "продукт3"]. Перед названием только свежего овоща или фрукта пиши слово "весовой" в нужном падеже.'
        )
    ]
    user_input = input_str
    messages.append(HumanMessage(content=user_input))
    res = model.invoke(messages)
    messages.append(res)
    return res.content
