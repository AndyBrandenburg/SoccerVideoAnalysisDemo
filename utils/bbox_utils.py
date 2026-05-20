def get_center_of_bbox(bbox):
    #Gets x and y coordinates of the bounding box
    x1, y1, x2, y2 = bbox
    #Calculates the midpoint between the x values and y values
    return int((x1 + x2) / 2), int((y1 + y2) / 2)

#Takes a bounding box and returns its width
def get_bbox_width(bbox):
    return bbox[2] - bbox[0]
