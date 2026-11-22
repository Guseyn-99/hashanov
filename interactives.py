"""Сценарии разборов. Номер строки соответствует примеру в lessons.py."""
from dataclasses import dataclass


@dataclass
class Frame:
    line: int
    indices: list
    state: dict
    note: str


def walkthrough(slug):
    frames = []

    def show(line, indices, note, **state):
        frames.append(Frame(line, list(indices), state, note))

    if slug == 'big-o':
        nums = [4, 7, 2, 9]
        count = 0
        show(2, [], 'До начала цикла счётчик равен нулю.', count=0)
        for i, x in enumerate(nums):
            show(4, [i], f'Проверяем остаток: {x} % 2 = {x % 2}.', x=x, count=count)
            if x % 2 == 0:
                count += 1
                show(5, [i], 'Число чётное. Увеличиваем счётчик.', count=count)
        show(6, [], 'Четыре числа проверены. Два из них чётные.', count=count)
    elif slug == 'indices':
        nums = [8, 5, 2, 9]
        total = 0
        show(2, [], 'Берём участок [1, 3). Начнём со второго числа.', left=1, right=3, total=0)
        for i in range(1, 3):
            total += nums[i]
            show(4, [i], f'Прибавляем nums[{i}] = {nums[i]}.', i=i, total=total)
        show(5, [1, 2], 'Правая граница 3 исключена. Возвращаем сумму двух чисел.', total=total)
    elif slug == 'fixed-window':
        nums = [2, 5, 1, 6, 3]
        k = 3
        current = sum(nums[:k])
        best = current
        show(4, range(k), 'Первое окно считаем целиком: 2 + 5 + 1.', k=k, current=current)
        show(5, range(k), 'Эта сумма становится первым рекордом.', current=current, best=best)
        for right in range(k, len(nums)):
            left = right - k
            current -= nums[left]
            show(7, range(left+1, right), f'Уходит число {nums[left]} с индекса {left}.', right=right, current=current, best=best)
            current += nums[right]
            window = range(left+1, right+1)
            show(8, window, f'Добавляем справа {nums[right]}. В окне снова три числа.', current=current, best=best)
            best = max(best, current)
            show(9, window, 'Сравниваем сумму окна с лучшей суммой.', current=current, best=best)
        show(10, [1, 2, 3], 'Лучшее окно выделено: 5 + 1 + 6 = 12.', best=best)
    elif slug == 'variable-window':
        nums = [2, 1, 4, 2]
        left = total = 0
        best = len(nums) + 1
        show(3, [], 'Ищем сумму от 6. Число 5 больше длины списка и обозначает, что ответа пока нет.', left=0, total=0, best=best)
        for right, x in enumerate(nums):
            window = range(left, right+1)
            total += x
            show(5, window, f'Добавляем {x} справа. ' + ('Суммы хватает.' if total >= 6 else 'Сумма пока меньше 6.'), left=left, right=right, total=total, best=best)
            while total >= 6:
                window = range(left, right+1)
                best = min(best, len(window))
                show(7, window, f'Сумма подходит. Длина этого окна равна {len(window)}.', total=total, best=best)
                removed = nums[left]
                total -= removed
                left += 1
                show(9, range(left,right+1), f'Вычли {removed} и сдвинули левую границу. Ещё раз проверим условие while.', left=left, right=right, total=total, best=best)
        show(10, [2, 3], 'Ответ — два элемента. Окно [4, 2] даёт сумму 6.', best=best)
    elif slug == 'prefix':
        nums = [3, 1, 4, 2]
        prefix = [0]
        show(2, [], 'До первого числа сумма равна нулю.', prefix=prefix.copy())
        for i, x in enumerate(nums):
            prev = prefix[-1]
            prefix.append(prev + x)
            show(4, range(i+1), f'Берём последнюю сумму {prev} и прибавляем {x}.', x=x, prefix=prefix.copy())
        for left, right in [(1,3),(0,4)]:
            show(7, range(left,right), f'Сумма [{left}, {right}) равна {prefix[right]} − {prefix[left]} = {prefix[right]-prefix[left]}.', left=left, right=right, prefix=prefix.copy())
    elif slug == 'set':
        nums = [1, 3, 1, 5, 3, 7]
        seen = set()
        result = []
        show(3, [], 'Создали пустое множество и пустой список ответа.', seen='set()', result=[])
        for i, x in enumerate(nums):
            new = x not in seen
            show(5, [i], f'{x} встречается впервые.' if new else f'{x} уже есть в seen. Пропускаем повтор.', x=x, seen=str(seen), result=result.copy())
            if new:
                seen.add(x)
                result.append(x)
                show(7, [i], f'Отметили {x} в seen и дописали его в конец result.', seen=str(seen), result=result.copy())
        show(8, [], 'Выводим числа в порядке первых появлений.', result=result)
    else:
        assert slug == 'dict'
        nums = [4, 7, 4, 4]
        counts = {}
        show(2, [], 'Словарь частот пока пуст.', counts={})
        for i, x in enumerate(nums):
            before = counts.get(x, 0)
            counts[x] = before + 1
            show(4, [i], f'Для ключа {x} было {before}. Добавляем одно появление.', x=x, counts=counts.copy())
        show(5, [], 'Четвёрка встретилась трижды, семёрка — один раз.', counts=counts)
    return nums, frames


# Вопрос, варианты, индекс верного ответа, объяснение.
QUESTIONS = {
 'home': [
  ('В условии сказано «ровно три дня подряд». Какой разбор открыть?', ['Префиксные суммы', 'Окно фиксированной длины', 'Словарь и частоты'], 1, 'Участок непрерывный, его длина заранее известна.'),
  ('Чем удобно отмечать числа, которые уже встречались?', ['Множеством set', 'Одним счётчиком', 'Строкой с индексом'], 0, 'Множество хранит разные числа и позволяет проверять x in seen.')],
 'big-o': [
  ('В списке 8 чисел. Сколько раз цикл проверит чётность?', ['4', '8', '16'], 1, 'На каждое число приходится одна проверка.'),
  ('Как растёт число проверок при одном проходе?', ['O(1)', 'O(n²)', 'O(n)'], 2, 'Вдвое больше чисел — вдвое больше проверок.')],
 'indices': [
  ('Какие индексы перебирает range(1, 3)?', ['1, 2', '1, 2, 3', '2, 3'], 0, 'Перебор начинается с 1 и заканчивается перед 3.'),
  ('Сколько элементов на участке [2, 2)?', ['2', '1', '0'], 2, 'Длина равна разности границ: 2 − 2 = 0.')],
 'fixed-window': [
  ('Окно [2, 5, 1] сдвинули на шаг. Справа входит 6. Что вычесть?', ['5', '1', '2'], 2, 'Левый элемент 2 покидает окно.'),
  ('С чего начать best, если числа могут быть отрицательными?', ['С нуля', 'С суммы первого окна', 'С длины списка'], 1, 'Начальное значение должно быть суммой реально существующего окна.')],
 'variable-window': [
  ('Сумма достигла target. Что сделать перед сжатием?', ['Проверить длину для best', 'Обнулить сумму', 'Закончить весь поиск'], 0, 'Сейчас окно подходит. После сжатия суммы может уже не хватить.'),
  ('Левая и правая границы включены. Как найти длину?', ['right − left', 'left + right', 'right − left + 1'], 2, 'Окно с одинаковыми границами содержит один элемент.')],
 'prefix': [
  ('Почему prefix начинается с 0?', ['Это индекс максимума', 'До первого числа сумма равна нулю', 'Все числа положительные'], 1, 'Нуль обозначает сумму пустого начала списка.'),
  ('Как получить сумму на участке [1, 3)?', ['prefix[3] − prefix[1]', 'prefix[3] + prefix[1]', 'prefix[2] − prefix[1]'], 0, 'Из суммы первых трёх чисел вычитаем первое число.')],
 'set': [
  ('Как создать пустое множество?', ['[]', '{}', 'set()'], 2, 'set() создаёт множество. {} создаёт словарь, а [] — список.'),
  ('Зачем в примере нужен result?', ['Для хранения индексов', 'Для сохранения порядка первых появлений', 'Для сортировки'], 1, 'Добавляем новое число в конец списка при первой встрече.')],
 'dict': [
  ('Что вернёт {}.get(7, 0)?', ['0', '7', '1'], 0, 'Ключа 7 пока нет. Метод возвращает заданное значение по умолчанию.'),
  ('В словаре {4: 3, 7: 1} увеличили счётчик числа 4. Сколько ключей теперь?', ['3', '4', '2'], 2, 'Изменилось значение существующего ключа. Ключи по-прежнему 4 и 7.')],
}
