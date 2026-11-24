# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Computes every number the slides quote from the parallel example: the ministry's Accessible
Transport Card service. Its numbers differ from the lab service (Home Adaptation Grant) and the
capstone service (Carer's Allowance), so no slide gives away a lab or capstone answer.

  uv run labs/_tools/parallel_example.py
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('prepare_files', HERE / 'prepare_files.py')
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)

OPERATORS = 40


def band(p, cuts):
    for score, cut in cuts:
        if p >= cut:
            return score
    return 1


def day1():
    print('day 1 · instruments for 40 transport operators')
    rows = [('regulation', 40, 300_000, 100_000, 15), ('guidance', 12, 100_000, 20_000, 2),
            ('funding', 6, 600_000, 300_000, 5)]
    for k, reach, one, annual, months in rows:
        total = one + 5 * annual
        r = band(reach / OPERATORS, [(5, .8), (4, .5), (3, .25), (2, .10)])
        print(f'  {k:11} reach {reach}/{OPERATORS} -> {r}  five-year {total:,} -> {G.score_cost(total)}  months {months} -> {G.score_speed(months)}')
    print('day 1 · two app options')
    for k, build, annual, exit_ in (('P', 100_000, 500_000, 300_000), ('Q', 600_000, 200_000, 50_000)):
        print(f'  {k}: first year {build + annual:,}  five years with exit {build + 5 * annual + exit_:,}')


def day2():
    print('day 2 · value case of a card assistant')
    benefits = {'citizen_time': 260_000, 'staff_time_redeployed': 90_000, 'wrong_answers': -15_000}
    run, build, r, n = 260_000, 300_000, .04, 5
    pvf = sum(1 / (1 + r) ** t for t in range(1, n + 1))
    b = sum(benefits.values())
    print(f'  benefits per year {b:,}  run {run:,}  build {build:,}  pv factor {pvf:.3f}')
    print(f'  npv public value {b * pvf - run * pvf - build:,.0f}  bcr {b * pvf / (build + run * pvf):.2f}')
    print(f'  npv fiscal (no cash released) {-run * pvf - build:,.0f}')
    print('  hours saved per 1,000 contacts: online 48, phone 21 (12,000 online and 9,000 phone contacts)')
    print(f'    online {48 * 12}, phone {21 * 9} hours')
    print('day 2 · test of service X, 30 cases')
    ar, en, n_l = 13, 10, 15
    rate_ar, rate_en = round(100 * ar / n_l, 1), round(100 * en / n_l, 1)
    crit_stop = False
    crit = True
    if crit_stop or rate_ar < 70 or rate_en < 70:
        d = 'STOP'
    elif crit or rate_ar < 90 or rate_en < 90 or abs(rate_ar - rate_en) > 5:
        d = 'FIX'
    else:
        d = 'GO'
    print(f'  arabic {ar}/{n_l} = {rate_ar}%  english {en}/{n_l} = {rate_en}%  gap {rate_ar - rate_en:.1f}  overall {ar + en}/30 = {100 * (ar + en) / 30:.1f}%  decision {d}')


def day3():
    print('day 3 · risks of the card assistant')
    for name, l, i in (('wrong discount rule in English', 3, 2), ('card blocked by a wrong answer', 2, 3),
                       ('missed escalation for a stranded passenger', 2, 4)):
        lvl = l * i
        b = 'catastrophic' if lvl == 16 else 'high' if lvl >= 8 else 'medium' if lvl >= 3 else 'low'
        print(f'  {name:45} {l}x{i} = {lvl} {b}')


if __name__ == '__main__':
    day1()
    day2()
    day3()
