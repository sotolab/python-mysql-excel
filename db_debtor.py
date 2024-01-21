
# MySQL을 Python에서 사용하는 기능
import pymysql

# json형태의 데이터를 처리하는 기능
import json

# 데이터 조작 및 분석 기능
import pandas as pd

# debug 처리하는 기능
import traceback

# OS 기본 커맨드 명령어 기능
import os

# 사용자가 제시한 조건에 맞는 파일명을 리스트로 반환하는 기능(ex:엑셀)
from glob import glob

# 데이터를 입력받을 객체들을 초기화 시킨다.
hostName = ''
hostPort = 0
userName = ''
passWord = ''
databaseName = ''

# config.json파일을 열고, utf-8 인코딩하고 데이터 읽기 모드로 파일객체인 jsonFile를 반환
with open('config.json', encoding='utf-8') as jsonFile:
    # json포맷 데이터를 Python 객체인 jsonData로 디코딩(데이터 변환)
    jsonData = json.load(jsonFile)

    '''
    jsonData딕셔너리에서 각 원소의 key를 이용하여 value를 별도 분리 저장
    DB에 저장될 DB정보들을 객체에 옮겨 저장
    '''
    productCode = jsonData["productCode"]
    projectName = jsonData["projectName"]
    version = jsonData["version"]
    hostName = jsonData["hostName"]
    hostPort = jsonData["hostPort"]
    userName = jsonData["userName"]
    passWord = jsonData["passWord"]
    databaseName = jsonData["databaseName"]

# 새계정 생성, 로그인 입력 정보 참거짓 판별, DB 연결, DB 생성, DB내 table 생성 기능이 있는 클래스
class Db_debtor(object):
    '''
    Python에서 MySQL에 코드로 지정한 서버, 포트, ID, PW, DB로 연결하는 함수
    연결 실패시 에러발생 메세지를 콘솔창에 출력하는 기능도 탑재함
    '''

    def connect_db(self):
        try:

            # 호스트명, 포트, MySQL유저아이디, 암호, 접속할 DB를 입력받아 MySQL에 연결한다. 
            connection = pymysql.connect(
                host=hostName,  # MySQL Server Address
                port=hostPort,  # MySQL Server Port
                user=userName,  # MySQL username
                password=passWord,  # password for MySQL username
                database=databaseName,  # Database name
                charset='utf8'
            )

            # 접속 실행 완료 메세지를 콘솔에 출력
            print('[connect_db] success~!: ', connection)

            # 커서, 연결자 반환
            return connection.cursor(), connection

            '''
            try 구문 실행 도중 에러 발생시 실행할 코드
            Exception 오류가 발생시 error에 담긴 오류 메세지를 출력
            '''
        except Exception as error:
            print("Exception while checking MYSQL Connection:" , traceback.format_exc())
            return False
    
    '''
    채무자 (Debtor)
    Python에서 MySQL에 코드로 지정한 서버, 포트, ID, PW, DB로 연결하고
    select_debtor_history 테이블의 데이터를 가져오는 함수
    '''
    def select_debtor_history(self):
        try:
            # User객체에서 DB를 연결하고 Connection객체, 연결자를 생성
            mydb, conn = self.connect_db()

            sql = """ 
                SELECT * 
                FROM  Debtor
                """

            '''
            Connection객체로 커서인 cur를 생성하고 MySQL에 쿼리문을 전달하여
            테이블에서 데이터 조회 결과를 레코드 단위의 원소가 튜플인 리스트로 반환
            동작이 끝나고 커서를 삭제하는 구문
            '''
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    result = cur.fetchall()
                    print('----------------------Trial_History All 데이터 조회 성공!!')
                    return result

            '''
            try내 코드실행시 오류 발생 했을 때 동작하는 코드
            Exception 오류가 발생시 error에 담긴 오류 메세지를 출력
            '''
        except Exception as error:
            print("Exception while checking MYSQL Connection:" , traceback.format_exc())
            return False
    
    '''
    채무자 (Debtor)
    Python에서 MySQL에 코드로 지정한 서버, 포트, ID, PW, DB로 연결하고
    select_condtion_debtor_history 테이블의 데이터를 조건에 맞으면 가져오는 함수
    '''
    def select_condtion_debtor_history(self, param):
        try:
            # User객체에서 DB를 연결하고 Connection객체, 연결자를 생성
            mydb, conn = self.connect_db()

            sql = """ 
                SELECT * 
                FROM  Debtor
                WHERE id = %s
                """

            '''
            Connection객체로 커서인 cur를 생성하고 MySQL에 쿼리문을 전달하여
            테이블에서 데이터 조회 결과를 레코드 단위의 원소가 튜플인 리스트로 반환
            동작이 끝나고 커서를 삭제하는 구문
            '''
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql, param)
                    result = cur.fetchall()
                    print('----------------------Trial_History 데이터 조회 성공!!')
                    return result

            '''
            try내 코드실행시 오류 발생 했을 때 동작하는 코드
            Exception 오류가 발생시 error에 담긴 오류 메세지를 출력
            '''
        except Exception as error:
            print("Exception while checking MYSQL Connection:" , traceback.format_exc())
            return False
        
    def list_folders_files(self, path):
        array_dirs = []
        array_files = []

        for root, dirs, files in os.walk(path):
            array_dirs.extend([os.path.join(root, d) for d in dirs])
            array_files.extend([os.path.join(root, f) for f in files])

        return array_dirs, array_files

    def read_excel_file(self, folder_path, file_name, sheet_name):
        array_dirs, array_files = self.list_folders_files(folder_path)

        if os.path.join(folder_path, file_name) in array_files:
            # df = pd.read_excel(os.path.join(folder_path, file_name))
            data = pd.read_excel(os.path.join(folder_path, file_name), header=None , sheet_name=sheet_name)[1:]  # 74 * 15
            return data
        else:
            print(f"{file_name} not found in the directory.")
            return None
    
    '''
    채무자 (Debtor)
    Python에서 MySQL에 코드로 지정한 서버, 포트, ID, PW, DB로 연결하고
    save_debtor_history 테이블에 데이터를 저장하는 함수
    '''
    def save_debtor_history(self):
        try:

            # Usage
            data = self.read_excel_file('import_data', 'debtor.xlsx',  'debtor')
            if data is not None:
                print("debtor: ", data)

            # 파이썬 데이터프레임에 칼럼명을 지정
            data.columns = ['debtor_name','case_Number', 'debtor_address', 'debtor_phone', 'debtor_email' , ]

            # mysql에 insert 하기 위해서는 NAN값을 처리해야 한다.(결측값 처리)
            data.fillna('없음', inplace=True)

            print('-----Debtor')
            
            # sql문 생성
            sql = '''INSERT INTO Debtor 
                        (debtor_name, case_Number, debtor_address, debtor_phone, debtor_email) 
                        VALUES (%s, %s, %s, %s, %s)
                    '''
            
            # User객체에서 DB를 연결하고 Connection객체, 연결자를 생성
            mydb, conn = self.connect_db()

            # db 테이블 insert(데이터 추가)
            with conn:
                with conn.cursor() as cur:
                    for _, row in data.iterrows():
                        # sql문에 엑셀 데이터를 삽입하여 MySQL에서 실행
                        cur.execute(sql, (row[0], row[1], row[2], row[3], row[4]))
                        # 변경사항 저장
                    conn.commit()

                    # 데이터 반환
                    return True, 'Debtor'

            return True

            '''
            try내 코드실행시 오류 발생 했을 때 동작하는 코드
            Exception 오류가 발생시 error에 담긴 오류 메세지를 출력
            '''
        except Exception as error:
            print("Exception while checking MYSQL Connection:" , traceback.format_exc())
            return False
