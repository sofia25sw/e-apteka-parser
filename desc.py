# from scrap_thread import scrap
#
# url = '"http://e-apteka.md/products/Ekvator_tab_2010mg__301"'
# with open('111.json', 'w', encoding='utf-8') as fp:
#     scrap([url], fp, 1)

from bs4 import BeautifulSoup
from requests import get
from re import sub
from pprint import pprint





def process_desc(content: list ) -> dict:
    # Создадим словарик для того, чтобы пихать туда описание в виде ключ-значение
    dct = {}
    # Зададим начальные значения значения ключ-значению, чтобы просто потому что надо, хз как объяснить, я вообще немного
    # уже заипалься, Соня вот не читает статьи, не учит питон, хотя давно уже должна бы выучить язык и учиться его
    # использовать. Но слишком часто ловлю себя на мысли, что ты иногда не понимаешь фундаментальных вещей в
    # программировании. Типа, какого типа будет переменная вот на этом участке кода, какое у нее будет значение.
    # Код надо читать и понимать, что он делает, иначе все никуда не годится. Первый же баг и ты не будешь понимать, как
    # его исправить. Моим заданием тебе в солик будет не задака по проге. А ты прочтешь книгу.
    # Марк Лутц, называется "Изучаем Python". От корки до корки! Будешь мне рассказывать, чему ты научилась за сегодняшний
    # день, что узнала нового и где по-твоему это можно использовать. Я хочу сделать из тебя программиста. А пока что ты
    # похожа на собачку, у которой лапки на клавиатуре :) Не обижайся, я правда пытаюсь тебе помочь. Но ты слишком редко
    # идешь мне навстречу и совершаешь самостоятельные попытки обучения. Ты боишься писать без меня код. Ты не читаешь
    # что-нибудь для развития своих навыков, не смотришь видео-лекции по проге на ютубе. В открытом пиратском доступе есть
    # миллион курсов, от тех же гикбрейнс. Посиди, посмотри. Не заставляю тебя платить за курс, делать домашки. Просто
    # смотри, изучай, пиши конспекты. А то ты так забила на учебу, а еще и на изучение питона. Оно само к тебе не придет,
    # нужно что-то делать. Не знаю, почему возможность съехать из общаги не мотивирует тебя что-то делать. Для меня
    # достаточно хороший мотиватор. Но ты еще слишком мелко барахтаешься. Выйдешь из универа с дипломом и попадешь в
    # глубоооокий океан. А ты пока еле-еле в луже плещешься. Так что берись-ка за головушку. Головушка умная, я проверял.
    # Значит, головушка может. Просто головушка лентяйка. Просто чего-то хочет, но не делает почти никаких движений в
    # сторону исполнения своих желаний. Я в тебя верю. И очень-очень люблю тебя <3 И твою головушку :)
    key, val = 'iidnousifub', ''
    # Так и не понял, на кой хрен мне тут i, но пусть будет. Как говорится: работает - не трогай.
    for i, tag in enumerate(content):
        # Элементы списка представляют из себя экземпляры класса Tag, поэтому мы сначала превратим их в строки, чтобы
        # удобнее работать со строковыми методами и регулярками
        tag = str(tag)
        # Ключи у нас окружены тегом 2 заголовка, поэтому так мы и будем их отбирать
        # Если у нас есть тег h2 внутри строки, то вот он ключ
        # В таком случае мы должны записать уже полученную пару ключ-значение в словарб, а затем очистить их
        # Так у нас запишется накопленная пара, и мы сможем искать новую пару
        if tag.startswith('<h2>'):
            # Здесь при помощи регулярок я удаляю все html-теги из строки, чтобы оставить только сам ключ
            tag = sub(r'<.+?>', '', tag).replace(r'\xa0', ' ')
            # Тут я просто выбрал все пробелы, которые встречаются более одного раза подряд и заменил на один пробел
            # \s в регулярках выбирает любой пробельный символ, в том числе и символ переноса строки
            # Чтобы у меня не удалялись переносы строк я просто сделал поиск и замену нескольких пробелов подряд, пока не
            # встречу конец строки ($), букву (\w) или цифру (\d)
            tag = sub(r'\s+(?=($|\S))', ' ', tag).strip()
            # Убираем все теги из значения в том числе
            dct[key] = sub(r'<.+?>', '', val)
            # Иногда в html пишут "&nbsp;", что означает пробел, который не переносит текст на новую строку, если место на
            # этой закончилось. При парсинге этот специальный пробел превращается в "\xa0". Нам это нахрен не нужно,
            # поэтому делаем его замену на обычный пробел
            dct[key] = dct[key].replace(r'\xa0', ' ')
            # И пробелы удаляем аналогично ключу
            dct[key] = sub(r'\s+(?=($|\S))', ' ', dct[key])
            # Убираем лишние пробелы в начале и конце строки значения
            dct[key] = dct[key].strip()
            # Когда мы добавили данные в наш словарь, можно менять старый ключ на свеженайденный и повторять процедуру
            key = tag
            val = ''
        # Если же мы нашли не тег заголовка, то скорее всего это значение или часть значения
        # Иногда значение, соответствующее одному ключу может находиться в разных строках, соответственно, строки надо
        # склеить
        else:
            # Т.к. переменная val у нас уже существует, то мы просто к ней через перенос строки добавляем очередное значение
            # Здесь прикол в том, что после нахождения "ключа", значение val обнуляется
            # А затем пока не найден следующий ключ, значение val будет дополняться
            val += ' ' + tag
    val = sub(r'\s+(?=($|\S))', ' ', val).replace('\xa0', ' ').strip()
    val = sub(r'</?\w+>', '', val)
    # Вот это надо сделать для того, чтобы добавить в словарь пару ключ-значение, которая оказалась последней
    # Вообще мы добавляем пару ключ-значение только в тот момент, когда находим следующий ключ
    # А если цикл закончился, так как у нас кончился список из внутренностей тега с описанием, то надо принудительно
    # оставшуюся пару добавить в словарь
    dct[key] = val
    # Первым элементом в списке из внутренностей тега описания не является ключ. Мы не знаем, в какой момент мы встретим
    # ключ. Поэтому не можем просто взять и отсечь кусок списка, сделав срез.
    # По умолчанию, ключ у нас равен пустой строке. Когда мы найдем первый настоящий ключ, который будет содержать
    # тег h2, то значения, предшествующие ему будут записаны в словарь с ключом ''
    # Поэтому тут нет ничего проще, кроме как просто убрать эту пару из словаря
    del dct['iidnousifub']
    return dct


if __name__ == '__main__':
    # Урл элемента
    url = "http://e-apteka.md/products/Ekvator_tab_2010mg__301"
    # Скачиваем и берем текст html
    page = get(url).text
    # Создаем из него soup
    soup = BeautifulSoup(page, 'html.parser')
    # Находим тег с описанием и берем от него contents, чтобы получить список внутренних тегов/текстов
    desc = soup.find('div', {'class': 'description'}).contents
    # Это просто, чтоб было понятно, где есть перенос строки, а где нет
    print('\n--- '.join(map(str, desc)))
    # Готово, епта
    pprint(process_desc(desc))

