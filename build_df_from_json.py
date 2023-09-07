def build_combined_df():

    import pandas as pd
    from globals import convert_empty_list
    from globals import convert_to_datetime

    df_lodz = pd.read_json("/home/kacper/mag_data_liter/urz_marsz_bip_scrapp/umw_news_results_curated/umw_lodz_news_c.json").T

    # set correct datatypes for easier data manipulation
    df_lodz['view_cnt'] = df_lodz['view_cnt'].apply(pd.to_numeric)

    # df_lodz = globals.convert_to_numeric(df_lodz, 'view_cnt')

    # df_lodz[['data_pub', 'data_mod']] = df_lodz[['data_pub', 'data_mod']].apply(pd.to_datetime, format='%d.%m.%Y')
    kolumny = ['data_pub', 'data_mod']

    for kolumna in kolumny:
        df_lodz = convert_to_datetime(df_lodz, kolumna, '%d.%m.%Y')

    # insert umw id
    df_lodz.insert(0, 'umw', 'umw_lodzkiego')

    # insert additional informational column
    df_lodz.insert(6, 'att_list_len', df_lodz['att_link'].str.len())

    # transform empty lists into empty cells

    kolumny = ['att_link', 'att_text']

    for kolumna in kolumny:
        df_lodz[kolumna] = df_lodz[kolumna].apply(convert_empty_list)

    # UMW Lubelskiego

    df_lubel = pd.read_json("/home/kacper/mag_data_liter/urz_marsz_bip_scrapp/umw_news_results_curated/umw_lubel_news_c.json").T

    df_lubel =  convert_to_datetime(df_lubel, 'data_pub', '%Y-%m-%d') 

    df_lubel.insert(0, 'umw', 'umw_lubelskiego')
    df_lubel.insert(6, 'att_list_len', df_lubel['att_link'].str.len())

    kolumny = ['att_text', 'att_link']

    for kolumna in kolumny:
        df_lubel[kolumna] = df_lubel[kolumna].apply(convert_empty_list)

    # UMW Mazowieckiego

    df_maz = pd.read_json("/home/kacper/mag_data_liter/urz_marsz_bip_scrapp/umw_news_results_curated/umw_maz_news_c.json").T

    df_maz =  convert_to_datetime(df_maz, 'data_pub', '%d.%m.%Y')
    df_maz =  convert_to_datetime(df_maz, 'data_mod', '%d.%m.%Y')

    df_maz['view_cnt'] = df_maz['view_cnt'].apply(pd.to_numeric)

    df_maz.dropna(subset = ["url"], inplace=True)

    df_maz.insert(0, 'umw', 'umw_mazowieckiego')
    df_maz.insert(6, 'att_list_len', df_maz['att_text'].str.len())

    df_maz['att_text'] = df_maz['att_text'].apply(convert_empty_list)

    # UMW Podlaskiego

    df_podlas = pd.read_json("/home/kacper/mag_data_liter/urz_marsz_bip_scrapp/umw_news_results_curated/umw_podlas_news_c.json").T

    df_podlas =  convert_to_datetime(df_podlas, 'data_pub', '%Y-%m-%d')
    df_podlas =  convert_to_datetime(df_podlas, 'data_mod', '%Y-%m-%d')

    df_podlas.insert(0, 'umw', 'umw_podlaskiego')
    df_podlas.insert(6, 'att_list_len', df_podlas['att_link'].str.len())

    kolumny = ['att_text', 'att_link']

    for kolumna in kolumny:
        df_podlas[kolumna] = df_podlas[kolumna].apply(convert_empty_list)

    # UMW Wielkopolskiego

    df_wielkopol = pd.read_json("/home/kacper/mag_data_liter/urz_marsz_bip_scrapp/umw_news_results_curated/umw_wielkopol_news_c.json").T

    df_wielkopol =  convert_to_datetime(df_wielkopol, 'data_pub', '%Y-%m-%d %H:%M:%S')
    df_wielkopol =  convert_to_datetime(df_wielkopol, 'data_mod', '%Y-%m-%d %H:%M:%S')

    df_wielkopol.insert(0, 'umw', 'umw_wielkopolskiego')

    # combine all dfs
    frames = [df_lodz, df_lubel, df_maz, df_podlas, df_wielkopol]

    df_all = pd.concat(frames, ignore_index=True)

    try:
        df_all.drop(columns="att_", axis=1, inplace=True)
    except:
        pass

    return df_all