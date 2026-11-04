#!/usr/bin/env python3
"""THREE_PAGER_PORTFOLIO_AI v0.3 — profil `exec` (C-level). Renderer générique piloté par payload.

Usage : python render_exec.py <payload.json> <out_dir> [--pdf]
- Le renderer n'écrit AUCUN contenu : il met en page le payload, résout les chiffres canoniques
  ({clé} → figures[clé].value), applique **gras**, puis exécute les contrôles de cohérence.
- Tout échec de contrôle arrête le rendu (exit 3). Les écarts de mise en page sont détectés par qa.py.
"""
import argparse, html, json, re, sys, hashlib, subprocess
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

HERE = Path(__file__).resolve().parent
SCHEMA = HERE.parents[1] / 'contracts' / 'three-pager-exec.schema.json'
PORTER_SUPPORT = ['Approvisionnement', 'Développement technologique', 'Infrastructure', 'Ressources humaines']
PORTER_PRIMARY = ['Logistique amont', 'Production', 'Logistique aval', 'Marketing et ventes', 'Services']
ROWS_Q = ['Core', 'Enabler', 'Support']
COLS_Q = ['Commodity', 'Parity', 'Differentiating']
FORBIDDEN = [r'GO_DRAFT', r'HITL', r'render_authorized', r'\b(A|EN|DRV|UC)-\w', r'\bD0\d', r'business case',
             r'aucun cas', r'non établi', r'class="tag', r'pas un business', r'panel ≠', r'hypothèse de travail']
STRAT_LABEL = {'cost': 'coûts', 'cash': 'cash', 'differentiation': 'différenciation', 'resilience': 'résilience'}
DEFAULT_LAYOUT = {
    'p1_rows': '76mm 1fr', 'p1_top_cols': '1.12fr .92fr 1fr', 'p1_bot_cols': '.86fr .92fr 1.42fr',
    'p2_rows': '1fr 36mm', 'p2_bot_cols': '1.25fr 1fr',
    'p3_rows': '1fr 40mm', 'p3_top_cols': '108mm 1fr', 'p3_bot_cols': '1.15fr 1fr 1fr',
    'p3_table_cols': ['40mm', None, '27mm', '29mm', '29mm'],
}


class CoherenceError(Exception):
    pass


def check(cond, code, msg):
    if not cond:
        raise CoherenceError(f'{code}: {msg}')


class R:
    def __init__(self, p):
        self.p = p
        self.fig = {k: v['value'] for k, v in p.get('figures', {}).items()}
        self.L = {**DEFAULT_LAYOUT, **p.get('layout', {})}

    def check_layout(self):
        for key, value in self.p.get('layout', {}).items():
            check(key in DEFAULT_LAYOUT, 'G-P0', f'layout inconnu : {key}')
            values = value if key == 'p3_table_cols' and isinstance(value, list) else [value]
            check(len(values) == 5 if key == 'p3_table_cols' else isinstance(value, str),
                  'G-P0', f'layout invalide : {key}')
            check(all(v is None or (isinstance(v, str) and
                  re.fullmatch(r'[0-9a-zA-Z.,()\s%+-]+', v) and len(v) <= 120)
                  for v in values), 'G-P0', f'valeur de grille invalide : {key}')

    # -- texte : échappement, chiffres canoniques, gras
    def t(self, s):
        if s is None:
            return ''
        def sub(m):
            k = m.group(1)
            check(k in self.fig, 'G-C5', f'chiffre non canonique {{{k}}}')
            return self.fig[k]
        s = re.sub(r'\{([a-z0-9_]+)\}', sub, s)
        s = html.escape(s, quote=False)
        return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)

    def stars(self, n):
        return '<span class="stars">' + '★' * n + f'<i>{"★" * (3 - n)}</i></span>'

    def card(self, title, body, take, cls=''):
        check(take and take.strip(), 'G-P1', f'carte sans « À retenir » : {title}')
        return (f'<div class="card {cls}" data-card data-no-overflow data-layout-box data-take="1"><h2>{self.t(title)}</h2>'
                f'<div class="body" data-no-overflow>{body}</div><p class="take"><b class="lbl">À retenir</b>{self.t(take)}</p></div>')

    def header(self, n, sub):
        return (f'<header class="header"><div class="kicker">{self.t(self.p["program"])}</div><div class="h1row">'
                f'<h1 class="title">{self.t(self.p["entity"])}</h1><div class="subtitle">{self.t(sub)}</div></div>'
                f'<div class="pageno">{n} / 3</div></header>')

    def footer(self, n, f, sources):
        return (f'<div class="footer-strip"><div class="footer-title">{self.t(f["label"])}</div><div class="footer-body">{self.t(f["body"])}</div></div>'
                f'<div class="source-line" data-no-overflow>{self.t(sources)}</div><div class="page-number">{n}/3</div>')

    # ------------------------------------------------------------------ PAGE 1
    def page1(self):
        p, P1, L = self.p, self.p['page1'], self.L
        sig = ''.join(f'<div class="kv"><span>{self.t(k)}</span><span>{self.t(v)}</span></div>' for k, v in P1['signaletique']['rows'])
        th = ''.join(f'<p class="lead">{self.t(x)}</p>' for x in P1['thesis']['paras'])
        drv = ''.join(f'<div class="drv"><span class="n">{i}</span><span><b>{self.t(d["label"])}</b> — {self.t(d["text"])}</span></div>'
                      for i, d in enumerate(p['drivers'], 1))
        B = P1['breakdown']
        mx = max(v for _, v in B['series'])
        bars = ''.join(f'<div class="bar-row"><div>{self.t(n)}</div><div class="bar-track"><div class="bar" style="width:{v / mx * 100:.1f}%"></div></div>'
                       f'<div class="bar-val">{v} %</div></div>' for n, v in B['series'])
        stk = ''.join(f'<div class="stk s{i}" style="width:{v}%">{self.t(n)}</div>' for i, (n, v) in enumerate(B['stack'], 1))
        brk = (f'<div class="ct">{self.t(B["series_title"])}</div>{bars}<div class="ct mt">{self.t(B["stack_title"])}</div>'
               f'<div class="stack">{stk}</div><div class="ct mt">{self.t(B["footnote"])}</div>')
        BO = P1['board']
        rows = ''
        for r in BO['rows']:
            role = f' : <span class="role">{self.t(r["role"])}</span>' if r.get('role') else ''
            rows += f'<div class="pp{" gap" if r.get("gap") else ""}"><b>{self.t(r["who"])}</b> — {self.t(r["what"])}{role}</div>'
        board = f'<p class="intro">{self.t(BO["intro"])}</p>{rows}'
        S = P1['swot']
        q = lambda h, xs: f'<div class="sw"><h3>{h}</h3><ul>{"".join(f"<li>{self.t(x)}</li>" for x in xs)}</ul></div>'
        cur = p['posture']['current']
        pos = ''.join(f'<div class="pos{" on" if code == cur else ""}"><b>{lab}</b>{code}{" · actuelle" if code == cur else ""}</div>'
                      for lab, code in [('Offensive', 'S-O'), ('Défensive', 'S-T'), ('Veille', 'W-T'), ('Opportuniste', 'W-O')])
        swot = f'<div class="swot">{q("Forces", S["s"])}{q("Faiblesses", S["w"])}{q("Opportunités", S["o"])}{q("Menaces", S["t"])}</div><div class="tows">{pos}</div>'
        return (f'<section class="page">{self.header(1, P1["subtitle"])}<main class="main" style="grid-template-rows:{L["p1_rows"]}">'
                f'<div class="grid" style="grid-template-columns:{L["p1_top_cols"]}" data-overlap-check>'
                f'{self.card("Signalétique", sig, P1["signaletique"]["take"])}{self.card("Thèse", th, P1["thesis"]["take"], "dark")}'
                f'{self.card("Drivers de valeur", drv, P1["drivers_take"])}</div>'
                f'<div class="grid" style="grid-template-columns:{L["p1_bot_cols"]}" data-overlap-check>'
                f'{self.card(B["title"], brk, B["take"])}{self.card("Board’s empowerment & ownership", board, BO["take"])}'
                f'{self.card("SWOT → posture TOWS", swot, S["take"])}</div></main>'
                f'{self.footer(1, P1["footer"], P1["sources"])}</section>')

    # ------------------------------------------------------------------ PAGE 2
    def act(self, a):
        if a.get('themes'):
            ref = f'<span class="ref">→ cas {" et ".join(str(x) for x in a["themes"])}</span>'
        elif a.get('transformation'):
            ref = f'<span class="ref">→ transformation {self.t(a["transformation"])}</span>'
        else:
            ref = '<span class="ref none">hors priorités</span>'
        return (f'<div class="act" data-card data-no-overflow data-layout-box><div class="act-h"><b>{self.t(a["name"])}</b>{self.stars(a["stars"])}</div>'
                f'<p>{self.t(a["desc"])}</p><p class="ben"><b>Bénéfice :</b> {self.t(a["benefit"])}<br>{ref}</p></div>')

    def page2(self):
        P2, L = self.p['page2'], self.L
        lecture_html = '<p class="lead" style="font-size:10pt">' + self.t(P2['lecture']['text']) + '</p>'
        mets = ''.join(f'<div class="metric"><div class="metric-value">{self.t(v)}</div><div class="metric-meta">{self.t(m)}</div></div>'
                       for v, m in P2['metrics']['items'])
        metrics_html = '<div class="metrics3">' + mets + '</div>'
        return (f'<section class="page">{self.header(2, P2["subtitle"])}<main class="main" style="grid-template-rows:{L["p2_rows"]}">'
                f'<div class="porterwrap"><div class="porter">'
                f'<div><div class="band-title">Activités de soutien</div><div class="support" data-overlap-check>{"".join(self.act(a) for a in P2["support"])}</div></div>'
                f'<div style="display:flex;flex-direction:column;min-height:0"><div class="band-title">Activités principales</div>'
                f'<div class="primary" style="flex:1" data-overlap-check>{"".join(self.act(a) for a in P2["primary"])}</div></div></div>'
                f'<div class="marge"><span>MARGE</span><small>{self.t(P2["margin_sub"])}</small></div></div>'
                f'<div class="grid" style="grid-template-columns:{L["p2_bot_cols"]}" data-overlap-check>'
                f'{self.card("Ordres de grandeur", metrics_html, P2["metrics"]["take"], "soft")}'
                f'{self.card("Lecture", lecture_html, P2["lecture"]["take"])}'
                f'</div></main>{self.footer(2, P2["footer"], P2["sources"])}</section>')

    # ------------------------------------------------------------------ PAGE 3
    def page3(self):
        p, P3, L = self.p, self.p['page3'], self.L
        Q = P3['quadrant']
        quad = '<div class="quad"><div></div>' + ''.join(f'<div class="qh">{c}</div>' for c in COLS_Q)
        for r in ROWS_Q:
            quad += f'<div class="qr">{r}</div>'
            for c in COLS_Q:
                chips = ''
                for x in Q['cells']:
                    if x['row'] == r and x['col'] == c:
                        nb = '<span class="nb">%s</span>' % x['theme'] if x.get('theme') else ''
                        chips += '<div class="chip">' + nb + self.t(x['label']) + '</div>'
                cls = 'hot' if (r, c) == ('Core', 'Differentiating') else ('fill' if chips else '')
                quad += f'<div class="qc {cls}">{chips}</div>'
        quad += '</div>'
        cols = ''.join(f'<col style="width:{w}">' if w else '<col>' for w in L['p3_table_cols'])
        trs = ''.join(f'<tr><td><span class="nb">{th["n"]}</span><b>{self.t(th["name"])}</b> {self.stars(th["stars"])}'
                      f'<span class="meta">{self.t(th["activity"])} → {self.t(th["strategy"])} · {self.t(th["horizon"])}</span></td>'
                      f'<td>{self.t(th["change"])}</td><td>{self.t(th["benefit"])}</td><td>{self.t(th["advantage"])}</td><td>{self.t(th["feature"])}</td></tr>'
                      for th in p['themes'])
        table = (f'<table class="table"><colgroup>{cols}</colgroup><tr><th>Priorité</th><th>Changement</th><th>Bénéfice</th>'
                 f'<th>Avantage compétitif</th><th>Caractéristique</th></tr>{trs}</table>')
        T = p['transformation']
        tr = (f'<p class="lead" style="font-size:10pt"><b>MT, 12–24 mois</b> : {self.t(T["mt"])}</p>'
              f'<p class="lead" style="font-size:10pt"><b>LT, 24–48 mois</b> : {self.t(T["lt"])}</p>')
        D = P3['ai_diag']
        gauge = ''.join(('<span class="on">' if lvl == D['level'] else '<span>') + lvl + '</span>' for lvl in ['Inconnue', 'Faible', 'Partiel', 'Établi'])
        diag = f'<div class="gauge">{gauge}</div><ul class="ul">{"".join(f"<li>{self.t(x)}</li>" for x in D["facts"])}</ul>'
        # stratégie dominante : dérivée du tableau des thèmes (pas saisie à la main)
        fam = {}
        for th in p['themes']:
            fam.setdefault(th['strategy_family'], []).append(th['n'])
        mx = max(len(v) for v in fam.values())
        dom = ''
        for i, (lab, key) in enumerate(P3['dominant']['rows']):
            ns = fam.get(key, [])
            check(ns, 'G-C6', f'famille de stratégie sans thème : {key}')
            txt = ('priorités ' if len(ns) > 1 else 'priorité ') + ' et '.join(str(n) for n in ns)
            w = 100 if len(ns) == mx else 55
            dom += f'<div class="strat"><span>{self.t(lab)}</span><span class="sb {["", "l", "s"][min(i, 2)]}" style="width:{w}%">{txt}</span></div>'
        return (f'<section class="page">{self.header(3, P3["subtitle"])}<main class="main" style="grid-template-rows:{L["p3_rows"]}">'
                f'<div class="grid" style="grid-template-columns:{L["p3_top_cols"]}" data-overlap-check>'
                f'{self.card("Magic Quadrant", quad, Q["take"])}{self.card(P3["themes_title"], table, P3["themes_take"])}</div>'
                f'<div class="grid" style="grid-template-columns:{L["p3_bot_cols"]}" data-overlap-check>'
                f'{self.card("Transformation MT / LT", tr, T["take"], "dark")}{self.card("Diagnostic public · IA, data, ML", diag, D["take"])}'
                f'{self.card("Stratégie dominante", dom, P3["dominant"]["take"])}</div></main>'
                f'{self.footer(3, P3["footer"], P3["sources"])}</section>')

    # ------------------------------------------------------------------ contrôles de cohérence
    def coherence(self, doc):
        p = self.p
        th_ids = {t['n'] for t in p['themes']}
        check(3 <= len(th_ids) <= 5, 'G-S9', f'{len(th_ids)} thèmes (3 à 5 attendus)')
        check(th_ids == set(range(1, len(th_ids) + 1)), 'G-S9', 'numéros des thèmes non consécutifs')
        acts = p['page2']['support'] + p['page2']['primary']
        check(len(p['page2']['support']) == 4 and len(p['page2']['primary']) == 5, 'G-S6', 'chaîne de Porter 4 + 5 attendue')
        check([a['name'] for a in p['page2']['support']] == PORTER_SUPPORT and
              [a['name'] for a in p['page2']['primary']] == PORTER_PRIMARY,
              'G-S6', 'noms ou ordre Porter non canoniques')
        refs = {n for a in acts for n in a.get('themes', [])}
        check(refs == th_ids, 'G-C1', f'renvois p.2 {sorted(refs)} ≠ thèmes p.3 {sorted(th_ids)}')
        check(all(n in th_ids for c in p['page3']['quadrant']['cells'] for n in [c.get('theme')] if n is not None),
              'G-C3', 'renvoi vers un thème inexistant')
        for a in acts:
            if a['stars'] == 3:
                check(a.get('themes') or a.get('transformation'), 'G-C1', f'maillon ★★★ sans renvoi : {a["name"]}')
        top = sum(1 for a in acts if a['stars'] == 3)
        check(p['page2'].get('top_count', top) == top, 'G-C7', f"sous-titre p.2 annonce {p['page2'].get('top_count')} maillons ★★★, la chaîne en compte {top}")
        drivers = {d['id'] for d in p['drivers']}
        check(len(drivers) == 5, 'G-C2', 'IDs de drivers dupliqués')
        covered = {d for t in p['themes'] for d in t['drivers']} | set(p['transformation']['covers'])
        check(covered == drivers, 'G-C2', f'drivers non couverts : {drivers - covered}')
        qthemes = {c['theme'] for c in p['page3']['quadrant']['cells'] if c.get('theme')}
        check(qthemes == th_ids, 'G-C3', f'thèmes du quadrant {sorted(qthemes)} ≠ {sorted(th_ids)}')
        rows_used = {c['row'] for c in p['page3']['quadrant']['cells']}
        qtake = p['page3']['quadrant']['take'].lower()
        check(len(rows_used) >= 2 or 'information publique' in qtake, 'G-C3', 'quadrant dégénéré sans phrase de limite')
        pc, lab = p['posture']['current'], p['posture']['label']
        needle = f'{lab} ({pc})'.lower()
        check(needle in p['page1']['swot']['take'].lower(), 'G-C4', 'posture absente du « À retenir » SWOT')
        check(needle in p['page3']['footer']['body'].lower(), 'G-C4', 'posture absente de la conclusion')
        body = re.sub(r'<style>.*?</style>', '', doc, flags=re.S)
        for pat in FORBIDDEN:
            check(not re.search(pat, body), 'G-P2..P5', f'expression interdite en exec : {pat}')
        check(body.count('data-take="1"') == body.count('class="take"'), 'G-P1', 'carte sans « À retenir »')
        return ['G-S6', 'G-S9', 'G-C1', 'G-C2', 'G-C3', 'G-C4', 'G-C5', 'G-C6', 'G-C7', 'G-P1', 'G-P2..P5']

    def build(self):
        validate_payload(self.p)
        self.check_layout()
        css = (HERE / 'exec_theme.css').read_text()
        doc = (f'<!doctype html><html lang="{self.p.get("language", "fr")}"><head><meta charset="utf-8"><title>{self.t(self.p["program"])} — {self.t(self.p["entity"])}</title>'
               f'<style>{css}</style></head><body>{self.page1()}{self.page2()}{self.page3()}</body></html>')
        return doc, self.coherence(doc)


def validate_payload(payload):
    schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(payload),
                    key=lambda error: tuple(str(x) for x in error.path))
    if errors:
        raise CoherenceError('SCHEMA: ' + '; '.join(f'{"/".join(map(str, e.path))}: {e.message}' for e in errors[:20]))


def main():
    parser = argparse.ArgumentParser(description='Compose an executive preview; validation requires bundle and archive.')
    parser.add_argument('payload', type=Path)
    parser.add_argument('out', type=Path)
    parser.add_argument('--pdf', action='store_true')
    parser.add_argument('--bundle', type=Path)
    parser.add_argument('--archive', type=Path)
    args = parser.parse_args()
    if bool(args.bundle) != bool(args.archive):
        parser.error('--bundle and --archive must be used together')
    payload_path, out = args.payload, args.out
    raw = payload_path.read_bytes()
    p = json.loads(raw)
    try:
        doc, checks = R(p).build()
    except CoherenceError as e:
        print(f'COHERENCE FAIL — {e}')
        sys.exit(3)
    evidence = {'status': 'UNVERIFIED_DEMO'}
    if args.bundle:
        sys.path.insert(0, str(HERE.parents[1] / 'scripts'))
        from validate_exec import validate_exec_payload
        evidence = validate_exec_payload(p, args.bundle, args.archive)
    out.mkdir(parents=True, exist_ok=True)
    stem = f'{p["entity"]}_{p["program"].split("—")[0].strip()}_Portfolio_AI_Diagnostic_{p["template_version"]}'.replace(' ', '_')
    (out / f'{stem}.html').write_text(doc, encoding='utf-8')
    manifest = {
        'template': p['template'], 'template_version': p['template_version'], 'render_profile': 'exec',
        'entity': p['entity'], 'cutoff': p['cutoff'], 'payload_sha256': hashlib.sha256(raw).hexdigest(),
        'lineage': p.get('lineage', {}), 'evidence_status': evidence['status'],
        'bundle_sha256': evidence.get('bundle_sha256'),
        'visual_qa': 'NOT_RUN' if not args.pdf else 'PENDING',
        'coherence_checks_passed': checks}
    manifest_path = out / 'render_manifest.json'
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'html': str(out / f'{stem}.html'), 'coherence': 'PASS', 'checks': checks}, ensure_ascii=False))
    if args.pdf:
        subprocess.run([sys.executable, str(HERE / 'render2.py'), str(out / f'{stem}.html'), str(out), stem], check=True)
        r = subprocess.run([sys.executable, str(HERE / 'qa.py'), str(out / f'{stem}.html'), '--report', str(out / 'qa.json'), '--screenshots', str(out / 'qa')])
        manifest['visual_qa'] = 'LAYOUT_PASS_MANUAL_PENDING' if r.returncode == 0 else 'FAIL'
        manifest['pdf_sha256'] = hashlib.sha256((out / f'{stem}.pdf').read_bytes()).hexdigest()
        manifest['qa_sha256'] = hashlib.sha256((out / 'qa.json').read_bytes()).hexdigest()
        manifest['png_sha256'] = [
            hashlib.sha256((out / f'{stem}_page{index}.png').read_bytes()).hexdigest()
            for index in range(1, 4)]
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        sys.exit(r.returncode)


if __name__ == '__main__':
    main()
