#!/usr/bin/env python3
"""Generate the 3,000-case Oracle QA manifest.

This is a planning and traceability tool. Cases start as PENDING deliberately:
they are not evidence of a passing game test. A case is only marked PASSED by a
real test runner/build record after the Godot implementation exists.
"""
from __future__ import annotations

import json
from pathlib import Path

DOMAINS = [
    ("core", "Arranque, input, cámara, accesibilidad y UI", 180),
    ("save", "Guardado, carga, migración y perfiles", 220),
    ("world", "Movimiento, colisión, vuelo, teletransporte y mapas", 360),
    ("combat", "Combate, daño, estados, IA y jefes", 720),
    ("powers", "Ki, técnicas, transformaciones y fusiones", 420),
    ("progression", "Nivel, stats, equipo, objetos y economía", 300),
    ("content", "Misiones, diálogos, NPCs, cofres y secretos", 300),
    ("z_campaign", "Campaña base Z", 180),
    ("gt_dlc", "GT DLC y Bills hub", 150),
    ("af_dlc", "AF DLC, Void World y postgame", 120),
    ("release", "Rendimiento, build Windows y regresiones", 50),
]


def main() -> None:
    cases = []
    for domain, description, count in DOMAINS:
        for number in range(1, count + 1):
            cases.append({
                "id": f"ORACLE-{domain.upper()}-{number:03d}",
                "domain": domain,
                "description": description,
                "status": "PENDING",
                "automation": "UNASSIGNED",
                "evidence": None,
            })
    assert len(cases) == 3000
    payload = {
        "schema_version": 1,
        "purpose": "Traceable QA plan; PENDING cases do not count as passing tests.",
        "summary": {"total": len(cases), "pending": len(cases), "passed": 0},
        "cases": cases,
    }
    destination = Path(__file__).with_name("oracle_manifest.json")
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {destination}: {len(cases)} pending Oracle cases")


if __name__ == "__main__":
    main()
