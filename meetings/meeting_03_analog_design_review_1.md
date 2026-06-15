# MINUTES OF MEETING

**Meeting ID:** MOM-RHADC-003
**Meeting Title:** Analog Design Review
**Date:** 22 April 2025
**Time:** 09:30 – 12:30 hrs
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
| Dr. Priya Menon | Radiation Hardening Specialist | Process Engineering |
| Deepak Rao | Digital Design Lead | Digital Design |
| Rohit Das | Systems Engineer | Systems Integration |
| Sanjay Bhatt | Project Controller | PMO |
| Lakshmi Srinivasan | Quality Assurance Manager | QA |

---

## Agenda

1. Review of action items from MOM-RHADC-002
2. SAR core design review — schematic and transistor level
3. Reference voltage generator and bandgap design review
4. Clock distribution design review
5. Power budget roll-up (per-block vs. 430 mW target)
6. EGR-3 layout compliance status
7. Risk review
8. AOB

---

## Discussion Points

**1. Action Item Review**
- AI-007: Complete. ISD v1.0 issued 12 Mar 2025, archived in PDMS.
- AI-008: Die area estimate complete. Estimated die area 14.2 mm² with EGR-3 overhead. Within reticle boundary (max 20 mm²). Confirmed by Anil Kapoor.
- AI-009: DSD v0.1 issued 01 Apr 2025. Comments under review; v1.0 target 30 Apr 2025.
- AI-010: DRDO response received. Col. Tiwari confirmed 450 mW is firm; spacecraft bus power allocation cannot be revised. Dr. Sharma acknowledged and directed team to maintain 430 mW internal target.
- AI-011: IUAC (heavy ion) slot confirmed Q3 2025 (08–12 Sep). TIFR (TID) slot confirmed Q2 2025 but tentative — backup slot in Q3. Cost approved.
- AI-012: TI-SAR behavioral model complete. Background calibration model developed by Vikram Joshi; integration with testbench ongoing.

**2. SAR Core Design Review**
Rajesh Nair presented the transistor-level schematic for the 16-bit SAR core. The design uses a split-capacitor DAC (top 8-bit + bottom 8-bit) with attenuation capacitor. Comparator is a dynamic latch with RHBD differential-pair reset topology per DEC-003 and DEC-008 rad-hard requirements.

Key concern raised by Vikram Joshi: comparator offset calibration range is currently ±8 mV. Simulation shows process corners (SS at –40°C) may produce offset as large as 12 mV, potentially exceeding calibration range. Rajesh Nair confirmed this has been observed and proposed increasing the calibration DAC range from 5-bit to 6-bit, adding one bit of headroom. This change increases comparator power by approximately 4 mW per channel (16 mW total for four channels).

The team discussed the impact on the power budget. After discussion, the 6-bit calibration DAC change was approved. Updated power estimate with this change: 438 mW nominal. Still within 450 mW requirement but only 12 mW above 430 mW internal target.

Dr. Menon confirmed the RHBD latch topology is compliant with EGR-3 layout rules for the dynamic nodes.

**3. Reference Voltage Generator**
Vikram Joshi presented the bandgap reference and LDO regulator design. The bandgap is a Widlar-type with curvature correction. Simulated TID sensitivity: bandgap output drift < 2 mV over 100 krad(Si), meeting the ≤ 5 mV stability requirement. The LDO uses a PMOS pass device with high-gain error amplifier.

One concern noted: the LDO error amplifier uses a minimum-length input differential pair, which is known to be more susceptible to threshold voltage shift under TID. Rajesh Nair directed Vikram Joshi to upsize the input pair to W/L = 40/2 (from current 20/1) to reduce sensitivity. This has no material impact on LDO bandwidth or power.

**4. Clock Distribution**
Deepak Rao presented the clock tree design. Phase skew between channels is targeted at < 1 ps after calibration. The clock buffer chain uses large-W/L devices (W/L = 80/0.5 effective) for TID robustness per DEC-003.

A concern was raised that the current clock distribution layout (not yet complete) may introduce systematic skew due to asymmetric routing length to channels 2 and 3. Deepak Rao agreed to review layout topology and implement H-tree clock routing to minimize systematic skew.

**5. Power Budget Roll-Up**

| Block | Estimated Power (mW) |
|-------|---------------------|
| SAR Core × 4 (with 6-bit cal DAC) | 182 |
| Reference Generator + LDO | 48 |
| Clock Distribution | 36 |
| DMC (Digital, incl. TMR) | 94 |
| Output Serializer (LVDS, incl. TMR) | 54 |
| Configuration Registers + I/O | 24 |
| **Total Estimated** | **438 mW** |

Dr. Sharma noted the 438 mW total is within the 450 mW requirement but only 8 mW above the 430 mW internal target after the 6-bit DAC change. He directed the team to identify at least 15 mW of additional power reduction opportunities before tapeout.

**6. EGR-3 Layout Compliance**
Layout is approximately 40% complete. No DRC violations in completed blocks. Rajesh Nair confirmed all completed analog cells are EGR-3 compliant. H-tree clock routing update required (AI from this meeting).

---

## Decisions Made

| Decision ID | Decision | Owner |
|-------------|----------|-------|
| DEC-009 | SAR comparator calibration DAC increased from 5-bit to 6-bit to accommodate ±12 mV worst-case offset; accepted power increase of 16 mW | Rajesh Nair |
| DEC-010 | LDO error amplifier input differential pair to be upsized to W/L = 40/2 to improve TID robustness | Vikram Joshi |
| DEC-011 | Clock tree routing to be redesigned as H-tree topology to minimise systematic inter-channel phase skew | Deepak Rao |

---

## Action Items

| AI ID | Action | Owner | Due Date |
|-------|--------|-------|----------|
| AI-013 | Update SAR comparator schematic with 6-bit calibration DAC; re-run corners simulation and confirm offset coverage | Vikram Joshi | 09 May 2025 |
| AI-014 | Upsize LDO input differential pair to W/L = 40/2; re-run TID simulation up to 100 krad; confirm bandgap drift < 5 mV | Vikram Joshi | 09 May 2025 |
| AI-015 | Redesign clock distribution as H-tree; provide updated layout and phase skew simulation | Deepak Rao | 16 May 2025 |
| AI-016 | Identify ≥ 15 mW additional power reduction opportunities in any block; present options at next review | Rajesh Nair | 09 May 2025 |
| AI-017 | Issue DSD v1.0 incorporating all design changes approved in this meeting | Rajesh Nair | 30 Apr 2025 |
| AI-018 | Complete EGR-3 layout for all analog blocks; run full-chip DRC and LVS; report results | Rajesh Nair | 30 May 2025 |

---

## Risks Identified / Updated

| Risk ID | Description | Likelihood | Impact | Status / Update |
|---------|-------------|-----------|--------|-----------------|
| RSK-001 | Power budget — total now 438 mW, only 12 mW headroom vs. 450 mW requirement; TID leakage could push over limit | Medium | High | Escalated; power reduction exercise mandated (AI-016) |
| RSK-004 | DMC background calibration verification complexity | Medium | Medium | Behavioral model in place; risk remains for corner coverage |
| RSK-005 | LDO minimum-length input pair TID susceptibility — identified this meeting; corrective action initiated (DEC-010) | Low (post-fix) | High | New |

---

## Next Meeting Objectives

Meeting 04 — Verification Planning Review (target: Week 16, ~06 May 2025):
- Present verification plan including block-level and full-chip testbench strategy
- Confirm coverage closure plan for DMC background calibration
- Review corner simulation requirements (PVT + radiation corners)
- Review DSD v1.0 completeness

---

## Meeting Conclusion

Dr. Sharma closed the meeting at 12:30 hrs. The design is progressing but the power budget remains a concern. DEC-009, DEC-010, and DEC-011 are all approved design changes requiring rework before layout freeze. All owners acknowledged action items.

**Minutes prepared by:** Sanjay Bhatt, Project Controller
**Date of issue:** 23 April 2025
**Distribution:** All attendees, Col. V. K. Tiwari (DRDO), PDMS
