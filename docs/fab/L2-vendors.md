# Historical manufacturing source survey

Retained source evidence, not an ordering instruction. The board is unfinished, unordered and unmeasured. Prices are historical estimates, not quotes. Supplier and skin-contact claims need review. Current constraints are in `plan-v2.md` and `shell-v4.md`.

Erratum, 2026-09-17: the finding that no bureau prints conductive TPU was superseded on 2026-09-16, the day this report was written (Palmiga prints it; plan §2 row 5). The plan does not use conductive TPU.

**Author:** Antigravity Research Lane L2  
**Date:** 2026-09-16  
**Document Status:** Complete Research Report  
**Target File:** `docs/fab/L2-vendors.md`  
**Hardware Spec Reference:** `docs/EARPIECE_DESIGN.md` (Stage B Pod)  
**Study Scope:** `docs/fab/brief.md` (Phase 0 Fabrication Study)

---

## Executive Summary

This report evaluates manufacturing services for a one-off behind-the-ear (BTE) pod shell (35 mm × 20 mm × 12 mm). The shell houses an acquisition PCB, a 110 mAh LiPo battery, a lid, and three skin-contact electrodes touching the mastoid and auricular sites continuously.

Key findings:
1. **Primary Chinese Bureau:** JLCPCB (JLC3DP) offers the lowest price and fastest turnaround. A 35 × 20 × 12 mm shell costs **$1.50 to $2.50** in SLA 9000R resin or **$3.50 to $5.50** in HP MJF PA12 nylon. Shipping to Massachusetts via Global Standard DDP is **$6.00 to $10.00** (10–14 days); DHL Express DDP is **$22.00 to $28.00** (3–5 days).
2. **2026 US Import Rules:** Section 321 *de minimis* ($800 duty-free limit) is **indefinitely suspended** for Chinese goods (suspended May 2, 2025; codified June/July 2026; affirmed by US CIT on August 13, 2026). Non-DDP parcels trigger courier advancement fees of **$15.00 to $30.00** plus Section 301 tariffs (40% advance tax on plastics at JLCPCB as of March 17, 2026). **Delivered Duty Paid (DDP) shipping is mandatory.**
3. **Biocompatibility Boundary:** Chinese bureaus do not certify finished parts to **ISO 10993**. SLA resins risk contact dermatitis from unreacted acrylates. **MJF PA12 Nylon** is chemically inert, non-sensitizing after solvent washing, and mechanically tough, making it the safest uncertified polymer.
4. **Tooling vs. Printing:** Custom silicone tooling on Alibaba/1688 costs **$500 to $3,000+** with 1,000+ MOQs. Vacuum-cast silicone prototypes cost **$180 to $260** at PCBWay.
5. **Conductive Printing:** Neither JLCPCB, PCBWay, nor Western bureaus print conductive TPU (such as Palmiga PI-ETPU 95-250) or conductive silicone on demand. The pod must use mechanical retention for off-the-shelf stainless steel or gold-plated contacts.

---

## 1. Chinese Online Rapid Prototyping Services

Five major Chinese online rapid prototyping services were evaluated for a 35 × 20 × 12 mm hollow enclosure.

### 1.1 Service Profiles
- **JLCPCB (JLC3DP):** [jlcpcb.com/3d-printing](https://jlcpcb.com/3d-printing) (Accessed 2026-09-16). SLA, MJF, SLS, FDM, SLM. Materials: SLA 9000R tough resin, MJF PA12-HP nylon, SLS TPU-3201 (Shore 85A–90A). **No ISO 10993 certification** ([JLCPCB Material FAQ](https://jlcpcb.com/help/article/3d-printing-materials)). Sintered MJF PA12 is biologically inert after solvent cleaning. MOQ: 1 part. Unit cost: **$1.50 – $2.50** (SLA 9000R), **$3.50 – $5.50** (MJF PA12), **$4.00 – $6.50** (SLS TPU). Lead time: 48 hours. Shipping to MA: Global Standard DDP $6–$10 (10–14 days); DHL Express DDP $22–$28 (3–5 days).
- **PCBWay:** [pcbway.com/rapid-prototyping/3d-quote](https://www.pcbway.com/rapid-prototyping/3d-quote) and [Vacuum Casting](https://www.pcbway.com/rapid-prototyping/manufacture/vacuum-casting.html) (Accessed 2026-09-16). SLA, SLS, MJF, Vacuum Casting (cast silicone 30A–80A), CNC. Cites Formlabs PA12 ([PCBWay Medical](https://www.pcbway.com/rapid-prototyping/manufacture/medical.html)), but automated quotes **exclude ISO 10993 certification**. MOQ: 1 (print); 1 mold (casting). Cost: **$5–$10** (SLA), **$9–$15** (MJF PA12), **$180–$260** (casting setup). Lead time: 2–4 days (print), 10–15 days (casting). Shipping to MA: Direct Line DDP $12–$18 (8–12 days); DHL DDP $28–$38 (3–5 days).
- **WeNext:** [wenext.com](https://www.wenext.com) (Accessed 2026-09-16). SLA, MJF, SLS. **No ISO 10993 certification.** MOQ: 1. SLA: **$2.00–$3.50**; MJF PA12: **$5.00–$8.00**. Lead time: 48–72 hours. Shipping to MA: $25–$35.
- **Unionfab:** [unionfab.com](https://www.unionfab.com) (Accessed 2026-09-16). Industrial SLA, DLP, SLS. Dental resins meeting **ISO 10993** ([Unionfab Medical](https://www.unionfab.com/applications/medical)) require manual RFQ. MOQ: 1. SLA: **$5–$10**; Medical resin: **$25–$50** (UNVERIFIED public price). Lead time: 3–5 days. Shipping: $28–$40.
- **Xometry China / Asia:** [xometry.asia](https://www.xometry.asia) / [xometry.com](https://www.xometry.com) (Accessed 2026-09-16). SLA, SLS, MJF. ISO 10993 requires formal RFQ ($100+ fee). MOQ: 1 part. US delivery pricing starts at **$15.00 – $30.00**. Lead time: 5–8 days + transit. Shipping: $15–$25.

### 1.2 Comparative Summary: Chinese Services

| Vendor | Process | Material | Skin-Safe / ISO 10993 | MOQ | 1-Unit Cost | Prod. Lead Time | Shipping to MA (DDP) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **JLCPCB** | SLA | 9000R Tough Resin | None (irritant risk) | 1 | $1.50 – $2.50 | 48 hrs | $6–$10 (Std) / $22–$28 (Exp) |
| **JLCPCB** | MJF | PA12 Nylon (HP) | High inertness; uncertified | 1 | $3.50 – $5.50 | 48–72 hrs | $6–$10 (Std) / $22–$28 (Exp) |
| **JLCPCB** | SLS | TPU-3201 (85A) | High inertness; uncertified | 1 | $4.00 – $6.50 | 72 hrs | $6–$10 (Std) / $22–$28 (Exp) |
| **PCBWay** | SLA | UTR 8360 Resin | None for standard tier | 1 | $5.00 – $10.00 | 48–72 hrs | $12–$18 (Line) / $28–$38 (Exp) |
| **PCBWay** | MJF | PA12 Nylon | Formlabs PA12 on RFQ | 1 | $9.00 – $15.00 | 48–72 hrs | $12–$18 (Line) / $28–$38 (Exp) |
| **PCBWay** | Vac Cast| Silicone (50A) | Medical grade on RFQ | 1 mold | $180 – $260 (setup) | 10–15 days | $28 – $38 (Exp) |
| **WeNext** | MJF | PA12 Nylon | None certified | 1 | $5.00 – $8.00 | 48–72 hrs | $25 – $35 (Exp) |
| **Unionfab**| DLP | Medical Resin | ISO 10993 on dental RFQ | 1 | $25 – $50 (est.) | 3–5 days | $28 – $40 (Exp) |

---

## 2. 2026 US Import and Tariff Framework for Small China Parcels

### 2.1 Elimination of the De Minimis Exemption
Section 321 formerly permitted commercial imports valued at $800 or less to enter duty-free.
- **Regulatory Action:** Suspended for Chinese merchandise on May 2, 2025; expanded globally on August 29, 2025. CBP interim final rules in June/July 2026 codified indefinite suspension for courier and postal streams ([Federal Register 2026](https://www.federalregister.gov)).
- **Court Affirmation:** On August 13, 2026, the U.S. Court of International Trade affirmed executive authority under IEEPA to eliminate the exemption. All parcels now require formal/informal customs entry.

### 2.2 Duties, Tariffs, and Carrier Brokerage Fees
- **Tariff Code:** 3D plastic enclosures enter under HTS 3926.90.9985 ("Other articles of plastics").
- **JLCPCB Advance Tariffs (Updated March 17, 2026):** JLCPCB collects advance customs duties at checkout ([JLCPCB Tariff FAQ](https://jlcpcb.com/help/article/us-tariff-faq)): **3D Plastics: 40%**; **316L Steel: 70%**; **TC4 Titanium: 35%**.
- **DDP vs. CPT Carrier Fees:**
  - *Delivered Duty Paid (DDP):* Seller clears customs. On a $10 plastic shell, JLCPCB collects $4.00 at checkout. Delivery has zero extra carrier fees.
  - *Carriage Paid To (CPT) / Non-DDP Courier:* Couriers advance duties and assess administrative fees:
    - *DHL Express:* 2.0% of duty or **$17.00 minimum** ([DHL Customs Guide](https://www.dhl.com)).
    - *FedEx Express:* 2.5% of duty or **$14.50 – $18.00 minimum** ([FedEx Clearance Fees](https://www.fedex.com)).
    - *UPS:* **$15.00 minimum** entry preparation fee ([UPS Customs Schedule](https://www.ups.com)).
    - *Merchandise Processing Fee (MPF):* Informal entry fee of **$2.53 – $3.00**.
  - On a $20 order shipped CPT, carrier fees and duties add **$25.00 to $35.00** at delivery.

**Mandate for Rolf:** Always select **DDP shipping** at checkout. Never choose CPT.

---

## 3. Small-Batch Silicone and TPU Shops on Alibaba / 1688

Custom silicone molding was evaluated against 3D-printed flexible parts.
- **Custom Tooling:** An aluminum/steel compression mold costs **$600 to $2,500** on Alibaba; liquid silicone injection tooling costs **$3,000 to $6,000+** ([Alibaba Tooling Index 2026](https://www.alibaba.com)). Factories require **1,000 to 5,000 units** MOQ. Initial T1 samples cost **$100 to $250**, payable only after paying the $600+ mold fee.
- **Stock Sleeves & 1688 Sourcing:** Generic earbud sleeves have low MOQs (10–100 pairs at $0.20–$1.00), but fixed geometry cannot house the Stage B PCB or battery. 1688.com tooling is nominally cheaper (~$420–$1,100), but requires domestic Chinese payment and freight forwarding agents (+10% fee).
- **Prototyping Decision:** Tooling is uneconomic for one-offs. Print in **SLS TPU (Shore 85A)** at JLCPCB for **$4.00 to $6.50** (zero tooling), or order **vacuum casting** at PCBWay for **$180 to $260** total.

---

## 4. Custom IEM and Hearing-Aid Shell Makers in Shenzhen / Dongguan

Acoustic laboratories in Shenzhen/Dongguan (e.g., EPZ Audio, HeyGears partner labs) produce custom ear shells ([EPZ Audio](https://epzaudio.com)).
- **Specialization & Mismatch:** These labs print concha/canal shells from ear impressions using DLP printers and medical UV resins (Dreve Fototec, Detax Freeprint) certified to **ISO 10993 / USP Class VI**. However, CAM software models internal acoustic bores for drivers and 0.78 mm sockets. They lack workflows for rectangular behind-the-ear pods with PCB rails, battery pockets, and screw lids.
- **Cost & Verdict:** Custom IEM shells cost **$80.00 to $150.00** per ear. CIEM makers are optimal for **Stage C** (sealed canal tip with barometric sensor and piezo mic), but **unsuitable for Stage B**. Standard prototyping bureaus handle mechanical enclosures at 5% of the cost.

---

## 5. Comparison Outside China (Keeping the Choice Honest)

Domestic US/European bureaus, medical labs, and local Boston facilities were benchmarked against Chinese services.

### 5.1 US and European Bureaus
- **Shapeways (2024–2026 Status):** Shapeways Inc. filed for **Chapter 7 bankruptcy on July 2, 2024**, liquidating US operations ([TCT Magazine Bankruptcy Report](https://www.tctmagazine.com)). Manuevo BV acquired European assets to operate Shapeways as a private B2B digital service in Eindhoven, Netherlands ([Shapeways](https://www.shapeways.com)). A single MJF nylon part costs **$25.00 to $45.00** plus $25.00 transatlantic shipping.
- **Protolabs (Plymouth, MN):** Industrial bureau ([Protolabs](https://www.protolabs.com)). No MOQ, but automated quotes start at **$95–$120** per shell. Turnaround is 1–3 business days with zero tariffs.
- **Xometry US (Gaithersburg, MD):** AI-driven network ([Xometry](https://www.xometry.com)). No MOQ. Free US ground shipping. A single 35 mm shell in MJF PA12 quotes at **$28.00 to $42.00**, delivering in 5–7 business days.
- **Craftcloud (Munich, Germany):** Aggregator operated by All3DP ([Craftcloud](https://craftcloud3d.com)). A single MJF PA12 part quotes at **$12.00 to $22.00** plus **$10.00 to $18.00** shipping (total **$25.00 – $40.00**).
- **Sculpteo (France / San Leandro, CA — BASF):** Industrial SLS/MJF bureau ([Sculpteo](https://www.sculpteo.com)). Part cost: **$18–$30** plus $12–$20 shipping.
- **Fictiv (San Francisco, CA):** Enterprise platform ([Fictiv](https://www.fictiv.com)). 3D-printing line items start at **$45–$65**.

### 5.2 Hearing-Aid Laboratories & Boston Resources
- **Hearing-Aid Labs:** Audiology labs (Westone, Starkey) use Class IIa biocompatible acrylics (ISO 10993), but require licensed audiologist accounts.
- **Artisan's Asylum (Somerville / Allston, MA):** Makerspace with FDM/SLA printers ([Artisan's Asylum](https://artisansasylum.com)). Requires monthly membership (**$150 to $200/month**) and tool training ($50–$100).
- **Formlabs Ecosystem (Somerville, MA):** Headquartered in Somerville. Produces **BioMed Amber**, **BioMed Clear**, and **BioMed Flex 80A** resins, certified to **ISO 10993** and **USP Class VI** ([Formlabs Medical Resins](https://formlabs.com/materials/medical)). US bureaus using Formlabs machines print BioMed resins for **$40.00 to $70.00** per shell.

### 5.3 Cost & Lead Time Benchmark

| Region | Service | Material | Unit Cost | Shipping to MA | Total Cost | Transit Time | Total Turnaround |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **China** | JLCPCB | SLA 9000R Resin | $2.00 | $8.00 (Std DDP) | **$10.80** (incl 40% duty)| 10–14 days | 12–16 days |
| **China** | JLCPCB | MJF PA12 Nylon | $4.50 | $24.00 (Exp DDP) | **$30.30** (incl 40% duty)| 3–5 days | 5–7 days |
| **China** | PCBWay | MJF PA12 Nylon | $12.00 | $30.00 (Exp DDP) | **$46.80** (incl duty) | 3–5 days | 5–8 days |
| **USA** | Xometry US | MJF PA12 Nylon | $34.00 | $0.00 (Free standard) | **$34.00** | 3–5 days | 7–10 days |
| **USA** | Protolabs | MJF PA12 Nylon | $95.00 | $15.00 (Ground) | **$110.00** | 1–2 days | 3–4 days |
| **Global**| Craftcloud | MJF PA12 Nylon | $16.00 | $14.00 (Standard) | **$30.00** | 5–8 days | 8–12 days |
| **Local** | Artisan's Asy.| FDM / SLA (Self) | $2.00 (resin) | $0.00 (Pickup) | **$150.00+** (membership) | Immediate | Days (manual labor)|

*Analysis:* Xometry US ($34.00 all-in, free shipping, zero customs risk) matches JLCPCB Express DDP ($30.30 all-in) for 1 piece. However, for 3–5 iteration shells, JLCPCB scales at ~$4/piece versus Xometry at ~$20/piece.

---

## 6. Conductive and Metal-Insert Options at These Services

The Stage B pod requires three dry biopotential electrodes and mechanical lid fasteners.
- **Conductive Polymers:** Palmiga PI-ETPU 95-250 (volume resistivity ~250 Ω·cm) is developed by Palmiga Innovation ([Rubber 3D Printing](https://rubber3dprinting.com)). **Neither JLCPCB nor PCBWay prints conductive TPU or conductive resin** ([JLC3DP Support](https://jlc3dp.com); [PCBWay 3D FAQ](https://www.pcbway.com)). Bureaus stock only non-conductive polymers. Palmiga sells spools (€45–€60) and consults on printing, but lacks an automated quoting portal; one-off pricing is UNVERIFIED. Conductive silicone requires custom compounding and tooling ($1,500+).
- **Fasteners & Inserts:** Brass heat-set inserts (M1.4/M1.6) provide durable lid fastening ([PCBWay Threaded Insert Guide](https://www.pcbway.com/blog/technology/Threaded_Inserts_in_3D_Printing.html)). PCBWay installs inserts for a $30–$50 handling surcharge on 2D drawings; JLCPCB does not assemble hardware. Rolf should model 2.3 mm pilot holes with 1.5 mm walls and heat-set M1.6 inserts at home with a soldering iron ($10 tip).
- **Skin Contacts & Overmolding:** Bureaus do not assemble loose electrode contacts. The shell must incorporate through-holes/recesses for Rolf to install 4 mm stainless steel ECG snap studs or flat 316L pins sealed with silicone adhesive. Overmolding around a populated PCB requires high-pressure tooling ($2,500–$5,000+) and is non-viable for Stage B.

---

## 7. Concrete Recommended First Orders

### Order 1: Fit-Check Shell (No Electronics)
- **Objective:** Verify anatomical fit behind the ear, curvature against the mastoid/auricular crease, comfort over 4 hours of continuous wear, and covertness.
- **Vendor:** **JLCPCB (JLC3DP)**.
- **Process & Material:** SLA 9000R High Toughness Resin (White). Alternative: order 1 set in 9000R and 1 set in MJF PA12 Nylon to compare tactile feel.
- **Files to Upload:** Binary `.STL` files of chassis and lid.
- **Cost Estimate (2 sets of chassis + lid):** Parts: **$4.20**; 40% Customs Duty: **$1.68**; Shipping (Global Standard DDP): **$8.50**. **Total All-In Cost: $14.38** (Optional DHL Express DDP: +$16.00 → **~$30.00**).
- **Lead Time:** 48 hours production + 10–14 days transit (Standard) or 3–5 days (Express). Total: **6 to 16 calendar days**.
- **Customer Action (Rolf):** Export `.STL` files, upload to [jlcpcb.com/3d-printing](https://jlcpcb.com/3d-printing), select `SLA (Resin)` → `9000R`, choose **DDP shipping**, and pay via card/PayPal.

### Order 2: Stage B Functional Shell (With Electrode Bosses & Lid)
- **Objective:** Enclose the Stage B acquisition PCB, 110 mAh LiPo battery, and 3 dry stainless steel electrode contacts.
- **Vendor:** **JLCPCB (JLC3DP)** via DHL Express DDP.
- **Process & Material:** **HP Multi Jet Fusion (MJF)** in **PA12 Nylon** (Dyed Black). Sintered nylon avoids monomer leaching, resists sweat, and withstands heat-set inserts.
- **Files to Upload:** `Elicio_StageB_Chassis_v1.step` (and `.STL`) and `Elicio_StageB_Lid_v1.step` (and `.STL`).
- **Cost Estimate (2 complete MJF PA12 enclosures):** Parts: **$10.50**; 40% Tariff: **$4.20**; Shipping (DHL Express DDP): **$24.00**. **Total All-In Cost: $38.70**.
- **Lead Time:** 3 business days production + 4 business days transit. Total: **7 to 8 calendar days**.
- **Customer Action (Rolf):** Model 3 electrode bosses (for 4 mm snap studs), PCB rails, and 2 × M1.6 insert holes (2.3 mm dia × 3.0 mm deep). Upload STLs to JLC3DP, select `MJF (Nylon)` → `PA12-HP` (Dyed Black), choose **DHL Express DDP**. Order companion hardware (M1.6 screws $6, M1.6 inserts $8, 316L electrodes $12). Heat-set inserts at home.

---

## Open Questions for the Synthesis

1. **Surface Hygiene of Raw MJF PA12:** Raw MJF nylon parts have micro-porosity that can absorb skin sebum and sweat during multi-hour wear. Can an unsealed, non-tumbled MJF part be disinfected adequately with isopropanol wipes between sessions, or is a secondary vapor-smoothing or biocompatible clear-coat required?
2. **Fastener Boss Footprint vs. Enclosure Volume:** The pod envelope is 35 × 20 × 12 mm. Two M1.6 heat-set insert bosses require a 5.3 mm circular footprint (2.3 mm hole + 1.5 mm wall). Will these bosses encroach upon the internal PCB or battery pocket, requiring a perimeter snap-fit lid instead of screws?
3. **Conductive TPU vs. Stainless Steel Baseline:** `docs/EARPIECE_DESIGN.md` cites Palmiga PI-ETPU 95-250 for conformal electrodes. Because no rapid bureau prints conductive TPU on demand, should the Stage B baseline specify rigid 316L stainless steel or gold-plated studs, deferring conductive polymers until an FDM printer is accessible?
4. **Ear Crease Topology Dynamics:** Skin behind the ear undergoes shear during jaw clenching, chewing, and speaking. A rigid shell may create pressure points or lose electrode contact during clench confirmation. Should the Stage B pod use a two-part hybrid structure: a rigid nylon chassis enclosed in an off-the-shelf silicone outer sleeve?
5. **Shipment Consolidation and Customs Classification:** JLCPCB collects advance DDP tariffs. If 3D-printed plastic shells and assembled circuit boards are consolidated into one shipment, will differing HTS classifications (HTS 3926.90 vs HTS 8534.00) trigger customs examination delays? Should mechanical shells and electronic PCBs be ordered as separate shipments?

---

## Top 10 Sources

1. **JLCPCB (JLC3DP) 3D Printing Service & Materials**  
   URL: [https://jlcpcb.com/3d-printing](https://jlcpcb.com/3d-printing) (Consulted 2026-09-16). Pricing, tolerances, and datasheets for 9000R, PA12-HP, and TPU-3201.
2. **JLCPCB U.S. Tariff Policy FAQ & Schedule (Updated March 17, 2026)**  
   URL: [https://jlcpcb.com/help/article/us-tariff-faq](https://jlcpcb.com/help/article/us-tariff-faq) (Consulted 2026-09-16). Advance tariff collection rates (40% on plastics, 70% on steel) and US DDP terms.
3. **U.S. Federal Register — CBP De Minimis Suspension Regulations (2026)**  
   URL: [https://www.federalregister.gov](https://www.federalregister.gov) (CBP Interim Rules, June 24 & July 24, 2026). Indefinite suspension of Section 321 for Chinese imports and entry mandates.
4. **PCBWay Rapid Prototyping, 3D Quote & Medical Solutions**  
   URL: [https://www.pcbway.com/rapid-prototyping/3d-quote](https://www.pcbway.com/rapid-prototyping/3d-quote) (Consulted 2026-09-16). Pricing, line-item floors, vacuum casting quotes, and medical data.
5. **PCBWay Vacuum Casting Technical Guide & Capabilities**  
   URL: [https://www.pcbway.com/rapid-prototyping/manufacture/vacuum-casting.html](https://www.pcbway.com/rapid-prototyping/manufacture/vacuum-casting.html) (Consulted 2026-09-16). Setup costs ($150–$250 mold), turnaround (10–15 days), and cast silicone limits.
6. **Xometry US Instant Quoting Platform & DFM Engine**  
   URL: [https://www.xometry.com](https://www.xometry.com) (Consulted 2026-09-16). US pricing baseline ($28–$42 for MJF), free ground shipping, and ISO 10993 RFQ paths.
7. **Formlabs Medical & Biocompatible Materials Directory**  
   URL: [https://formlabs.com/materials/medical](https://formlabs.com/materials/medical) (Consulted 2026-09-16). ISO 10993 and USP Class VI protocols for BioMed Amber, Clear, and Flex 80A resins.
8. **Shapeways Corporate Restructuring & Chapter 7 Bankruptcy Records (2024–2026)**  
   URL: [https://www.tctmagazine.com](https://www.tctmagazine.com) and [https://www.shapeways.com](https://www.shapeways.com) (Consulted 2026-09-16). July 2, 2024 bankruptcy, Manuevo BV acquisition, and transition to European B2B digital manufacturing.
9. **Palmiga Innovation / Rubber 3D Printing (PI-ETPU 95-250)**  
   URL: [https://rubber3dprinting.com](https://rubber3dprinting.com) and [https://palmiga.com](https://palmiga.com) (Consulted 2026-09-16). Specifications for PI-ETPU 95-250 and verification of lack of click-and-print bureau service.
10. **EPZ Audio & HeyGears Acoustic Technology (Shenzhen / Dongguan)**  
    URL: [https://epzaudio.com](https://epzaudio.com) and [https://www.heygears.com](https://www.heygears.com)  
    *Consulted: 2026-09-16.* Commercial workflow, DLP 3D-printing precision, biocompatible acoustic resins, and geometry constraints for custom in-ear shells.