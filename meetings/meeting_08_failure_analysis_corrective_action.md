# MINUTES OF MEETING

**Meeting ID:** MOM-RHADC-008
**Meeting Title:** Failure Analysis and Corrective Action Review
**Date:** 04 November 2025
**Time:** 09:30 – 13:00 hrs
**Location:** Conference Room B2, Building 7, GSRML
**Chairperson:** Dr. Arvind Sharma, Program Director

---

## Attendees

| Name | Role | Department |
|------|------|------------|
| Dr. Arvind Sharma | Program Director | PMO |
| Anil Kapoor | Fabrication Manager | Wafer Fab |
| Lakshmi Srinivasan | Quality Assurance Manager | QA |
| Rajesh Nair | Chief Design Engineer | Analog Design |
| Vikram Joshi | Senior Analog Designer | Analog Design |
| Deepak Rao | Digital Design Lead | Digital Design |
| Dr. Priya Menon | Radiation Hardening Specialist | Process Engineering |
| Sunil Verma | Lead Verification Engineer | Design Verification |
| Meena Iyer | Packaging and Reliability Lead | Packaging / QA |
| Sanjay Bhatt | Project Controller | PMO |
| Col. (Retd.) V. K. Tiwari | Customer Representative | DRDO |

---

## Agenda

1. Review of action items from MOM-RHADC-007
2. DMC-region failure analysis findings
3. ETCH-7 tool and rework process review
4. Temperature characterisation results
5. Post-irradiation (TIFR) characterisation results — ENOB margin closure
6. Corrective action proposal and decision
7. Production lot strategy
8. Risk review
9. AOB

---

## Discussion Points

**1. Action Item Review**
- AI-035: Complete. Failure analysis findings presented below.
- AI-036: Complete. ETCH-7 review findings presented below.
- AI-037: Complete. Temperature characterisation results presented below.
- AI-038: Complete. TIFR irradiation results presented below.
- AI-039: Deferred pending outcome of this meeting's decisions.

**2. DMC-Region Failure Analysis Findings**
Lakshmi Srinivasan presented failure analysis results on 14 failed die sampled from Wafer 2. Decapsulation and SEM/EDX analysis revealed micro-voiding at metal-1 contacts specifically within the DMC TMR voter input register cells — the same cells modified under DEC-014 (one-cycle pipeline delay registers with 50 µm physical spacing). The voiding pattern is consistent with incomplete contact fill during the rework thermal cycle following the ETCH-7 contact etch tool drift identified in Meeting 07.

Critically, Lakshmi Srinivasan noted that the additional physical spacing introduced by DEC-014 placed these specific register cells nearer to a reticle stitching boundary region that has historically shown marginally higher contact void incidence on the GS180H process, though within normal process limits under nominal conditions. Combined with the ETCH-7 drift during the rework cycle, contact integrity in this specific region was compromised.

Dr. Menon stated this is an unintended interaction: the SEU mitigation spacing change (DEC-014), while electrically sound, placed sensitive cells in a layout region with a known (if historically minor) process sensitivity, and this sensitivity was significantly amplified by the unrelated tool drift.

**3. ETCH-7 Tool and Rework Process Review**
Anil Kapoor confirmed the ETCH-7 recalibration on 18 September (performed prior to the Wafer 2 rework cycle) used an updated etch recipe parameter set that had not been fully qualified against the contact module process of record. This is a process control gap. Anil Kapoor took ownership of this finding and confirmed corrective action has already been initiated at the fab: all tool recalibrations must now pass a qualification lot check before being released for production use.

**4. Temperature Characterisation Results**
Vikram Joshi presented results from temperature-chamber testing on functional die from all three wafers (sample size: 45 die, 15 per wafer):

| Parameter | –40°C | +27°C | +85°C | Requirement |
|-----------|-------|-------|-------|-------------|
| ENOB | 14.29 bits | 14.36 bits | 14.21 bits | ≥ 14.2 bits |
| SNR | 87.6 dBFS | 88.3 dBFS | 87.1 dBFS | ≥ 87 dBFS |
| Power | 431 mW | 421 mW | 428 mW | ≤ 450 mW |

All temperature corners pass, including +85°C which shows the tightest margin (0.01 bits SNR margin above requirement... actually within spec at 0.1 dBFS). Vikram Joshi noted +85°C is the tightest corner for SNR and recommended continued monitoring during reliability qualification.

**5. Post-Irradiation Characterisation Results (TIFR)**
Dr. Menon presented results from the TIFR TID irradiation campaign (20–24 Oct 2025), 10 die irradiated to 100 krad(Si) and electrically tested at –40°C per ATP v0.1 (per DEC-017 mandatory test):

| Parameter | Result (post-100 krad, –40°C) | Requirement | Status |
|-----------|-------------------------------|--------------|--------|
| ENOB | 14.27 bits (mean), 14.19 bits (worst die) | ≥ 14.2 bits | **1 of 10 die marginally below spec** |
| SNR | 87.3 dBFS (mean), 86.8 dBFS (worst die) | ≥ 87 dBFS | **1 of 10 die fails** |

Nine of ten die pass both criteria with reasonable margin, consistent with the DEC-015 simulation prediction of 14.24 bits / 87.2 dBFS. One die (Wafer 3, die location near wafer edge) failed both criteria narrowly. Dr. Menon stated this is consistent with normal silicon variation around a simulated margin that was already known to be slim (RSK-007), rather than a systematic design issue — but the failure rate (1/10) is a concern for production yield of mission-critical parts.

Sunil Verma noted this confirms RSK-007 was a valid concern; the slim simulated margin (0.04 bits) translates to real measurable yield loss at the worst-case corner on actual silicon.

**6. Corrective Action Proposal and Decision**
Two separate corrective actions were discussed:

*Corrective Action 1 — Contact/Process Issue (DMC region voiding):*
Anil Kapoor proposed reverting the TMR voter input register physical placement (from DEC-014) to avoid the reticle stitching-sensitive region, while retaining the 50 µm spacing requirement by routing the registers in a different orientation. This requires a layout-only ECO (no schematic change) and re-verification of timing and DRC/LVS. Dr. Menon confirmed this does not compromise the SEU mitigation intent of DEC-014.

This was discussed at length. Dr. Sharma asked whether DEC-014 itself should be reconsidered. Dr. Menon clarified that the SEU mitigation approach (pipeline registers with spacing) remains correct and necessary; only the specific physical placement needs to change. The team agreed to proceed with a placement-only ECO rather than reversing DEC-014's underlying approach.

*Corrective Action 2 — ENOB Margin at Worst-Case Corner:*
Rajesh Nair proposed a further refinement to the SAR comparator regeneration timing, building on DEC-015, to add an additional 5% timing margin specifically targeting the post-irradiation cold corner. He cautioned this is a more conservative change than DEC-015 and will require a full re-verification cycle similar to that performed after Meeting 05. Given that 9 of 10 die already pass, Col. Tiwari asked whether this is strictly necessary or whether production screening could be used instead.

After discussion, Dr. Sharma decided that, given this is a radiation-hardened device for a mission-critical satellite payload, the program will pursue the additional timing margin fix rather than rely on screening alone. This represents a revision of the position taken in Meeting 06 (DEC-016/017) where post-irradiation ENOB was treated as a validation item rather than requiring further design change; the new silicon data necessitates a design correction.

---

## Decisions Made

| Decision ID | Decision | Owner |
|-------------|----------|-------|
| DEC-020 | Layout-only ECO approved to relocate TMR voter input register cells away from reticle stitching-sensitive region, retaining 50 µm spacing per DEC-014; full DRC/LVS and timing re-verification required | Rajesh Nair / Deepak Rao |
| DEC-021 | **Reversal of implicit Meeting 06 position:** Additional 5% SAR regeneration timing margin (beyond DEC-015) approved to address measured post-irradiation ENOB/SNR shortfall at worst-case corner; full re-verification cycle required before next tapeout revision | Rajesh Nair / Vikram Joshi |
| DEC-022 | Fab tool recalibration qualification gate (qualification lot check) formally adopted as mandatory process control for all etch tools | Anil Kapoor |

---

## Action Items

| AI ID | Action | Owner | Due Date |
|-------|--------|-------|----------|
| AI-040 | Implement layout ECO relocating TMR voter input registers per DEC-020; re-run full-chip DRC/LVS and timing analysis | Deepak Rao | 25 Nov 2025 |
| AI-041 | Implement additional 5% SAR regeneration timing margin per DEC-021; re-run full corner simulation matrix, with emphasis on SS/–40°C/100 krad | Rajesh Nair / Vikram Joshi | 09 Dec 2025 |
| AI-042 | Re-run formal verification on relocated TMR voter logic to reconfirm all 22 properties | Deepak Rao | 25 Nov 2025 |
| AI-043 | Document ETCH-7 qualification gate procedure formally in fab process control documentation | Anil Kapoor | 18 Nov 2025 |
| AI-044 | Prepare revised tapeout package (GDS-II Rev R05) incorporating DEC-020 and DEC-021 changes for production lot | Rajesh Nair | 16 Dec 2025 |
| AI-045 | Quarantine remaining Wafer 2 die pending disposition; exclude from any qualification or flight-candidate population | Lakshmi Srinivasan | 11 Nov 2025 |

---

## Risks Identified / Updated

| Risk ID | Description | Likelihood | Impact | Status / Update |
|---------|-------------|-----------|--------|-----------------|
| RSK-007 | ENOB margin at worst-case radiation corner — confirmed as real silicon issue (1/10 die failed); corrective action now in progress (DEC-021) | High | High | Escalated; design correction underway |
| RSK-010 | Tool recalibration process control gap — root cause of Wafer 2 yield/voiding issue confirmed; corrective action adopted (DEC-022) | Low (post-fix) | High | Mitigated |
| RSK-011 | Revised tapeout (R05) introduces new schedule risk; production lot start will slip pending re-verification of DEC-020 and DEC-021 | High | High | New — Sanjay Bhatt owner |

---

## Next Meeting Objectives

Meeting 09 — Packaging and Reliability Review (target: ~late January 2026):
- Confirm R05 re-verification closure (AI-040 through AI-042)
- Review packaging qualification status for CQFP-80
- Review reliability qualification test plan and any failures
- Confirm production lot readiness

---

## Meeting Conclusion

Dr. Sharma closed the meeting at 13:00 hrs. This was a significant review: it confirmed a real silicon issue at the worst-case radiation corner (RSK-007) and identified a process control gap that caused the Wafer 2 yield anomaly. Both have approved corrective actions. The program schedule will be revised to reflect the R05 re-verification cycle. Col. Tiwari acknowledged the decisions and requested visibility into the revised schedule.

**Minutes prepared by:** Sanjay Bhatt, Project Controller
**Date of issue:** 05 November 2025
**Distribution:** All attendees, Col. V. K. Tiwari (DRDO), PDMS
