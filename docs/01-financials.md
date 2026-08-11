# Paton Hall — Financial Model

**Status:** Planning model, not an audited forecast. Every figure is an assumption published for inspection.
**Compiled:** 2026-08-11
**Horizon:** 12 months, matching the one-year lease (`PH-052`). Month 12 is a renewal decision, not a waypoint.
**Site:** costed at 4 Breadalbane, the preferred site. The model is not specific to it — see §8.4.
**Companion to:** `00-repository.md`

---

## 1. The shape of the thing, in four lines

- Fixed monthly cost: **$4,500**, inside the $5,000 ceiling.
- Membership break-even: **51 members**.
- One part-time employee becomes affordable at roughly **$7,750/month** of revenue.
- Two become affordable at roughly **$10,500/month**.

Everything below is the arithmetic behind those four numbers, plus the one place the model gets uncomfortable (§6).

---

## 2. Cost base

| Line | Monthly | Annual | Note |
|---|---:|---:|---|
| Rent | $2,500 | $30,000 | **Assumed gross.** See §8.1 if TMI is extra. |
| Utilities — hydro, gas, water | $600 | $7,200 | 1927 uninsulated garage, winter-weighted. Least reliable figure here. |
| Insurance — CGL, contents, public assembly | $350 | $4,200 | Planning figure. Must be confirmed against real quotes. |
| Internet — business fibre | $150 | $1,800 | |
| Maintenance, cleaning, consumables | $300 | $3,600 | Includes coffee, markers, shop supplies. |
| Software and admin | $150 | $1,800 | Membership platform, bookkeeping, domain, payments. |
| Repairs and contingency reserve | $450 | $5,400 | 10% of the above. A century-old building earns this line. |
| **Total** | **$4,500** | **$54,000** | **$500/month of headroom against the $5,000 ceiling.** |

**Not in this table, deliberately:** staff (§5), bench capital (§7), and any leasehold improvement. Operating cost and investment are kept separate so neither hides inside the other.

---

## 3. Revenue architecture

Five streams. The first one carries the building; the rest buy the future.

| # | Stream | Role |
|---|---|---|
| 1 | **Memberships** | Covers operating cost. Non-negotiable foundation. |
| 2 | **Learning days and seminars** | Ticketed for non-members. Funnel and margin. |
| 3 | **Certified training (EPTAC / IPC)** | The industry revenue. Gated on `PH-032`. |
| 4 | **Space rental** | Member-led and external events. Uses idle hours. |
| 5 | **Corporate patrons** | A firm underwrites a monthly slot for hiring access and named seats in each training cohort. |

**Not modelled, on purpose:** any revenue from member ventures or investment access. Paton Hall takes no fee, commission or carry (`PH-029`). That line is worth zero here, correctly.

---

## 4. Memberships and break-even

### 4.1 Tier mix and blended ARPU

| Tier | Price | Share of members | Contribution to ARPU |
|---|---:|---:|---:|
| Bench | $50 | 50% | $25.00 |
| Shop | $100 | 35% | $35.00 |
| Keyholder | $200 | 15% | $30.00 |
| **Blended ARPU** | | | **$90.00** |

### 4.2 Break-even

$4,500 ÷ $90 = **50 members.** At the actual integer mix:

| Tier | Members | Revenue |
|---|---:|---:|
| Bench @ $50 | 26 | $1,300 |
| Shop @ $100 | 18 | $1,800 |
| Keyholder @ $200 | 7 | $1,400 |
| **Total** | **51** | **$4,500** |

**Fifty-one members covers rent, heat, light, insurance, internet, supplies and contingency, with no events, no training and no sponsors.** That is the whole argument in a single number: the Hall's fixed cost is rent, not a machine fleet.

### 4.3 Sensitivity of break-even

| If… | Break-even becomes |
|---|---:|
| Utilities run $1,000 not $600 | 56 members |
| Lease is net and TMI adds $700/mo | 59 members |
| Both of the above | 64 members |
| ARPU comes in at $80 (thinner Keyholder tier) | 57 members |
| Rent-free first month negotiated | unchanged, but adds $2,500 to launch float |

Even the pessimistic corner, 64 members, is modest for a city with Hamilton's industrial population. That is the model's strength, and it needs no dressing up.

---

## 5. The staffing ladder

**Assumption:** one part-time role at 20 hrs/week, $25/hour, plus roughly 12% statutory burden (CPP, EI, EHT, WSIB, vacation accrual).

> 20 hrs × 52 weeks ÷ 12 months = 86.7 hrs/month × $25 = $2,167 + burden ≈ **$2,500/month all-in.**

| Rung | Staffing | Monthly cost | Revenue to cover | Prudent trigger (with 10% surplus) |
|---|---|---:|---:|---:|
| **1** | Volunteer | $4,500 | $4,500 | $5,000 |
| **2** | One part-timer | $7,000 | $7,000 | **$7,750** |
| **3** | Two part-timers | $9,500 | $9,500 | **$10,500** |

### 5.1 What has to fire to reach each rung

**Rung 2 — one part-timer at $7,750/month.** Memberships get you most of the way and cannot get you all of it.

| Source | Contribution |
|---|---:|
| 65 members @ $90 | $5,850 |
| Learning days, ~3/month | $1,100 |
| Space rental | $600 |
| Hosted training, annualised | $720 |
| **Total** | **$8,270** |

Comfortably clears $7,750. **Memberships alone never reach Rung 2.** At $90 ARPU it would take 78 members to fund a part-timer on memberships alone: achievable, but slower and more fragile than adding a second stream. Programming is what makes employment possible.

**Rung 3 — two part-timers at $10,500/month.** Requires certified training running as a real line rather than an occasional event.

| Source | Contribution |
|---|---:|
| 90 members @ $95 | $8,550 |
| Learning days, ~4/month | $1,700 |
| Space rental | $1,000 |
| Training, own bench + hosted | $3,000 |
| Corporate patrons ×2 | $1,500 |
| **Total** | **$15,750** |

Clears comfortably, with room for reserve and bench amortisation. **Rung 3 is a training-revenue question, not a membership question.** If EPTAC does not convert (`PH-032`), Rung 3 does not happen in year one, and the model says so.

---

## 6. Twelve-month scenarios

Member ramp assumptions, base case: 20 founding members pre-sold before doors open, then roughly 5/month tapering to 2/month.

| Month | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Members | 26 | 32 | 37 | 42 | 46 | **50** | 54 | 57 | 60 | 62 | 64 | 65 |

Break-even is crossed in **Month 6**.

### 6.1 Year-one totals

| | Conservative | Base | Upside |
|---|---:|---:|---:|
| Members at Month 12 | 40 | 65 | 90 |
| Blended ARPU | $85 | $90 | $95 |
| Membership revenue | $29,580 | $53,550 | $62,700 |
| Learning days | $4,800 | $8,700 | $13,200 |
| Space rental | $2,400 | $4,500 | $7,200 |
| Certified training | $2,160 | $8,640 | $20,000 |
| Corporate patrons | $0 | $3,000 | $10,000 |
| **Total revenue** | **$38,940** | **$78,390** | **$113,100** |
| Operating cost | $54,000 | $54,000 | $54,000 |
| **Surplus before staff** | **($15,060)** | **$24,390** | **$59,100** |
| Staff cost in year | $0 | $10,000 (1 PT from M9) | $35,000 (2 PT from M6) |
| **Net year-one position** | **($15,060)** | **$14,390** | **$24,100** |

Training assumptions: hosted cohorts of 8 students at roughly $900/seat, with the Hall taking a 30% host share (~$2,160 per cohort). Conservative assumes 1 cohort in the year; base assumes 4; upside assumes 8 with some own-delivered.

### 6.2 Where the model gets uncomfortable

**The conservative case exits Month 12 at a positive run-rate but loses about $15,000 across the year.**

That is the shape of every ramp rather than a flaw in the model. The Month-12 run-rate under conservative assumptions is roughly $4,650/month against $4,500 of cost, which sustains. But the first five months sit below break-even, and something has to pay for them.

**The fix is structural and it is cheap:** sell founding memberships before rent starts.

> **25 founding members × 6 months prepaid × $90 = $13,500.**

That lands within a few hundred dollars of the conservative-case first-year gap, and matches the 3-month reserve target. **Pre-selling the founding cohort is the single most important financial action available before Month 0**, and it doubles as the seed community that solves the cold-start problem in `00-repository.md` §10.

If the founding cohort cannot be sold before opening, that is real information about demand, delivered at the cheapest possible moment.

---

## 7. Capital — the bench cell

**Not in the operating budget. Funded from surplus, patron sponsorship, or grant — never from operating float.**

Indicative build for a demountable, teaching-grade bench cell (`PH-033`):

| Item | Cost |
|---|---:|
| ESD benches ×2, knock-down frames | $2,400 |
| ESD matting, wrist straps, grounding | $800 |
| Inspection microscope (Mantis-class) | $4,500 |
| Soldering and hot-air stations ×3 | $2,400 |
| Portable fume extraction ×2 | $1,800 |
| Test gear — scope, PSU, meters | $1,200 |
| Camera and display rig | $1,400 |
| Consumables and tooling | $600 |
| **Total** | **$15,100** |

Notes that matter:

- **Every item is portable.** Mats not flooring; portable extraction not ducted; knock-down frames. On a one-year lease this is not optional — it is what makes the investment defensible at all. The equipment survives the address (`PH-053`).
- **The camera and display rig earns its place.** It converts one bench into a room-scale teaching instrument, so a single trainer demonstrates to a full seminar instead of four people crowding a scope.
- **Dual use is the justification.** The bench serves members on build nights and trainers during certification. Neither use alone would justify the spend inside twelve months. Together they do.
- **Comparators** (`PH-034`): a 20-station institutional lab runs $100,000–300,000+; funded mobile training labs run $500,000–1,200,000. This cell teaches the same standard at roughly 20–50× less.

---

## 8. Assumptions, stated so they can be attacked

### 8.1 The ones most likely to be wrong

1. **Rent is gross.** If $2,500 is net and TMI adds $500–900/month, break-even moves to 56–61 members and the conservative case worsens by $6,000–11,000 across the year. **Confirm before circulating any financial document.**
2. **Utilities at $600.** A 1927 uninsulated concrete-block garage through a Hamilton winter could run materially higher. The contingency line absorbs some of this; a $1,000 month does not break the model but does move break-even to 56.
3. **Insurance at $350.** Public assembly, after-hours keyholder access, build nights and eventual soldering together sit outside a standard small-commercial policy. A placeholder until quoted.
4. **ARPU at $90.** Depends on a healthy Shop tier. If the membership skews to Bench, ARPU falls toward $70 and break-even rises to 64.
5. **Training converts.** All certified-training revenue is gated on `PH-032` — EPTAC is in conversation, nothing signed. The base case survives its removal (falling to roughly $69,750 revenue, still funding one part-timer); the upside case does not.

### 8.2 Deliberately conservative choices

- No revenue booked from member ventures, investment access, or referrals.
- No grant income modelled, despite `PH-009`/`PH-010` being live and relevant. Any Ontario Job Grant or SDF participation is upside, not plan.
- Volunteer labour valued at zero, which understates the true cost base and is the honest way to present it.
- No membership price increases across the twelve months.

### 8.4 The model is not specific to 4 Breadalbane

- Rent at $2,500/month for roughly 2,000 sq ft is the input the whole cost base rests on. **It is a market rate, not a one-off.**
- The requirement is modest and repeatable: 1,500–2,500 sq ft of open single-storey space, ground-level vehicle access, parking, three-phase power where available, at or under $2,500/month.
- Other Hamilton properties are being actively scouted (`PH-055`). If 4 Breadalbane does not proceed, the cost base moves by the difference in rent and nothing else in this model changes.
- Practical consequence: break-even moves roughly **1 member per $90/month of rent difference**. A room at $3,000 needs 57 members instead of 51.

---

### 8.3 Reserve policy

- Target: **3 months' operating cost = $13,500.**
- On a one-year lease the reserve doubles as **the move fund**. If renewal fails, it pays for relocation without an emergency appeal to members.
- Base case reaches it by Month 12. Conservative case does not, which is the clearest argument for the founding-member float in §6.2.

---

## 9. What good looks like at Month 12

Not a revenue number. Four pieces of evidence:

1. A membership that covers costs without events or training.
2. At least one certified cohort delivered, with named students.
3. At least one employer who paid — or successfully claimed a grant — for training at the Hall.
4. Programming that runs on nights the organisers are not there.

A Hall with those four things and a lost lease is in a far better position than one with a renewed lease and none of them.
