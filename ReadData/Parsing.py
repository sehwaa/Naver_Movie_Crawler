'''
Created on 2018. 5. 3.

@author: SEHWA
'''
#coding: utf-8

from Connection.Connection import driver
import selenium
from selenium.common.exceptions import NoSuchAttributeException,\
    NoSuchElementException

#[배우/제작진] 제작사/수입사/배급사 파싱
def agency():
    try:
        agency_name = driver.find_element_by_xpath("//dl[@class='agency_name']")
        agency_text = agency_name.text
        
        #제작사 / 수입사 / 배급사 정보 존재 유무 확인 (없으면 None)
        try:
            producer_test = driver.find_elements_by_class_name("agency_sub0")
            if producer_test == [] :
                producer_test = None
        except NoSuchElementException:
            print("제작사 없음")
            producer_test = None
        
        try:
            importer_test = driver.find_element_by_class_name("agency_sub1")
            if importer_test == []:
                importer_test = None
        except NoSuchElementException:
            print("수입사 없음")
            importer_test = None 
            
        try:
            distributor_test = driver.find_element_by_class_name("agency_sub2")
            if distributor_test == []:
                distributor_test = None
        except NoSuchElementException:
            print("배급사 없음")
            distributor_test = None
            
        #제작사 / 수입사 / 배급사 데이터 저장
        if producer_test is not None and importer_test is None and distributor_test is not None:
            producer = agency_text.split('\n')[0]
            distributor = agency_text.split('\n')[1]
            print("제작사 : " + producer)
            print("배급사: " + distributor)
        elif producer_test is not None and importer_test is not None and distributor_test is None:
            producer = agency_text.split('\n')[0]
            importer = agency_text.split('\n')[1]
            print("제작사 : " + producer)
            print("수입사 : " + importer)
        elif producer_test is None and importer_test is not None and distributor_test is not None:
            importer = agency_text.split('\n')[0]
            distributor = agency_text.split('\n')[1]
            print("수입사 : " + importer)
            print("배급사 : " + distributor)
        elif producer_test is not None and importer_test is not None and distributor_test is not None :
            producer = agency_text.split('\n')[0]
            importer = agency_text.split('\n')[1]
            distributor = agency_text.split('\n')[2]
            print("제작사 : " + producer)
            print("수입사 : " + importer)
            print("배급사 : " + distributor)
        elif producer_test is not None and importer_test is None and distributor_test is None:
            producer = agency_text
            print("제작사 : " + producer)
        elif producer_test is None and importer_test is not None and distributor_test is None:
            importer = agency_text
            print("수입사 : " + importer)
        elif producer_test is None and importer_test is None and distributor_test is not None:
            distributor = agency_text
            print("배급사 : " + distributor)
        else:
            print("정보 없음")
    except NoSuchElementException:
        agency_name = None
        print('정보 없음')
    
#[평점] 개봉 전 평점 정보 파싱
def beforeOpeningscore():
    try:
        #기대 지수
        expectateIndex = driver.find_element_by_class_name("exp_info")
        like = expectateIndex.text.split('\n')[0]
        dislike = expectateIndex.text.split('\n')[1]
        print("보고싶어요 : " + like)
        print("글쎄요 : " + dislike)
        
        #네티즌 평점
        star_score_text = driver.find_element_by_id("beforePointArea")
        star_score = star_score_text.text.split('\n')[3]
        before_participator = star_score_text.text.split('\n')[4]
        print("개봉 전 네티즌 평점 : " + star_score)
        print("참여자 수 : " + before_participator.replace("참여", ""))
    except:
        print("국내 개봉 되지 않은 영화입니다")
        
#[평점] 개봉 후 네티즌 평점 정보 파싱(총 평점, 점수 분포 정보)
def afterNetizenOpeningscore():
    try:
        #네티즌 평점 정보 (총 평점 - 별점)
        netizen_score_all = driver.find_element_by_id("netizen_point_tab_inner")
        netizen_score = netizen_score_all.text.split('\n')[0]
        after_participator_netizen = netizen_score_all.text.split('\n')[1]
        
        print("개봉 후 네티즌 평점 : " + netizen_score)
        print("네티즌 평점 참여자 수 : " + after_participator_netizen)
    except:
        print("개봉 후 네티즌 평점 정보 없음")
               
    try:
        #네티즌 점수 분포 (점수 분포 막대 그래프)
        netizen_score_graph_text = driver.find_element_by_id("netizen_point_graph")
        netizen_score_graph = netizen_score_graph_text.text.split("\n")
        #점수 분포 리스트
        netizen_score_graph_list = []
        
        #index가 2로 안나누어 떨어지는 netizen_score_graph 요소만 netizen_score_graph_list에 삽입
        for index in range(0, len(netizen_score_graph)):
            if index % 2 != 0 :
                netizen_score_graph_list.append(netizen_score_graph[index])
        
        #이 영화를 선호하는 연령대 텍스트 전처리
        netizen_score_favorite_group_text = netizen_score_graph_list[-1].replace("이 영화를 가장 좋아하는 그룹은 ", "")
        netizen_score_favorite_group = netizen_score_favorite_group_text.replace("입니다.", "")    
        
        #리스트 첫 번째 요소 삭제 (필요없는 데이터이므로 삭제)
        del netizen_score_graph_list[0]
                
        #리스트 마지막 요소 삭제(선호하는 연령대 데이터)
        del netizen_score_graph_list[-1]
        
        #점수 분포 텍스트 전처리 ('%' 삭제)
        for index in range(0, len(netizen_score_graph_list)):
            netizen_score_graph_list[index] = netizen_score_graph_list[index].replace("%", "")
        
        print(netizen_score_graph_list)
        print("선호하는 그룹(네티즌) : " +netizen_score_favorite_group)  
        
    except:
        print("네티즌 평점 막대 그래프 정보 없음")

#[평점] 개봉 후 관람객 평점 정보 파싱 (총 평점, 점수 분포 정보)      
def afterAudienceOpeningScore():
    try:
        #관람객 평점 정보 (총 평점 - 별점)
        audience_score_all = driver.find_element_by_id("actual_point_tab_inner")
        audience_score = audience_score_all.text.split('\n')[0]
        after_participator_audience = audience_score_all.text.split('\n')[1]
        
        print("개봉 후 관람객 평점 : " + audience_score)
        print("관람객 평점 참여자 수 : " + after_participator_audience)
    except:
        print("개봉 후 관람객 평점 정보 없음")
        
    try:
        #관람객 점수 분포 (점수 분포 막대 그래프)
        audience_score_graph_text = driver.find_element_by_id("actual_point_graph")
        audience_score_graph = audience_score_graph_text.text.split("\n")
        #점수 분포 리스트
        audience_score_graph_list = []
        
        #index가 2로 안나누어 떨어지는 netizen_score_graph 요소만 netizen_score_graph_list에 삽입
        for index in range(0, len(audience_score_graph)):
            if index % 2 != 0 :
                audience_score_graph_list.append(audience_score_graph[index])
        
        #이 영화를 선호하는 연령대 텍스트 전처리
        audience_score_favorite_group_text = audience_score_graph_list[-1].replace("이 영화를 가장 좋아하는 그룹은 ", "")
        audience_score_favorite_group = audience_score_favorite_group_text.replace("입니다.", "")    
        
        #리스트 첫 번째 요소 삭제 (필요없는 데이터이므로 삭제)
        del audience_score_graph_list[0]
                
        #리스트 마지막 요소 삭제(선호하는 연령대 데이터)
        del audience_score_graph_list[-1]
        
        #점수 분포 텍스트 전처리 ('%' 제거)
        for index in range(0, len(audience_score_graph_list)):
            audience_score_graph_list[index] = audience_score_graph_list[index].replace("%", "")
        
        print(audience_score_graph_list)
        print("선호하는 그룹(관람객) : " + audience_score_favorite_group)  
        
    except:
        print("관람객 평점 막대 그래프 정보 없음")
        
#[평점] 개봉 후 네티즌 평점 정보 파싱(남녀별, 연령별)
def afterNetizenOpeningscore_genderAndage():
    try:
        gender_score_text = driver.find_element_by_id("netizen_group_graph")
        gender_score_graph = gender_score_text.text.split('\n')
        
        #남녀 참여율 리스트
        gender_score_participation_rate = []
        #남녀 평점 리스트
        gender_score_star_score = []
        
        #연령별 참여율 리스트
        age_score_participation_rate = []
        #연령별 평점 리스트
        age_score_star_score = []   
             
        ##파싱 정보 전처리
        #남녀 참여율 리스트 데이터 채우기
        male_rate = gender_score_graph[0].replace("%", "") # '%' 제거
        female_rate = gender_score_graph[1].replace("%", "") # '%' 제거
        gender_score_participation_rate.append(male_rate) #남자 참여율
        gender_score_participation_rate.append(female_rate) #여자 참여율
        
        #남녀 평점 리스트 데이터 채우기
        male_score = gender_score_graph[3].replace("평점 ", "") #'평점' 제거
        female_score = gender_score_graph[5].replace("평점 ", "") #'평점' 제거
        gender_score_star_score.append(male_score) #남자 평점
        gender_score_star_score.append(female_score) #여자 평점
        
        print(gender_score_participation_rate)
        print(gender_score_star_score)
        
        #연령대 평점 임시 리스트
        age_score_star_score_temp = []
        
        #연령대 평점 리스트 데이터 채우기(10대, 20대, 30대, 40대 이상 순)
        for index in range(7, 15):
            age_score_star_score_temp.append(gender_score_graph[index])
        #필요없는 데이터 제거
        for index in range(0, len(age_score_star_score_temp)):
            if index % 2 != 0 :
                age_score_star_score.append(age_score_star_score_temp[index].replace("평점 ", ""))#'평점' 제거          
    
        print(age_score_star_score)
        
        #연령대 참여율 리스트 데이터 채우기(10대, 20대, 30대, 40대 이상 순)
        for index in range(15, 19):
            age_score_participation_rate.append(gender_score_graph[index].replace("%", ""))#'%' 제거
        
        print(age_score_participation_rate)
    except:
        print("남녀별, 연령별 평점 정보 없음")

        
#[평점] 개봉 후 관람객 평점 정보 파싱(남녀별, 연령별)
def afterAudienceOpeningscore_genderAndage():
    try:
        gender_score_text = driver.find_element_by_id("actual_group_graph")
        gender_score_graph = gender_score_text.text.split('\n')

        #남녀 참여율 리스트
        gender_score_participation_rate = []
        #남녀 평점 리스트
        gender_score_star_score = []
        
        #연령별 참여율 리스트
        age_score_participation_rate = []
        #연령별 평점 리스트
        age_score_star_score = []
        
        ##파싱 정보 전처리
        #남녀 참여율 리스트 데이터 채우기
        male_rate = gender_score_graph[0].replace("%", "") # '%' 제거
        female_rate = gender_score_graph[1].replace("%", "") # '%' 제거
        gender_score_participation_rate.append(male_rate) #남자 참여율
        gender_score_participation_rate.append(female_rate) #여자 참여율
        
        #남녀 평점 리스트 데이터 채우기
        male_score = gender_score_graph[3].replace("평점 ", "") #'평점' 제거
        female_score = gender_score_graph[5].replace("평점 ", "") #'평점' 제거
        gender_score_star_score.append(male_score) #남자 평점
        gender_score_star_score.append(female_score) #여자 평점
        
        print(gender_score_participation_rate)
        print(gender_score_star_score)
        
        #연령대 평점 임시 리스트
        age_score_star_score_temp = []
        
        #연령대 평점 리스트 데이터 채우기(10대, 20대, 30대, 40대 이상 순)
        for index in range(7, 15):
            age_score_star_score_temp.append(gender_score_graph[index])
        #필요없는 데이터 제거
        for index in range(0, len(age_score_star_score_temp)):
            if index % 2 != 0 :
                age_score_star_score.append(age_score_star_score_temp[index].replace("평점 ", ""))#'평점' 제거          
    
        print(age_score_star_score)
        
        #연령대 참여율 리스트 데이터 채우기(10대, 20대, 30대, 40대 이상 순)
        for index in range(15, 19):
            age_score_participation_rate.append(gender_score_graph[index].replace("%", ""))#'%' 제거
        
        print(age_score_participation_rate)
    except:
        print("남녀별, 연령별 평점 정보 없음")