# MINUTES OF MEETING

**Meeting ID:** MOM-RHADC-004
**Meeting Title:** Verification Planning Review
**Date:** 06 May 2025
**Time:** 10:00 – 12:30 hrs
**Location:** Conference Room A1, Building 5, GSRML
**Chairperson:** Sunil Verma, Lead Verification Engineer

*Note: Dr. Sharma attending a program directors' review at DRDO HQ; chair delegated to Sunil Verma.*

---

## Attendees

| Name | Role | Department |
|------|------|------------|
| Sunil Verma | Lead Verification Engineer (Chair) | Design Verification |
| Kavya Reddy | Verification Engineer | Design Verification |
| Rajesh Nair | Chief Design Engineer | Analog Design |
| Vikram Joshi | Senior Analog Designer | Analog Design |
| Deepak Rao | Digital Design Lead | Digital Design |
| Rohit Das | Systems Engineer | Systems Integration |
| Sanjay Bhatt | Project Controller | PMO |
| Lakshmi Srinivasan | Quality Assurance Manager | QA |
| Dr. Priya Menon | Radiation Hardening Specialist | Process Engineering |

---

## Agenda

1. Review of action items from MOM-RHADC-003 (design change updates)
2. Verification plan presentation — block-level and full-chip
3. Coverage closure strategy for DMC background calibration (RSK-004)
4. PVT + radiation corner simulation plan
5. Formal verification scope (digital blocks)
6. Risk review
7. AOB

---

## Discussion Points

**1. Action Item Review**
- AI-013: Complete. 6-bit calibration DAC simulated across all corners. Offset coverage confirmed ±13.5 mV across SS/–40°C. Meets requirement.
- AI-014: Complete. W/L = 40/2 LDO input pair re-simulated. TID drift 1.8 mV at 100 krad(Si). Confirmed well within 5 mV limit.
- AI-015: H-tree clock routing design complete. Inter-channel phase skew post-layout simulation: < 0.6 ps across PVT. Satisfactory.
- AI-016: Power reduction exercise — Rajesh Nair identified 18 mW saving: 8 mW from clock buffer bias current optimisation, 6 mW from output serializer duty-cycle switching reduction, 4 mW from reference LDO standby mode. Updated total power estimate: 420 mW nominal. Now 10 mW below 430 mW internal target. Team satisfied.
- AI-017: DSD v1.0 issued 29 Apr 2025. Archived in PDMS.
- AI-018: EGR-3 layout 65% complete. Full DRC/LVS report not yet available; expected 30 May as planned.

**2. Verification Plan Presentation**
Sunil Verma presented the RHADC Verification Plan (VP-RHADC-v0.2). Verification strategy is structured in three tiers:

*Tier 1 — Block-Level Simulation:*
- SAR core: transistor-level simulation in Spectre, PVT corners (SS/TT/FF × –40/27/85°C), pre- and post-radiation corners (25 krad and 100 krad delta-Vth models per GSRML Process Radiation Model v3.1)
- Reference generator: AC, transient, TID sensitivity
- Clock distribution: Phase noise, skew, jitter under temperature and TID
- DMC digital block: RTL simulation with UVM testbench, functional coverage targets defined

*Tier 2 — Full-Chip Simulation:*
- Mixed-signal testbench using Spectre/Xcelium co-simulation
- Key tests: DNL/INL sweep, SFDR vs. frequency, SNR at Nyquist, power vs. supply, startup sequence
- Background calibration convergence test: requirement is convergence within 1024 clock cycles under all PVT conditions

*Tier 3 — Radiation Corner Simulation:*
- Repeat critical full-chip tests at post-100 krad transistor models
- SEU injection: fault injection on TMR voters to verify correct operation

Kavya Reddy noted that Tier 3 coverage for SEU fault injection requires the RTL gate-level netlist. Gate-level availability depends on layout completion (AI-018). This creates a dependency that could compress the verification schedule.

Sunil Verma flagged this as a risk: if layout is delayed beyond 30 May, gate-level radiation corner simulation cannot begin until late June, which compresses tapeout preparation.

**3. DMC Background Calibration Coverage (RSK-004)**
Kavya Reddy presented the coverage strategy for the DMC background calibration block. The key concern (from RSK-004) is achieving functional coverage of calibration convergence across PVT corners. Proposed approach:
- Directed constrained-random stimulus to stress inter-channel gain/offset mismatch injection
- Convergence monitored via functional coverage monitor in UVM testbench
- Target: 100% coverage of convergence across all defined PVT corner combinations (12 corners)
- Estimated simulation time: ~240 hours of compute time on cluster

Sunil Verma requested additional compute cluster allocation to ensure coverage closure before tapeout. Sanjay Bhatt agreed to raise priority allocation request with the computing infrastructure team.

**4. Formal Verification Scope**
Deepak Rao confirmed that the TMR logic (DMC voters, clock control registers, output serializer control) will be formally verified using model checking (JasperGold). Properties to be written against the DSD v1.0 specification. Target: all safety properties proven; no vacuity. Formal verification kickoff scheduled 09 May.

**5. Simulation Corner Matrix**
The full PVT + TID corner matrix agreed:
- Process: SS, TT, FF (3 corners)
- Voltage: –10%, nominal, +10% (3 levels)
- Temperature: –40°C, +27°C, +85°C (3 levels)
- TID: Pre-rad, 25 krad, 100 krad (3 levels)
Total effective corners: 81. Rohit Das noted this is a large matrix and simulation runtime must be managed carefully.

Rajesh Nair proposed prioritising the 27 worst-case corner combinations (SS/low-V/–40°C and FF/high-V/+85°C at all TID levels) for full simulation, with a reduced set for remaining corners. Sunil Verma agreed this is acceptable provided the coverage plan is documented in the VP.

---

## Decisions Made

| Decision ID | Decision | Owner |
|-------------|----------|-------|
| DEC-012 | Full PVT × TID simulation matrix reduced to prioritised 27 worst-case corners for full simulation; remaining corners run at critical tests only; documented in VP | Sunil Verma |
| DEC-013 | Formal verification (model checking) applied to all TMR logic blocks; completion required before tapeout sign-off | Deepak Rao |

---

## Action Items

| AI ID | Action | Owner | Due Date |
|-------|--------|-------|----------|
| AI-019 | Issue Verification Plan VP-RHADC v1.0 incorporating agreed corner matrix and DMC coverage strategy | Sunil Verma | 23 May 2025 |
| AI-020 | Raise compute cluster priority allocation request for 240-hour DMC calibration simulation campaign | Sanjay Bhatt | 09 May 2025 |
| AI-021 | Begin formal verification of TMR logic; report first property results at Verification Status Review | Deepak Rao | 23 May 2025 |
| AI-022 | Complete EGR-3 layout and issue full-chip DRC/LVS report (from AI-018); gate-level netlist required for Tier 3 | Rajesh Nair | 30 May 2025 |
| AI-023 | Define and document SEU fault injection test plan for TMR voter blocks | Kavya Reddy | 23 May 2025 |

---

## Risks Identified / Updated

| Risk ID | Description | Likelihood | Impact | Status / Update |
|---------|-------------|-----------|--------|-----------------|
| RSK-001 | Power budget — nominal 420 mW; risk reduced following power optimisation | Low | Medium | Reduced. Continue monitoring at corners |
| RSK-002 | Schedule — layout delay beyond 30 May would compress gate-level Tier 3 simulation before tapeout | Medium | High | Elevated; linked to AI-022 |
| RSK-004 | DMC calibration coverage closure — compute resource dependency identified | Medium | Medium | Mitigation: compute allocation request raised |
| RSK-006 | Gate-level simulation schedule dependency on layout completion; could compress Tier 3 verification window | Medium | High | New — Sunil Verma owner |

---

## Next Meeting Objectives

Meeting 05 — Verification Status Review (target: Week 22, ~17 Jun 2025):
- Report block-level simulation closure status
- Report formal verification property results
- Report DMC background calibration convergence coverage
- Report full-chip simulation initial results (SNR, ENOB, power)
- Review DRC/LVS clean status and tapeout readiness path

---

## Meeting Conclusion

Sunil Verma closed the meeting at 12:30 hrs on behalf of Dr. Sharma. Minutes to be reviewed by Dr. Sharma before circulation. All action item owners acknowledged responsibilities.

**Minutes prepared by:** Kavya Reddy, Verification Engineer (acting secretary)
**Date of issue:** 07 May 2025
**Distribution:** All attendees, Dr. A. Sharma, Col. V. K. Tiwari (DRDO), PDMS
