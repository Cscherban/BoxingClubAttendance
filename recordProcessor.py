import numpy
import pandas as pd
import os.path


class BoxingClubProcessor():

    def __init__(self, fileName, date=None):
        if not os.path.exists(fileName):
            raise ValueError("Please provide a valid file")
        self.csvFileName = fileName
        self.csvAsDataFrame = pd.read_csv(fileName)
        self.date = date
        print(self.csvFileName)


    def set_date(self, date):
        self.date = date

    @staticmethod
    def _extract_gtid(scanner_output):
        if scanner_output is None:
            return None

        split_output = scanner_output.split("=")
        if len(split_output) < 3:
            return None
        res = scanner_output.split("=")[1]
        if len(res) != 9:
            return None

        try:
            i = int(res)
            return i
        except ValueError:
            # Handle the exception
            return None

    def process_scanner_output(self, scanner_output):
        return self._extract_gtid(scanner_output)

    def get_dict(self):
        return self.csvAsDataFrame.to_dict()

    def get_html(self):
        return self.csvAsDataFrame.to_html()

    def add_date_to_csv(self, date):
        df = self.csvAsDataFrame
        print(df)
        num_rows, num_cols = df.shape

        try:
            df.insert(loc=num_cols, column=date, value=["--" for i in range(num_rows)])
        except:
            return

        df.to_csv(self.csvFileName,index=False)
        self.csvAsDataFrame = df

    def remove_date_from_csv(self, date):
        df = self.csvAsDataFrame
        df = df.drop(columns=date)
        df.to_csv(self.csvFileName,index=False)
        self.csvAsDataFrame = df

    def _validate_gtid(self, gtid):
        if len(gtid) != 9 or int(gtid) == 0:
            return False
        return True

    def add_new_person(self, gtid, name):
        df = self.csvAsDataFrame
        dict = {df.columns[i] : "--" for i in range(len(df.columns))}
        if not self._validate_gtid(gtid) or self.check_exists(int(gtid)):
            raise ValueError("Invalid GTID/User Already Exists")
        dict["GTID"] = gtid
        dict["Name"] = name
        df = df.append(dict, ignore_index=True)
        df.to_csv(self.csvFileName,index=False)
        self.csvAsDataFrame = df

    def mark_as_attended(self, gtid):
        if self.date is None:
            return False
        df = self.csvAsDataFrame
        df.loc[df["GTID"] == gtid, [self.date]] = "Present"
        df.to_csv(self.csvFileName,index=False)
        self.csvAsDataFrame = df

    def remove_gtid(self, gtid):
        df = self.csvAsDataFrame
        df = df.drop(gtid, axis=0)
        df.to_csv(self.csvFileName,index=False)
        self.csvAsDataFrame = df

    def check_exists(self, gtid):
        df = self.csvAsDataFrame
        if gtid == 0:
            return False

        for elem in df["GTID"]:
            if gtid == elem:
                return True
        return False
