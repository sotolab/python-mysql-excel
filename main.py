
from db_create_table import Database
from db_debtor import Db_debtor

# mysql >
# mysql > create database myprojectdb character set utf8mb4 collate utf8mb4_general_ci;
# mysql > create user 'myprojcetuser'@'localhost' identified by '12345678!';
# mysql > GRANT ALL privileges ON myprojectdb.* TO  'myprojcetuser'@'localhost' ;
# mysql > flush privileges;
# mysql > exit;


def save_table():

    # db 클래스 객체 정의
    dbConfig = Db_debtor()

    # save_trial_history 생성, 완료 : Ture 반환, 오류 : False 반환  
    isSaved = dbConfig.save_debtor_history()
    print("isSaved: ", isSaved)


def select_table():

    # db 클래스 객체 정의
    dbConfig = Db_debtor()

    # create_trial_history 생성, 완료 : Ture 반환, 오류 : False 반환  
    dataList = dbConfig.select_debtor_history()
    print("dataList: ", dataList)

def create_table():

    # db 클래스 객체 정의
    dbConfig = Database()

    # # create_trial_history 생성, 완료 : Ture 반환, 오류 : False 반환  
    # isCreated = dbConfig.create_trial_history()
    # print("isCreated: ", isCreated)

    # # create_debt_history 생성, 완료 : Ture 반환, 오류 : False 반환  
    # isCreated = dbConfig.create_debt_history()
    # print("isCreated: ", isCreated)

    # create_debtor 생성, 완료 : Ture 반환, 오류 : False 반환  
    isCreated = dbConfig.create_debtor()
    print("isCreated: ", isCreated)

    # # create_rehabilitation_creditor 생성, 완료 : Ture 반환, 오류 : False 반환  
    # isCreated = dbConfig.create_rehabilitation_creditor()
    # print("isCreated: ", isCreated)

def delete_all_table():

    # db 클래스 객체 정의
    dbConfig = Database()

    isDeleteAll = dbConfig.delete_all_db_table()
    print("isDeleteAll: ", isDeleteAll)

def main():

    # tables 생성
    create_table()

    # delete_all_table()

    # tables 데이터 가져오기
    select_table()

    # tables 데이터 저장하기
    save_table()    


if __name__ == '__main__':
    main()
