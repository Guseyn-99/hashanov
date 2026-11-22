const copyButton = document.querySelector('[data-copy]')

if (copyButton && navigator.clipboard) {
  const code = copyButton.closest('.code-panel').querySelector('code')
  let resetTimer

  copyButton.hidden = false
  copyButton.addEventListener('click', async () => {
    clearTimeout(resetTimer)

    try {
      await navigator.clipboard.writeText(code.textContent)
      copyButton.textContent = 'Скопировано'
    } catch {
      copyButton.textContent = 'Не удалось скопировать'
    }

    resetTimer = setTimeout(() => {
      copyButton.textContent = 'Копировать'
    }, 2200)
  })
}
