def centroid(hull):
    result = [0, 0]
    det, tempDet = 0, 0
    x_list = [vertex[0] for vertex in hull]
    y_list = [vertex[1] for vertex in hull]

    for i in range(0, len(hull)):
        if i+1 == len(hull):
            j=0
        else:
            j = i+1

        tempDet = x_list[i]*y_list[j] - x_list[j]*y_list[i]
        det +=tempDet

        result[0] += (x_list[i]+x_list[j])*tempDet
        result[1] += (y_list[i]+y_list[j])*tempDet

    result[0] /= 3*det
    result[1] /= 3*det

    return result


