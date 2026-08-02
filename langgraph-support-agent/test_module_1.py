from tools import check_user_balance

if __name__ == "__main__":
    print("Testing Tool with valid user ID...")
    result1 = check_user_balance.invoke({"user_id": "USR_101"})
    print(result1)
    print("\n" + "="*40 + "\n")
    
    print("Testing Tool with invalid user ID...")
    result2 = check_user_balance.invoke({"user_id": "USR_999"})
    print(result2)