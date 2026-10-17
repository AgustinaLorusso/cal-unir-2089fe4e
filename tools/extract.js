// Se ejecuta en la página del calendario de UNIR (https://campusvirtual.unir.net/p/calendar?mode=month)
// PASO 1: pegar esto y después avanzar/retroceder un mes en el calendario para que la página haga una petición.
window.__cal = window.__cal || {};
(function () {
  const oo = XMLHttpRequest.prototype.open, os = XMLHttpRequest.prototype.send, osh = XMLHttpRequest.prototype.setRequestHeader;
  XMLHttpRequest.prototype.open = function (m, u) { this.__u = u; this.__h = {}; return oo.apply(this, arguments); };
  XMLHttpRequest.prototype.setRequestHeader = function (k, v) { this.__h[k] = v; return osh.apply(this, arguments); };
  XMLHttpRequest.prototype.send = function (b) {
    if (String(this.__u).includes('calendarView')) { window.__cal.url = this.__u; window.__cal.hdrs = this.__h; }
    return os.apply(this, arguments);
  };
})();
'listo: ahora cambiá de mes';

// PASO 2 (después de cambiar de mes): descarga todo el rango y arma las filas.
// const h = Object.assign({}, window.__cal.hdrs); delete h['X-Correlation-Id']; delete h['X-Request-Id'];
// const r = await fetch(window.__cal.url, {method:'POST', headers:h, body: JSON.stringify({startDateTime:'2026-09-01T00:00:00.000Z', endDateTime:'2027-08-31T23:59:59.999Z'})});
// const d = (await r.json()).data;
// window.__s = d.map(e=>[e.id, e.titulo, e.asignatura||'', e.type, e.fechaInicio, e.fechaFin, e.isInstantEvent?1:0].join('|')).join('\n');
// window.__s.length
//
// PASO 3: leer window.__s en trozos de 900 caracteres: window.__s.slice(0,900), window.__s.slice(900,1800), ...
