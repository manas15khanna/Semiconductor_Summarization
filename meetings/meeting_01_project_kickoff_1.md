# MINUTES OF MEETING

**Meeting ID:** MOM-RHADC-001
**Meeting Title:** Project Kickoff and Requirements Review
**Date:** 14 January 2025
**Time:** 09:00 – 11:30 hrs
**Location:** Conference Room B2, Building 7, Government Semiconductor Research and Manufacturing Laboratory (GSRML)
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
| Col. (Retd.) V. K. Tiwari | Customer Representative | DRDO Satellite Program Office |
| Sanjay Bhatt | Project Controller | PMO |
| Lakshmi Srinivasan | Quality Assurance Manager | QA |

---

## Agenda

1. Program overview and objectives
2. Customer requirements walkthrough (DRDO-SAT-ADC-REQ-v2.1)
3. Preliminary schedule and milestone review
4. Resource allocation and team structure
5. Risk identification — initial pass
6. Action item assignment
7. AOB

---

## Discussion Points

**1. Program Overview**
Dr. Sharma opened the meeting and introduced the program. The Radiation Hardened Satellite ADC Development Program (RHADC) is a government-funded effort to design, fabricate, qualify, and deliver a 16-bit, 250 MSPS analog-to-digital converter suitable for deployment in low Earth orbit (LEO) and medium Earth orbit (MEO) satellite payloads. The device must meet MILSPEC radiation tolerance thresholds and is targeted at payload signal processing applications.

**2. Requirements Walkthrough**
Col. Tiwari presented the customer requirements document DRDO-SAT-ADC-REQ-v2.1. Key performance targets:
- Resolution: 16-bit
- Sample rate: 250 MSPS
- ENOB: ≥ 14.2 bits at Nyquist
- SNR: ≥ 87 dBFS
- Power consumption: ≤ 450 mW total (analog + digital)
- Supply voltage: 1.8 V analog, 1.2 V digital
- Total Ionizing Dose (TID) tolerance: ≥ 100 krad(Si)
- Single Event Latchup (SEL) immunity: LET threshold ≥ 60 MeV·cm²/mg
- Single Event Upset (SEU) rate: ≤ 1 × 10⁻⁷ upsets/bit/day at GEO
- Operating temperature: –40°C to +85°C
- Package: Ceramic quad flat pack (CQFP-80)

Rohit Das raised a concern that the 450 mW power budget may be tight at 250 MSPS for 16-bit resolution, particularly given the radiation hardening overhead typically added to digital control logic. Dr. Priya Menon concurred, noting that RHBD (Radiation Hardening by Design) techniques such as triple modular redundancy (TMR) on critical state machines typically add 20–35% area and power overhead.

Dr. Sharma directed the analog design team to conduct a preliminary power feasibility check before the architecture review. Col. Tiwari acknowledged the concern but stated the 450 mW figure is a firm requirement from the spacecraft bus power budget.

**3. Schedule Review**
Sanjay Bhatt presented the baseline program schedule. Key milestones:
- Architecture Review: Week 6
- Analog Design Review: Week 14
- Verification Planning Review: Week 16
- Tapeout: Week 28
- Wafer delivery (first lot): Week 42
- Reliability qualification complete: Week 54
- Production Readiness Review: Week 58

The schedule was noted as aggressive given the rad-hard qualification requirements. Meena Iyer flagged that the packaging qualification timeline of 10 weeks between wafer delivery and PRR may be insufficient if reliability failures require design or process rework.

**4. Resource Allocation**
Rajesh Nair confirmed the analog design team of four engineers is in place. Sunil Verma indicated he needs one additional verification engineer for functional coverage closure; the request will be submitted to HR.

**5. Technology Node**
The program will target the 180 nm CMOS rad-hard process available in-house (GSRML Process Node GS180H). Dr. Menon confirmed this process has heritage for TID up to 150 krad(Si) with the appropriate layout rules applied. Use of the enhanced guard-ring structure (EGR-3 layout kit) is mandatory for all analog blocks.

---

## Decisions Made

| Decision ID | Decision | Owner |
|-------------|----------|-------|
| DEC-001 | Program to target GSRML GS180H 180 nm rad-hard process | Dr. Sharma |
| DEC-002 | CQFP-80 ceramic package selected as baseline | Meena Iyer |
| DEC-003 | RHBD techniques (TMR on critical digital logic, EGR-3 layout rules for analog) mandated for all blocks | Dr. Menon |
| DEC-004 | Power budget of 450 mW accepted as a firm requirement; design team to assess feasibility and flag risk if not achievable | Rajesh Nair |

---

## Action Items

| AI ID | Action | Owner | Due Date |
|-------|--------|-------|----------|
| AI-001 | Conduct preliminary power feasibility analysis for 16-bit 250 MSPS ADC on GS180H; present findings at Architecture Review | Rajesh Nair | 07 Feb 2025 |
| AI-002 | Confirm EGR-3 layout kit availability and latest DRC deck version with Process Engineering | Dr. Menon | 28 Jan 2025 |
| AI-003 | Submit headcount request for one additional verification engineer to HR | Sunil Verma | 21 Jan 2025 |
| AI-004 | Prepare detailed program schedule (Level 3) with task-level owners and circulate for review | Sanjay Bhatt | 31 Jan 2025 |
| AI-005 | Obtain signed copy of DRDO-SAT-ADC-REQ-v2.1 and archive in the program document management system | Sanjay Bhatt | 21 Jan 2025 |
| AI-006 | Identify candidate radiation test facilities for TID and SEE testing; confirm availability and cost | Dr. Menon | 07 Feb 2025 |

---

## Risks Identified

| Risk ID | Description | Likelihood | Impact | Owner |
|---------|-------------|-----------|--------|-------|
| RSK-001 | Power consumption may exceed 450 mW target due to RHBD overhead on 16-bit 250 MSPS architecture | High | High | Rajesh Nair |
| RSK-002 | Program schedule is aggressive; reliability qualification window may be insufficient if first-pass silicon has issues | Medium | High | Sanjay Bhatt |
| RSK-003 | Availability of external radiation test facility (heavy ion SEE testing) may cause schedule slippage | Medium | Medium | Dr. Menon |

---

## Next Meeting Objectives

Meeting 02 — Architecture Review (target: Week 6, ~25 Feb 2025):
- Present ADC architecture options (pipeline, SAR, time-interleaved) with power/area/performance trade-off analysis
- Present results of power feasibility study (AI-001)
- Confirm selected architecture and partitioning
- Define top-level block diagram and interface specification
- Review preliminary radiation hardening strategy per block

---

## Meeting Conclusion

Dr. Sharma closed the meeting at 11:30 hrs. All attendees acknowledged their action items. The next meeting is provisionally scheduled for 25 February 2025. Minutes to be circulated within 48 hours.

**Minutes prepared by:** Sanjay Bhatt, Project Controller
**Date of issue:** 15 January 2025
**Distribution:** All attendees, Program Document Management System (PDMS)
