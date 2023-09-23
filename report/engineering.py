import os.path

import pandas as pd


def get_player(parent_path):
    return pd.read_csv(f'{parent_path}/new/players_all.csv').drop('Unnamed: 0', axis=1)


def generate_eda_path(parent_path):
    return f'{parent_path}/new/eda_all.csv'


def save_df(parent_path, df):
    df.to_csv(generate_eda_path(parent_path), index=False)
    return df


def exists_final_csv(parent_path):
    return os.path.exists(generate_eda_path(parent_path))


def get_xbet(parent_path):
    df = (pd.read_csv(f'{parent_path}/new/1xbet_all.csv')
          .drop(['Team', 'Age', 'Position'], axis=1)
          .rename(columns={'Drb_x': 'Drb_Off', 'Drb_y': 'Drb_Def'}))
    df['Rating'] = df['Rating'] * 10
    return df


def get_understat(parent_path):
    return pd.read_csv(f'{parent_path}/new/understat_all.csv').drop(['No', 'Team'], axis=1)


def get_capology(parent_path):
    return pd.read_csv(f'{parent_path}/new/capology_all.csv')


def merge(player_df, xbet_df, understat_df, capology_df):
    # 프로필 + 연봉
    eda_df = player_df.merge(capology_df[['Weekly Salary', 'Base Salary', 'ADJ Salary', 'Name', 'year']], how='left',
                             left_on=['Name', 'year'], right_on=['Name', 'year'])
    eda_df = eda_df[~eda_df.duplicated(['year', 'Name'], keep='first')]  # 중복 제거
    # 프로필 + 연봉 + 스텟(understat)
    eda_df = eda_df.merge(understat_df, how='left', left_on=['Name', 'year'], right_on=['Name', 'year'])

    # 프로필 + 연봉 + 스텟(understat) + 스텟(1xbet)
    eda_df = eda_df.merge(
        xbet_df[[
            'Name', 'year', 'SpG', 'KeyP', 'Drb_Off', 'Fouled', 'Off',
            'Disp', 'UnsTch', 'Rating', 'Tackles', 'Inter', 'Fouls',
            'Offsides', 'Clear', 'Drb_Def', 'Blocks', 'AvgP', 'PS%']],
        how='left',
        left_on=['Name', 'year'],
        right_on=['Name', 'year']
    )
    return eda_df


age_order = ['<21', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '32<']


def feature_check(eda_df):
    eda_df = eda_df.copy()
    eda_df = eda_df.dropna()
    eda_df['Age Lev'] = eda_df['Age'].apply(lambda age: '<21' if age < 21 else '32<' if age > 32 else f'{age}')
    eda_df['Age Lev'] = pd.Categorical(eda_df['Age Lev'], categories=age_order, ordered=True)
    return eda_df


def get_data(parent_path='../data'):
    if exists_final_csv(parent_path):
        print(f'load final csv file, file : {generate_eda_path(parent_path)}')
        return pd.read_csv(generate_eda_path(parent_path))
    else:
        print(f'start to merge csv files')
        # plyaer data load 및 정리(프로필)
        player_df = get_player(parent_path)
        # 1xbet data load 및 정리(스텟)
        xbet_df = get_xbet(parent_path)
        # understat data load 및 정리(스텟)
        understat_df = get_understat(parent_path)
        # capology load(연봉)
        capology_df = get_capology(parent_path)
        eda_df = merge(player_df, xbet_df, understat_df, capology_df)
        print(f'complete to merge csv files, save to csv({generate_eda_path(parent_path)})')
        return save_df(parent_path, feature_check(eda_df))
