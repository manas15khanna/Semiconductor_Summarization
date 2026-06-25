# MINUTES OF MEETING

**Meeting ID:** MOM-RHADC-009
**Meeting Title:** Packaging and Reliability Review
**Date:** 29 January 2026
**Time:** 09:30 – 13:00 hrs
**Location:** Conference Room B2, Building 7, GSRML
**Chairperson:** Dr. Arvind Sharma, Program Director

---

## Attendees

| Name | Role | Department |
|------|------|------------|
| Dr. Arvind Sharma | Program Director | PMO |
| Meena Iyer | Packaging and Reliability Lead | Packaging / QA |
| Anil Kapoor | Fabrication Manager | Wafer Fab |
| Rajesh Nair | Chief Design Engineer | Analog Design |
| Deepak Rao | Digital Design Lead | Digital Design |
| Sunil Verma | Lead Verification Engineer | Design Verification |
| Dr. Priya Menon | Radiation Hardening Specialist | Process Engineering |
| Lakshmi Srinivasan | Quality Assurance Manager | QA |
| Sanjay Bhatt | Project Controller | PMO |
| Col. (Retd.) V. K. Tiwari | Customer Representative | DRDO |

---

## Agenda

1. Review of action items from MOM-RHADC-008
2. R05 re-verification closure confirmation
3. Production lot fabrication and yield summary (Lot GS180H-PL-01)
4. Packaging assembly and CQFP-80 qualification status
5. Reliability qualification test results
6. Thermal stress / packaging failure review
7. Risk review
8. AOB

---

## Discussion Points

**1. Action Item Review**
- AI-040: Complete. TMR voter input register layout ECO implemented and DRC/LVS clean.
- AI-041: Complete. Additional 5% regeneration timing margin implemented; results below.
- AI-042: Complete. Formal verification re-run, 22/22 properties proven on relocated registers.
- AI-043: Complete. ETCH-7 qualification gate procedure documented and adopted fab-wide.
- AI-044: Complete. GDS-II Rev R05 tapeout package issued 15 Dec 2025; production lot wafer start 18 Dec 2025.
- AI-045: Complete. Remaining Wafer 2 die quarantined and excluded from flight-candidate population.

**2. R05 Re-Verification Closure**
Rajesh Nair confirmed full corner simulation matrix re-run with the additional 5% timing margin. Worst-case corner (SS/–40°C/100 krad) now shows simulated ENOB = 14.33 bits and SNR = 87.9 dBFS, a meaningfully improved margin compared to the DEC-015 result (14.24 bits / 87.2 dBFS). Sunil Verma confirmed this margin improvement directly addresses the silicon shortfall identified in Meeting 08.

**3. Production Lot Fabrication and Yield Summary**
Anil Kapoor reported production Lot GS180H-PL-01 (10 wafers, R05 design) completed fabrication on 12 January 2026, on schedule. No process excursions occurred; the ETCH-7 qualification gate (DEC-022) was exercised twice during the lot run with no anomalies. Overall lot yield: 91.7% functional die — a marked improvement over the engineering lot's 86.4%, and no spatial clustering of failures was observed on any wafer.

**4. Packaging Assembly and CQFP-80 Qualification Status**
Meena Iyer presented packaging status. 120 functional die from Lot PL-01 have been assembled into CQFP-80 ceramic packages at the GSRML packaging facility. Die attach uses gold-silicon eutectic; wire bonds are gold ball bonds, 1 mil diameter, per the qualified assembly process.

Initial packaged-unit electrical test (post-assembly) on the first 40 units: 39/40 pass functional and parametric test. One unit failed open-circuit on one LVDS output pin, attributed to a wire bond lift during assembly, not a die-level issue — isolated to assembly handling and not considered systemic.

**5. Reliability Qualification Test Results**
Meena Iyer presented reliability qualification results per MIL-STD-883 methodology, performed on 60 packaged units:

| Test | Sample Size | Result | Status |
|------|-------------|--------|--------|
| Temperature cycling (–55°C to +125°C, 500 cycles) | 20 | 20/20 pass | PASS |
| High-temperature storage life (150°C, 1000 hrs) | 15 | 15/15 pass | PASS |
| Constant acceleration (20,000g, Y1 axis) | 10 | 10/10 pass | PASS |
| Hermeticity (fine and gross leak) | 60 | 60/60 pass | PASS |
| **Thermal shock (–65°C to +150°C, 100 cycles)** | 15 | **12/15 pass, 3 fail** | **FAIL** |

The thermal shock failures are significant. Meena Iyer reported that all three failed units exhibited die-attach delamination, identified via scanning acoustic microscopy (SAM) imaging, localized to the corner regions of the die. Cross-sectioning confirmed partial voiding in the gold-silicon eutectic die-attach layer.

Meena Iyer noted this thermal stress failure mode is consistent with a known sensitivity of the eutectic die-attach process to die size combined with the package cavity dimensions — the RHADC die at 14.2 mm² (per the EGR-3 layout area established at Meeting 03 / AI-008) is near the upper end of the qualified range for the current CQFP-80 cavity and die-attach process recipe, and thermal cycling between –65°C and +150°C generates higher shear stress at the die corners than the previously qualified, smaller reference die used to originally qualify this package/process combination.

Dr. Sharma noted this connects back to DEC-002 (CQFP-80 ceramic package selected as baseline at Meeting 01) and the area growth from EGR-3 rad-hard layout rules (flagged as a concern by Anil Kapoor in Meeting 02). The combination of the larger-than-typical die and the existing die-attach process has not previously been stress-qualified together at this severity.

**6. Thermal Stress / Packaging Corrective Action Discussion**
Meena Iyer proposed two potential corrective actions: (a) modify the die-attach process to use a softer, more compliant epoxy die-attach material in place of gold-silicon eutectic, which would reduce thermal shear stress but requires re-qualification of thermal conductivity and reliability characteristics; or (b) introduce a stress-relief die-attach pattern (partial eutectic dot-attach instead of full-area attach) to reduce stress concentration while retaining eutectic attach.

Dr. Menon raised a concern about option (a): epoxy die-attach typically has lower thermal conductivity, which could affect junction temperature under the 425 mW operating power established through the program (per power budget decisions from Meetings 02, 03, and 05). She recommended thermal simulation be performed before committing to either option.

After discussion, the team agreed to pursue the dot-attach pattern modification (option b) as the primary path, since it retains the eutectic material's thermal conductivity advantage, with epoxy die-attach retained as a fallback if dot-attach does not resolve the issue.

Col. Tiwari asked about schedule impact. Dr. Sharma confirmed this will require a focused re-qualification cycle on thermal shock only, not a full reliability re-qualification, since all other tests passed.

---

## Decisions Made

| Decision ID | Decision | Owner |
|-------------|----------|-------|
| DEC-023 | R05 design (DEC-020 + DEC-021 corrective actions) confirmed verified and is the production baseline; Lot GS180H-PL-01 confirmed as the production-representative lot | Rajesh Nair |
| DEC-024 | Die-attach process to be modified to a dot-attach (partial-area eutectic) pattern to address thermal shock die-attach delamination; epoxy die-attach retained as documented fallback option | Meena Iyer |
| DEC-025 | Thermal shock qualification (only) to be repeated on units assembled with the revised dot-attach process; full reliability test suite not required to be repeated given all other tests passed | Meena Iyer / Lakshmi Srinivasan |

---

## Action Items

| AI ID | Action | Owner | Due Date |
|-------|--------|-------|----------|
| AI-046 | Perform thermal simulation comparing dot-attach vs. full eutectic vs. epoxy die-attach junction temperature at 425 mW operating power | Dr. Menon | 12 Feb 2026 |
| AI-047 | Qualify dot-attach die-attach process; assemble 15 units for thermal shock re-test | Meena Iyer | 26 Feb 2026 |
| AI-048 | Repeat thermal shock qualification (–65°C to +150°C, 100 cycles) on dot-attach units; report results | Meena Iyer | 19 Mar 2026 |
| AI-049 | Investigate and disposition the single wire-bond-lift failure from initial packaged-unit test; confirm isolated assembly issue, not systemic | Meena Iyer | 12 Feb 2026 |
| AI-050 | Update reliability qualification report (RQR v0.4) reflecting all test results and the pending thermal shock re-qualification | Lakshmi Srinivasan | 26 Feb 2026 |

---

## Risks Identified / Updated

| Risk ID | Description | Likelihood | Impact | Status / Update |
|---------|-------------|-----------|--------|-----------------|
| RSK-007 | ENOB margin at worst-case radiation corner | Low (post R05 fix) | High | Substantially mitigated; closed pending PRR confirmation |
| RSK-011 | Schedule — R05 re-verification cycle completed; production lot delivered on schedule | Low | Medium | Reduced |
| RSK-012 | Thermal shock die-attach delamination — packaging qualification failure linked to die size / package cavity interaction; corrective action in progress | Medium | High | New — Meena Iyer owner; blocking PRR |

---

## Next Meeting Objectives

Meeting 10 — Production Readiness Review (target: ~late March 2026):
- Confirm thermal shock re-qualification results (AI-048) — must pass before production release
- Confirm full reliability qualification report closure
- Final review of all open risks across the program
- Formal production release decision

---

## Meeting Conclusion

Dr. Sharma closed the meeting at 13:00 hrs. The program has made strong progress: the ENOB margin issue is substantially resolved and production yield has improved significantly. However, the thermal shock packaging failure (RSK-012) is now a blocking item for production release and must be closed before the Production Readiness Review. Col. Tiwari noted DRDO's expectation that this be resolved without further schedule slippage where possible.

**Minutes prepared by:** Sanjay Bhatt, Project Controller
**Date of issue:** 30 January 2026
**Distribution:** All attendees, Col. V. K. Tiwari (DRDO), PDMS
