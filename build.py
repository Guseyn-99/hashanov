"""Обновить статические страницы: python build.py"""
from html import escape
from pathlib import Path
import json
from lessons import drills, lessons
from interactives import QUESTIONS, HINTS, walkthrough

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / 'public'


def page(title, body, depth='', area='topics', extra_script=''):
    home = depth + 'index.html'
    contents = '#topics' if title == 'Алгоритмы на Python' else home + '#topics'
    nav = ''.join(
        f'<a href="{url}"' + (' aria-current="location"' if area == key else '') + f'>{name}</a>'
        for key, name, url in [('topics', 'Модули', contents), ('games', 'Игры', depth + 'games.html')])
    script = f'<script defer src="{depth}{extra_script}"></script>' if extra_script else ''
    return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · Hashanov</title><link rel="stylesheet" href="{depth}style.css"><script defer src="{depth}script.js"></script>{script}</head>
<body><a class="skip" href="#main">К содержанию</a><header class="topbar"><div class="shell masthead">
<a class="brand" href="{home}"><span class="brand-mark" aria-hidden="true">#</span>Hashanov<span class="brand-dot">.</span></a>
<nav class="topnav" aria-label="Навигация">{nav}</nav></div></header>
{body}<footer class="shell footer"><span>Hashanov</span><span>Гусейн Гасанов</span></footer></body></html>'''


MODULES = {
    'Основы': 'Считаем операции и учимся задавать границы участка.',
    'Массивы': 'Ищем нужный отрезок и считаем суммы за один проход.',
    'Хеш-структуры': 'Запоминаем числа и считаем, сколько раз они встретились.',
}

GAMES = {
    'seen': ('Охота на повторы', 'Отмечай, какие числа уже встречались.', 'set', 'set()'),
    'window': ('Поймай окно', 'Найди отрезок с самой большой суммой.', 'fixed-window', '[i:j]'),
}


def homepage():
    modules = []
    for number, (group, intro) in enumerate(MODULES.items(), 1):
        group_lessons = [item for item in lessons if item['group'] == group]
        rows = ''.join(
            f'<li><a href="topics/{item["slug"]}.html"><small>{number}.{i}</small>'
            f'<span>{escape(item["title"])}</span><i aria-hidden="true">›</i></a></li>'
            for i, item in enumerate(group_lessons, 1))
        modules.append(f'''<section class="module"><header>
<p class="eyebrow">Модуль {number:02}</p><h3>{group}</h3><p>{intro}</p></header>
<ol class="lesson-list">{rows}</ol></section>''')
    return page('Алгоритмы на Python', f'''<main class="shell home" id="main">
<section class="hero"><p class="eyebrow hero-label">Справочник Гусейна Гасанова</p>
<h1>Алгоритмы на Python<span class="hero-dot">.</span></h1>
<p class="hero-description">Разбираю задачи на маленьких примерах и показываю, что происходит на каждом шаге.</p>
<a class="button" href="#topics">К модулям</a><a class="hero-link" href="games.html">Перейти к играм</a></section>
<section class="topics" id="topics"><h2>Модули</h2>{''.join(modules)}</section></main>''')


def quiz(slug):
    fields = []
    for number, (question, options, correct, why) in enumerate(QUESTIONS[slug], 1):
        choices = []
        for i, option in enumerate(options):
            reason = why if i == correct else HINTS[slug][number - 1][i]
            choices.append(f'''<div class="choice"><button type="button" data-correct="{int(i == correct)}"
data-reason="{escape(reason, quote=True)}"><span class="letter" aria-hidden="true">{'АБВ'[i]}</span>
<span>{escape(option)}</span><span class="mark" aria-hidden="true"></span></button>
<p class="answer-note" hidden></p></div>''')
        fields.append(f'''<div class="question" role="group" aria-labelledby="question-{number}">
<header><span class="eyebrow">Вопрос {number} из 2</span><h3 id="question-{number}">{escape(question)}</h3></header>
<div class="options">{''.join(choices)}</div><span class="sr-only" role="status"></span></div>''')
    return f'''<section class="quiz" id="quiz"><h2>Проверь себя</h2>{''.join(fields)}
<div class="controls"><button type="button" data-retry>Ответить заново</button></div></section>'''


def games_index():
    cards = ''.join(f'''<li><a class="game-link" href="games/{key}.html">
<span class="game-token" aria-hidden="true">{token}</span><span><strong>{title}</strong><small>{summary}</small></span>
<i aria-hidden="true">›</i></a></li>''' for key, (title, summary, _, token) in GAMES.items())
    return page('Игры', f'''<main class="shell home" id="main"><header class="section-intro">
<p class="eyebrow">Практика на Python</p><h1>Игры</h1><p>Один ход — один шаг алгоритма. В каждой игре три раунда.</p></header>
<ul class="game-list">{cards}</ul></main>''', area='games')


def game_page(key):
    title, summary, topic, _ = GAMES[key]
    return page(title, f'''<main class="shell reading" id="main"><a class="backlink" href="../games.html">Все игры</a>
<header class="section-intro"><h1>{title}</h1><p>{summary}</p></header>
<section class="game-board" data-game="{key}" aria-label="Игровое поле">
<div class="game-bar"><strong data-round></strong><span data-score></span></div>
<div class="arena"><h2 data-task></h2><div class="tiles"></div><p class="game-memory"></p>
<div class="game-actions controls"></div><p class="game-note" role="status"></p></div>
<div class="controls game-foot"><button type="button" data-new>Начать сначала</button>
<button type="button" class="primary" data-next hidden>Следующий раунд</button></div></section>
<a class="backlink" href="../topics/{topic}.html">Разобрать тему на Python</a></main>''', '../', 'games', 'games.js')


def player(d):
    nums, frames = walkthrough(d['slug'])
    cells = ''.join(f'<span class="cell"><small>{i}</small><b>{n}</b></span>' for i,n in enumerate(nums))
    lines = '\n'.join(f'<span class="line" data-line="{i}">{escape(line)}</span>'
                       for i,line in enumerate(d['code'].splitlines(), 1))
    data = escape(json.dumps([dict(vars(f), state={key: value if isinstance(value, str) else repr(value) for key, value in f.state.items()}) for f in frames], ensure_ascii=False), quote=True)
    return f'''<div class="player" data-frames="{data}">
<div class="controls player-controls" role="group" aria-label="Управление разбором">
<button type="button" data-step="first">В начало</button><button type="button" data-step="back">Назад</button>
<button type="button" class="primary" data-step="next">Дальше</button><button type="button" data-step="last">В конец</button>
<span class="counter"></span></div>
<div class="source" id="code"><div class="code-toolbar"><span>Python 3</span><button type="button" data-copy>Копировать</button></div>
<pre tabindex="0" aria-label="Код примера"><code>{lines}</code></pre></div>
<div class="memory"><h3>Список nums</h3><div class="cells">{cells}</div><h3>Переменные</h3><dl></dl></div>
<p class="explain" aria-live="polite"></p></div>'''


def window_lab():
    return '''<section id="window"><h2>Подвигай границы сам</h2>
<p>Найди самый короткий участок с суммой от 8. Добавляй числа справа. Когда суммы хватит, попробуй убрать число слева.</p>
<div class="window-box" data-window><div class="cells"></div><p class="metrics"></p>
<div class="controls"><button class="primary" data-move="expand">Добавить справа</button><button data-move="shrink">Убрать слева</button>
<button data-move="reset">Заново</button></div><p class="window-note" role="status"></p></div></section>'''


def trace_table(d):
    headings = ''.join(f'<th scope="col">{escape(c)}</th>' for c in d['columns'])
    rows = []
    for step in d['trace']:
        cells = ''.join(f'<td>{escape(str(value))}</td>' for value in step)
        rows.append(f'<tr>{cells}</tr>')
    return f'<details><summary>Весь прогон таблицей</summary><div class="table-scroll"><table><thead><tr>{headings}</tr></thead><tbody>{"".join(rows)}</tbody></table></div></details>'


def article(d):
    slug = d['slug']
    task, cases = drills[slug]
    extra = window_lab() if slug == 'variable-window' else ''
    return page(d['title'], f'''<main class="shell reading" id="main"><article>
<header class="lesson-head"><p class="eyebrow">Модуль {list(MODULES).index(d['group']) + 1:02} · {d['group']}</p><h1>{d['title']}</h1><p>{d['signal']}</p></header>
<nav class="jump" aria-label="На этой странице"><a href="#trace">Разбор</a><a href="#cost">Сложность</a><a href="#practice">Практика</a><a href="#quiz">Тест</a></nav>
<section class="idea" id="idea"><h2>Как я рассуждаю</h2><p>{d['idea']}</p></section>
<section id="trace"><h2>Разбор по шагам</h2><p>{d['problem']}</p>{player(d)}{trace_table(d)}
<details><summary>Вывод программы</summary><pre>{escape(d['output'])}</pre></details></section>{extra}
<section id="cost"><h2>Сложность и границы</h2><p>{d['cost']}</p><details><summary>Границы и частые ошибки</summary><p>{d['edge']}</p></details></section>
<section id="practice"><h2>Самостоятельная практика</h2><p>{task}</p><details><summary>Примеры для проверки</summary><p>{cases}</p></details>
<details><summary>Ещё одна задача</summary><p>{d['quiz']}</p><details><summary>Подсказка</summary><p>{d['hint']}</p></details>
<details><summary>Сверить ответ</summary><p>{d['answer']}</p></details></details></section>{quiz(slug)}</article></main>''','../')


if __name__ == '__main__':
    (PUBLIC / 'topics').mkdir(parents=True, exist_ok=True)
    (PUBLIC / 'index.html').write_text(homepage(), encoding='utf-8')
    (PUBLIC / 'games').mkdir(exist_ok=True)
    (PUBLIC / 'games.html').write_text(games_index(), encoding='utf-8')
    for key in GAMES:
        (PUBLIC / 'games' / f'{key}.html').write_text(game_page(key), encoding='utf-8')
    for lesson in lessons:
        (PUBLIC / 'topics' / (lesson['slug'] + '.html')).write_text(article(lesson), encoding='utf-8')
