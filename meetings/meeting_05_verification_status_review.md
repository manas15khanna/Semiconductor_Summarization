# MINUTES OF MEETING

**Meeting ID:** MOM-RHADC-005
**Meeting Title:** Verification Status Review
**Date:** 17 June 2025
**Time:** 09:30 – 12:00 hrs
**Location:** Conference Room B2, Building 7, GSRML
**Chairperson:** Dr. Arvind Sharma, Program Director

---

## Attendees

| Name | Role | Department |
|------|------|------------|
| Dr. Arvind Sharma | Program Director | PMO |
| Sunil Verma | Lead Verification Engineer | Design Verification |
| Kavya Reddy | Verification Engineer | Design Verification |
| Rajesh Nair | Chief Design Engineer | Analog Design |
| Vikram Joshi | Senior Analog Designer | Analog Design |
| Deepak Rao | Digital Design Lead | Digital Design |
| Dr. Priya Menon | Radiation Hardening Specialist | Process Engineering |
| Rohit Das | Systems Engineer | Systems Integration |
| Sanjay Bhatt | Project Controller | PMO |
| Lakshmi Srinivasan | Quality Assurance Manager | QA |

---

## Agenda

1. Review of action items from MOM-RHADC-004
2. Block-level simulation closure status
3. Formal verification status (TMR blocks)
4. Full-chip simulation results — SNR, ENOB, power
5. DMC background calibration coverage status
6. DRC/LVS status and tapeout path
7. Risk review
8. AOB

---

## Discussion Points

**1. Action Item Review**
- AI-019: VP-RHADC v1.0 issued 22 May 2025. Archived in PDMS.
- AI-020: Compute cluster priority raised. Additional 40-node allocation confirmed from 15 May.
- AI-021: Formal verification in progress — see item 3 below.
- AI-022: Layout 88% complete. DRC/LVS report not yet available — delayed one week to 06 Jun. See item 6 below.
- AI-023: SEU fault injection test plan issued 22 May.

**2. Block-Level Simulation Status**
Vikram Joshi reported:
- SAR core: All 27 priority corners simulated. All pass DNL/INL ≤ ±0.5 LSB at nominal. At SS/–40°C/100 krad corner, DNL peaks at ±0.72 LSB — within the ±1 LSB specification.
- Reference generator: Post-TID simulation complete. Bandgap drift 1.9 mV at 100 krad — pass.
- Clock distribution: H-tree layout simulated. Inter-channel skew < 0.7 ps at all corners — meets < 1 ps requirement.

**3. Formal Verification — TMR Blocks**
Deepak Rao reported formal verification results:
- Clock control registers: 18/18 properties proven. Clean.
- Configuration registers: 12/12 properties proven. Clean.
- DMC TMR voter logic: 22 properties defined. 19 proven. **3 properties failing** — related to correct majority vote output when all three TMR inputs toggle simultaneously within a 1-clock-cycle window. This scenario can occur during SEU on the voter input flip-flops.

Deepak Rao explained the failing case: if two of the three TMR inputs to the majority voter toggle in the same clock edge due to a high-LET particle hit, the current voter implementation does not latch the pre-event correct value; it propagates the upset. The TMR protection is ineffective for this simultaneous dual-bit upset scenario.

Dr. Menon stated this is a known but often overlooked issue with synchronous TMR. The standard fix is to add pipeline registers with independent clock domains or use asynchronous voter with output register. She proposed adding a one-cycle delay register on each TMR input branch before the voter, implemented in separate physical cells with spacing requirements to reduce probability of simultaneous particle hit.

Dr. Sharma directed this to be treated as a blocking issue for tapeout. DEC-008 (TMR mandatory for DMC) stands, but the implementation must be corrected.

**4. Full-Chip Simulation Results**
Sunil Verma reported initial full-chip mixed-signal simulation results:

| Parameter | Result | Requirement | Status |
|-----------|--------|-------------|--------|
| ENOB at Nyquist (TT/27°C/pre-rad) | 14.31 bits | ≥ 14.2 bits | PASS |
| SNR at Nyquist | 88.1 dBFS | ≥ 87 dBFS | PASS |
| DNL (peak) | ±0.51 LSB | ≤ ±1 LSB | PASS |
| INL (peak) | ±0.88 LSB | ≤ ±2 LSB | PASS |
| Power (nominal) | 423 mW | ≤ 450 mW | PASS |
| ENOB at 100 krad corner (SS/–40°C) | 13.87 bits | ≥ 14.2 bits | **FAIL** |
| SNR at 100 krad corner (SS/–40°C) | 85.4 dBFS | ≥ 87 dBFS | **FAIL** |

The two failures at the 100 krad / SS / –40°C corner are significant. Sunil Verma traced the ENOB degradation to increased comparator noise at the SS process corner combined with post-TID threshold shift on the comparator regeneration path transistors.

Rajesh Nair reviewed the comparator design. He believes the root cause is the regeneration time constant increasing at SS/cold/post-TID, which reduces the time for full regeneration within the clock cycle, leaving residual offset that degrades ENOB. He proposed increasing the regeneration clock phase duration by 10% in the SAR timing sequence. This change would require a revision to the SAR timing controller in the digital block and a re-simulation.

Deepak Rao noted the timing controller change is straightforward but must be done carefully to avoid impacting inter-channel synchronisation.

**5. DMC Background Calibration Coverage**
Kavya Reddy reported DMC convergence coverage: 9/12 PVT corners at 100% coverage. 3 corners (SS/–40°C/100 krad variants) not yet complete due to extended simulation runtime (~18 hours per corner). Expected to complete by 27 June with the extended compute allocation.

**6. DRC/LVS Status**
Rajesh Nair reported: full-chip DRC run completed 13 June. **147 DRC violations** found, primarily in the clock distribution H-tree routing (short spacing violations between H-tree metal segments and power grid at M3 layer). LVS: 2 open-net errors in the digital macro area (Deepak Rao investigating). No violations in analog blocks.

The DRC violations are routing-level issues, not design-rule fundamental issues. Expected to be resolved within one week.

---

## Decisions Made

| Decision ID | Decision | Owner |
|-------------|----------|-------|
| DEC-014 | TMR voter implementation to be revised: one-cycle pipeline delay register added on each input branch with physical cell spacing per Dr. Menon's recommendation; this is a blocking tapeout issue | Deepak Rao / Dr. Menon |
| DEC-015 | SAR timing controller to be revised to extend regeneration clock phase by 10%; re-simulation at SS/–40°C/100 krad corner required to confirm ENOB recovery | Rajesh Nair / Deepak Rao |

---

## Action Items

| AI ID | Action | Owner | Due Date |
|-------|--------|-------|----------|
| AI-024 | Implement revised TMR voter with input pipeline registers; re-run formal verification; confirm all 22 properties proven | Deepak Rao | 04 Jul 2025 |
| AI-025 | Implement 10% extended regeneration phase in SAR timing controller; re-run full-chip simulation at SS/–40°C/100 krad corner; confirm ENOB ≥ 14.2 bits | Rajesh Nair / Vikram Joshi | 04 Jul 2025 |
| AI-026 | Resolve 147 DRC violations in H-tree routing; re-run DRC to clean; resolve 2 LVS open-net errors | Rajesh Nair / Deepak Rao | 27 Jun 2025 |
| AI-027 | Complete DMC convergence coverage for remaining 3 corners; confirm 100% closure; report to tapeout review | Kavya Reddy | 27 Jun 2025 |
| AI-028 | Update tapeout readiness checklist (TRC v0.1); identify all remaining open items | Sunil Verma | 04 Jul 2025 |

---

## Risks Identified / Updated

| Risk ID | Description | Likelihood | Impact | Status / Update |
|---------|-------------|-----------|--------|-----------------|
| RSK-002 | Tapeout schedule — TMR voter fix (AI-024) and ENOB fix (AI-025) add ~2 weeks minimum; tapeout may slip from Week 28 to Week 30 | High | High | Escalated; Dr. Sharma to advise DRDO |
| RSK-006 | Gate-level simulation — DRC not yet clean; Tier 3 simulation start delayed | Medium | Medium | Linked to AI-026 |
| RSK-007 | ENOB failure at worst-case radiation corner — root cause identified; fix proposed but not yet verified | High | High | New; blocking tapeout |
| RSK-008 | TMR simultaneous dual-bit upset vulnerability — blocking tapeout finding from formal verification | High | High | New; DEC-014 issued |

---

## Next Meeting Objectives

Meeting 06 — Tapeout Readiness Review (target: Week 30, ~15 Jul 2025):
- Confirm DEC-014 and DEC-015 implementation and re-verification closure
- Confirm DRC/LVS clean
- Confirm 100% DMC coverage closure
- Present complete tapeout readiness checklist
- Approve or defer tapeout

---

## Meeting Conclusion

Dr. Sharma closed the meeting at 12:00 hrs. Two blocking tapeout issues have been identified (DEC-014 and DEC-015). These must be resolved before tapeout can be approved. Dr. Sharma will notify Col. Tiwari of the expected 2-week tapeout schedule slip. All action item owners confirmed understanding and urgency.

**Minutes prepared by:** Sanjay Bhatt, Project Controller
**Date of issue:** 18 June 2025
**Distribution:** All attendees, Col. V. K. Tiwari (DRDO), PDMS
