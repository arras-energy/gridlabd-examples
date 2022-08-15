def on_init(t):
    object_list = gridlabd.get('objects')
    for obj in object_list:
        data = gridlabd.get_object(obj)
        if "bustype" in data.keys() and data["bustype"] == "SWING":
            gridlabd.set_value("main","parent",obj)

    return True