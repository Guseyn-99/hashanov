function setupPlayer(player) {
  const frames = JSON.parse(player.dataset.frames)
  const lines = [...player.querySelectorAll('.line')]
  const cells = [...player.querySelectorAll('.cell')]
  const buttons = [...player.querySelectorAll('[data-step]')]
  let position = 0

  function draw() {
    const frame = frames[position]
    lines.forEach(line => line.classList.toggle('active', Number(line.dataset.line) === frame.line))
    cells.forEach((cell, i) => cell.classList.toggle('active', frame.indices.includes(i)))
    const variables = player.querySelector('dl')
    variables.replaceChildren()
    for (const [name, value] of Object.entries(frame.state)) {
      const term = document.createElement('dt')
      term.textContent = name
      const definition = document.createElement('dd')
      definition.textContent = typeof value === 'string' ? value : JSON.stringify(value)
      variables.append(term, definition)
    }
    player.querySelector('.explain').textContent = 'Строка ' + frame.line + '. ' + frame.note
    player.querySelector('.counter').textContent = 'Шаг ' + (position + 1) + ' из ' + frames.length
    for (const button of buttons) {
      button.disabled = ['first','back'].includes(button.dataset.step)
        ? position === 0 : position === frames.length - 1
    }
  }
  for (const button of buttons) {
    button.addEventListener('click', () => {
      position = {first: 0, back: position - 1, next: position + 1, last: frames.length - 1}[button.dataset.step]
      draw()
    })
  }
  const copy = player.querySelector('[data-copy]')
  copy.hidden = !navigator.clipboard
  copy.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(lines.map(line => line.textContent).join('\n'))
      copy.textContent = 'Скопировано'
    } catch {
      copy.textContent = 'Выдели код для копирования'
    }
  })
  draw()
}

function setupQuiz(form) {
  for (const field of form.querySelectorAll('fieldset')) {
    const feedback = field.querySelector('.feedback')

    field.addEventListener('change', event => {
      const correct = event.target.value === field.dataset.answer
      feedback.textContent = (correct ? 'Верно. ' : 'Неверно. ') + feedback.dataset.why
      field.dataset.result = correct ? 'yes' : 'no'
    })

    form.addEventListener('reset', () => {
      feedback.textContent = ''
      field.removeAttribute('data-result')
    })
  }
}

function setupWindow(box) {
  const nums = [3, 2, 4, 1, 7]
  const target = 8
  let left = 0, right = 0, total = 0, best = Infinity
  const cells = nums.map((value, i) => {
    const el = document.createElement('span')
    el.className = 'cell'
    el.innerHTML = '<small>' + i + '</small><b>' + value + '</b>'
    box.querySelector('.cells').append(el)
    return el
  })
  function draw(message) {
    cells.forEach((el, i) => el.classList.toggle('active', i >= left && i < right))
    const len = right - left
    if (total >= target) best = Math.min(best, len)
    box.querySelector('.metrics').textContent = 'Окно [' + left + ', ' + right + ') · Сумма ' + total + ' · Длина ' + len + ' · Лучшая длина ' + (Number.isFinite(best) ? best : '—')
    box.querySelector('.window-note').textContent = message
    box.querySelector('[data-move="expand"]').disabled = right === nums.length
    box.querySelector('[data-move="shrink"]').disabled = left === right
  }
  for (const button of box.querySelectorAll('[data-move]')) {
    button.addEventListener('click', () => {
      if (button.dataset.move === 'reset') {
        left = right = total = 0
        best = Infinity
        draw('Окно пустое. Добавь первое число.')
        return
      }
      if (button.dataset.move === 'expand') total += nums[right++]
      else total -= nums[left++]
      let tip = total >= target ? 'Суммы хватает. Проверь, можно ли укоротить окно слева.' : 'Сумма меньше 8. Добавь следующее число справа.'
      if (right === nums.length && total < target) tip = 'Справа чисел больше нет. Можно начать заново.'
      if (best === 2) tip = 'Нашёл оптимум: 1 + 7 = 8. В списке нет одного числа от 8.'
      draw(tip)
    })
  }
  draw('Окно пустое. Добавь первое число.')
}

document.querySelectorAll('.player').forEach(setupPlayer)
document.querySelectorAll('.quiz form').forEach(setupQuiz)
document.querySelectorAll('[data-window]').forEach(setupWindow)
