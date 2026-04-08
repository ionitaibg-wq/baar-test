text_email = f"""
Procedura BAAR OMNIASIG – documente primite

Nr. Caz BAAR: {nr_caz}
Șasiu auto: {sasiu}
Data start / valabilitate poliță: {data_start}

Intermediere: {intermediar}
Cod RAF: {cod_raf}

Tip proprietar: {request.form.get("tip_proprietar")}
Proprietar auto: {proprietar}
"""
