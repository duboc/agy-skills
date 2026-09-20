# Geometry recipes

All drawing math lives here. Work in meters first, convert to px last.

## Scale

`SCALE = px_per_meter`. Choose so the largest object spans 45–60% of the 680px canvas width.
- Objects ≤1,5 m → SCALE ≈ 220
- Objects ≤3 m → SCALE ≈ 110
- Rooms ≤6 m (floor plans) → SCALE ≈ 60

Conversion: `px = m × SCALE`. Round to integers. Record SCALE in the parameter block.

## Parameter block (always write first)

```
<!-- SCALE: 220 px/m | floor: y=400
     table:  L=1.40m→308px, H=0.90m→198px → top y=202
     camera: h_above_field=1.20m→264px → lens y=... -->
```

Every coordinate in the SVG traces to a line here. On correction, edit here, recompute, redraw.

## FOV cone onto a plane

Camera at P, half-angle θ, plane at perpendicular distance h:
`half_width_m = h × tan(θ)` → intersections at `P.x ± half_width_m × SCALE`.

Typical phone lenses (landscape): main ≈ 75–80° horizontal / ≈ 50° vertical; ultrawide ≈ 105–120° / ≈ 75–85°; telephoto ≈ 30–40°. Prefer the main lens in specs — ultrawide distortion hurts measurement and CV use cases.

Coverage check: target of width W is covered iff `2·h·tan(θ) ≥ W`. State the margin in prose ("covers 1,1 m against a 0,82 m table").

## Angular span (oblique/tilted camera over a plane)

Camera at height h above the plane, target near edge at horizontal distance d₁, far edge at d₂:
- angle to near edge (from vertical): `atan(d₁/h)`
- angle to far edge: `atan(d₂/h)`
- required FOV = difference; center tilt = midpoint.

Fits iff span ≤ lens FOV on the aligned axis. Orient the sensor's long axis along the target's long/depth axis.

## Minimum height to cover a length (overhead camera)

`h_min = (L/2) / tan(FOV_h/2)`, then state the chosen margin separately. Example: L=1,40 m, FOV 78° gives h≈0,864 m; 10% height margin gives ≈0,951 m. A 1,1–1,3 m mounting range is a larger design allowance and must be justified independently.

## Pixel density falloff (oblique views)

Ground sampling distance grows ~linearly with distance from the lens. Rule of thumb worth stating in prose: an object at 2× the distance has ~½ the pixels per cm. Relevant for CV specs (detection at the far end).

## Occlusion shadow (oblique views)

For a point camera at (0,h), a vertical obstacle top at (d,t), and a level plane y=0, the ray through the top intersects the plane at x=h*d/(h-t). The hidden strip behind the obstacle is `t*d/(h-t)`, valid for h>t and d>=0. When t is much smaller than h, `t*d/h` is a first-order approximation; disclose that assumption. If h<=t, this forward ray does not yield a finite ground intersection behind the obstacle. Lens FOV, obstacle width and sensor orientation can further limit visibility.

## Clearances and reach

- Support must reach: mount height + hardware offset ≤ max extension. State both numbers.
- Circulation (floor plans): people need ≥0,60 m to pass, ≥0,80 m to stand and work, ≥1,20 m for two-sided access. Draw clearance zones as dashed rectangles with their own cota.
- Cantilever check: compare load moments, base geometry, hardware ratings and applicable safety factors. Length or mass alone does not establish stability or a required counterweight. Mark missing ratings and treat the drawing as a schematic, not load certification.

## Orthographic projection set

- **Side (elevation, long axis)**: X = length, Y = height. Widths invisible.
- **End (elevation, short axis)**: X = width, Y = height. Lengths invisible — protrusions on the long sides become visible here.
- **Top (plan)**: X = length, Y = width. Heights invisible — annotate heights as text if needed (`h=2,10 m`).

Choose the minimal set that answers the user's question; offer the missing view when it would reveal something (e.g., "a planta mostraria a circulação").

## Worked example (full chain)

"Sensor 1,2 m above a 0,8 m bench, 90° FOV — does it cover?"
1. SCALE 220. Bench 0,8 m → 176px, x=252–428, top y=278. Floor y=400, bench height say 0,75 m → 165px → bench top at y=235... (compute from real bench height, not assumed).
2. Sensor: 1,2 m above bench top → 264px above it.
3. Coverage: 2 × 1,2 × tan(45°) = 2,4 m ≥ 0,8 m → covered, margin 0,8 m per side.
4. Rays to bench-top plane at x = 340 ± 264 (clipped to canvas if needed; note clipping in prose).
5. Cotas: bench width (bottom), sensor-to-bench (internal dashed), total height (left edge).
