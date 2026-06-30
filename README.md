# Covert-C2-Lab: DNS-over-HTTPS C2 Simulation & Detection Research

> ⚠️ EDUCATIONAL USE ONLY — Authorized lab environments exclusively.
> This project was built to study covert channel behavior and improve
> defensive detection capabilities. Never deploy outside isolated VMs.

---

## Project Overview

A lightweight research framework that simulates Command and Control (C2) 
communication patterns using DNS-over-HTTPS (DoH) transport and AES-256 
encrypted payloads — built to generate realistic detection data for SOC 
and threat hunting analysis.

This project is the **blue team side of offensive research**: 
build the behavior → capture the traffic → write the detections.

---

## Architecture

┌─────────────────┐    AES-256 Encrypted over HTTPS    ┌──────────────────┐
│  Simulated      │ ─────────────────────────────────> │  Flask Listener  │
│  Agent (VM2)    │ <───────────────────────────────── │  (VM1 / Server)  │
└─────────────────┘    Mocked DoH TXT Record Response  └──────────────────┘
         │                                                       │
         └──────────────── Wireshark / Zeek ────────────────────┘
                           (Monitoring VM3)

---

## Research Objectives

- Demonstrate how AES-256 encryption renders DPI signatures ineffective
  against encrypted C2 payloads (high-entropy traffic analysis)
- Simulate DNS TXT record abuse for task delivery (T1071.004)
- Generate labeled pcap data for Sigma/Suricata rule development
- Compare detection coverage: signature-based vs. behavioral analytics

---

## MITRE ATT&CK Coverage

| Technique | Name | Research Focus |
|-----------|------|----------------|
| T1071 | Application Layer Protocol | Behavioral baseline vs. anomaly |
| T1071.004 | DNS for C2 | TXT record abuse detection |
| T1140 | Deobfuscate/Decode Files | Entropy-based payload detection |
| T1573 | Encrypted Channel | DPI bypass — AES traffic signatures |

---

## Detection Engineering Outputs

The primary deliverable of this project is the **detection layer**:

- `/detections/sigma/` — 4 Sigma rules (beaconing, DNS TXT abuse,
  high-entropy payload, process ancestry)
- `/detections/suricata/` — 2 Suricata rules (oversized DNS, 
  anomalous TXT frequency)
- `/pcaps/` — Labeled capture files for analyst training
- `/report/` — Full technical write-up with ATT&CK mapping

---

## Lab Setup

### Requirements
- 3 VMs (Kali attacker sim, Ubuntu server, monitoring node)
- Python 3.10+

### Install
pip install flask cryptography requests dnspython

### Run Server (VM1)
python server.py

### Run Agent Simulator (VM2 — isolated network only)
python agent.py

---

## Detection Findings

### Finding 1: Beaconing Regularity
Fixed 5-second intervals are detectable via network flow analysis.
Jitter reduces detection but leaves statistical fingerprints.
→ Sigma rule: `detections/sigma/c2_beaconing_regularity.yml`

### Finding 2: DNS TXT Record Abuse
TXT records carrying base64-encoded task strings are statistically 
anomalous vs. legitimate DNS TXT usage (SPF/DKIM records).
→ Sigma rule: `detections/sigma/dns_txt_c2_abuse.yml`

### Finding 3: High-Entropy Payloads in HTTPS
AES-256 Fernet-encrypted data produces near-maximum Shannon entropy.
Detectable via entropy scoring on proxy logs.
→ Sigma rule: `detections/sigma/high_entropy_https_payload.yml`

---

## References
- MITRE ATT&CK T1071.004
- MITRE ATT&CK T1090.004 (Domain Fronting)
- OWASP Testing Guide
- WithSecure C2 Detection Lab Series