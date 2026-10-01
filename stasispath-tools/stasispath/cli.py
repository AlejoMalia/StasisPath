"""
StasisPath Command-Line Interface (CLI).
Provides rapid biophysical calculations directly from the shell terminal.
"""

import sys
import argparse
from stasispath.f3_ischemia import tau_eq
from stasispath.f4_nucleation import t_max_nucleation
from stasispath.thermal_stress import fracture_risk
from stasispath.cpa_toxicity import predicted_ocr_retention
from stasispath.predictions import eval_p19
from stasispath.reporting import generate_protocol_report
from stasispath.organ_projector import (
    project_multiorgan_constraints,
    format_multiorgan_markdown_report,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="stasispath",
        description="StasisPath: Biophysics & Cryopreservation Toolkit (StasisPath Framework)",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: tau (Ischemia)
    p_tau = subparsers.add_parser("tau", help="Calculate equivalent normothermic ischemic time (tau_eq)")
    p_tau.add_argument("--time", "-t", type=float, required=True, help="Exposure time in hours")
    p_tau.add_argument("--temp", "-T", type=float, required=True, help="Tissue temperature in °C")

    # Command: nucleation (Formula F4)
    p_nuc = subparsers.add_parser("nucleation", help="Calculate maximum supercooling duration before freezing")
    p_nuc.add_argument("--volume", "-v", type=float, required=True, help="Organ volume in Liters")

    # Command: stress (Thermal fracture)
    p_stress = subparsers.add_parser("stress", help="Evaluate thermomechanical stress near Tg (-123 °C)")
    p_stress.add_argument("--rate", "-r", type=float, required=True, help="Cooling/warming rate in °C/min")
    p_stress.add_argument("--lc", type=float, required=True, help="Characteristic radius LC in cm")

    # Command: toxicity (Arrhenius CPA damage)
    p_tox = subparsers.add_parser("toxicity", help="Predict Arrhenius CPA toxicity and OCR retention")
    p_tox.add_argument("--temp", "-T", type=float, default=-22.0, help="Perfusion temperature in °C (default -22)")
    p_tox.add_argument("--time", "-t", type=float, default=25.0, help="Exposure duration in minutes (default 25)")
    p_tox.add_argument("--cpa", type=str, default="M22", help="CPA formulation (default M22)")

    # Command: eval-p19 (preregistered experiment P19, frozen rule)
    p_p19 = subparsers.add_parser("eval-p19", help="Evaluate preregistered experiment P19 under its frozen rule")
    p_p19.add_argument("--c", type=float, required=True, help="LTP in arm C (M22), %% of baseline (e.g. 135)")
    p_p19.add_argument("--b", type=float, required=True, help="LTP in arm B (V3 positive control), %% of baseline (e.g. 138)")
    p_p19.add_argument("--ci-low", type=float, required=True, help="95 %% CI of (C-B), lower bound, percentage points")
    p_p19.add_argument("--ci-high", type=float, required=True, help="95 %% CI of (C-B), upper bound, percentage points")
    p_p19.add_argument("--d", type=float, default=None, help="optional LTP in arm D (loading only), for the diagnosis")

    # Command: report
    p_rep = subparsers.add_parser("report", help="Generate Markdown protocol evaluation report")
    p_rep.add_argument("--name", type=str, default="Organ Specimen", help="Organ name")
    p_rep.add_argument("--mass", type=float, required=True, help="Mass in kg")
    p_rep.add_argument("--vol", type=float, required=True, help="Volume in Liters")
    p_rep.add_argument("--lc", type=float, required=True, help="Characteristic dimension LC in cm")
    p_rep.add_argument("--cpa", type=str, default="M22", help="CPA name")

    # Command: multiorgan (Multi-Organ Constraint Projector)
    p_multi = subparsers.add_parser("multiorgan", help="Project biophysical constraints across organs from anthropometry")
    p_multi.add_argument("--age", type=float, default=45.0, help="Subject age in years (default: 45)")
    p_multi.add_argument("--height", type=float, default=175.0, help="Height in cm (default: 175)")
    p_multi.add_argument("--weight", type=float, default=73.0, help="Weight in kg (default: 73)")
    p_multi.add_argument("--sex", type=str, default="M", choices=["M", "F", "m", "f"], help="Sex (M/F)")
    p_multi.add_argument("--delay", type=float, default=15.0, help="Pre-perfusion delay in minutes (default: 15)")

    # Command: recipe (Cryogenic Freezing Trajectory)
    p_rec = subparsers.add_parser("recipe", help="Generate controlled-rate freezer cooling profile")
    p_rec.add_argument("--cpa", type=str, default="M22", help="CPA formulation (M22, V3, VS55)")
    p_rec.add_argument("--lc", type=float, default=2.0, help="Characteristic radius LC in cm")
    p_rec.add_argument("--csv", type=str, default=None, help="Export CSV path")
    p_rec.add_argument("--planer", type=str, default=None, help="Export Planer Kryo script path")

    # Command: washout (Stepwise Osmotic Dilution)
    p_wash = subparsers.add_parser("washout", help="Design stepwise osmotic CPA dilution protocol with mannitol")
    p_wash.add_argument("--cpa", type=str, default="M22", help="CPA formulation (M22, V3)")
    p_wash.add_argument("--thickness", type=float, default=0.04, help="Slice thickness or organ LC in cm (default: 0.04 cm)")
    p_wash.add_argument("--vascular", action="store_true", help="Flag if organ is vascularized perfusion")

    # Command: boa (TotalSegmentator / BOA Ingestion)
    p_boa = subparsers.add_parser("boa", help="Ingest BOA or TotalSegmentator CT/MRI segmentation file")
    p_boa.add_argument("--file", "-f", type=str, required=True, help="Path to segmentation .json or .csv")
    p_boa.add_argument("--age", type=float, default=45.0, help="Subject age")
    p_boa.add_argument("--height", type=float, default=175.0, help="Height in cm")
    p_boa.add_argument("--weight", type=float, default=73.0, help="Weight in kg")
    p_boa.add_argument("--sex", type=str, default="M", help="Sex (M/F)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "tau":
        res = tau_eq(t_hours=args.time, T_c=args.temp)
        print(f"Equivalent Ischemic Time (tau_eq) at 37 °C: {res:.3f} hours ({res * 60:.1f} minutes)")
    elif args.command == "nucleation":
        t_max = t_max_nucleation(V_L=args.volume)
        print(f"Stochastic Nucleation Limit (t_max): {t_max:.3f} hours ({t_max * 60:.1f} minutes)")
    elif args.command == "stress":
        res = fracture_risk(cooling_rate_c_min=args.rate, lc_cm=args.lc)
        print(f"Thermal Stress: {res['sigma_thermal_mpa']:.3f} MPa (Limit: {res['sigma_critical_mpa']} MPa)")
        print(f"Risk Assessment: {res['risk_level']} (Will fracture: {res['will_fracture']})")
    elif args.command == "toxicity":
        res = predicted_ocr_retention(T_c=args.temp, t_exposure_min=args.time, cpa=args.cpa)
        print(f"Predicted OCR Retention: {res['predicted_ocr_percent']:.1f} % (D_CPA = {res['d_cpa']:.3f})")
        print(f"Safety Status: {res['status']}")
    elif args.command == "eval-p19":
        res = eval_p19(args.c, args.b, (args.ci_low, args.ci_high), args.d)
        print(f"P19 verdict: {res['verdict'].value}")
        print(res["reading"])
        if res["diagnosis"]:
            print(f"Diagnosis (arm D): {res['diagnosis']}")
    elif args.command == "report":
        rep = generate_protocol_report(
            organ_name=args.name,
            mass_kg=args.mass,
            V_L=args.vol,
            lc_cm=args.lc,
            cpa=args.cpa,
        )
        print(rep)
    elif args.command == "multiorgan":
        res = project_multiorgan_constraints(
            age_years=args.age,
            height_cm=args.height,
            weight_kg=args.weight,
            sex=args.sex,
            preperfusion_delay_min=args.delay,
        )
        md_table = format_multiorgan_markdown_report(res)
        print(md_table)
    elif args.command == "recipe":
        from stasispath.thermal_recipes import generate_vitrification_recipe, export_recipe_csv, export_planer_kryo_format
        steps = generate_vitrification_recipe(cpa=args.cpa, organ_lc_cm=args.lc)
        print(f"Generated {len(steps)} recipe steps for {args.cpa} (LC = {args.lc} cm):")
        for s in steps:
            print(f"  Step {s.step_number} [{s.step_type}]: {s.start_temp_c:.1f}°C -> {s.target_temp_c:.1f}°C at {s.rate_c_min:.2f}°C/min ({s.duration_min:.1f} min) | {s.phase_name}")
        if args.csv:
            export_recipe_csv(steps, args.csv)
            print(f"Exported CSV recipe to: {args.csv}")
        if args.planer:
            export_planer_kryo_format(steps, args.planer)
            print(f"Exported Planer Kryo script to: {args.planer}")
    elif args.command == "washout":
        from stasispath.cpa_washout import design_washout_protocol
        res = design_washout_protocol(initial_cpa=args.cpa, sample_thickness_or_lc_cm=args.thickness, is_organ_vascularized=args.vascular)
        print(f"Stepwise Washout Schedule for {res['cpa']} (Total: {res['total_duration_minutes']} min, Safe: {res['all_steps_osmotically_safe']}):")
        for st in res["steps"]:
            print(f"  Step {st.step_number}: {st.cpa_concentration_pct:.0f}% CPA ({st.cpa_molarity_m} M) + {st.osmotic_buffer_mannitol_mm:.0f} mM Mannitol at {st.temperature_c:.0f}°C | {st.duration_minutes:.1f} min (Peak V/V0: {st.peak_relative_volume:.3f})")
    elif args.command == "boa":
        from stasispath.boa_connector import project_from_boa_file
        res = project_from_boa_file(
            filepath=args.file,
            age_years=args.age,
            height_cm=args.height,
            weight_kg=args.weight,
            sex=args.sex,
        )
        print(format_multiorgan_markdown_report(res))


if __name__ == "__main__":
    main()


