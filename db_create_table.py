
# MySQL을 Python에서 사용하는 기능
import pymysql

# json형태의 데이터를 처리하는 기능
import json

# debug 처리하는 기능
import traceback

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
class Database(object):
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
    DB는 남겨두고 내부 존재하는 테이블들만 삭제하는 함수
    연결 실패시 에러발생 메세지를 콘솔창에 출력
    '''
    def delete_all_db_table(self):
        try:
            mydb ,conn = self.connect_db()   

            print('[delete_all_db_table] success~!: ', conn)      
            
            # Cursor 객체 생성
            with conn.cursor() as cursor:
                # 현재 데이터베이스의 모든 테이블 이름을 조회하는 SQL 쿼리
                sql = """
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = 'myprojectdb'
                """
                cursor.execute(sql)

                # 조회된 모든 테이블에 대해 삭제 명령 실행
                tables = cursor.fetchall()
                for table in tables:
                    drop_sql = f"DROP TABLE `{table[0]}`"
                    cursor.execute(drop_sql)
                    print(f"Table {table[0]} deleted.")

            # 변경 사항 커밋
            conn.commit()

            # 연결자 반환
            return True

        # 연결 실패시 에러발생 메세지를 콘솔창에 출력
        except Exception as error:
            print("Exception while checking MYSQL Connection:", traceback.format_exc())
            return False
    
    '''
    재판내역 (Trial History)
    Python에서 MySQL에 코드로 지정한 서버, 포트, ID, PW, DB로 연결하고
    create_trial_history 테이블이 없으면 생성하는 함수
    '''
    def create_trial_history(self):
        try:
            # User객체에서 DB를 연결하고 Connection객체, 연결자를 생성
            conn, mydb = self.connect_db()

            # DB에 연결되면 실행
            if conn.connection:
                # usermember테이블을 생성하는 쿼리문
                sql = """
                    CREATE TABLE IF NOT EXISTS  Trial_History (
                        id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
                        jurisdiction_court varchar(100) DEFAULT NULL,
                        case_number varchar(100) DEFAULT NULL,
                        case_name varchar(255) DEFAULT NULL,
                        verdict_date date DEFAULT NULL,
                        plaintiff varchar(100) DEFAULT NULL,
                        defendant varchar(100) DEFAULT NULL,
                        claim_amount decimal(15,2) DEFAULT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """

                # CREATE TABLE `재판내역` (
                #     `관할법원` varchar(100) DEFAULT NULL,
                #     `사건번호` varchar(100) DEFAULT NULL,
                #     `사건명` varchar(255) DEFAULT NULL,
                #     `선고일자` date DEFAULT NULL,
                #     `원고` varchar(100) DEFAULT NULL,
                #     `피고` varchar(100) DEFAULT NULL,
                #     `청구금액` decimal(15,2) DEFAULT NULL
                # ) ;

                # 쿼리문을 MySQL에서 실행
                cnt = conn.execute(sql)

                # 완료 메세지를 콘솔에 출력
                print("Well done, create_trial_history : ", cnt)

                # DB 연결 닫기
                mydb.close()
                return True

            # DB 연결 닫기
            mydb.close()
            return False

            '''
            try내 코드실행시 오류 발생 했을 때 동작하는 코드
            Exception 오류가 발생시 error에 담긴 오류 메세지를 출력
            '''
        except Exception as error:
            print("Exception while checking MYSQL Connection:" , traceback.format_exc())
            return False
    
    '''
    채권내역 (Debt History)
    Python에서 MySQL에 코드로 지정한 서버, 포트, ID, PW, DB로 연결하고
    debt_history 테이블이 없으면 생성하는 함수
    '''
    def create_debt_history(self):
        try:
            # User객체에서 DB를 연결하고 Connection객체, 연결자를 생성
            conn, mydb = self.connect_db()

            # DB에 연결되면 실행
            if conn.connection:
                # usermember테이블을 생성하는 쿼리문
                sql = """
                    CREATE TABLE IF NOT EXISTS  Debt_history (
                        id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
                        cause_date date DEFAULT NULL,
                        recovery_claim_cause varchar(255) DEFAULT NULL,
                        principal decimal(15,2) DEFAULT NULL,
                        interest decimal(15,2) DEFAULT NULL,
                        interest_rate decimal(5,2) DEFAULT NULL,
                        interest_start_date date DEFAULT NULL,
                        voting_right_amount decimal(15,2) DEFAULT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """

                # CREATE TABLE `채권내역` (
                #     `원인일자` date DEFAULT NULL,
                #     `회생채권원인` varchar(255) DEFAULT NULL,
                #     `원금` decimal(15,2) DEFAULT NULL,
                #     `이자` decimal(15,2) DEFAULT NULL,
                #     `이율` decimal(5,2) DEFAULT NULL,
                #     `이자개시일` date DEFAULT NULL,
                #     `의결권액` decimal(15,2) DEFAULT NULL
                #     ) ;

                # 쿼리문을 MySQL에서 실행
                cnt = conn.execute(sql)

                # 완료 메세지를 콘솔에 출력
                print("Well done, create_debt_history : ", cnt)

                # DB 연결 닫기
                mydb.close()
                return True

            # DB 연결 닫기
            mydb.close()
            return False

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
    Debtor 테이블이 없으면 생성하는 함수
    '''
    def create_debtor(self):
        try:
            # User객체에서 DB를 연결하고 Connection객체, 연결자를 생성
            conn, mydb = self.connect_db()

            # DB에 연결되면 실행
            if conn.connection:
                # usermember테이블을 생성하는 쿼리문
                sql = """
                    CREATE TABLE IF NOT EXISTS Debtor (
                        id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
                        case_Number int DEFAULT NULL,
                        debtor_name varchar(30) DEFAULT NULL,
                        debtor_address varchar(100) DEFAULT NULL,
                        debtor_phone varchar(20) DEFAULT NULL,
                        debtor_email varchar(30) DEFAULT NULL ,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """

                # CREATE TABLE `채무자` (
                #     `사건번호` int DEFAULT NULL,
                #     `성명` varchar(100) DEFAULT NULL,
                #     `주소` varchar(255) DEFAULT NULL,
                #     `전화번호` varchar(20) DEFAULT NULL,
                #     `이메일` varchar(100) DEFAULT NULL
                #     );

                # 쿼리문을 MySQL에서 실행
                cnt = conn.execute(sql)

                # 완료 메세지를 콘솔에 출력
                print("Well done, create_debt_history : ", cnt)

                # DB 연결 닫기
                mydb.close()
                return True

            # DB 연결 닫기
            mydb.close()
            return False

            '''
            try내 코드실행시 오류 발생 했을 때 동작하는 코드
            Exception 오류가 발생시 error에 담긴 오류 메세지를 출력
            '''
        except Exception as error:
            print("Exception while checking MYSQL Connection:" , traceback.format_exc())
            return False
    
    '''
    회생채권자 (Rehabilitation Creditor)
    Python에서 MySQL에 코드로 지정한 서버, 포트, ID, PW, DB로 연결하고
    Debtor 테이블이 없으면 생성하는 함수
    '''
    def create_rehabilitation_creditor(self):
        try:
            # User객체에서 DB를 연결하고 Connection객체, 연결자를 생성
            conn, mydb = self.connect_db()

            # DB에 연결되면 실행
            if conn.connection:
                # usermember테이블을 생성하는 쿼리문
                sql = """
                    CREATE TABLE IF NOT EXISTS Rehabilitation_creditor (
                        id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
                        creditor_name varchar(30) DEFAULT NULL,
                        creditor_address varchar(100) DEFAULT NULL,
                        creditor_phone varchar(20) DEFAULT NULL,
                        creditor_email varchar(30) DEFAULT NULL,
                        creditor_list_number int DEFAULT NULL,
                        report_number int DEFAULT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """

                #  CREATE TABLE `회생채권자` (
                #     `성명` varchar(100) DEFAULT NULL,
                #     `주소` varchar(255) DEFAULT NULL,
                #     `전화번호` varchar(20) DEFAULT NULL,
                #     `이메일` varchar(100) DEFAULT NULL,
                #     `채권자목록번호` int DEFAULT NULL,
                #     `신고번호` int DEFAULT NULL
                #     ) ;

                # 쿼리문을 MySQL에서 실행
                cnt = conn.execute(sql)

                # 완료 메세지를 콘솔에 출력
                print("Well done, create_debt_history : ", cnt)

                # DB 연결 닫기
                mydb.close()
                return True

            # DB 연결 닫기
            mydb.close()
            return False

            '''
            try내 코드실행시 오류 발생 했을 때 동작하는 코드
            Exception 오류가 발생시 error에 담긴 오류 메세지를 출력
            '''
        except Exception as error:
            print("Exception while checking MYSQL Connection:" , traceback.format_exc())
            return False