import psycopg2

class DataSource:
    def __init__(self):
        self.connection = psycopg2.connect(database='hussaink', user='hussaink', password='orange434farm', host="localhost")

    def getMajorList(self):
        '''
        Retrieves the names of all of the majors
        Returns:
            A list of major names
        '''
        major_list = []
        try:
            cursor = self.connection.cursor()
            query = "SELECT major FROM table_2017 ORDER BY major ASC"
            cursor.execute(query)
            for item in cursor.fetchall():
                str = ''.join(item)
                major_list.append(str)
            return major_list

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    def getMaxAndMinSalary(self):
        '''
        Retrieves the maximum salary and the minimun salary in the table
        Return:
            The maximum salary and the minimun salary
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT MAX(salary), MIN(salary) FROM table_2017"
            cursor.execute(query)
            Salary = cursor.fetchall()
            return Salary

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    def getMaxAndMinPopularity(self):
        '''
        Retrieves the maximum popularity and the minimun popularity in the table
        Return:
            The maximum popularity and the minimun popularity
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT MAX(popularity), MIN(popularity) FROM table_2017"
            cursor.execute(query)
            Popularity = cursor.fetchall()
            return Popularity

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    def getMajorsBySalary(self, minSalary, maxSalary):
        '''
        Retrieves the names of all of the majors that are in the salary scale
        Parameters:
            minSalary - the minimum of the desired salary
            maxSalary - the maximum of the desired salary
        Returs:
            A list of major that are within the salary range
        '''
        majorBySalary_list = []
        try:
            cursor = self.connection.cursor()
            query = "SELECT major FROM table_2017 WHERE salary BETWEEN " + minSalary + " AND " + maxSalary + " ORDER BY salary ASC"
            cursor.execute(query)
            for item in cursor.fetchall():
                str = ''.join(item)
                majorBySalary_list.append(str)
            return majorBySalary_list
        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    def getSalary(self, major):
        '''
        Retrieves the salary of the specified major
        Parameters:
            major - retrieve the salary of the this major from the data
        Returns:
            The median annual salary of this major in dollar, or None if the query fails.
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT salary FROM table_2017 WHERE major LIKE '" + major + "'"
            cursor.execute(query)
            salary = cursor.fetchone()
            return int(salary[0])

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getPopularity(self, major):
        pass
        '''
        Retrieves the popularity of the specified major
        Parameters:
            major - retrieve the popularity of the this major from the data
        Returns:
            the popularity of this major as an integer number in thousands, or None if the query fails.
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT popularity FROM table_2017 WHERE major LIKE '" + major + "'"
            cursor.execute(query)
            popularity = cursor.fetchone()
            print(type(popularity[0]))
            pop = str(popularity[0])
            if len(str(popularity[0])) > 3:
                string = str(popularity[0])
                pop = string[0] + "," + string[1:]
            return pop

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getMajorsByPopularity(self, minPopularity, maxPopularity):
        '''
        Retrieves the names of all of the majors that are in the popularity scale
        Parameters:
            minPopularity - the minimum of the desired popularity
            maxPopularity - the maximum of the desired popularity
        Returs:
            A list of major that are within the popularity range
        '''
        majorByPopularity_list = []
        try:
            cursor = self.connection.cursor()
            query = "SELECT major FROM table_2017 WHERE popularity BETWEEN " + minPopularity + " AND " + maxPopularity + " ORDER BY popularity ASC"
            cursor.execute(query)
            for item in cursor.fetchall():
                str = ''.join(item)
                majorByPopularity_list.append(str)
            return majorByPopularity_list
        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    def getMaleAndFemalePopularityPercentage(self, major):
        '''
        Retrieves the percentages of male and female with inputted degree from dataset.
        PARAMETERS:
            major - inputted degree needing to be obtained from database
        RETURN:
            Percentages of male and female holding this degree, or None if query cannot be found
        '''
        try:
            cursor = self.connection.cursor()
            query = "SELECT male, female FROM percentages WHERE major LIKE '" + major + "'"
            cursor.execute(query)
            percentages_list = []
            percentages = cursor.fetchall()
            percentages_list.append(percentages[0][0])
            percentages_list.append(percentages[0][1])
            return (percentages_list)

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    def getMaxInstitutionPopularity(self, major):
        '''
        Retrieves the kind of institution which has the highest popularity of the specified major
        PARAMETERS:
            major - retrieve the kind of institution which has the highest popularity of the this major from the data
        RETURNS:
            A text representing the kind of institution which has the highest popularity of this major, or None if the query fails.
        '''
        major_list = self.getMajorList()
        cursor = self.connection.cursor()
        if major in major_list:
            query = ("SELECT 'Private, non-profit institution', popprivatenp FROM majors WHERE major =\'" + major + "\' AND popprivatenp = GREATEST(poppublic, popprivatenp, popprivatefp) \n"
                    "UNION SELECT 'Private, for-profit institution', popprivatefp FROM majors WHERE major =\'" + major + "\' AND popprivatefp = GREATEST(poppublic, popprivatenp, popprivatefp) \n"
                    "UNION SELECT 'Public institution', poppublic FROM majors WHERE major =\'" + major + "\' AND poppublic = GREATEST(poppublic, popprivatenp, popprivatefp)")
            cursor.execute(query)
            institution = cursor.fetchall()
            return institution

def main():
    pass
main()
