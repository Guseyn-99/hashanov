"""Обновить статические страницы: python build.py"""
from html import escape
from pathlib import Path
import json
from lessons import drills, lessons
from interactives import QUESTIONS, walkthrough

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / 'public'


def page(title, body, depth=''):
    home = depth + 'index.html'
    return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · Hashanov</title><link rel="stylesheet" href="{depth}style.css"><script defer src="{depth}script.js"></script></head>
<body><a class="skip" href="#main">К содержанию</a><header class="topbar"><div class="shell masthead">
<a class="brand" href="{home}"><span class="brand-mark" aria-hidden="true">#</span>Hashanov<span class="brand-dot">.</span></a>
<nav class="topnav" aria-label="Навигация"><a href="{home}#topics">Оглавление</a></nav></div></header>
{body}<footer class="shell footer"><span>Hashanov</span><span>Гусейн Гасанов</span></footer></body></html>'''


def topic_card(item):
    return f'''<a class="topic-card" href="topics/{item['slug']}.html">
<strong>{escape(item['title'])}</strong><span>{escape(item['summary'])}</span></a>'''


def homepage():
    groups = list(dict.fromkeys(item['group'] for item in lessons))
    catalog = ''
    for group in groups:
        cards = ''.join(topic_card(item) for item in lessons if item['group'] == group)
        catalog += f'<section class="group"><h3>{group}</h3><div class="card-list">{cards}</div></section>'
    return page('Алгоритмы на Python', f'''<main class="shell home" id="main">
<section class="hero"><p class="eyebrow hero-label">СПРАВОЧНИК ГУСЕЙНА ГАСАНОВА</p>
<h1>Алгоритмы на Python<span class="hero-dot">.</span></h1>
<p class="hero-description">Как узнать задачу, пройти пример руками и объяснить своё решение на собеседовании.</p>
<a class="button" href="#topics">Выбрать тему</a></section>
<section class="topics" id="topics"><h2>Темы справочника</h2>{catalog}</section></main>''')


def quiz(slug):
    fields = []
    for number, (question, options, correct, why) in enumerate(QUESTIONS[slug], 1):
        choices = ''.join(
            f'<label><input type="radio" name="q{number}" value="{i}"><span>{escape(option)}</span></label>'
            for i, option in enumerate(options))
        fields.append(f'''<fieldset data-answer="{correct}"><legend>{number}. {escape(question)}</legend>
<div class="options">{choices}</div><p class="feedback" role="status" data-why="{escape(why, quote=True)}"></p></fieldset>''')
    return f'''<section class="quiz" id="quiz"><h2>Проверь себя</h2><form>{''.join(fields)}
<div class="controls"><button type="reset">Сбросить ответы</button></div></form></section>'''


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
<header class="lesson-head"><p class="eyebrow">{d['group']}</p><h1>{d['title']}</h1><p>{d['signal']}</p></header>
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
    for lesson in lessons:
        (PUBLIC / 'topics' / (lesson['slug'] + '.html')).write_text(article(lesson), encoding='utf-8')
