// ============================================================
// POCKET MIRROR - Parametric 3D Model for CNC Woodworking
// Material: Walnut / Oak / Beech
// Units: millimeters
// ============================================================

// === PARAMETERS (edit these) ===
mirror_diameter = 70;
mirror_radius = mirror_diameter / 2;
wall_thickness = 4;
total_height = 16;
half_height = total_height / 2;

mirror_insert_diameter = 58;
mirror_insert_depth = 2;
mirror_lip = 1;

photo_insert_diameter = 58;
photo_insert_depth = 2;

edge_fillet = 2;

hinge_barrel_diameter = 5;
hinge_barrel_length = 20;
hinge_pin_diameter = 2.5;
hinge_recess_width = 6;
hinge_recess_depth = 3;

magnet_diameter = 6;
magnet_depth = 2.5;

$fn = 120;

// === MODULES ===

module rounded_cylinder(r, h, fillet) {
    hull() {
        translate([0, 0, fillet])
            rotate_extrude()
                translate([r - fillet, 0, 0])
                    circle(r = fillet);
        translate([0, 0, h - fillet])
            rotate_extrude()
                translate([r - fillet, 0, 0])
                    circle(r = fillet);
    }
}

module top_half() {
    difference() {
        rounded_cylinder(mirror_radius, half_height, edge_fillet);

        // Mirror recess
        translate([0, 0, -0.01])
            cylinder(d = mirror_insert_diameter + 2*mirror_lip, h = mirror_insert_depth + 0.01);
        translate([0, 0, -0.01])
            cylinder(d = mirror_insert_diameter, h = mirror_insert_depth + mirror_lip + 0.01);

        // Hinge channel
        translate([0, -mirror_radius + hinge_recess_depth/2, half_height/2])
            cube([hinge_recess_width, hinge_recess_depth, half_height + 1], center = true);

        // Hinge pin hole
        translate([0, -mirror_radius + hinge_recess_depth, half_height/2])
            rotate([0, 90, 0])
                cylinder(d = hinge_pin_diameter + 0.5, h = hinge_barrel_length + 2, center = true);

        // Magnet hole
        translate([0, mirror_radius - wall_thickness - magnet_diameter/2, magnet_depth/2])
            cylinder(d = magnet_diameter, h = magnet_depth + 0.01);

        // Mating lip recess
        translate([0, 0, -0.01])
            cylinder(d = mirror_diameter - 2*wall_thickness + 0.3, h = 1.5 + 0.01);
    }
}

module bottom_half() {
    difference() {
        rounded_cylinder(mirror_radius, half_height, edge_fillet);

        // Photo recess
        translate([0, 0, half_height - photo_insert_depth])
            cylinder(d = photo_insert_diameter, h = photo_insert_depth + 0.01);

        // Hinge channel
        translate([0, -mirror_radius + hinge_recess_depth/2, half_height/2])
            cube([hinge_recess_width, hinge_recess_depth, half_height + 1], center = true);

        // Hinge pin hole
        translate([0, -mirror_radius + hinge_recess_depth, half_height/2])
            rotate([0, 90, 0])
                cylinder(d = hinge_pin_diameter + 0.5, h = hinge_barrel_length + 2, center = true);

        // Magnet hole
        translate([0, mirror_radius - wall_thickness - magnet_diameter/2, half_height - magnet_depth])
            cylinder(d = magnet_diameter, h = magnet_depth + 0.01);
    }

    // Mating lip
    difference() {
        translate([0, 0, half_height - 0.01])
            cylinder(d = mirror_diameter - 2*wall_thickness, h = 1.5);
        translate([0, 0, half_height - 0.02])
            cylinder(d = mirror_diameter - 2*wall_thickness - 2, h = 1.52);
    }
}

module hinge_pin() {
    color("gold")
        cylinder(d = hinge_pin_diameter, h = hinge_barrel_length);
}

// === ASSEMBLIES ===

module assembly_closed() {
    color("SaddleBrown") {
        bottom_half();
        translate([0, 0, total_height])
            rotate([180, 0, 0])
                top_half();
    }
    translate([-hinge_barrel_length/2, -mirror_radius + hinge_recess_depth, total_height/2])
        rotate([0, 90, 0])
            hinge_pin();
}

module assembly_open() {
    color("SaddleBrown") {
        bottom_half();
        translate([0, -mirror_radius + hinge_recess_depth, half_height])
            rotate([120, 0, 0])
                translate([0, mirror_radius - hinge_recess_depth, 0])
                    top_half();
    }
}

module cnc_layout() {
    translate([-mirror_radius - 5, 0, 0])
        color("SaddleBrown") top_half();
    translate([mirror_radius + 5, 0, 0])
        color("SaddleBrown") bottom_half();
}

// === RENDER (uncomment desired view) ===
assembly_closed();
// assembly_open();
// cnc_layout();
// top_half();
// bottom_half();
