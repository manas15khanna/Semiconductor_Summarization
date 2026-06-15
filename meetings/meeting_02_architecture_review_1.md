# MINUTES OF MEETING

**Meeting ID:** MOM-RHADC-002
**Meeting Title:** Architecture Review
**Date:** 25 February 2025
**Time:** 10:00 – 13:00 hrs
**Location:** Conference Room B2, Building 7, GSRML
**Chairperson:** Dr. Arvind Sharma, Program Director

---

## Attendees

| Name | Role | Department |
|------|------|------------|
| Dr. Arvind Sharma | Program Director | PMO |
| Rajesh Nair | Chief Design Engineer | Analog Design |
| Sunil Verma | Lead Verification Engineer | Design Verification |
| Dr. Priya Menon | Radiation Hardening Specialist | Process Engineering |
| Anil Kapoor | Fabrication Manager | Wafer Fab |
| Meena Iyer | Packaging and Reliability Lead | Packaging / QA |
| Rohit Das | Systems Engineer | Systems Integration |
| Vikram Joshi | Senior Analog Designer | Analog Design |
| Sanjay Bhatt | Project Controller | PMO |
| Deepak Rao | Digital Design Lead | Digital Design |

*Note: Col. Tiwari (DRDO) not present; apologies received.*

---

## Agenda

1. Review of action items from MOM-RHADC-001
2. Power feasibility study results (AI-001)
3. ADC architecture trade-off presentation
4. Radiation hardening strategy per block
5. Top-level block diagram and interface definition
6. Risk review update
7. AOB

---

## Discussion Points

**1. Action Item Review**
- AI-001: Complete. Power feasibility study presented by Rajesh Nair (see item 2 below).
- AI-002: Complete. EGR-3 layout kit v4.2 confirmed available. DRC deck version GS180H-DRC-22 is current.
- AI-003: Complete. HR request submitted; new verification engineer (Kavya Reddy) joining 03 March 2025.
- AI-004: Level 3 schedule circulated 30 Jan. Minor comments received; updated version issued 10 Feb.
- AI-005: Complete. Signed requirements document archived as PDMS-RHADC-REQ-001.
- AI-006: Complete. TIFR Mumbai (TID) and IUAC New Delhi (heavy ion SEE) identified as candidate facilities. Provisional booking slots obtained for Q3 2025. Formal cost estimate pending facility confirmation.

**2. Power Feasibility Study (AI-001)**
Rajesh Nair presented the power feasibility analysis. A 4-stage pipeline architecture operating at 250 MSPS on GS180H was estimated at 510–540 mW worst-case, exceeding the 450 mW target by 13–20%. A 4-channel time-interleaved SAR (TI-SAR) architecture operating individual channels at 62.5 MSPS was estimated at 420–470 mW. The TI-SAR approach meets the budget at nominal conditions but leaves limited headroom.

Vikram Joshi noted that radiation-induced leakage current at end-of-life TID (100 krad) typically increases analog block quiescent current by 8–15% on GS180H. This pushes the TI-SAR worst-case power estimate to 455–540 mW. The pipeline architecture is not viable within the power budget.

Rajesh Nair recommended proceeding with the 4-channel TI-SAR architecture with aggressive power optimization in the reference voltage generator and clock distribution. Dr. Menon concurred. Rohit Das asked whether the 450 mW requirement could be revisited with DRDO; Dr. Sharma agreed to raise it with Col. Tiwari but directed the team to design to 430 mW target internally to maintain margin.

**3. Architecture Selection**
The 4-channel time-interleaved SAR ADC architecture was reviewed in detail. Key partitioning:
- 4× 16-bit SAR core channels, each at 62.5 MSPS
- Shared reference voltage generator (bandgap + low-noise LDO)
- Clock distribution tree with skew calibration logic
- Digital error correction and channel mismatch calibration block (DMC)
- TMR applied to: DMC, clock control, output serializer, configuration registers
- Synchronous LVDS output interface

Deepak Rao raised a concern about the DMC block complexity. Achieving 16-bit channel mismatch correction with TMR overhead within the power budget will require careful architecture. He proposed a background calibration approach running at reduced update rate during normal operation.

The team agreed this is a valid approach but noted it introduces verification complexity. Sunil Verma flagged that behavioral model coverage for background calibration convergence will need dedicated effort.

**4. Radiation Hardening Strategy**
Dr. Menon presented the per-block rad-hard strategy:
- All analog blocks: EGR-3 guard ring layout, enclosed NMOS transistors
- SAR comparator: RHBD latch topology with differential-pair reset
- Reference generator: Dedicated substrate isolation, EGR-3
- Clock tree: TMR on control registers; analog clock buffers use large-W/L devices to reduce threshold shift sensitivity
- DMC (digital): Full TMR with voter logic
- Output serializer: TMR
- I/O pads: Rad-hard I/O cell library (GSRML-IO-RH-v2)

Anil Kapoor noted that the EGR-3 layout rules increase area by approximately 25% relative to a standard GS180H layout. He flagged that die area must be estimated carefully to avoid reticle boundary issues.

**5. Interface Definition**
Rohit Das confirmed the output interface: LVDS serial at 2× output rate, JESD204B compatible. Power supply sequencing requirement to be defined in the design specification document (DSD).

---

## Decisions Made

| Decision ID | Decision | Owner |
|-------------|----------|-------|
| DEC-005 | 4-channel time-interleaved SAR ADC architecture selected as the program baseline | Dr. Sharma |
| DEC-006 | Internal design power target set to 430 mW (20 mW margin against 450 mW requirement); Dr. Sharma to raise possible 450 mW relaxation with DRDO | Rajesh Nair / Dr. Sharma |
| DEC-007 | Background calibration approach adopted for channel mismatch correction (DMC block) | Deepak Rao |
| DEC-008 | TMR mandatory for DMC, clock control registers, output serializer, and configuration registers | Dr. Menon / Deepak Rao |

---

## Action Items

| AI ID | Action | Owner | Due Date |
|-------|--------|-------|----------|
| AI-007 | Issue top-level block diagram and interface specification document (ISD v1.0) | Rohit Das | 14 Mar 2025 |
| AI-008 | Complete preliminary die area estimate including EGR-3 overhead; confirm within reticle boundary | Rajesh Nair | 14 Mar 2025 |
| AI-009 | Draft Design Specification Document (DSD v0.1) covering SAR core, reference, clock, DMC, and I/O | Rajesh Nair + Deepak Rao | 04 Apr 2025 |
| AI-010 | Contact DRDO (Col. Tiwari) regarding possible revision of 450 mW power requirement; document response | Dr. Sharma | 07 Mar 2025 |
| AI-011 | Confirm IUAC and TIFR test slot bookings; obtain cost approval from finance | Dr. Menon | 21 Mar 2025 |
| AI-012 | Prepare behavioral model for TI-SAR including background calibration for use in system-level verification | Sunil Verma / Vikram Joshi | 28 Mar 2025 |

---

## Risks Identified / Updated

| Risk ID | Description | Likelihood | Impact | Status / Update |
|---------|-------------|-----------|--------|-----------------|
| RSK-001 | Power budget exceedance — TI-SAR architecture narrows gap but end-of-life TID leakage remains a concern | Medium | High | Updated; under active monitoring |
| RSK-002 | Schedule risk from aggressive qualification timeline | Medium | High | No change |
| RSK-003 | Radiation test facility availability | Medium | Medium | Provisional slots obtained; risk reduced |
| RSK-004 | DMC background calibration complexity may introduce verification gaps and schedule risk | Medium | Medium | New — Sunil Verma owner |

---

## Next Meeting Objectives

Meeting 03 — Analog Design Review (target: Week 14, ~22 Apr 2025):
- Review SAR core schematic and transistor-level design
- Review reference voltage generator and clock distribution design
- Confirm power budget allocation per block against 430 mW internal target
- Review EGR-3 layout compliance status
- Confirm DSD v1.0 issued

---

## Meeting Conclusion

Dr. Sharma closed the meeting at 13:00 hrs. Architecture selection (DEC-005) is the key decision of this review and is now baselined. All action items acknowledged by owners. Minutes to be circulated within 48 hours.

**Minutes prepared by:** Sanjay Bhatt, Project Controller
**Date of issue:** 26 February 2025
**Distribution:** All attendees, Col. V. K. Tiwari (DRDO), PDMS
