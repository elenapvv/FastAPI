import psycopg2
import typing
import random
import string
from models import Data
from models import GeneralData
from models import data_length
from starlette import status
from starlette.responses import Response
import xml.etree.ElementTree as xml


# Таблица базы данных состоит из id (автоинкремент) и data
class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(dbname='databaseForShvabe', user='postgres',
                                password='zaqxsw', host='localhost')
            self.cursor = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def add(self, retrieved_data) -> Response:
        # Добавление данных в базу данных

        try:
            self.cursor.execute('INSERT INTO "dataTable" (data) VALUES (%s)',
                                (retrieved_data.data,))
            self.conn.commit()
            return Response(status_code=status.HTTP_200_OK)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_general_data(self, limit, offset) -> typing.Optional[GeneralData]:
        # Получение всех данных
        if not limit:
            limit = 'NULL'
        self.cursor.execute('SELECT * from "dataTable" LIMIT '
                            '%s OFFSET %s',
                            (limit, offset))
        result = self.cursor.fetchall()
        data_result = GeneralData(dataOutput=[])
        for row in result:
            data_result.dataOutput.append(Data(data_id=row[0], data=row[1]))
        return data_result

    def edit(self, record) -> Response:
        # Редактирование данных
        try:
            self.cursor.execute("""UPDATE "dataTable" SET data = (%s)
                WHERE id = (%s)""", (record.data, record.data_id))
            self.conn.commit()
            return Response(status_code=status.HTTP_200_OK)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_single_data(self, data_id, data_type):
        # Получение данных по ID
        self.cursor.execute('SELECT * from "dataTable" WHERE id = (%s) LIMIT 1', (data_id,))
        result = self.cursor.fetchall()
        # Получение XML
        if data_type.lower() == "xml":
            root = xml.Element("Products")
            appt = xml.Element("product")
            root.append(appt)
            xml_id = xml.SubElement(appt, "id")
            xml_id.text = str(result[0][0])
            xml_data = xml.SubElement(appt, "data")
            xml_data.text = result[0][1]
            return xml.tostring(root).decode("utf-8")
        # Получение JSON
        return Data(data_id=result[0][0], data=result[0][1])