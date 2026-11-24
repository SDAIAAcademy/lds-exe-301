# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Recomputes every figure in the lab keys from the case files and checks it.

  uv run labs/solutions/check.py          all labs and the capstone figures
  uv run labs/solutions/check.py 2.1      one lab

Prints PASS for each lab or stops at the first difference. Run it after the generator
(labs/_tools/prepare_files.py) whenever a case file changes.
"""
import csv
import importlib.util
import sys
from collections import defaultdict
from pathlib import Path

LABS = Path(__file__).resolve().parents[1]
F = LABS / 'files'


def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


G = mod('prepare_files', LABS / '_tools' / 'prepare_files.py')
RT = mod('run_tests', LABS / 'testing' / 'run_tests.py')
VC = mod('value_case', LABS / 'tools' / 'value_case.py')


def load(p):
    with open(p, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def lab_1_1():
    roles = defaultdict(list)
    for a, _, role, conflict in G.MINISTRY_ACTIONS:
        roles[role].append(a)
    assert set(roles) == set(G.ROLES), roles
    conflicts = defaultdict(list)
    for a, _, role, c in G.MINISTRY_ACTIONS:
        if c:
            conflicts[c].append((a, role))
    assert len(conflicts) == 3
    for c, items in conflicts.items():
        assert len({r for _, r in items}) >= 2, items
        print(f'  {c}: ' + ', '.join(f'{a} {r}' for a, r in items))
    print('  roles: ' + '; '.join(f'{r} {",".join(v)}' for r, v in roles.items()))


def lab_1_2():
    draft = {r['instrument']: r for r in load(F / 'd1/team_draft_scores.csv')}
    errors = []
    for key, reach, cost, speed, total in G.instrument_scores():
        for crit, val in (('reach', reach), ('cost', cost), ('speed', speed)):
            if int(draft[key][crit]) != val:
                errors.append((key, crit, int(draft[key][crit]), val))
        print(f'  {key:15} reach {reach} cost {cost} speed {speed} sum {reach + cost + speed}  five-year cost {total:,}')
    assert len(errors) == 4, errors
    print('  draft errors: ' + '; '.join(f'{k} {c} {w} -> {v}' for k, c, w, v in errors))


def lab_1_3():
    rows = load(F / 'd1/procurement_options.csv')
    out = {}
    for r in rows:
        b, a, e = int(r['build_cost_sar']), int(r['annual_cost_sar']), int(r['exit_cost_sar'])
        out[r['option']] = (b + a, b + 5 * a + e)
        print(f"  {r['option']}: first year {b + a:,}  five years with exit {b + 5 * a + e:,}  local content {r['local_content_pct']}%  independent test {r['independent_test_offered']}")
    assert min(out, key=lambda k: out[k][0]) == 'X'
    assert min(out, key=lambda k: out[k][1]) == 'Y'
    assert max(out, key=lambda k: out[k][1]) == 'X'


def lab_1_4():
    counts = defaultdict(int)
    for _, _, cat in G.CLAIMS:
        counts[cat] += 1
    assert counts == {'public_value': 6, 'adoption': 3, 'private_return': 3, 'fiscal_saving': 2, 'not_a_benefit': 2}, counts
    print('  ' + ', '.join(f'{k} {v}' for k, v in sorted(counts.items())))
    print('  ' + '; '.join(f'{c} {cat}' for c, _, cat in G.CLAIMS))


def baselines(enq_path, dec_path):
    enq, dec = load(enq_path), load(dec_path)
    out = {}
    for lang in ('ar', 'en'):
        sub = [r for r in enq if r['language'] == lang]
        n = sum(float(r['contacts']) for r in sub)
        out[f'wrong_info_per_1000_{lang}'] = sum(float(r['wrong_info_complaints_per_1000']) * float(r['contacts']) for r in sub) / n
        out[f'repeat_pct_{lang}'] = sum(float(r['repeat_contact_pct']) * float(r['contacts']) for r in sub) / n
        ph = [r for r in sub if r['channel'] == 'phone']
        pn = sum(float(r['contacts']) for r in ph)
        out[f'phone_wait_{lang}'] = sum(float(r['avg_wait_min']) * float(r['contacts']) for r in ph) / pn
        out[f'phone_in_target_{lang}'] = sum(float(r['answered_in_target_pct']) * float(r['contacts']) for r in ph) / pn
        ds = [r for r in dec if r['language'] == lang]
        apps = sum(float(r['applications']) for r in ds)
        out[f'incomplete_pct_{lang}'] = 100 * sum(float(r['incomplete_on_arrival']) for r in ds) / apps
        out[f'median_days_{lang}'] = sum(float(r['median_working_days_to_decision']) * float(r['applications']) for r in ds) / apps
    apps = sum(float(r['applications']) for r in dec)
    out['incomplete_pct_all'] = 100 * sum(float(r['incomplete_on_arrival']) for r in dec) / apps
    out['median_days_weighted'] = sum(float(r['median_working_days_to_decision']) * float(r['applications']) for r in dec) / apps
    for area in ('urban', 'semi_urban', 'rural'):
        ds = [r for r in dec if r['area'] == area]
        a = sum(float(r['applications']) for r in ds)
        out[f'median_days_{area}'] = sum(float(r['median_working_days_to_decision']) * float(r['applications']) for r in ds) / a
    for g in ('older_self', 'disability_self', 'carer'):
        ds = [r for r in dec if r['group'] == g]
        ap = sum(float(r['appealed']) for r in ds)
        out[f'overturn_pct_{g}'] = 100 * sum(float(r['overturned_on_appeal']) for r in ds) / ap
    online = defaultdict(float)
    tot = defaultdict(float)
    for r in enq:
        tot[r['group']] += float(r['contacts'])
        if r['channel'] == 'online':
            online[r['group']] += float(r['contacts'])
    for g in tot:
        out[f'online_share_{g}'] = 100 * online[g] / tot[g]
    return out


def lab_2_1():
    out, table = VC.compute('grant')
    for k in ('contacts_per_year', 'deflected_contacts', 'citizen_hours_saved', 'benefits_per_year',
              'run_cost_per_year', 'npv_public_value', 'npv_fiscal', 'bcr', 'decision_days_saved_total'):
        print(f'  {k:26} {out[k]:,.2f}')
    per = {(g, l): p for g, l, _, _, _, p in table}
    print('  hours per 1,000 contacts: ' + ', '.join(f'{g}/{l} {p:.1f}' for (g, l), p in per.items()))
    assert out['bcr'] < 1 and out['npv_fiscal'] < out['npv_public_value'] < 0
    assert per[('older_self', 'ar')] == min(per.values())
    # the draft's errors: adoption counted, staff time counted twice and as cash, review staff omitted
    draft_annual = 1_000_000 + 746_667 + 746_667
    print(f'  draft benefits {draft_annual:,} vs recomputed {out["benefits_per_year"]:,.0f}; draft omitted review staff {2 * 290_000:,}')
    # sensitivity the lab asks for: English quality after the test (B: 16 of 20 = 0.8)
    import tempfile, os
    rows = load(F / 'd2/assumptions.csv')
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'a.csv'
        with open(p, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            for r in rows:
                r = dict(r)
                if r['key'] == 'quality_en':
                    r['value'] = '0.8'
                w.writerow(r)
        o2, _ = VC.compute('grant', p)
    print(f'  with quality_en 0.8: benefits {o2["benefits_per_year"]:,.0f}, npv {o2["npv_public_value"]:,.0f}')


def lab_2_2():
    b = baselines(F / 'd2/enquiries_monthly.csv', F / 'd2/decisions_monthly.csv')
    for k, v in b.items():
        print(f'  {k:30} {v:.1f}')
    assert b['incomplete_pct_en'] > b['incomplete_pct_ar'] + 10
    assert b['median_days_weighted'] > 30
    levels = defaultdict(list)
    for j, _, lvl, _ in G.JOURNEY:
        levels[lvl].append(j)
    print('  levels: ' + '; '.join(f'{k} {",".join(v)}' for k, v in levels.items()))
    print('  outcome measures: ' + ', '.join(m for m, _, k in G.MEASURES if k == 'outcome'))


def lab_2_3_and_2_4(cfgs=('a', 'b')):
    res = {}
    for cfg in cfgs:
        rows, rec = RT.evaluate(cfg, recorded_only=True)
        s = RT.summarise(rows)
        res[cfg] = s
        print(f"  {cfg.upper()}: ar {s['passed']['ar']}/{s['n']['ar']} en {s['passed']['en']}/{s['n']['en']} critical {','.join(s['critical']) or '-'} stop {','.join(s['stop_critical']) or '-'} decision {s['decision']}")
        print(f"     failures {s['failures']}")
        print(f"     by group {s['by_group']}  pairs {s['pairs']}")
    return res


def lab_2_3():
    r = lab_2_3_and_2_4()
    assert r['a']['decision'] == 'STOP' and r['b']['decision'] == 'FIX'


def lab_2_4():
    r = lab_2_3_and_2_4()
    assert r['b']['critical'] == ['T35'] and r['b']['rate'] == {'ar': 95.0, 'en': 80.0}
    assert r['b']['pairs']['ar_only'] == 3


def lab_3_1():
    rows, _ = RT.evaluate('b', recorded_only=True)
    s = RT.summarise(rows)
    total = s['passed']['ar'] + s['passed']['en']
    print(f'  B overall {total}/40 = {100 * total / 40:.1f}% (the draft record says 95%); ar {s["rate"]["ar"]}%, en {s["rate"]["en"]}%')
    assert total == 35
    print('  draft record errors: decides eligibility; vendor as owner; trains on questions; 95%; no language results; no human route; no review date')


def lab_3_2():
    bad_level, changed = [], []
    for rid, _, l, i, lvl, treat, owner in G.RISKS:
        if l * i != lvl:
            bad_level.append((rid, lvl, l * i))
        kl, ki, kt, ko = G.RISK_KEY[rid]
        level = kl * ki
        band = 'catastrophic' if level == 16 else 'high' if level >= 8 else 'medium' if level >= 3 else 'low'
        if kt != treat or (kl, ki) != (l, i):
            changed.append((rid, treat, kt))
        print(f'  {rid} {kl}x{ki} = {level:2} {band:12} {kt:9} {ko}')
    print('  level arithmetic errors: ' + str(bad_level))
    print('  treatment changes: ' + str(changed))
    assert bad_level == [('R02', 8, 12)]
    vendors = [r[0] for r in G.RISKS if 'مزود' in r[6]]
    assert vendors == ['R06']


def lab_3_3():
    probs = [(k, p) for k, _, _, _, _, p in G.PACK if p]
    print('  pack problems: ' + str(probs))
    assert len(probs) == 4
    print('  appeal draft problems: rephrase is not human review; appeal to the same officer; Arabic only; no deadline; restart from scratch')


def lab_3_4():
    rows = load(F / 'd3/workforce_profile.csv')
    total = sum(int(r['headcount']) for r in rows)
    gap = sum(int(r['headcount']) - int(r['meeting_baseline_now']) for r in rows)
    base = [r for r in rows if r['target_card'] == 'AP-AM']
    base_gap = sum(int(r['headcount']) - int(r['meeting_baseline_now']) for r in base)
    spec = [r for r in rows if r['target_card'] != 'AP-AM']
    print(f'  staff {total}; below their target now {gap}; of them on the AP-AM baseline {base_gap}; specialist roles {sum(int(r["headcount"]) for r in spec)}')
    prog = {r['measure']: float(r['value']) for r in load(F / 'd3/programme_results.csv')}
    print(f"  programme: completion {100 * prog['completed'] / prog['enrolled']:.0f}%, complaints {prog['wrong_info_complaints_per_1000_before']} -> {prog['wrong_info_complaints_per_1000_after']}, audit {prog['audit_sample_drafts_checked_ok_pct_before']} -> {prog['audit_sample_drafts_checked_ok_pct_after']}")
    assert total == 693 and gap == 502


def capstone():
    out, table = VC.compute('carers')
    for k in ('contacts_per_year', 'benefits_per_year', 'run_cost_per_year', 'npv_public_value', 'npv_fiscal', 'bcr', 'decision_days_saved_total'):
        print(f'  {k:26} {out[k]:,.2f}')
    r = lab_2_3_and_2_4(('c',))
    assert r['c']['decision'] == 'STOP' and r['c']['stop_critical'] == ['C18']
    b = baselines(F / 'capstone/carers_enquiries_monthly.csv', F / 'capstone/carers_decisions_monthly.csv')
    for k in ('incomplete_pct_ar', 'incomplete_pct_en', 'median_days_weighted', 'overturn_pct_carer', 'phone_wait_ar', 'phone_wait_en'):
        print(f'  {k:26} {b[k]:.1f}')


LABS_ALL = {'1.1': lab_1_1, '1.2': lab_1_2, '1.3': lab_1_3, '1.4': lab_1_4, '2.1': lab_2_1, '2.2': lab_2_2,
            '2.3': lab_2_3, '2.4': lab_2_4, '3.1': lab_3_1, '3.2': lab_3_2, '3.3': lab_3_3, '3.4': lab_3_4,
            'capstone': capstone}

if __name__ == '__main__':
    want = sys.argv[1:] or list(LABS_ALL)
    for k in want:
        print(f'lab {k}')
        LABS_ALL[k]()
        print(f'lab {k}: PASS')
