function startGame(board) {
  const find = selector => board.querySelector(selector)
  const isSeen = board.dataset.game === 'seen'
  const seenRounds = [
    [[1, 3, 1, 5], [2, 6, 6, 2]],
    [[4, 4, 2, 4, 2], [0, 3, 0, 0, 5]],
    [[-1, 0, 1, -1, 0, 2], [3, -3, 3, 7, -3, 7]]
  ]
  const windowRounds = [
    [[2, 1, 6, 4, 3], [5, 2, 3, 8, 4]],
    [[3, 4, 2, 7, 5, 1], [2, 5, 3, 8, 4, 6]],
    [[-6, -2, -3, -7, -1], [-4, -8, -2, -1, -7]]
  ]
  let sequence, round, points, nums, cursor, width, attempted, seen
  const actions = find('.game-actions')
  const next = find('[data-next]')
  const reset = find('[data-new]')

  function action(text, handler, primary = false) {
    const button = document.createElement('button')
    button.type = 'button'
    button.textContent = text
    if (primary) button.className = 'primary'
    button.addEventListener('click', handler)
    actions.append(button)
    return button
  }

  function note(text, state = '') {
    find('.game-note').dataset.result = state
    find('.game-note').textContent = text
  }

  function draw() {
    const tiles = find('.tiles').children
    for (let i = 0; i < tiles.length; i++) {
      tiles[i].classList.toggle('in-play', i >= cursor && i < cursor + width)
      tiles[i].classList.toggle('past', isSeen && i < cursor)
    }
    find('[data-score]').textContent = 'Очки · ' + points
    if (isSeen) {
      find('[data-task]').textContent = cursor < nums.length ? 'Число ' + nums[cursor] + ' уже встречалось?' : 'Список пройден'
      find('.game-memory').textContent = 'seen = ' + (seen.size ? '{' + [...seen].join(', ') + '}' : 'set()')
    } else {
      const slice = nums.slice(cursor, cursor + width)
      find('.game-memory').textContent = 'Сумма окна: ' + slice.map(n => n < 0 ? '(' + n + ')' : n).join(' + ') + ' = ' + sum(slice)
      actions.children[0].disabled = cursor === 0
      actions.children[1].disabled = cursor === nums.length - width
    }
  }

  function finishRound(message) {
    actions.hidden = true
    if (round === sequence.length - 1) {
      note(message + ' Игра пройдена. Очки за ответы с первой попытки: ' + points + ' из ' +
        (isSeen ? sequence.reduce((n, list) => n + list.length, 0) : sequence.length) + '.', 'yes')
      reset.textContent = 'Сыграть ещё раз'
      reset.focus({preventScroll: true})
    } else {
      note(message, 'yes')
      next.hidden = false
      next.focus({preventScroll: true})
    }
  }

  function classify(repeat) {
    const value = nums[cursor]
    const known = seen.has(value)
    if (known !== repeat) {
      attempted = true
      note(known ? 'Посмотри в seen: ' + value + ' там уже есть.' : 'В seen пока нет числа ' + value + '. Проверь ещё раз.', 'no')
      return
    }
    if (!attempted) points++
    attempted = false
    seen.add(value)
    cursor++
    draw()
    const explanation = known ? 'Верно. Это повтор, множество осталось прежним.' : 'Верно. Добавили ' + value + ' в seen.'
    if (cursor === nums.length) finishRound(explanation)
    else note(explanation, 'yes')
  }

  function sum(values) { return values.reduce((total, value) => total + value, 0) }

  function move(delta) {
    const previous = cursor
    cursor += delta
    const leaving = delta === 1 ? nums[previous] : nums[previous + width - 1]
    const entering = delta === 1 ? nums[cursor + width - 1] : nums[cursor]
    note('Из окна вышло ' + leaving + ', вошло ' + entering + '.')
    draw()
  }

  function takeWindow() {
    const sums = nums.slice(width - 1).map((_, i) => sum(nums.slice(i, i + width)))
    if (sums[cursor] !== Math.max(...sums)) {
      attempted = true
      note('Есть окно с большей суммой. Сдвинь границу и сравни результат.', 'no')
      return
    }
    if (!attempted) points++
    draw()
    finishRound('Верно. Сумма ' + sums[cursor] + ' — самая большая для окна длины ' + width + '.')
  }

  function loadRound() {
    nums = sequence[round]
    cursor = 0
    width = isSeen ? 1 : [2, 3, 2][round]
    seen = new Set()
    attempted = false
    actions.replaceChildren()
    actions.hidden = false
    next.hidden = true
    reset.textContent = 'Начать сначала'
    find('[data-round]').textContent = 'Раунд ' + (round + 1) + ' из ' + sequence.length
    find('.tiles').replaceChildren(...nums.map(n => {
      const tile = document.createElement('span')
      tile.textContent = n
      return tile
    }))
    if (isSeen) {
      action('Новое число', () => classify(false), true)
      action('Повтор', () => classify(true))
      note('Иди слева направо. Сначала загляни в seen, затем сделай ход.')
    } else {
      find('[data-task]').textContent = 'Где самая большая сумма ' + (width === 2 ? 'двух' : 'трёх') + ' соседних чисел?'
      action('Влево', () => move(-1))
      action('Вправо', () => move(1))
      action('Выбрать окно', takeWindow, true)
      note('Сдвигай окно, сравнивай суммы и выбери лучшее.')
    }
    draw()
  }

  function restart() {
    sequence = (isSeen ? seenRounds : windowRounds).map(pool => pool[Math.floor(Math.random() * pool.length)])
    round = 0
    points = 0
    loadRound()
  }
  next.addEventListener('click', () => { round++; loadRound(); actions.querySelector('button:not(:disabled)').focus({preventScroll: true}) })
  reset.addEventListener('click', restart)
  restart()
}

document.querySelectorAll('[data-game]').forEach(startGame)
