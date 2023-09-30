import imageprocess

def annotate(ds, image):
    image = imageprocess.draw_line(image, (100,200), (200,300))

    rows = ds.Rows
    columns = ds.Columns

    point1 = (rows // 2, 0)
    point2 = (0, columns // 2)
    point3 = (rows // 2, columns)
    point4 = (rows, columns // 2)

    image = imageprocess.add_text(image, (200,300), "200mm")
    image = imageprocess.add_text(image, (169,0), "H")
    image = imageprocess.add_text(image, (0,169), "R")
    image = imageprocess.add_text(image, (169,330), "F")
    image = imageprocess.add_text(image, (330,169), "L")
    return image