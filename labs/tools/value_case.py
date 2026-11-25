# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Public-value calculator for the assistant: cost-benefit over the horizon and a distribution
table by user group and language. It reads the service files and an assumptions file; change
the assumptions in a copy and pass it with --assumptions.

  uv run labs/tools/value_case.py                         the grant service, supplied assumptions
  uv run labs/tools/value_case.py --assumptions my.csv    your copy
  uv run labs/tools/value_case.py --service carers        the capstone service
"""
import argparse
import csv
from collections import defaultdict
from pathlib import Path

LABS = Path(__file__).resolve().parents[1]


def load(path):
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def compute(service='grant', assumptions=None):
    if service == 'grant':
        enq, dec = LABS / 'files/d2/enquiries_monthly.csv', LABS / 'files/d2/decisions_monthly.csv'
        ass = assumptions or LABS / 'files/d2/assumptions.csv'
    else:
        enq, dec = LABS / 'files/capstone/carers_enquiries_monthly.csv', LABS / 'files/capstone/carers_decisions_monthly.csv'
        ass = assumptions or LABS / 'files/capstone/carers_assumptions.csv'
    A = {r['key']: float(r['value']) for r in load(ass)}
    dist = defaultdict(lambda: defaultdict(float))
    tot = defaultdict(float)
    for r in load(enq):
        c = float(r['contacts'])
        lang, ch, g = r['language'], r['channel'], r['group']
        defl = c * A['routine_share'] * A['deflect_' + ch] * A['quality_' + lang]
        mins = (float(r['avg_wait_min']) + A['handling_min']) if ch != 'online' else A['online_followup_min']
        cit_h = defl * mins / 60
        d = dist[(g, lang)]
        d['contacts'] += c
        d['deflected'] += defl
        d['citizen_hours'] += cit_h
        tot['contacts'] += c
        tot['deflected'] += defl
        tot['citizen_hours'] += cit_h
        tot['staff_hours'] += defl * A['handling_min'] / 60
        tot['wrong_answers'] += defl * A['wrong_answer_rate_' + lang]
    inc = sum(float(r['incomplete_on_arrival']) for r in load(dec))
    apps = sum(float(r['applications']) for r in load(dec))
    avoided = inc * A['incomplete_reduction']
    year = {
        'citizen_time_value': tot['citizen_hours'] * A['citizen_value_per_hour'],
        'staff_time_value': tot['staff_hours'] * A['staff_cost_per_hour'],
        'rework_avoided_value': avoided * A['rework_hours_per_incomplete'] * A['staff_cost_per_hour'],
        'wrong_answer_cost': -tot['wrong_answers'] * A['cost_per_wrong_answer'],
    }
    cash = (year['staff_time_value'] + year['rework_avoided_value']) * A['cash_release_share']
    run = A['run_cost_per_year'] + A['review_staff_fte'] * A['staff_cost_per_fte_year']
    n, r = int(A['years']), A['discount_rate']
    pvf = sum(1 / (1 + r) ** t for t in range(1, n + 1))
    benefits = sum(year.values())
    out = {
        'contacts_per_year': tot['contacts'], 'applications_per_year': apps,
        'deflected_contacts': tot['deflected'], 'citizen_hours_saved': tot['citizen_hours'],
        'staff_hours_freed': tot['staff_hours'], 'incomplete_avoided': avoided,
        'decision_days_saved_total': avoided * A['days_saved_per_incomplete'],
        **year, 'benefits_per_year': benefits, 'cash_per_year': cash, 'run_cost_per_year': run,
        'build_cost': A['build_cost'], 'pv_factor': pvf,
        'npv_public_value': benefits * pvf - run * pvf - A['build_cost'],
        'npv_fiscal': cash * pvf - run * pvf - A['build_cost'],
        'bcr': benefits * pvf / (A['build_cost'] + run * pvf),
    }
    table = []
    for (g, lang), d in sorted(dist.items()):
        table.append((g, lang, d['contacts'], d['deflected'], d['citizen_hours'],
                      1000 * d['citizen_hours'] / d['contacts']))
    return out, table


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--service', choices=['grant', 'carers'], default='grant')
    ap.add_argument('--assumptions', type=Path)
    a = ap.parse_args()
    out, table = compute(a.service, a.assumptions)
    print(f'public-value case · service {a.service} · {int(out["pv_factor"] * 1000) / 1000} present-value factor')
    for k in ('contacts_per_year', 'deflected_contacts', 'citizen_hours_saved', 'staff_hours_freed',
              'incomplete_avoided', 'decision_days_saved_total'):
        print(f'{k:28} {out[k]:>14,.0f}')
    print('per year, riyals')
    for k in ('citizen_time_value', 'staff_time_value', 'rework_avoided_value', 'wrong_answer_cost',
              'benefits_per_year', 'cash_per_year', 'run_cost_per_year'):
        print(f'{k:28} {out[k]:>14,.0f}')
    print(f'{"build_cost":28} {out["build_cost"]:>14,.0f}')
    print(f'{"npv_public_value":28} {out["npv_public_value"]:>14,.0f}')
    print(f'{"npv_fiscal":28} {out["npv_fiscal"]:>14,.0f}')
    print(f'{"benefit_cost_ratio":28} {out["bcr"]:>14.2f}')
    print('distribution: group, language, contacts, deflected, citizen hours saved, hours per 1,000 contacts')
    for g, lang, c, d, h, per in table:
        print(f'{g:16} {lang}  {c:>8,.0f} {d:>8,.0f} {h:>9,.0f} {per:>7.1f}')


if __name__ == '__main__':
    main()
