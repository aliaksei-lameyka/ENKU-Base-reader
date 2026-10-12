"""Check thin-pack candidates against unchanged, actual R130 native geometry.

The 10 mm target comes from the historical envelope, not a registered current
enclosure. The STEP contains the real native PCB and a nominal PH-2 envelope;
other component bodies and vendor finished-pack drawings are absent. A failed
trial is retained as evidence. This script cannot authorize manufacture.
"""
import gzip
import hashlib
import io
import json
import math
import zipfile
from pathlib import Path

import cadquery as cq
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle
from PIL import Image

HERE = Path(__file__).resolve().parent
BOARD = HERE.parent
CHECKS = BOARD / "kicad" / "checks"
PCB = BOARD / "kicad" / "enku-mainboard-r0.1.kicad_pcb"
EXPECTED_PCB = "c5b1785535fd7d12c02ee8aaae5b8f96da9404f2bc55d919644b85209ebb4a96"
EXPECTED_ARTIFACT = "5b8b3ef9e41b3176acdd4d893f981fac0b2709a1c37fe8e8a32652b95be1844d"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rectangle_overlap(a, b):
    return max(0.0, min(a[2], b[2]) - max(a[0], b[0])) * max(
        0.0, min(a[3], b[3]) - max(a[1], b[1])
    )


def point_distance(rect, point):
    return math.hypot(
        max(rect[0] - point[0], 0.0, point[0] - rect[2]),
        max(rect[1] - point[1], 0.0, point[1] - rect[3]),
    )


def brick(x, y, z, w, length, t):
    return cq.Workplane("XY").box(w, length, t, centered=False).translate((x, y, z)).val()


assert sha(PCB) == EXPECTED_PCB
artifact = CHECKS / "native_server_R130.zip"
assert sha(artifact) == EXPECTED_ARTIFACT
geometry = json.loads(gzip.decompress((CHECKS / "geometry_checkpoint_R130.json.gz").read_bytes()))
with zipfile.ZipFile(artifact) as z:
    assert z.testzip() is None
    assert z.read("source_pcb.sha256").decode().split()[0] == EXPECTED_PCB
    assert json.loads(z.read("geometry.json")) == geometry
    actual_server = json.loads(z.read("server_comparison.json"))
    assert actual_server["server_matches_local_checkpoint"] is True
    assert actual_server["opens"] == actual_server["ERC"] == actual_server["schematic_parity"] == 0
    assert actual_server["drc_types"] == {"hole_clearance": 20}
    assert z.read("version.txt").decode().strip() == "10.0.7"

assert geometry["bbox"] == [18, 20, 77, 121]
rf = next(z for z in geometry["zones"] if z["rule"] and z["no_pads"] and z["layers"] == [0, 2, 4, 6])
assert len(rf["polygons"]) == 1
rf_points = rf["polygons"][0]
assert sorted(map(tuple, rf_points)) == sorted([(26.25, 69), (26.25, 21), (5.25, 21), (5.25, 69)])
rf_rect = [5.25, 21, 26.25, 69]
holes = {p["ref"]: p["pos"] for p in geometry["pads"] if p["ref"] in ("H1", "H2", "H3", "H4")}
old = json.loads((HERE / "BAT_REV3_mechanical_audit_R130.json").read_text())
assert holes == old["hole_centers_mm"]
selection = json.loads((BOARD / "bom" / "battery_selection_R131.json").read_text())
assert selection["case_increase_allowed"] is False

native_step = HERE / "native_board_PH2_R130.step"
assert sha(native_step) == old["native_STEP_sha256"]
native = cq.importers.importStep(str(native_step)).val().mirror("XZ")
bounds = native.BoundingBox()
assert abs(bounds.xmin - 18) < 1e-6 and abs(bounds.ymin - 20) < 1e-6
assert abs(bounds.xmax - 77) < 1e-6 and abs(bounds.ymax - 121) < 1e-6
ph_top = bounds.zmax
assert abs(ph_top - old["native_PH2_top_Z_mm"]) < 1e-6
ph_xy = [64.6, 90.55, 74.2, 98.45]
ph_reserved = brick(ph_xy[0], ph_xy[1], ph_top - 5.5, 9.6, 7.9, 5.5)

assumptions = old["scenario_assumptions"]
front_min = -(assumptions["front_wall_mm"] + assumptions["display_T_mm"] + assumptions["front_display_gap_mm"])
target = float(selection["historical_reference_case_target_mm"])
rear_inner = front_min + target - assumptions["rear_wall_mm"]
pcb_t = old["native_KiCad_board_T_mm"]
low_pack_z = pcb_t + assumptions["component_pack_insulation_gap_mm"]
x0, y0 = 26.75, 28.0
boss_radius = assumptions["boss_diameter_mm"] / 2
plan_gap = assumptions["plan_clearance_mm"]
rows = []
candidates = [selection["primary_candidate"], selection["thinner_wider_alternative"],
              dict(model="LP355380", supplier="Polybattery", capacity_mAh=2000, T_mm=3.5, W_mm=53, L_mm=80),
              dict(model="315088", supplier="Koosay", capacity_mAh=2000, T_mm=3.1, W_mm=50, L_mm=88)]
for candidate in candidates:
    t, w, length = (candidate[k] for k in ("T_mm", "W_mm", "L_mm"))
    rect = [x0, y0, x0 + w, y0 + length]
    pack = brick(x0, y0, low_pack_z, w, length, t)
    analytic_volume = rectangle_overlap(rect, ph_xy) * max(0.0, min(low_pack_z + t, ph_top) - max(low_pack_z, ph_top - 5.5))
    actual_volume = pack.intersect(ph_reserved).Volume()
    assert abs(actual_volume - analytic_volume) < 1e-6
    rows.append(dict(**candidate, trial_xy_mm=[x0, y0], trial_pack_base_Z_mm=low_pack_z,
                     nominal_pack_top_Z_mm=low_pack_z + t,
                     RF_reserved_overlap_mm2=rectangle_overlap(rect, rf_rect),
                     beyond_board_edge_mm=max(0.0, rect[2] - 77),
                     beyond_previous_board_minus_0_5mm_margin_mm=max(0.0, rect[2] - 76.5),
                     nominal_end_room_before_assumed_H4_boss_mm=113.5 - rect[3],
                     boss_violations=[ref for ref, point in holes.items() if point_distance(rect, point) < boss_radius + plan_gap - 1e-9],
                     PH2_reserved_intersection_mm3=actual_volume,
                     confirmed_finished_pack_maximum_mm=None,
                     current_layout_fit_qualified=False))

# A continuous interval argument, not a grid sampling result. Allowing zero PCB
# edge margin, every 50x84 pouch wholly within the board and outside the unchanged
# RF polygon must start in x=[26.25,27]. With the declared 5 mm bosses +0.5 mm gap,
# top H2 and bottom H4 constrain y to [28,29.5]. Every such rectangle contains J1.
w, length = 50.0, 84.0
x_interval = [rf_rect[2], geometry["bbox"][2] - w]
y_interval = [holes["H2"][1] + boss_radius + plan_gap,
              holes["H4"][1] - boss_radius - plan_gap - length]
assert x_interval == [26.25, 27.0] and y_interval == [28.0, 29.5]
assert x_interval[1] <= ph_xy[0] and x_interval[0] + w >= ph_xy[2]
assert y_interval[1] <= ph_xy[1] and y_interval[0] + length >= ph_xy[3]
proof = dict(edge_margin_mm=0, candidate_plan_W_L_mm=[w, length],
             RF_clear_x_start_interval_mm=x_interval,
             assumed_boss_clear_y_start_interval_mm=y_interval,
             minimum_J1_XY_overlap_mm2=(ph_xy[2] - ph_xy[0]) * (ph_xy[3] - ph_xy[1]),
             XY_translation_alone_can_remove_overlap=False,
             assumptions_are_not_registered_enclosure_dimensions=True)

primary = rows[0]
assert primary["model"] == "335084" and primary["RF_reserved_overlap_mm2"] == 0
assert primary["boss_violations"] == [] and primary["beyond_board_edge_mm"] == 0
assert abs(primary["beyond_previous_board_minus_0_5mm_margin_mm"] - 0.25) < 1e-6
assert primary["PH2_reserved_intersection_mm3"] > 250
assert ph_top > rear_inner  # Current nominal header alone violates this 10 mm reference stack.

failed = cq.Assembly(name="R131_FIXED_10mm_REFERENCE_TRIAL_FAILED_NOT_RELEASED")
failed.add(native, name="native_R130_PCB_and_nominal_PH2_envelope", color=cq.Color(.1, .5, .3))
failed.add(brick(x0, y0, low_pack_z, 50, 84, 3.3),
           name="335084_catalogue_cell_only_INTENTIONAL_PH2_INTERSECTION", color=cq.Color(.2, .4, .9, .5))
trial_step = HERE / "thin_battery_fixed_10mm_failed_trial_R131.step"
failed.save(str(trial_step))
roundtrip = cq.importers.importStep(str(trial_step)).val()
assert abs(roundtrip.Volume() - (native.Volume() + 50 * 84 * 3.3)) < 1e-5
assert abs(roundtrip.BoundingBox().zmax - ph_top) < 1e-6

report = dict(revision="R131 selection study, hardware R130 unchanged", selected_cell="Koosay 335084",
              tested_hardware_commit="889a069afb8aed9515fbff6daba5f5e659ff9753",
              preserved_R130_proof_commit="04a8344f1f71e6bdebb8cb8815ccbac8292fa6cc",
              source_pcb_sha256=sha(PCB), actual_native_artifact_sha256=sha(artifact),
              actual_artifact_CRC_verified=True, actual_native_geometry_matches_checkpoint=True,
              actual_native_server_comparison=actual_server, native_STEP_sha256=sha(native_step),
              historical_fixed_reference_case_T_mm=target, user_approved_case_increase=False,
              current_registered_enclosure_dimensions_mm=None,
              scenario_assumptions=assumptions, source_outline_mm=geometry["bbox"],
              source_RF_polygon_mm=rf_points, source_holes_mm=holes,
              nominal_PH2_top_Z_mm=ph_top, reference_rear_inner_Z_mm=rear_inner,
              nominal_PH2_excess_over_reference_rear_inner_mm=ph_top - rear_inner,
              candidates=rows, continuous_translation_result=proof,
              failed_trial_STEP_sha256=sha(trial_step),
              failed_trial_STEP_reimport_volume_and_height_verified=True,
              all_actual_component_bodies_checked=False, finished_pack_drawing_checked=False,
              thinner_pack_alone_solves_current_reference_stack=False,
              next_layout_goal="Separate battery and tall components in XY or change the packaging topology within the fixed case target; recheck actual component and panel bodies before a PCB placement change.",
              analytical_and_CAD_checks_passed=True, current_layout_mechanical_fit_passed=False,
              mechanical_release_accepted=False, purchase_release_accepted=False, fabrication_ready=False)
(HERE / "thin_battery_audit_R131.json").write_text(json.dumps(report, indent=2) + "\n")

fig, (plan, section) = plt.subplots(1, 2, figsize=(14, 10), gridspec_kw={"width_ratios": [1.1, 1]})
plan.add_patch(Rectangle((18, 20), 59, 101, fill=False, edgecolor="#216b4e", linewidth=2, label="Actual PCB: 59 x 101 x 1.6 mm"))
for pad in geometry["pads"]:
    for poly in pad["polygons"].get("0", []):
        plan.add_patch(Polygon(poly, color="#999999", alpha=.25, linewidth=0))
plan.add_patch(Polygon(rf_points, facecolor="#edb52c", alpha=.3, hatch="//", label="Actual RF metal restriction"))
for row, color in zip(rows[:3], ["#216aca", "#bb4444", "#7a54a3"]):
    plan.add_patch(Rectangle((x0, y0), row["W_mm"], row["L_mm"], fill=False, linewidth=2,
                            edgecolor=color, label=f"{row['model']}: {row['T_mm']} x {row['W_mm']} x {row['L_mm']} mm"))
plan.add_patch(Rectangle((ph_xy[0], ph_xy[1]), 9.6, 7.9, facecolor="#b88331", alpha=.7))
plan.text(69.4, 94.5, "PH-2", ha="center", va="center", fontsize=9)
for ref, point in holes.items():
    plan.add_patch(Circle(point, boss_radius, fill=False, color="#333333", linestyle="--"))
    plan.text(*point, ref, ha="center", va="center", fontsize=8)
plan.set(xlim=(14, 84), ylim=(125, 17), xlabel="KiCad X / mm", ylabel="KiCad Y / mm")
plan.set_aspect("equal")
plan.grid(alpha=.15)
plan.set_title("Candidate plans on actual native coordinates\n5 mm bosses / 0.5 mm gap are study assumptions", fontsize=11)
plan.legend(loc="upper center", bbox_to_anchor=(.5, -.08), fontsize=9)

section.axhspan(0, pcb_t, color="#216b4e", alpha=.2)
section.axhline(rear_inner, color="#a92d2d", linestyle="--", linewidth=2,
                label=f"Rear inner plane for fixed 10 mm reference: Z={rear_inner:.2f}")
section.add_patch(Rectangle((.1, ph_top - 5.5), .65, 5.5, facecolor="#b88331", alpha=.85))
section.add_patch(Rectangle((1.1, low_pack_z), .65, 3.3, facecolor="#216aca", alpha=.65))
section.text(.425, ph_top + .16, "PH-2\n5.5 mm nominal", ha="center", fontsize=10)
section.text(1.425, low_pack_z + 3.3 + .16, "335084\n3.3 mm nominal cell", ha="center", fontsize=10)
section.set(xlim=(-.05, 1.95), ylim=(-.1, 8.7), ylabel="Z from native PCB bottom / mm")
section.set_xticks([])
section.grid(axis="y", alpha=.2)
section.set_title("Current reference stack fails\nBars compare heights; they are not separate XY bays", fontsize=11)
section.legend(loc="upper left", fontsize=8)
fig.suptitle("ENKU R131: thinner battery, unchanged case target — NO MECHANICAL RELEASE", fontsize=14, y=.98)
fig.text(.51, .13, f"Primary: 335084, advertised 2000 mAh. Finished PCM pack maximum: unknown.\n"
         f"Nominal PH-2 exceeds the reference rear inner plane by {ph_top - rear_inner:.3f} mm.\n"
         f"Low pouch intersects its reserved envelope: {primary['PH2_reserved_intersection_mm3']:.2f} mm³.\n"
         "XY translation alone cannot clear PH-2 inside the declared RF/boss region.\n"
         "Other bodies, real enclosure, insulation/NTC retention and swelling are not qualified.", fontsize=9)
fig.subplots_adjust(top=.90, bottom=.25, wspace=.32)
png_bytes = io.BytesIO()
fig.savefig(png_bytes, format="png", dpi=150)
Image.open(io.BytesIO(png_bytes.getvalue())).verify()
(HERE / "thin_battery_fixed_target_R131.png").write_bytes(png_bytes.getvalue())
Image.open(HERE / "thin_battery_fixed_target_R131.png").verify()
plt.close(fig)
print(json.dumps({"selected_cell": report["selected_cell"], "native_geometry_verified": True,
                  "nominal_PH2_excess_mm": report["nominal_PH2_excess_over_reference_rear_inner_mm"],
                  "PH2_intersection_mm3": primary["PH2_reserved_intersection_mm3"],
                  "current_layout_fit_passed": False, "fabrication_ready": False}, indent=2))
