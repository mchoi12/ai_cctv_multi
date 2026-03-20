# core/vlm_model.py

import base64
import cv2
from openai import OpenAI

client = OpenAI(api_key="여기에_본인_API_KEY")  # 환경변수 OPENAI_API_KEY 사용

def analyze_image(frame):
    try:
        # 이미지 → base64
        _, buffer = cv2.imencode('.jpg', frame)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "이 이미지에서 사람 수를 숫자로만 답해줘"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=50
        )

        text = response.choices[0].message.content.strip()

        # 숫자만 추출
        import re
        match = re.search(r'\d+', text)
        people = int(match.group()) if match else 0

        return {"people": people, "objects": []}

    except Exception as e:
        print(f"[VLM ERROR] {e}")
        return {"people": 0, "objects": []}