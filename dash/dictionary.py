from dash import html
import dash_bootstrap_components as dbc

stats = {
    'feature': [
        'Weekly Salary', 'Base Salary', 'ADJ Salary', 'Apps', 'Min', 'G', 'NPG', 'A', 'xG',
        'NPxG', 'xA', 'xGBuildup', 'SpG', 'KeyP',
        'Drb_Off', 'Fouled', 'Off', 'Disp', 'UnsTch', 'Rating', 'Tackles',
        'Inter', 'Fouls', 'Offsides', 'Clear', 'Drb_Def', 'Blocks', 'AvgP', 'PS%'
    ],
    'mean': [
        '주급', '연봉', '조정 연봉', '출전 경기', '출전 시간', '골', '패널티킥 제외 골', '도움', '기대 골',
        '패널티 킥 제외 기대 골', '기대 도움', '특점 확률이 높은 상황에 관여한 정도', '경기 당 슈팅 횟수', '키패스 (슈팅으로 이어진 패스)',
        '드리블 성공', '파울 얻어낸 것', '오프사이드', '패스미드 등으로 볼 소유권 잃음', '드리블 중 볼 소유권 잃음', '평점', '태클 횟수',
        '인터셉트', '파울한 것', '오프사이드 유도', '볼 클리어 횟수', '드리블 허용', '볼 블락', '경기당 패스 횟수', '패스 성공률'
    ]
}


def explain_terms():
    rows = []
    for (feature, mean) in zip(stats['feature'], stats['mean']):
        rows.append(html.Div([html.Span(feature), html.Span(' - '), html.Span(mean)]))
    return html.Div(rows)
