from dash import html

stats_word = {
    'A': '도움',
    'ADJ Salary': '조정 연봉',
    'Apps': '출전 경기',
    'AvgP': '경기당 패스 횟수',
    'Base Salary': '연봉',
    'Blocks': '공 블락',
    'Clear': '공 클리어 횟수',
    'Disp': '공 소유권 잃음(패스 실수)',
    'Drb_Def': '드리블 허용',
    'Drb_Off': '드리블 성공',
    'Fouled': '파울 얻어낸 것',
    'Fouls': '파울한 것',
    'G': '골',
    'Inter': '인터셉트',
    'KeyP': '슈팅으로 이어진 패스',
    'Min': '출전 시간',
    'NPG': '골(패널티킥 제외)',
    'NPxG': '기대 골(패널티킥 제외)',
    'Off': '오프사이드',
    'Offsides': '오프사이드 유도',
    'PS%': '패스 성공률',
    'Rating': '평점',
    'SpG': '경기 당 슈팅 횟수',
    'Tackles': '태클 횟수',
    'UnsTch': '공 소유권 잃음(드리블)',
    'Weekly Salary': '주급',
    'xA': '기대 도움',
    'xG': '기대 골',
    'xGBuildup': '득점에 관여한 정도(마무리 제외)',
    'xGChain': '득점에 관여한 정도',
}


def explain_terms():
    rows = [html.Div(html.H4('< Feature 설명 >'))]
    for feature, mean in stats_word.items():
        rows.append(
            html.Div(
                [html.Span(feature, style={'color': 'red'}), html.Span(' - '), html.Span(mean, style={'color': 'blue'})],
                style={'fontSize': 18}
            )
        )
    return html.Div(rows, style={'marginLeft': 20, 'marginTop': 20})
