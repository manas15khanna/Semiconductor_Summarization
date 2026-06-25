# MINUTES OF MEETING

**Meeting ID:** MOM-RHADC-007
**Meeting Title:** Fabrication and Yield Review
**Date:** 30 September 2025
**Time:** 09:30 – 12:30 hrs
**Location:** Conference Room B2, Building 7, GSRML
**Chairperson:** Dr. Arvind Sharma, Program Director

---

## Attendees

| Name | Role | Department |
|------|------|------------|
| Dr. Arvind Sharma | Program Director | PMO |
| Anil Kapoor | Fabrication Manager | Wafer Fab |
| Rajesh Nair | Chief Design Engineer | Analog Design |
| Vikram Joshi | Senior Analog Designer | Analog Design |
| Sunil Verma | Lead Verification Engineer | Design Verification |
| Dr. Priya Menon | Radiation Hardening Specialist | Process Engineering |
| Meena Iyer | Packaging and Reliability Lead | Packaging / QA |
| Lakshmi Srinivasan | Quality Assurance Manager | QA |
| Sanjay Bhatt | Project Controller | PMO |

---

## Agenda

1. Review of action items from MOM-RHADC-006
2. Engineering lot fabrication summary
3. Inline process monitor and parametric data review
4. Wafer-level electrical test results
5. Yield analysis
6. Silicon vs. simulation comparison (ENOB margin risk, RSK-007)
7. Risk review
8. AOB

---

## Discussion Points

**1. Action Item Review**
- AI-029: Complete. Tapeout package delivered 17 Jul 2025.
- AI-030: Complete. Tapeout release note issued, ENOB margin risk documented.
- AI-031: Complete. ATP v0.1 issued including mandatory post-irradiation ENOB test.
- AI-032: Complete. Weekly fab progress reports established; wafer start confirmed 21 Jul 2025.
- AI-033: Complete. Package drawings finalised; CQFP-80 ceramic body inventory confirmed at 250 units.
- AI-034: Complete. TIFR irradiation slot booked for 20–24 Oct 2025.

**2. Engineering Lot Fabrication Summary**
Anil Kapoor reported the engineering lot (3 wafers, Lot GS180H-EL-01) completed fabrication on 24 September 2025, three days later than the 22 September target due to a rework cycle on Wafer 2 following a metal-1 contact resistance excursion detected at inline metrology (Week 5 of processing). The excursion was traced to a contact etch tool drift on Tool ETCH-7; the tool was recalibrated and Wafer 2 was reworked successfully. Wafers 1 and 3 were unaffected.

**3. Inline Process Monitor and Parametric Data**
Anil Kapoor presented inline PCM (process control monitor) data:
- Poly sheet resistance: within spec on all three wafers
- NMOS/PMOS Vt: within spec, slight shift (+15 mV NMOS) on Wafer 2 attributed to the rework thermal cycle — flagged for monitoring
- Metal-1 contact resistance: Wafer 2 recovered to within spec post-rework; Wafers 1 and 3 nominal
- Oxide thickness uniformity: within spec all wafers

Dr. Menon noted the +15 mV Vt shift on Wafer 2 is within the process window but recommended that Wafer 2 die be tracked separately during electrical test to assess any correlation with the ENOB margin risk (RSK-007).

**4. Wafer-Level Electrical Test Results**
Rajesh Nair presented wafer-level (probe) test results across all three wafers, 2,184 total die sites (728 per wafer):

| Parameter | Result Summary |
|-----------|-----------------|
| DC functional test (power-on, register read/write) | 91.3% pass |
| ENOB (room temp, pre-rad, functional die only) | Mean 14.38 bits, σ = 0.09 bits |
| SNR (room temp, pre-rad) | Mean 88.4 dBFS |
| Power consumption (room temp, nominal) | Mean 419 mW |
| LVDS output timing | 96.8% pass (of functional die) |

Initial silicon results at room temperature, pre-radiation, are consistent with simulation predictions. Rajesh Nair noted this is encouraging but does not yet validate the worst-case corner margin (RSK-007), which requires temperature and post-irradiation testing.

**5. Yield Analysis**
Lakshmi Srinivasan presented the overall yield breakdown:

| Wafer | Gross Die | Functional Die | Yield |
|-------|-----------|-----------------|-------|
| Wafer 1 | 728 | 681 | 93.5% |
| Wafer 2 (reworked) | 728 | 512 | **70.3%** |
| Wafer 3 | 728 | 693 | 95.2% |
| **Lot Total** | **2,184** | **1,886** | **86.4%** |

Wafer 2 yield is significantly lower than Wafers 1 and 3. Failure bin analysis shows the majority of Wafer 2 failures are concentrated in the DMC digital block region, with a higher incidence of functional test failures (register read/write errors) compared to Wafers 1 and 3. Lakshmi Srinivasan noted this correlates spatially with die located near the wafer edge, suggesting possible process non-uniformity introduced during the rework cycle.

Anil Kapoor stated that a 70% yield on a reworked wafer is not unusual but the spatial clustering and DMC-region correlation warrants investigation before committing to a production lot strategy. He recommended this be escalated for root cause analysis.

Dr. Sharma agreed and noted this lower-than-expected yield on Wafer 2, combined with the DMC-region failure clustering, should be treated as a distinct concern from the general engineering lot results, to be investigated via failure analysis.

**6. Silicon vs. Simulation — ENOB Margin Risk (RSK-007)**
Sunil Verma noted that room-temperature pre-radiation ENOB (mean 14.38 bits) is comfortably above the 14.2-bit requirement, but this does not exercise the worst-case SS/–40°C/100 krad corner that showed only a 0.04-bit margin in simulation (per DEC-015 and RSK-007). Full corner validation requires temperature chamber testing and post-irradiation testing at TIFR (20–24 Oct 2025, per AI-034). This remains an open risk until that data is available.

---

## Decisions Made

| Decision ID | Decision | Owner |
|-------------|----------|-------|
| DEC-018 | Wafer 2 DMC-region yield failures to be formally investigated via failure analysis prior to any production lot decision | Anil Kapoor / Lakshmi Srinivasan |
| DEC-019 | Die from all three wafers to proceed to temperature and radiation characterisation testing; Wafer 2 functional die to be tracked and reported separately given the Vt shift and yield anomaly | Rajesh Nair |

---

## Action Items

| AI ID | Action | Owner | Due Date |
|-------|--------|-------|----------|
| AI-035 | Perform failure analysis on a sample of failed DMC-region die from Wafer 2; determine root cause of clustered functional failures | Lakshmi Srinivasan | 21 Oct 2025 |
| AI-036 | Review ETCH-7 tool recalibration records and rework process recipe for potential contribution to Wafer 2 yield loss | Anil Kapoor | 14 Oct 2025 |
| AI-037 | Conduct temperature-chamber electrical test (–40°C, +27°C, +85°C) on sample of functional die from all three wafers; report ENOB, SNR, power vs. temperature | Rajesh Nair / Vikram Joshi | 17 Oct 2025 |
| AI-038 | Execute TIFR TID irradiation characterisation per AI-034 booking; report post-irradiation ENOB and SNR | Dr. Menon | 28 Oct 2025 |
| AI-039 | Prepare production lot sizing recommendation contingent on failure analysis outcome (AI-035) | Anil Kapoor | 28 Oct 2025 |

---

## Risks Identified / Updated

| Risk ID | Description | Likelihood | Impact | Status / Update |
|---------|-------------|-----------|--------|-----------------|
| RSK-007 | ENOB margin at worst-case radiation corner — not yet validated on silicon; pending AI-037/AI-038 | Medium | High | Open |
| RSK-009 | First silicon yield — overall lot yield 86.4% acceptable, but Wafer 2 at 70.3% with DMC-region clustering is a concern | Medium | High | Escalated; DEC-018 issued |
| RSK-010 | Possible process excursion from ETCH-7 contact etch tool drift may recur in future lots if root cause not resolved before production lot start | Medium | High | New — Anil Kapoor owner |

---

## Next Meeting Objectives

Meeting 08 — Failure Analysis and Corrective Action Review (target: ~04 Nov 2025):
- Present DMC-region failure analysis root cause (AI-035)
- Present temperature and post-irradiation characterisation results (AI-037, AI-038)
- Confirm or revise ENOB margin risk status (RSK-007)
- Propose corrective action for yield/process issue
- Reassess production lot strategy

---

## Meeting Conclusion

Dr. Sharma closed the meeting at 12:30 hrs. While overall lot yield and pre-radiation electrical results are encouraging, the Wafer 2 anomaly and outstanding worst-case corner validation mean the program cannot yet confirm full silicon success. Failure analysis and characterisation testing are now critical path.

**Minutes prepared by:** Sanjay Bhatt, Project Controller
**Date of issue:** 01 October 2025
**Distribution:** All attendees, Col. V. K. Tiwari (DRDO), PDMS
