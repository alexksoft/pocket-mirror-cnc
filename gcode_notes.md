# G-code / CAM Notes

## CAM Software
- **Fusion 360** (free for hobbyists) — import STL, generate toolpaths
- **VCarve Pro** — excellent for 2.5D wood projects
- **Estlcam** — simple, effective for 3-axis
- **FreeCAD Path** — free alternative

## Toolpath Strategy

### External Profile (3D contour)
```
Tool: Ball-end R2mm (dia 4mm)
Strategy: 3D contour / spiral
Stepdown: 1mm
Stepover: 0.5mm (finishing)
Stock to leave (rough): 0.5mm
Final pass: climb milling
```

### Mirror/Photo Pocket
```
Tool: Flat-end 6mm
Strategy: Pocket (adaptive clearing)
Stepdown: 1.5mm
Stepover: 50% rough, 10% finish
Entry: Helix ramp 2 deg
Floor: separate finishing pass
```

### Hinge Slot (6mm wide x 4mm deep x 20mm long)
```
Tool: Flat-end 3mm or 6mm
Strategy: Slot milling
Stepdown: 1mm
Entry: Ramp from edge
Leave 0.1mm for final pass
```

### Magnet Hole (dia 6mm x 2.5mm deep)
```
Tool: Drill 6mm or end mill 6mm
Strategy: Boring / peck drilling
Peck: 1mm
```

### Pin Hole (dia 2.5mm, through hinge area)
```
Tool: Drill 2.5mm
Strategy: Drilling
Note: Drill AFTER hinge slot
```

## Work Holding

### Best: Vacuum table
- Flat reference surface required
- Add sacrificial MDF layer

### Alternative: Custom MDF fixture
- Mill negative pocket in MDF
- Place workpiece, secure with toggle clamps
- Best for production runs

### Simple: Double-sided tape
- Apply evenly on spoilboard
- Risk of shift during heavy cuts

## Machine Setup

### GRBL:
```gcode
G21        ; mm mode
G90        ; absolute positioning
G17        ; XY plane
M3 S18000  ; spindle on
G0 Z10     ; safe height
```

## Tips
- Always verify Z-zero before cutting
- Use dust collection
- Monitor for burning (walnut burns easily)
- Keep tools sharp
- Sand with grain direction after machining
