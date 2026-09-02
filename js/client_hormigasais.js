/*
 * Cliente web LBH para /video/analizar.
 */
(function (window, document) {
  'use strict'

  const DEFAULT_ENDPOINT = 'https://api.hormigasais.com/video/analizar'
  const ENDPOINT = window.HORMIGASAIS_VIDEO_API || DEFAULT_ENDPOINT

  function getElement(id) {
    return document.getElementById(id)
  }

  function setText(id, value) {
    const element = getElement(id)
    if (element) element.textContent = value == null ? '—' : String(value)
  }

  function showLoading(isLoading) {
    const element = getElement('video-loading')
    if (element) element.hidden = !isLoading
  }

  function showError(message) {
    const element = getElement('video-error')
    if (element) {
      element.hidden = false
      element.textContent = message
    }
  }

  function clearError() {
    const element = getElement('video-error')
    if (element) {
      element.hidden = true
      element.textContent = ''
    }
  }

  async function readJsonSafely(response) {
    const contentType = response.headers.get('content-type') || ''
    const raw = await response.text()
    let data = null
    try {
      data = raw ? JSON.parse(raw) : null
    } catch (_) {
      data = null
    }

    if (!response.ok || !data || typeof data !== 'object' || Array.isArray(data)) {
      const error = new Error('El servicio de video no devolvió una respuesta JSON válida.')
      error.status = response.status
      error.contentType = contentType
      throw error
    }
    return data
  }

  function renderizarVeredicto(data) {
    setText('resultado-resolucion', data.resolucion_definitiva || data.clasificacion || 'NO_DETERMINADO')
    setText('score-biologico', data.score_biologico)
    setText('score-ia', data.score_ia)
    setText('badge-feromona', data.badge_feromona || (data.feromona && data.feromona.type ? data.feromona.type : 'LBH_FEROMONA'))
    setText('resultado-nota', data.nota)

    const result = getElement('video-result')
    if (result) result.hidden = false

    return data
  }

  async function analizarVideoEnjambre(urlVideo) {
    const url = String(urlVideo || '').trim()
    if (!/^https?:\/\//i.test(url)) {
      throw new Error('Introduce una URL HTTP o HTTPS válida.')
    }

    clearError()
    showLoading(true)
    try {
      const response = await fetch(ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ url })
      })
      const data = await readJsonSafely(response)
      return renderizarVeredicto(data)
    } catch (error) {
      showError(error && error.message ? error.message : 'No se pudo conectar con el servicio de video.')
      throw error
    } finally {
      showLoading(false)
    }
  }

  window.analizarVideoEnjambre = analizarVideoEnjambre
  window.renderizarVeredicto = renderizarVeredicto
})(window, document)
