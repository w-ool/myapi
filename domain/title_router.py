from fastapi import APIRouter, Form
from sentence_transformers import SentenceTransformer, util
from database import SessionLocal
from models import Title
import json
import numpy as np
import torch

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

        # 상위 5개 결과 반환 (벡터값을 포함하지 않음)
        result = {
            "similar_titles": [{
                "title": title,
                "similarity": similarity
            } for title, similarity in sorted_similarity[:5]]
        }
    else:
        result = {"message": "작품을 찾을 수 없습니다. 줄거리를 입력해주세요."}

    # 데이터베이스 세션 닫기
    db.close()

    for title, similarity in result.items():
        result[title] = str(similarity)

    return result

# 새로운 엔드포인트를 정의합니다.
@router.get("/recommend")
def recommend_titles(summary_input: str):
    # 데이터베이스 세션 열기
    db = SessionLocal()

    # 스토리 요약을 입력으로 받고 벡터를 계산합니다.
    model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
    input_vector = model.encode(summary_input)

    # 모든 작품들과의 유사도를 계산하고 결과를 저장할 딕셔너리를 생성합니다.
    similarity_dict = {}

    titles = db.query(Title).all()

    for title in titles:
        vector_str = title.vector  # 데이터베이스에서 문자열 형식의 벡터 데이터 가져오기
        vector = np.array(json.loads(vector_str))  # JSON 문자열을 NumPy 배열로 변환
        vector = torch.from_numpy(vector).float()
        similarity = util.cos_sim(input_vector, vector)
        similarity_dict[title.title] = similarity

    # 결과를 유사도 높은 순으로 정렬
    sorted_similarity = sorted(similarity_dict.items(), key=lambda x: x[1], reverse=True)

    # 상위 5개 결과 반환
    result = {
        "recommended_titles": [{
            "title": title,
            "similarity": similarity
        } for title, similarity in sorted_similarity[:5]]
    }

    for title, similarity in result.items():
        result[title] = str(similarity)

    # 데이터베이스 세션 닫기
    db.close()

    return result