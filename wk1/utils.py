def compute_letterbox(virtual_width, virtual_height, window):
    """
    Compute scale and centered rectangle to render a virtual surface into a window
    while preserving aspect ratio (letterbox/pillarbox).

    Returns (scale, (scaled_width, scaled_height), (offset_x, offset_y)).
    """
    window_width, window_height = window.get_size()

    if virtual_width <= 0 or virtual_height <= 0 or window_width <= 0 or window_height <= 0:
        return 0, (0, 0), (0, 0)

    scale = min(window_width / virtual_width, window_height / virtual_height)
    scaled_width = int(virtual_width * scale)
    scaled_height = int(virtual_height * scale)
    offset_x = (window_width - scaled_width) // 2
    offset_y = (window_height - scaled_height) // 2

    return scale, (scaled_width, scaled_height), (offset_x, offset_y)