from fastapi import APIRouter
from sentence_transformers import SentenceTransformer, util
from database import SessionLocal
from models import Title
import json
import numpy as np

router = APIRouter(prefix="/api/title")


@router.get("/list")
def title_list(user_input: str):
    # 데이터베이스 세션 열기
    db = SessionLocal()

    # 입력값에서 공백 제거
    # user_input = user_input.replace(" ", "")

    # 유사도 계산 및 결과 저장할 딕셔너리
    similarity_dict = {}

    # 입력값과 유사한 작품들 찾기
    input_title = db.query(Title).filter(Title.title == user_input).first()

    if input_title:
        input_vector_str = input_title.vector  # 데이터베이스에서 문자열 형식의 벡터 데이터 가져오기

        # JSON 형식의 문자열을 파싱하여 NumPy 배열로 변환
        input_vector = np.array(json.loads(input_vector_str))

        titles = db.query(Title).all()

        for title in titles:
            vector_str = title.vector  # 데이터베이스에서 문자열 형식의 벡터 데이터 가져오기
            vector = np.array(json.loads(vector_str))  # JSON 문자열을 NumPy 배열로 변환
            similarity = util.cos_sim(input_vector, vector)
            similarity_dict[title.title] = similarity

        # 결과를 유사도 높은 순으로 정렬
        sorted_similarity = sorted(similarity_dict.items(), key=lambda x: x[1], reverse=True)

        # 입력값과 동일한 경우는 제외
        if sorted_similarity and sorted_similarity[0][0] == user_input:
            sorted_similarity.pop(0)

        # 상위 5개 결과 반환
        result = dict(sorted_similarity[:5])
    else:
        result = {"message": "작품을 찾을 수 없습니다. 줄거리를 입력해주세요."}

    # 데이터베이스 세션 닫기
    db.close()

    return result