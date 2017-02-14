#!/usr/bin/env python3

from PIL import Image, ImageDraw

def image_from_matrix(matrix, block_size=1):
    """Generates an image from a 2d boolean matrix.

    The matrix can be any data structure that supports ``len`` on both
    dimensions and can be indexed by two subscripts (which is then
    treated as a bool).

    Each element is drawn as a square of the specified `block_size`,
    where 0 is drawn in white and 1 is drawn in black.

    Parameters
    ----------
    matrix : Sequence[Sequence[Any]]
    block_size : int, optional

    Returns
    -------
    PIL.Image.Image

    """
    if block_size <= 0:
        raise ValueError('Block size must be positive.')
    rows = len(matrix)
    columns = len(matrix[0])
    image = Image.new('1', (columns * block_size, rows * block_size), color=1)
    draw = ImageDraw.Draw(image)
    for i in range(rows):
        for j in range(columns):
            if matrix[i][j]:
                x0 = j * block_size
                y0 = i * block_size
                x1 = (j + 1) * block_size - 1
                y1 = (i + 1) * block_size - 1
                draw.rectangle([x0, y0, x1, y1], fill=0)
    del draw
    return image
