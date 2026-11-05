"""DOM layout checks. These checks complement manual review of the three PNGs."""
import argparse
import asyncio
import json
from pathlib import Path

from browser import launch

JS = r'''() => {
  const visible = e => { const r=e.getBoundingClientRect(), s=getComputedStyle(e);
    return s.display!=='none' && s.visibility!=='hidden' && r.width>0 && r.height>0; };
  const pages = [...document.querySelectorAll('.page')];
  const report = {page_count: pages.length, pages: []};
  for (const page of pages) {
    const pr=page.getBoundingClientRect();
    const found={overlaps:[], overflows:[], out_of_bounds:[], small_fonts:[], low_padding:[]};
    for (const c of page.querySelectorAll('[data-overlap-check]')) {
      const children=[...c.children].filter(e => e.hasAttribute('data-layout-box') && visible(e));
      for (let i=0;i<children.length;i++) for (let j=i+1;j<children.length;j++) {
        const a=children[i].getBoundingClientRect(), b=children[j].getBoundingClientRect();
        if (Math.min(a.right,b.right)-Math.max(a.left,b.left)>1 &&
            Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>1) found.overlaps.push([i,j]);
      }
    }
    for (const e of page.querySelectorAll('[data-no-overflow]')) {
      if (visible(e) && (e.scrollHeight>e.clientHeight+1 || e.scrollWidth>e.clientWidth+1))
        found.overflows.push({tag:e.tagName, cls:e.className, card:e.closest('.card')?.querySelector('h2')?.textContent?.trim(), client_height:e.clientHeight, scroll_height:e.scrollHeight, client_width:e.clientWidth, scroll_width:e.scrollWidth});
    }
    for (const e of page.querySelectorAll('*')) {
      if (!visible(e)) continue;
      const r=e.getBoundingClientRect();
      if (r.left<pr.left-1 || r.top<pr.top-1 || r.right>pr.right+1 || r.bottom>pr.bottom+1)
        found.out_of_bounds.push({tag:e.tagName, cls:e.className});
      if (e.childNodes.length===1 && e.firstChild.nodeType===Node.TEXT_NODE && e.textContent.trim() &&
          parseFloat(getComputedStyle(e).fontSize)<11.95)
        found.small_fonts.push({tag:e.tagName, text:e.textContent.trim().slice(0,80)});
    }
    for (const e of page.querySelectorAll('[data-card]')) {
      const s=getComputedStyle(e);
      if (Math.min(...[s.paddingTop,s.paddingRight,s.paddingBottom,s.paddingLeft].map(parseFloat))<11.95)
        found.low_padding.push({tag:e.tagName, cls:e.className});
    }
    report.pages.push(found);
  }
  return report;
}'''


async def check(html, screenshots=None):
    from playwright.async_api import async_playwright

    async with async_playwright() as playwright:
        browser = await launch(playwright)
        page = await browser.new_page(viewport={'width': 1404, 'height': 993})
        await page.set_content(html.read_text(encoding='utf-8'), wait_until='networkidle')
        result = await page.evaluate(JS)
        if screenshots:
            screenshots.mkdir(parents=True, exist_ok=True)
            for i in range(result['page_count']):
                await page.locator('.page').nth(i).screenshot(path=str(screenshots / f'qa_page{i+1}.png'))
        await browser.close()
    keys = ('overlaps', 'overflows', 'out_of_bounds', 'small_fonts', 'low_padding')
    result['summary'] = {key: sum(len(p[key]) for p in result['pages']) for key in keys}
    result['pass'] = result['page_count'] == 3 and all(result['summary'][key] == 0 for key in keys)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('html', type=Path)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--screenshots', type=Path)
    args = parser.parse_args()
    result = asyncio.run(check(args.html, args.screenshots))
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'page_count': result['page_count'], **result['summary'], 'pass': result['pass']}))
    if not result['pass']:
        raise SystemExit(2)

