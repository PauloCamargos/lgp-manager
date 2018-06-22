#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Data-Logger-Arduino Main Application
Project of the discipline of Database.
This code handles the Database querys

GitHub: http://github.com/paulocamargos/data-logger-arduino

Notes
-----
USED SQL:
    * INSERT
    * CREATE
    * Delete_
    * UPDATE_
    * MAX
    * INNER JOIN_
    * ORDER BY_
Authors
-------
    * Paulo
    * Thiago
    * Italo
	* Pablo
References_
----------
    1. http://initd.org/psycopg/docs/genindex.html
    2. http://initd.org/psycopg/docs/
"""
import psycopg2  # PostgreSQL database adapter for Python


class Banco:
    """Database class. Use this class to create connection and execute CRUD
    commands on a database.

    Parameters
    ----------
    database : String
        Database name.
    schema : type
        Schema which the tables are stored.
    user : String
        User's username to access to database.
    password : type
        User's password to access the database.
    port : int
        Port number which the database uses.
    host : String
        Database host address.

    """
    def __init__(self, database, schema, user, password, port=5432,
                 host='localhost'):
        self.database = database
        self.schema = schema
        self.user = user
        self.password = password
        self.port = port
        self.host = host
        self.con = None
        self.cur = None
        self.query = None

    def connection(self):
        """Creates connection with the database using the specified parameter at
        the class constructor.

        Returns
        -------
        void

        """
        try:
            self.con = psycopg2.connect(database=self.database,
                                        user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port)

            self.cur = self.con.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            print("exception: " + error)

    def insertDataInto(self, table, **kwargs):
        """Inserts data into a table using the parameters as fields and it's
        values as data to be inserted.

        Parameters
        ----------
        table : String
            Table which the data will be inserted.
        **kwargs : String
            Fields and values to be inserted in the table. Use the template
            fieldName='value' to pass the columns and values. Unlimited number
            of parameters allowed here.

        Returns
        -------
        void

        """
        fields = []
        values = []
        unknownValues = []
        self.query = "INSERT INTO " + self.schema + "." + table

        for key in kwargs:
            # Table's fields
            fields.append(key)
            # Table's values
            values.append(kwargs[key])
            # Placeholders
            unknownValues.append("%s")

        # Reversing to keep fields and values in the right order
        fields.reverse()
        values.reverse()

        # Converting the lists into string
        knownFields = ", ".join(fields)
        placehold = ', '.join(unknownValues)

        # Converting known values into a tuple
        knownValues = tuple(values)
        self.query = "INSERT INTO " + self.schema + "." + table \
                     + "(" + knownFields + ") " \
                     + "VALUES(" + placehold + ")"
        # DEBUG: print(self.query)
        # DEBUG: print(knownValues)

        self.cur.execute(self.query, knownValues)
        self.con.commit()

    def updateDataFrom(self, table, condition, condition_value, **parameters):
        """Updates data of a table using the parameters as fields and it's
        values as data to be updated.

        Parameters
        ----------
        table : String
            Table which the data will be updated.
        condition : String
            Field record where data will be updated.
        condition_value : String
            Value record where data will be updated.
        **kwargs : String
            Fields and values to be updated in the table. Use the template
            fieldName='value' to pass the columns and values. Unlimited number
            of parameters allowed here.

        Returns
        -------
        void
        """

        fields_values = " "
        values = []

        self.query = "UPDATE " + self.schema + "." + table

        for key in parameters:
            # Table's fields
            fields_values += str(key) + "=%s,"
            # Table's values
            values.append(parameters[key])

        values.append(condition_value)
        fields_values = fields_values[:-1]
        knownValues = tuple(values)

        self.query += " SET" + fields_values + " WHERE " + condition + "=%s"

        print(self.query)
        print(knownValues)

        try:
            self.cur.execute(self.query, knownValues)
            self.con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def selectDataWhere(self, table, condition, condition_value, *args):
        """Selects data from a specified table with a specified condition.

        Parameters
        ----------
        table : String
            Table from which data will be retrieved.
        condition : String
            Field name of the where clause.
        condition_value : String
            Field's value of the where clause.
        *args : String
            Fields to be retrieved.

        Returns
        -------
        Tuple
            Returns a tupe with the data retrieved from the database.

        """
        fields = " "
        for arg in args:
            fields += arg + ", "

        fields = fields[:-2]

        self.query = "SELECT " + fields + " FROM " + self.schema + "." + table \
                    + " WHERE " + condition + "=%s"

        condition_value = (condition_value ,)
        self.cur.execute(self.query, condition_value)
        row = self.cur.fetchone()
        return row

    def selectLastDataFrom(self, table):
        """Selects the last record from a specified table.

        Parameters
        ----------
        table : String
            Table's name from which last record will be retrieved and returned

        Returns
        -------
        tuple
            Returns a single tuple with the last row of a table.

        """
        self.query = "SELECT MAX(id) FROM " + self.schema + "." + table
        self.cur.execute(self.query)
        id_last_record = (self.cur.fetchone(),)
        self.query = "SELECT * FROM " + self.schema + "." + table \
                    + " WHERE id=%s"
        self.cur.execute(self.query, id_last_record)
        one_row_data = self.cur.fetchone()
        return one_row_data

    def selectAllDataFrom(self, table):
        """Selects all data from a specified table.

        Parameters
        ----------
        table : String
            Table's name from which all data will be retrieved and returned.

        Returns
        -------
        Tuple
            Return a tuple containing all data from a table, each one inside a
            tuple.

        """
        self.query = "SELECT * FROM " + self.schema + "." + table + " ORDER BY id asc;"
        self.cur.execute(self.query)
        rows = self.cur.fetchall()
        return rows

    def deleteDataFrom(self, table, condition, condition_value):
        """Short summary.

        Parameters
        ----------
        table : String
            Table from which data will be removed.
        condition : String
            Field name of the where clause.
        condition_value : String
            Field's value of the where clause.

        Returns
        -------
        type
            Description of returned object.

        """
        self.query = "DELETE FROM " + self.schema + "." + table \
                     + " WHERE " + condition + "=%s"

        condition_value = (condition_value, )

        self.cur.execute(self.query, condition_value)
        self.con.commit()
        # DEBUG: print(self.query)

    def deleteLastRecordFrom(self, table):
        """Deletes the last record from a specified table.

        Parameters
        ----------
        table : String
            Table's name of which the last record will be deleted. This action is irreversible.

        Returns
        -------	('Pablo Nunes', 'pablo@ufu.br', 'pablon','senha'),
	('Marcio Cunha', 'marcio@ufu.br', 'marioc', 'password123');

        void
        """
        self.cur.execute("SELECT MAX(id) FROM " + self.schema + "." + table)
        id_last_record = (self.cur.fetchone(),)
        self.query = "DELETE FROM " + self.schema + "." + table \
                     + " WHERE id=%s"
        self.cur.execute(self.query, id_last_record)
        self.con.commit()
        # DEBUG: print(self.query)

    def deleteAllDataFrom(self, table):
        """Deletes all data from a specified table.

        Parameters
        ----------
        table : String
            Table's name of which all data will be deleted. This action is irreversible.

        Returns
        -------
        void
        """
        self.query = "DELETE FROM " + self.schema + "." + table
        self.cur.execute(self.query)
        self.con.commit()
# -------------- CUSTOM METHODS---------------------
    def visualizeByUser(self, user_id=None):
        """Selects the id of a measure, it's value and it's unity and the name of the user who
        registered the data. User id is optional. If not passed, returns all records.

        Parameters
        ----------
        user_id (optional): Int
            User id whose database associated records will be retrieved. If not passed, all records
            will be retrieved and returned.

        Returns
        -------
        Tuple
            Returns a tuple of tupes. Each tuple is a record retrieved.

        """
        self.query = "SELECT m.id AS id_measure, u.usr_fullname , m.read_value, p.unity, e.description FROM arduinoproject.measures m \
                        INNER JOIN arduinoproject.users u ON m.id_user = u.id \
                        INNER JOIN arduinoproject.physical_quantity p ON m.id_pquantity = p.id \
                        INNER JOIN arduinoproject.environment e ON m.id_environment = e.id \
                        ORDER BY m.id ASC"
        self.cur.execute(self.query)
        rows = self.cur.fetchall()
        return rows

    def select_free_xbees(self):
        """
            Returns all unassociated xbees
        """


        self.query = "SELECT e.description, e.serial_number, x.address_64_bit, x.xbee_type FROM assets.equipments e \
                            RIGHT JOIN assets.xbees x ON e.xbee = x.id \
                            WHERE e.xbee IS NULL"
        self.cur.execute(self.query)
        rows = self.cur.fetchall()
        return rows

    def closeConnecetion(self):
        """Closes the connection.

        Returns
        -------
        void
        """
        self.con.close()


def main():
    banco = Banco('projects', 'arduinoproject', 'postgres', 'banco')
    # Cria conexao:
    banco.connection()
    # NOTE: One Time Configurations (utilize as linhas abaixo para configurar
    # o banco de dados, é necessário realizar somentre na primeira execução)
    # banco.insertDataInto(table='physical_quantity',
    #                      description='Temperature', unity='°C')
    # banco.insertDataInto(table='physical_quantity',
    #                      description='Umidty', unity='%')
    # banco.insertDataInto(table='environment', description='soil')
    # banco.insertDataInto(table='environment', description='water')
    # banco.insertDataInto(table='environment', description='air')
    # banco.deleteDataFrom(table='physical_quantity',
    #                      condition='id', condition_value='4')
    # banco.selectAllDataFrom(table='users')
    # banco.updateData(table='physical_quantity', condition='id',
    #                  condition_value= '7', description='tensao',
    #                  unity='volts')


if __name__ == "__main__":
    main()
