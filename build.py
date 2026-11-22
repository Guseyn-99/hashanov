"""Обновить статические страницы: python build.py"""
from html import escape
from pathlib import Path
from lessons import BASE, drills, lessons

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / 'public'


def page(title, body, depth=''):
    home = depth + 'index.html'
    return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · Hashanov</title><link rel="stylesheet" href="{depth}style.css"><script defer src="{depth}script.js"></script></head>
<body><a class="skip" href="#main">К содержанию</a><header class="topbar"><div class="shell masthead">
<a class="brand" href="{home}"><span class="brand-mark" aria-hidden="true">#</span>Hashanov<span class="brand-dot">.</span></a>
<nav class="topnav" aria-label="Навигация"><a href="{home}#topics">Оглавление</a><a href="{BASE}index.html">Курс ОП.04</a></nav></div></header>
{body}<footer class="shell footer"><span>Hashanov</span><span>Гусейн Гасанов</span></footer></body></html>'''


def topic_card(item):
    return f'''<a class="topic-card" href="topics/{item['slug']}.html"><span class="topic-info">
<span class="topic-category">{item['module']}</span><strong>{item['title']}</strong>
<span>{item['signal']}</span></span><span class="topic-action">Читать</span></a>'''


def homepage():
    groups = list(dict.fromkeys(item['group'] for item in lessons))
    catalog = ''
    for group in groups:
        cards = ''.join(topic_card(item) for item in lessons if item['group'] == group)
        catalog += f'<section class="group"><h3>{group}</h3><div class="card-list">{cards}</div></section>'
    return page('Алгоритмы на Python', f'''<main class="shell home" id="main">
<section class="hero"><div class="hero-copy"><p class="eyebrow hero-label">СПРАВОЧНИК ГУСЕЙНА ГАСАНОВА</p>
<h1>Алгоритмы<br>на Python<span class="hero-dot">.</span></h1>
<p class="hero-description">Как узнать задачу, пройти пример руками и объяснить своё решение на собеседовании.</p>
<a class="button" href="#topics">Выбрать тему</a></div><div class="hero-visual"><div class="visual-grid"></div>
<div class="hero-code"><div class="hero-code-header"><span></span><span></span><span></span><b>window.py</b></div>
<div class="hero-code-body"><div class="code-comment"># Сдвиг окна</div><div>total -= nums[right - k]</div><div>total += nums[right]</div></div></div></div></section>
<section class="topics" id="topics"><div class="topics-heading"><h2>Темы справочника</h2><span class="topic-count">{len(lessons)} конспектов</span></div>{catalog}</section></main>''')


def article(item):
    d = item
    headers = ''.join(f'<th scope="col">{escape(c)}</th>' for c in d['columns'])
    rows = []
    for step in d['trace']:
        cells = ''.join(f'<td>{escape(str(value))}</td>' for value in step)
        rows.append(f'<tr>{cells}</tr>')
    task, cases = drills[d['slug']]
    return page(d['title'], f'''<main class="shell lesson-layout" id="main"><article class="lesson"><header class="lesson-header">
<p class="eyebrow">{d['group']} / {d['module']}</p><h1>{d['title']}</h1><p class="lesson-intro">{d['signal']}</p></header>
<section id="idea"><h2>Как я рассуждаю</h2><p>{d['idea']}</p></section>
<section id="trace"><h2>Разбор по шагам</h2><p>{d['problem']}</p>
<div class="table-wrap"><table><thead><tr>{headers}</tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
<section id="code"><h2>Решение на Python</h2><div class="code-panel"><div class="code-toolbar"><span>Python 3</span><button type="button" data-copy hidden>Копировать</button></div>
<pre><code>{escape(d['code'])}</code></pre></div><p>Вывод программы</p><pre class="result">{escape(d['output'])}</pre></section>
<section id="cost"><h2>Сложность и границы</h2><p>{d['cost']}</p><p class="note">{d['edge']}</p></section>
<section id="practice"><h2>Проверь себя</h2><p>{d['quiz']}</p><details><summary>Подсказка</summary><p>{d['hint']}</p></details>
<details><summary>Сверить ответ</summary><p>{d['answer']}</p></details><h3>Теперь напиши сам</h3><p>{task}</p><details><summary>Примеры для проверки</summary><p>{cases}</p></details></section>
<section><p><a href="{BASE}{d['source']}">Материал преподавателя по теме · ОП.04</a></p><a href="../index.html#topics">Все темы Hashanov</a></section></article>
<nav class="article-nav" aria-label="Содержание темы"><p>В конспекте</p><a href="#idea">Идея</a><a href="#trace">Ручной прогон</a><a href="#code">Код</a><a href="#cost">Сложность и границы</a><a href="#practice">Практика</a></nav></main>''','../')


if __name__ == '__main__':
    (PUBLIC / 'topics').mkdir(parents=True, exist_ok=True)
    (PUBLIC / 'index.html').write_text(homepage(), encoding='utf-8')
    for lesson in lessons:
        (PUBLIC / 'topics' / (lesson['slug'] + '.html')).write_text(article(lesson), encoding='utf-8')
