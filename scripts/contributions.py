"""Generate a repository-hosted contribution heatmap using GitHub's API."""
import json
import os
from datetime import date
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen


def render(calendar):
    weeks = calendar['weeks']
    if not weeks or not any(w['contributionDays'] for w in weeks):
        raise ValueError('Empty calendar; keeping the previous image')
    colors = ['#1d2b3e', '#20534e', '#287d69', '#43b68f', '#7af0ca']
    levels = dict(zip(['NONE', 'FIRST_QUARTILE', 'SECOND_QUARTILE',
                       'THIRD_QUARTILE', 'FOURTH_QUARTILE'], colors))
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="330" viewBox="0 0 1200 330" role="img" aria-labelledby="title">',
             '<title id="title">Sooraj’s GitHub contribution calendar</title>',
             '<rect width="1200" height="330" rx="24" fill="#101e32"/>',
             '<g font-family="Arial, Helvetica, sans-serif">',
             '<text x="36" y="48" font-size="24" font-weight="bold" fill="#7af0ca">Coffee in. Commits out.</text>',
             f'<text x="36" y="76" font-size="15" fill="#b9c8dc">{int(calendar["totalContributions"]):,} contributions over the past year</text>']
    step = min(20, 1080 / len(weeks))
    last_month = None
    for column, week in enumerate(weeks):
        for day in week['contributionDays']:
            d = date.fromisoformat(day['date'])
            count = int(day['contributionCount'])
            x = 72 + column * step
            y = 120 + int(day['weekday']) * 20
            if d.month != last_month and (last_month is None or d.day <= 7):
                parts.append(f'<text x="{x:.1f}" y="108" font-size="12" fill="#b9c8dc">{d:%b}</text>')
                last_month = d.month
            color = levels[day['contributionLevel']]
            parts.append(f'<rect x="{x:.1f}" y="{y}" width="{step-4:.1f}" height="16" rx="3" fill="{color}"><title>{count} contributions on {escape(day["date"])}</title></rect>')
    for label, row in [('Mon', 1), ('Wed', 3), ('Fri', 5)]:
        parts.append(f'<text x="34" y="{132+row*20}" font-size="12" fill="#b9c8dc">{label}</text>')
    parts.append('<text x="36" y="298" font-size="12" fill="#b9c8dc">A little progress, one day at a time.</text>')
    parts.append('<text x="944" y="298" font-size="12" fill="#b9c8dc">Less</text>')
    for i, color in enumerate(colors):
        parts.append(f'<rect x="{980+i*22}" y="285" width="16" height="16" rx="3" fill="{color}"/>')
    parts.append('<text x="1094" y="298" font-size="12" fill="#b9c8dc">More</text></g></svg>')
    return '\n'.join(parts)


def main():
    query = '''query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks { contributionDays { date weekday contributionCount contributionLevel } }
          }
        }
      }
    }'''
    body = json.dumps({'query': query, 'variables': {'login': 'Sooraj-wq'}}).encode()
    request = Request('https://api.github.com/graphql', data=body, headers={
        'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
        'Content-Type': 'application/json', 'User-Agent': 'sooraj-profile-calendar'})
    with urlopen(request, timeout=45) as response:
        result = json.load(response)
    if result.get('errors'):
        raise RuntimeError('GitHub could not return the calendar; keeping the previous image')
    calendar = result['data']['user']['contributionsCollection']['contributionCalendar']
    svg = render(calendar)
    destination = Path('assets/contributions.svg')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.with_suffix('.tmp').write_text(svg, encoding='utf-8')
    destination.with_suffix('.tmp').replace(destination)


if __name__ == '__main__':
    main()
