import multiprocessing

def internalViewshedAlgorithm(n,analysis_type,dem,precision,miss_params,item):
        matrix_vis = ws.viewshed_raster (analysis_type, item[1], dem, interpolate = precision > 0)
        mask = [item[1]["radius"]]
 
        inner_radius_specified = "radius_in" not in miss_params
 
        if inner_radius_specified:
            mask += [ item[1]["radius_in"] ]
 
        if  "azim_1" not in miss_params and  "azim_2" not in miss_params:
            if not inner_radius_specified:
                mask += [ None ]
 
            mask += [ item[1]["azim_1"], item[1]["azim_2"] ]
            print (mask)
 
        dem.set_mask(*mask)
 
        r = dem.add_to_buffer (matrix_vis, n, report = True)
        return [item[1]["id"],*r]

if __name__ == '__main__':
    n = 1
    analysis_type = 1
    dem = 1
    precision = 1
    miss_params = 1

    # Create a list of items to process
    pt = {
        "point1": 2,
        "point2": 5,
        "point3": 1,
        "point4": 0
    }
    # Create a Manager to handle the shared result array
    manager = multiprocessing.Manager()
    result = manager.list()
    items = pt.items()

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.starmap(
            internalViewshedAlgorithm, 
            [(n, analysis_type, dem, precision, miss_params, item) for item in items]
        )

        result.extend(results)

    # Access the final result array
    print(result)