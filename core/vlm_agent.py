# core/vlm_agent.py

def generate_description(event, count):
    """
    VLM 스타일 자연어 생성
    """

    if event == "crowd":
        return f"다수 인원({count}명)이 밀집하여 안전 사고 위험이 높은 상황입니다."

    elif event == "loitering":
        return f"{count}명이 특정 구역에 머무르며 비정상적인 배회 행동이 감지되었습니다."

    elif event == "fight":
        return "폭력 행위로 의심되는 상황이 감지되었습니다."

    elif event == "fall":
        return "사람이 쓰러진 것으로 보이는 응급 상황이 감지되었습니다."

    return "정상 상황입니다."