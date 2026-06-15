# MINUTES OF MEETING

**Meeting ID:** MOM-RHADC-006
**Meeting Title:** Tapeout Readiness Review
**Date:** 15 July 2025
**Time:** 09:00 – 12:00 hrs
**Location:** Conference Room B2, Building 7, GSRML
**Chairperson:** Dr. Arvind Sharma, Program Director

---

## Attendees

| Name | Role | Department |
|------|------|------------|
| Dr. Arvind Sharma | Program Director | PMO |
| Rajesh Nair | Chief Design Engineer | Analog Design |
| Vikram Joshi | Senior Analog Designer | Analog Design |
| Sunil Verma | Lead Verification Engineer | Design Verification |
| Kavya Reddy | Verification Engineer | Design Verification |
| Deepak Rao | Digital Design Lead | Digital Design |
| Dr. Priya Menon | Radiation Hardening Specialist | Process Engineering |
| Anil Kapoor | Fabrication Manager | Wafer Fab |
| Meena Iyer | Packaging and Reliability Lead | Packaging / QA |
| Rohit Das | Systems Engineer | Systems Integration |
| Sanjay Bhatt | Project Controller | PMO |
| Lakshmi Srinivasan | Quality Assurance Manager | QA |
| Col. (Retd.) V. K. Tiwari | Customer Representative | DRDO |

---

## Agenda

1. Review of action items from MOM-RHADC-005
2. TMR voter fix status (DEC-014)
3. SAR ENOB fix status (DEC-015)
4. DRC/LVS clean status
5. Verification closure — complete status
6. Tapeout Readiness Checklist review
7. Fabrication kick-off readiness confirmation
8. Customer sign-off on tapeout
9. AOB

---

## Discussion Points

**1. Action Item Review**
- AI-024: Complete. Revised TMR voter with input pipeline registers implemented. Formal verification re-run: all 22 properties proven. No new failures. Physical spacing between TMR input register cells confirmed ≥ 50 µm per Dr. Menon's spacing requirement.
- AI-025: Complete. 10% extended regeneration phase implemented in SAR timing controller. Re-simulation at SS/–40°C/100 krad: ENOB = 14.24 bits, SNR = 87.2 dBFS. Both pass requirements. Nominal power impact: +2 mW. Updated total power: 425 mW.
- AI-026: Complete. All 147 DRC violations resolved. 2 LVS open-net errors resolved (metal fill connectivity issue in digital macro). Full-chip DRC and LVS: **CLEAN** as of 10 July 2025.
- AI-027: Complete. DMC convergence coverage: 12/12 corners at 100% closure. All background calibration scenarios covered.
- AI-028: Tapeout Readiness Checklist (TRC v0.3) distributed prior to this meeting.

**2. TMR Voter Fix (DEC-014) Confirmation**
Deepak Rao confirmed the revised voter implementation. Dr. Menon reviewed the physical layout and confirmed the 50 µm spacing requirement between input register cells is met in all four instances. She noted that this change partially addresses the simultaneous dual-bit upset concern; the probability of simultaneous particle hit on two physically separated registers is significantly reduced. She stated this meets the GSRML SEU design guidance for the application.

**3. SAR ENOB Fix (DEC-015) Confirmation**
Rajesh Nair presented the re-simulation results. ENOB passes at 14.24 bits across all 27 priority corners. He confirmed that the 10% extended regeneration phase does not impair inter-channel synchronisation; timing margin analysis shows ≥ 350 ps of guardband in the channel synchronisation path.

Col. Tiwari asked whether the 14.24 bits at worst-case corner provides adequate mission margin. Rajesh Nair confirmed the requirement is ≥ 14.2 bits; the 0.04-bit margin is acknowledged as slim. Dr. Sharma directed this to be flagged in the tapeout release note as a risk item to be validated on silicon.

**4. DRC/LVS Status**
Rajesh Nair confirmed DRC and LVS are fully clean as of 10 July 2025 on GDS-II revision RHADC-GDS-R04. Anil Kapoor confirmed the GDS-II file has been received and pre-DRC check at the fab side has also passed.

**5. Verification Closure Summary**
Sunil Verma presented the final verification closure summary:

| Verification Item | Status |
|-------------------|--------|
| Block-level simulation (27 priority corners) | CLOSED — All pass |
| Full-chip simulation (nominal) | CLOSED — All pass |
| Full-chip simulation (100 krad/SS/–40°C) | CLOSED — All pass (post DEC-015) |
| Formal verification — TMR blocks | CLOSED — 22/22 properties proven |
| SEU fault injection — TMR voters | CLOSED — Correct output confirmed in all fault injection scenarios |
| DMC calibration coverage (12 corners) | CLOSED — 100% |
| DRC/LVS | CLOSED — Clean |

One item noted as observation (not blocking): Tier 3 gate-level simulation at the FF/+85°C/pre-rad corner shows SNR = 87.4 dBFS — passes requirement but timing analysis shows one path at 8% timing slack. Deepak Rao stated this path is within the timing tool sign-off methodology and not a violation.

**6. Tapeout Readiness Checklist Review**
TRC v0.3 reviewed item by item. All 34 checklist items confirmed closed or with documented acceptable deviations. Dr. Sharma confirmed the TRC as complete.

**7. Fabrication Kick-Off**
Anil Kapoor confirmed the fab is ready to receive the tapeout package. First lot (3 wafers, engineering lot) will use GS180H Lot 1. Target first wafer start: 21 July 2025. Target wafer completion (first lot): 9 weeks after wafer start, approximately 22 September 2025.

Anil Kapoor noted that the current GS180H poly gate etch tool (Tool SET-4) is scheduled for preventive maintenance 28–30 July. The three-day maintenance window does not impact wafer start on 21 July if tapeout sign-off is received today.

**8. Customer Sign-Off**
Col. Tiwari acknowledged the verification closure and tapeout readiness. He noted the slim ENOB margin at the worst-case radiation corner and formally requested that silicon validation of ENOB at post-irradiation conditions be included in the acceptance test plan. Dr. Sharma agreed and directed Sunil Verma to update the acceptance test plan (ATP) accordingly.

Col. Tiwari signed the tapeout sign-off form (PDMS-RHADC-TPOUT-001) at 11:40 hrs. Tapeout approved.

---

## Decisions Made

| Decision ID | Decision | Owner |
|-------------|----------|-------|
| DEC-016 | Tapeout of RHADC-GDS-R04 approved; wafer start authorised for 21 July 2025 (engineering lot, 3 wafers) | Dr. Sharma / Anil Kapoor |
| DEC-017 | Post-irradiation ENOB measurement at SS-equivalent conditions to be included in acceptance test plan as a mandatory pass/fail criterion | Sunil Verma |

---

## Action Items

| AI ID | Action | Owner | Due Date |
|-------|--------|-------|----------|
| AI-029 | Deliver final tapeout package (GDS-II, LVS netlist, final DRC report, DSD v1.0) to Wafer Fab by 18 July 2025 | Rajesh Nair | 18 Jul 2025 |
| AI-030 | Issue tapeout release note documenting the slim ENOB margin at worst-case corner as a silicon validation risk item | Rajesh Nair | 18 Jul 2025 |
| AI-031 | Update acceptance test plan (ATP v0.1) to include post-irradiation ENOB test as mandatory | Sunil Verma | 01 Aug 2025 |
| AI-032 | Confirm engineering lot wafer start and weekly fab progress reporting mechanism | Anil Kapoor | 25 Jul 2025 |
| AI-033 | Prepare package and assembly drawings; confirm CQFP-80 ceramic body inventory | Meena Iyer | 01 Aug 2025 |
| AI-034 | Book TID irradiation test slot at TIFR for post-silicon characterisation; target October 2025 | Dr. Menon | 01 Aug 2025 |

---

## Risks Identified / Updated

| Risk ID | Description | Likelihood | Impact | Status / Update |
|---------|-------------|-----------|--------|-----------------|
| RSK-007 | ENOB at worst-case radiation corner — passes simulation with only 0.04-bit margin; silicon validation required | Medium | High | Open; mandatory silicon validation added to ATP |
| RSK-002 | Schedule — tapeout slipped 2 weeks vs. plan (Week 28 → Week 30); first silicon now ~22 Sep; overall program impact being assessed | Medium | Medium | Monitoring |
| RSK-009 | First silicon yield from engineering lot unknown; if yield < 50%, device screening for characterisation may be insufficient | Medium | High | New — Anil Kapoor owner |

---

## Next Meeting Objectives

Meeting 07 — Fabrication and Yield Review (target: ~late September 2025, after engineering lot wafer delivery):
- Report engineering lot fabrication results and yield
- Review inline process monitors and parametric data
- Present wafer-level test results
- Assess whether first silicon meets key electrical parameters
- Discuss production lot planning

---

## Meeting Conclusion

Dr. Sharma declared tapeout approved and the meeting closed at 12:00 hrs. The program is now in the fabrication phase. Sanjay Bhatt will update the program schedule and circulate revised milestones reflecting the 2-week slip.

**Minutes prepared by:** Sanjay Bhatt, Project Controller
**Date of issue:** 16 July 2025
**Distribution:** All attendees, PDMS
