#!/usr/bin/env python3
"""
Pocket Mirror 3D Model - STL Generator for CNC Manufacturing
No external dependencies. Run: python3 generate_stl.py
Output: pocket_mirror_top.stl, pocket_mirror_bottom.stl, pocket_mirror_assembly.stl
"""
import struct, math

# === PARAMETERS (mm) ===
DIAMETER = 70.0
RADIUS = DIAMETER / 2
HALF_HEIGHT = 8.0
MIRROR_DIAMETER = 58.0
MIRROR_DEPTH = 2.0
MIRROR_LIP = 1.0
PHOTO_DIAMETER = 58.0
PHOTO_DEPTH = 2.0
FILLET_RADIUS = 2.0
SEGMENTS = 72
FILLET_SEGMENTS = 8


def compute_normal(v1, v2, v3):
    u = (v2[0]-v1[0], v2[1]-v1[1], v2[2]-v1[2])
    v = (v3[0]-v1[0], v3[1]-v1[1], v3[2]-v1[2])
    nx = u[1]*v[2] - u[2]*v[1]
    ny = u[2]*v[0] - u[0]*v[2]
    nz = u[0]*v[1] - u[1]*v[0]
    l = math.sqrt(nx*nx + ny*ny + nz*nz)
    return (nx/l, ny/l, nz/l) if l > 1e-10 else (0, 0, 1)


def write_stl(filename, tris):
    with open(filename, 'wb') as f:
        f.write(b'Pocket Mirror CNC' + b'\0' * 62)
        f.write(struct.pack('<I', len(tris)))
        for t in tris:
            n = compute_normal(*t)
            f.write(struct.pack('<fff', *n))
            for v in t:
                f.write(struct.pack('<fff', *v))
            f.write(struct.pack('<H', 0))
    print(f"  {filename}: {len(tris)} triangles")


def circle(r, z, segs=SEGMENTS):
    return [(r*math.cos(2*math.pi*i/segs),
             r*math.sin(2*math.pi*i/segs), z) for i in range(segs)]


def disc(c, pts, flip=False):
    n = len(pts)
    t = []
    for i in range(n):
        j = (i+1) % n
        t.append((c, pts[j], pts[i]) if flip else (c, pts[i], pts[j]))
    return t


def wall(b, tp):
    n = len(b)
    tr = []
    for i in range(n):
        j = (i+1) % n
        tr.append((b[i], b[j], tp[j]))
        tr.append((b[i], tp[j], tp[i]))
    return tr


def annular(o, inn, flip=False):
    n = len(o)
    tr = []
    for i in range(n):
        j = (i+1) % n
        if flip:
            tr.append((o[j], o[i], inn[i]))
            tr.append((o[j], inn[i], inn[j]))
        else:
            tr.append((o[i], o[j], inn[j]))
            tr.append((o[i], inn[j], inn[i]))
    return tr


def gen_top():
    """Top half (lid) with mirror recess. z=0 is recess floor, z=MIRROR_DEPTH+HALF_HEIGHT is top."""
    t = []
    z0 = 0
    zm = MIRROR_DEPTH
    zt = MIRROR_DEPTH + HALF_HEIGHT
    ro = RADIUS
    rl = MIRROR_DIAMETER/2 + MIRROR_LIP
    rf = RADIUS - FILLET_RADIUS

    # Mating face annular ring
    t.extend(annular(circle(rf, zm), circle(rl, zm), flip=True))
    # Mirror recess wall
    t.extend(wall(circle(rl, z0), circle(rl, zm)))
    # Mirror recess floor
    t.extend(disc((0, 0, z0), circle(rl, z0), flip=True))

    # Outer shell with fillet
    rings = []
    for i in range(FILLET_SEGMENTS+1):
        a = math.pi/2 * (1 - i/FILLET_SEGMENTS)
        r = ro - FILLET_RADIUS + FILLET_RADIUS*math.cos(a)
        z = zm + FILLET_RADIUS - FILLET_RADIUS*math.sin(a)
        rings.append(circle(min(r, ro), max(z, zm)))
    rings.append(circle(ro, zm + FILLET_RADIUS))
    rings.append(circle(ro, zt - FILLET_RADIUS))
    for i in range(FILLET_SEGMENTS+1):
        a = math.pi/2 * i/FILLET_SEGMENTS
        r = ro - FILLET_RADIUS + FILLET_RADIUS*math.cos(a)
        z = zt - FILLET_RADIUS + FILLET_RADIUS*math.sin(a)
        rings.append(circle(r, min(z, zt)))

    for i in range(len(rings)-1):
        t.extend(wall(rings[i], rings[i+1]))
    t.extend(annular(rings[0], circle(rf, zm), flip=True))
    t.extend(disc((0, 0, zt), rings[-1], flip=False))
    return t


def gen_bottom():
    """Bottom half (base) with photo recess. z=0 is bottom, z=HALF_HEIGHT is mating face."""
    t = []
    zm = HALF_HEIGHT
    zr = HALF_HEIGHT - PHOTO_DEPTH
    ro = RADIUS
    rp = PHOTO_DIAMETER/2

    # Outer shell with fillet
    rings = []
    for i in range(FILLET_SEGMENTS+1):
        a = math.pi/2 * (1 - i/FILLET_SEGMENTS)
        r = ro - FILLET_RADIUS + FILLET_RADIUS*math.cos(a)
        z = FILLET_RADIUS - FILLET_RADIUS*math.sin(a)
        rings.append(circle(r, max(z, 0)))
    rings.append(circle(ro, FILLET_RADIUS))
    rings.append(circle(ro, zm - FILLET_RADIUS))
    for i in range(FILLET_SEGMENTS+1):
        a = math.pi/2 * i/FILLET_SEGMENTS
        r = ro - FILLET_RADIUS + FILLET_RADIUS*math.cos(a)
        z = zm - FILLET_RADIUS + FILLET_RADIUS*math.sin(a)
        rings.append(circle(r, min(z, zm)))

    for i in range(len(rings)-1):
        t.extend(wall(rings[i], rings[i+1]))
    # Bottom cap
    t.extend(disc((0, 0, 0), rings[0], flip=True))
    # Top face with recess
    t.extend(annular(rings[-1], circle(rp, zm), flip=False))
    # Recess wall
    t.extend(wall(circle(rp, zm), circle(rp, zr)))
    # Recess floor
    t.extend(disc((0, 0, zr), circle(rp, zr), flip=False))
    return t


if __name__ == "__main__":
    print("=" * 50)
    print("POCKET MIRROR - STL Generator for CNC")
    print("=" * 50)
    print(f"  Diameter: {DIAMETER} mm")
    print(f"  Total height: {HALF_HEIGHT*2} mm")
    print(f"  Mirror recess: dia {MIRROR_DIAMETER} mm, depth {MIRROR_DEPTH} mm")
    print(f"  Photo recess: dia {PHOTO_DIAMETER} mm, depth {PHOTO_DEPTH} mm")
    print(f"  Edge fillet: R{FILLET_RADIUS} mm")
    print()

    top = gen_top()
    write_stl("pocket_mirror_top.stl", top)

    bot = gen_bottom()
    write_stl("pocket_mirror_bottom.stl", bot)

    asm = list(bot) + [tuple((v[0], v[1], v[2] + HALF_HEIGHT + 1) for v in tri) for tri in top]
    write_stl("pocket_mirror_assembly.stl", asm)

    print()
    print("Done! Import STL files into Fusion 360 / VCarve / Estlcam for CAM.")
    print()
    print("CNC notes:")
    print(f"  - Stock size per half: {DIAMETER+4} x {DIAMETER+4} x {HALF_HEIGHT+4} mm")
    print(f"  - 2-sided machining recommended")
    print(f"  - Ball-end R2mm for fillet, flat 6mm for pockets")
