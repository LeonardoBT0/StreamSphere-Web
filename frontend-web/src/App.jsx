import { useState } from 'react'

const CATEGORIES = [
  'Entretenimiento', 'Educacion', 'Musica', 'Videojuegos',
  'Deportes', 'Noticias', 'Tecnologia', 'Cocina',
  'Viajes', 'Vlogs', 'Cine', 'Ciencia'
]

const INITIAL_FORM = {
  duration_seconds: 420,
  category: 'Musica',
  publish_hour: 20,
  publish_weekday: 5,
  title_length: 55,
  description_length: 300,
  is_hd: 1,
  creator_subscribers: 500000,
  creator_avg_views_30d: 25000
}

function App() {
  const [form, setForm] = useState(INITIAL_FORM)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  function handleChange(e) {
    const { name, value, type } = e.target
    setForm(prev => ({
      ...prev,
      [name]: type === 'number' || type === 'range' ? Number(value) : value
    }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const res = await fetch('/api/analysis/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      })

      if (!res.ok) {
        const text = await res.text()
        throw new Error(text || `Error ${res.status}`)
      }

      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function getBadgeClass(rendimiento) {
    if (rendimiento === 'ALTO') return 'badge badge-alto'
    if (rendimiento === 'MEDIO') return 'badge badge-medio'
    return 'badge badge-bajo'
  }

  return (
    <div className="container">
      <header className="header">
        <h1>StreamSphere</h1>
        <p className="subtitle">Analisis de rendimiento de video</p>
      </header>

      <div className="content">
        <form className="form" onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="field">
              <label>Duracion (segundos)</label>
              <input type="number" name="duration_seconds" value={form.duration_seconds} onChange={handleChange} min={1} max={7200} />
            </div>

            <div className="field">
              <label>Categoria</label>
              <select name="category" value={form.category} onChange={handleChange}>
                {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>

            <div className="field">
              <label>Hora de publicacion (0-23)</label>
              <input type="number" name="publish_hour" value={form.publish_hour} onChange={handleChange} min={0} max={23} />
            </div>

            <div className="field">
              <label>Dia de la semana (0=Lun, 6=Dom)</label>
              <input type="number" name="publish_weekday" value={form.publish_weekday} onChange={handleChange} min={0} max={6} />
            </div>

            <div className="field">
              <label>Longitud del titulo</label>
              <input type="number" name="title_length" value={form.title_length} onChange={handleChange} min={1} max={200} />
            </div>

            <div className="field">
              <label>Longitud de descripcion</label>
              <input type="number" name="description_length" value={form.description_length} onChange={handleChange} min={0} max={10000} />
            </div>

            <div className="field">
              <label>HD (0=No, 1=Si)</label>
              <select name="is_hd" value={form.is_hd} onChange={handleChange}>
                <option value={0}>No</option>
                <option value={1}>Si</option>
              </select>
            </div>

            <div className="field">
              <label>Suscriptores del creador</label>
              <input type="number" name="creator_subscribers" value={form.creator_subscribers} onChange={handleChange} min={0} />
            </div>

            <div className="field">
              <label>Vistas promedio (30d)</label>
              <input type="number" name="creator_avg_views_30d" value={form.creator_avg_views_30d} onChange={handleChange} min={0} />
            </div>
          </div>

          <button className="btn" type="submit" disabled={loading}>
            {loading ? 'Analizando...' : 'Analizar rendimiento'}
          </button>
        </form>

        <div className="result-area">
          {loading && (
            <div className="state state-loading">
              <div className="spinner"></div>
              <p>Procesando solicitud...</p>
            </div>
          )}

          {error && (
            <div className="state state-error">
              <strong>Error:</strong> {error}
            </div>
          )}

          {result && !loading && (
            <div className="result-card">
              <div className="result-header">
                <span className={getBadgeClass(result.rendimiento_esperado)}>
                  {result.rendimiento_esperado}
                </span>
              </div>

              <div className="probabilities">
                <h3>Probabilidades</h3>
                {Object.entries(result.probabilidades).map(([cls, prob]) => (
                  <div key={cls} className="prob-bar-row">
                    <span className="prob-label">{cls}</span>
                    <div className="prob-bar-bg">
                      <div
                        className="prob-bar-fill"
                        style={{ width: `${(prob * 100).toFixed(1)}%` }}
                      ></div>
                    </div>
                    <span className="prob-value">{(prob * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>

              <div className="recomendacion">
                <h3>Recomendacion</h3>
                <p>{result.recomendacion}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App