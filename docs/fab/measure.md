# Blank anatomy measurement guide

This guide explains the M1 to M8 reference parameters used by the shell scripts. It contains no completed measurements. It is not a fit result or an ordering instruction. The selected v4 snap shell has not been printed or validated.

Store any completed guide, photos or parameter overlay in ignored `measurements/`. Do not fill this tracked file with Rolf's measurements. The right-ear orientation in the reference template is a drawing convention, not a physiological result.

## Reference template and limits

The [template](template.pdf) and [packing table](packing-v2.md) describe the historical `A_501015_series_w20_y8_iII_s3` reference. They are not the current 18 mm snap-shell outline. If printed, use 100 percent scale and check its 50 mm bar before using dimensions. A template is not a passive printed fit test.

The historical bow-3 geometry uses a chord of approximately 47.90 mm and a placement allowance of 3 mm. Its M1 gate is approximately 50.90 mm. This is a nominal CAD rule, not an anatomical safety threshold. Recalculate the full folded-board and shell fit after changing parameters.

The values in `scripts/cad/params/default.toml` are examples. A blank measurement is unknown, not evidence that a default fits. Do not connect powered electronics to a body while gathering geometry information.

## M1: ear root length

![M1 reference landmarks](sheets/m1.svg)

Straight distance between the upper and lower points where the ear attaches to the skull. This is not the curved crease length. The generator compares M1 with its reference chord and placement allowance.

## M2: crease arc

![M2 reference landmarks](sheets/m2.svg)

Distance along the crease between the same attachment points. The historical shell overlays hold their reference crease bow fixed. M2 does not automatically resize those exports.

## M3: sulcus clearance

![M3 reference landmarks](sheets/m3.svg)

Clearance between the skull in the crease and the helix rim at mid-ear height. It is a span input, not proof of comfort or pressure tolerance.

## M4: helix root thickness

![M4 reference landmarks](sheets/m4.svg)

Thickness of the cartilage bridge at the upper attachment. The reference generator uses it for hook-root positioning. Do not compress tissue to obtain a smaller value.

## M5: glasses temple thickness

![M5 reference landmarks](sheets/m5.svg)

Thickness of a glasses arm where it passes the ear. A reference value of zero means no glasses allowance. In the original generator, a nonzero value enables a glasses flat, not a complete glasses fit model.

## M6: mastoid offset

![M6 reference landmarks](sheets/m6.svg)

Distance from the crease to the bony prominence behind the lower ear. The reference generator records it rather than moving a contact automatically. Contact-site suitability needs separate review.

## M7: crease top to mid-concha

![M7 reference landmarks](sheets/m7.svg)

Distance along the crease from its upper attachment to the level of the ear-canal opening. It is recorded rather than used as an automatic contact-placement rule.

## M8: helix rise

![M8 reference landmarks](sheets/m8.svg)

Vertical distance from the upper attachment to the highest point of the helix. The original generator uses it in hook-radius construction. The v4 overlay still needs a separate fit review.

## Local record

An anatomy overlay passed to `bte_fit_shell.py --params` should identify its orientation, measurement date, method and uncertainty. Keep that record local. Check accepted parameters with `--help` and follow [CAD instructions](../../scripts/cad/README.md).

The scripts reject some parameter changes because feature constants are fixed. A successful export establishes only the checks reported in its manifest. It does not establish skin compatibility, electrical contact, fit or safety.
