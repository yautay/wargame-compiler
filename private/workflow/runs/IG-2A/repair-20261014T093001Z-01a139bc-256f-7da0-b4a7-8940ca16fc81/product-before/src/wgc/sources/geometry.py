"""Exact rectangle conversion for the wgc-inventory-1 coordinate contract."""
from fractions import Fraction
from math import floor, ceil

SCALE = 1_000_000


def fraction(value):
    return Fraction(str(value))


def micro_points(value):
    scaled = fraction(value) * SCALE
    if scaled.denominator != 1:
        raise ValueError('PDF geometry exceeds micro-point precision')
    return int(scaled)


def effective_crop(media, crop):
    box = [max(media[0], crop[0]), max(media[1], crop[1]),
           min(media[2], crop[2]), min(media[3], crop[3])]
    if box[0] >= box[2] or box[1] >= box[3]:
        raise ValueError('CropBox and MediaBox have no positive intersection')
    return box


def check_box(box):
    if (len(box) != 4 or any(type(v) is not int for v in box)
            or not (0 <= box[0] < box[2] <= SCALE and 0 <= box[1] < box[3] <= SCALE)):
        raise ValueError('invalid top-left page-millionths box')


def pdf_to_box(native_box, page):
    """Native unrotated PDF bottom-left units -> enclosing top-left millionths.

    UserUnit scales both the native region and its page, so it cancels here.
    Values outside the effective CropBox fail; there is no silent clipping.
    """
    crop = [Fraction(v, SCALE) for v in page['effective_crop_box']]
    x0, y0, x1, y1 = map(fraction, native_box)
    if not (crop[0] <= x0 < x1 <= crop[2] and crop[1] <= y0 < y1 <= crop[3]):
        raise ValueError('native region outside effective CropBox')
    w, h = crop[2] - crop[0], crop[3] - crop[1]
    return [floor((x0-crop[0])*SCALE/w), floor((crop[3]-y1)*SCALE/h),
            ceil((x1-crop[0])*SCALE/w), ceil((crop[3]-y0)*SCALE/h)]


def box_to_pdf(box, page):
    """Top-left millionths -> exact native PDF bounds (Fractions)."""
    check_box(box)
    x0, y0, x1, y1 = [Fraction(v, SCALE) for v in page['effective_crop_box']]
    w, h = x1-x0, y1-y0
    return [x0+w*box[0]/SCALE, y1-h*box[3]/SCALE,
            x0+w*box[2]/SCALE, y1-h*box[1]/SCALE]


def display_box(box, rotation):
    """Clockwise PDF /Rotate, normalized displayed top-left coordinates."""
    check_box(box)
    x0, y0, x1, y1 = box
    if rotation == 0: return list(box)
    if rotation == 90: return [SCALE-y1, x0, SCALE-y0, x1]
    if rotation == 180: return [SCALE-x1, SCALE-y1, SCALE-x0, SCALE-y0]
    if rotation == 270: return [y0, SCALE-x1, y1, SCALE-x0]
    raise ValueError('rotation must be 0, 90, 180 or 270')


def display_size_points(page):
    x0, y0, x1, y1 = page['effective_crop_box']
    unit = Fraction(page['user_unit']['numerator'], page['user_unit']['denominator'])
    width, height = Fraction(x1-x0, SCALE)*unit, Fraction(y1-y0, SCALE)*unit
    return (height, width) if page['rotation'] in (90, 270) else (width, height)


def overlaps(a, b):
    return max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3])


def area(box):
    return (box[2]-box[0]) * (box[3]-box[1])
