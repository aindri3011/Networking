import random
import threading
import datetime

import pytz
from rest_framework import status

from ..mongodb import user_collection


class CreateUser:

    def __init__(self, serializer):
        """
        SERIALIZING USER DATA
        """
        self.data = serializer.data

        self.serializer = serializer.data
        self.user_collection = user_collection

        ist = pytz.timezone('Asia/Kolkata')
        self.now = datetime.datetime.now(ist)
        self.error_valid = ""

    def create_user_id(self):
        """
        CREATING UNIQUE USER-IDS
        """
        id_part1 = self.now.strftime("%Y%j%H%M%S")
        id_part2 = str(random.randint(111, 999))
        self.new_id = "User" + id_part1 + "_" + id_part2
        self.data.update({"user_id": self.new_id})

    def create_user(self):

        if self.user_collection.find_one({"email_id": self.data['email_id']}):

            self.error_valid = "Email already exists"
        else:
            self.user_collection.insert_one(self.data)

    def start_process(self):
        try:
            t1 = threading.Thread(target=self.create_user_id)
            t1.start()
            t1.join()
        except Exception as e:
            error_str = "Class : CreateUserID\n Thread : Thread1" + e
            return {"data": error_str, "status": status.HTTP_400_BAD_REQUEST}

        try:
            t2 = threading.Thread(target=self.create_user)
            t2.start()
            t2.join()
        except Exception as e:
            error_str = "Class : CreateUser\n Thread : Thread1" + e
            return {"data": error_str, "status": status.HTTP_400_BAD_REQUEST}
        if self.error_valid:
            return {"data": {"status": "error", "return_data": self.error_valid}, "status": status.HTTP_200_OK}
        return {"data": {"status": "success", "return_data": self.new_id}, "status": status.HTTP_200_OK}


class ReadLogin:
    """
      LOGIN AUTHENTICATED USERS
      """

    def __init__(self, serializer):

        self.user_login_col = user_collection

        self.email_id = serializer.data['email_id']
        self.password = serializer.data['password']

        self.return_data = {}  # Return data

    def check_user(self):
        q1 = {"email_id": self.email_id}
        q2 = {"password": self.password}
        query = {"$and": [q1, q2]}
        doc = self.user_login_col.find_one(query, {"_id": False})  # FETCHING USER DATA
        try:
            self.return_data.update({"email_id": doc["email_id"]})
            self.return_data.update({"name": doc["name"]})
            self.return_data.update({"comment": "Welcome To Network Portal"})
        except:
            self.has_user = False
            self.return_data.update({"comment": "Wrong Username / Password"})

    def start_process(self):

        try:
            t1 = threading.Thread(target=self.check_user)
            t1.start()
            t1.join()
        except Exception as e:
            error_str = "Class : check user\n Thread : Thread1" + e
            return {"data": error_str, "status": status.HTTP_400_BAD_REQUEST}

        return {"data": {"status": "success", "return_data": self.return_data}, "status": status.HTTP_200_OK}
