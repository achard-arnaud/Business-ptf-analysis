#!/usr/bin/env python3
from __future__ import annotations
import argparse, asyncio, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd):
    print('+', ' '.join(map(str, cmd)))
    subprocess.run(list(map(str, cmd)), check=True)


def main():
    ap = argparse.ArgumentParser(prog='two-pager-nice')
    sub = ap.add_subparsers(dest='command', required=True)
    b = sub.add_parser('build')
    b.add_argument('config')
    b.add_argument('--output', default=str(ROOT / 'dist'))
    b.add_argument('--name')
    q = sub.add_parser('qa')
    q.add_argument('html')
    q.add_argument('--report', required=True)
    q.add_argument('--screenshots')
    a = sub.add_parser('all')
    a.add_argument('config')
    a.add_argument('--output', default=str(ROOT / 'dist'))
    a.add_argument('--name')
    args = ap.parse_args()

    if args.command == 'build':
        cmd = [sys.executable, ROOT/'scripts/render.py', args.config, '--output', args.output]
        if args.name: cmd += ['--name', args.name]
        run(cmd)
    elif args.command == 'qa':
        cmd = [sys.executable, ROOT/'scripts/qa.py', args.html, '--report', args.report]
        if args.screenshots: cmd += ['--screenshots', args.screenshots]
        run(cmd)
    else:
        out = Path(args.output)
        stem = args.name or Path(args.config).stem
        run([sys.executable, ROOT/'scripts/render.py', args.config, '--output', out, '--name', stem])
        run([sys.executable, ROOT/'scripts/qa.py', out/f'{stem}.html', '--report', out/f'{stem}_qa.json', '--screenshots', out/'qa'])

if __name__ == '__main__':
    main()
