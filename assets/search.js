// Come sono bravo? サイト内検索
// 検索用データ /search-index.json は tools/normalize_site.py が作る
(function () {
  var input = document.getElementById('site-search');
  var box = document.getElementById('search-results');
  if (!input || !box) return;
  var data = null, loading = null, timer = null;

  function norm(s) {
    return s.normalize('NFKC').replace(/[’‘`´]/g, "'").toLowerCase();
  }
  function esc(s) {
    return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }
  function load() {
    if (data) return Promise.resolve(data);
    if (!loading) {
      box.innerHTML = '<p class="small">検索データを読み込んでいます…</p>';
      loading = fetch('/search-index.json').then(function (r) { return r.json(); }).then(function (d) {
        d.forEach(function (p) { p.nt = norm(p.t); p.nx = norm(p.x); p.ng = norm(p.g); });
        data = d; return d;
      });
    }
    return loading;
  }
  function snippet(p, terms) {
    var i = p.nx.indexOf(terms[0]);
    if (i < 0) return esc(p.x.slice(0, 90)) + (p.x.length > 90 ? '…' : '');
    var s = Math.max(0, i - 40), e = Math.min(p.x.length, i + terms[0].length + 60);
    var raw = p.x.slice(s, e), low = p.nx.slice(s, e), out = '', k = 0;
    // 当たった語を強調（検索語は長い順に）
    var sorted = terms.slice().sort(function (a, b) { return b.length - a.length; });
    while (k < raw.length) {
      var hit = null;
      for (var j = 0; j < sorted.length; j++) if (sorted[j] && low.substr(k, sorted[j].length) === sorted[j]) { hit = sorted[j]; break; }
      if (hit) { out += '<mark>' + esc(raw.substr(k, hit.length)) + '</mark>'; k += hit.length; }
      else { out += esc(raw[k]); k++; }
    }
    return (s > 0 ? '…' : '') + out + (e < p.x.length ? '…' : '');
  }
  function run() {
    var q = norm(input.value).trim();
    if (!q) { box.innerHTML = ''; return; }
    var terms = q.split(/\s+/);
    load().then(function (d) {
      var hits = [];
      d.forEach(function (p) {
        var score = 0;
        for (var i = 0; i < terms.length; i++) {
          var t = terms[i], inT = p.nt.indexOf(t) >= 0, inG = p.ng.indexOf(t) >= 0, inX = p.nx.indexOf(t) >= 0;
          if (!inT && !inG && !inX) return;
          score += (inT ? 10 : 0) + (inG ? 3 : 0) + (inX ? 1 : 0);
        }
        hits.push([score, p]);
      });
      hits.sort(function (a, b) { return b[0] - a[0]; });
      var max = 50, html = '<p class="small">' + hits.length + '件' + (hits.length > max ? '（上位' + max + '件を表示）' : '') + '</p>';
      hits.slice(0, max).forEach(function (h) {
        var p = h[1];
        html += '<article class="search-hit"><a href="' + esc(p.u) + '">' + esc(p.t) + '</a>' +
          '<span class="tag plain">' + esc(p.g) + '</span><p>' + snippet(p, terms) + '</p></article>';
      });
      if (!hits.length) html = '<p class="small">見つかりませんでした。言葉を短くするか、別の書き方で試してください。</p>';
      box.innerHTML = html;
    }).catch(function () {
      box.innerHTML = '<p class="small">検索データを読み込めませんでした。</p>';
    });
  }
  input.addEventListener('focus', load, { once: true });
  input.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(run, 200); });
  input.form && input.form.addEventListener('submit', function (e) { e.preventDefault(); run(); });
  var q = new URLSearchParams(location.search).get('q');
  if (q) { input.value = q; run(); }
})();
