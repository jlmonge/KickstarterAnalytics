#this file will contain all the functions that test the analytic functions from analytic_functions.py

from app_interface import loadJsonFile
from analytic_functions import average_length_ks, most_funded_category_per_year,countProjects#other analytic function here



global data
class unit_tests_average_length_ks:
    def run_all(self):
        self.single_ks()
        self.empty_file()
        self.two_ks_same_value()
        self.several_different_ks_lengths_value()
        self.several_different_ks_years()
        self.same_deadline_and_launched()
        self.deadline_before_launched()
    def single_ks(self):#tests list with a single value
        mockData = [{ 'deadline': '2015-10-09', 'launched': '2015-08-11 12:12:28'}]
        labels, analyticByYear,unused = average_length_ks(mockData)
        assert (labels[0] == "2015"),"With only one ks, we pass back the correct year"
        assert (analyticByYear[0] == 59), "With only one ks, the average is the length of the ks"
    def two_ks_same_value(self):#tests a list with two of the same value
        mockData = [{ 'deadline': '2015-10-09', 'launched': '2015-08-11 12:12:28'},{ 'deadline': '2015-10-09', 'launched': '2015-08-11 12:12:28'}]
        labels, analyticByYear,unused = average_length_ks(mockData)
        assert (labels[0] == "2015"), "with these two ks, the only label should be 2015"
        assert (analyticByYear[0] == 59), "with two ks of the same length the average is the length of the kickstarters"
    def empty_file(self):#tests an empty list
        mockData = [{}]
        labels, analyticByYear,unused = average_length_ks(mockData)
        assert (len(labels) == 0), "With empty data, length of labels is zero"
        assert (len(analyticByYear) == 0), "With empty data, length of analyticByYear is zero"
    def several_different_ks_lengths_value(self):#tests kickstarters with varried lengths
        mockData = [{ 'deadline': '2015-10-07', 'launched': '2015-08-11 12:12:28'},{ 'deadline': '2015-10-09', 'launched': '2015-08-11 12:12:28'},
        { 'deadline': '2015-10-08', 'launched': '2015-08-11 12:12:28'},{ 'deadline': '2015-10-09', 'launched': '2015-08-11 12:12:28'}]
        labels, analyticByYear,unused = average_length_ks(mockData)
        assert (labels[0] == "2015"), "with these four ks, the only label should be 2015"
        assert (analyticByYear[0] == 58.25), "with two ks of the length 57,59,60,59 days should be 55"
    def several_different_ks_years(self):#tests kickstarters with varied years
        mockData = [{ 'deadline': '2015-10-10', 'launched': '2015-08-11 12:12:28'},{ 'deadline': '2015-10-09', 'launched': '2014-08-11 12:12:28'},
        { 'deadline': '2015-10-08', 'launched': '2015-08-11 12:12:28'},{ 'deadline': '2015-10-09', 'launched': '2014-08-11 12:12:28'}]
        labels, analyticByYear,unused = average_length_ks(mockData)
        assert ("2015" in labels), "within these four ks, a label should be 2015"
        assert ("2014" in labels), "within these four ks, a label should be 2014"
        find2014 = 0
        find2015 = 1
        if labels[find2014] != "2014":
            find2014 = find2014 + 1
            find2015 = find2015 - 1
        assert (analyticByYear[find2014] == 424), "the two 2014 ks of the length 424 days should be have average lenght of 424"
        assert (analyticByYear[find2015] == 59), "the two 2015 ks of the length 58 and 60 days should be have average lenght of 59"
    def same_deadline_and_launched(self):#tests if deadline is the same day as launched
        mockData = [{ 'deadline': '2015-10-10', 'launched': '2015-10-10 12:12:28'}]
        labels, analyticByYear,unused = average_length_ks(mockData)
        assert (labels[0] == "2015"), "with this, the only label should be 2015"
        assert (analyticByYear[0] == 0), "ks of the length 0 days should return zero"
    def deadline_before_launched(self):#tests if kickstarters with a launch date before the deadline date were disposed of.
        mockData = [{ 'deadline': '2015-10-10', 'launched': '2016-10-10 12:12:28'}]
        labels, analyticByYear,unused = average_length_ks(mockData)
        assert ("2016" not in labels), "launched after deadline, ks is thrown away"


#NOTE: Current implementation of count projects does not handle years after 2018.
class unit_tests_count_projects:
    def run_all(self):
        self.single_ks()
        self.empty_file()
        self.several_ks_per_year()
        self.several_ks_in_several_years()
    def single_ks(self):#Test a single value
        mockData = [{'launched': '2015-08-11 12:12:28'}]
        returnDictionary = countProjects(mockData)
        assert(returnDictionary['2015'][7] == 1),"ks in 08 of 2015 is found in the correct location"
    def empty_file(self):#Test an empty data structure being passed
        mockData = [{}]
        returnDictionary = countProjects(mockData)
        for year in returnDictionary:
            for month in range(0,11):
                assert(returnDictionary[year][month] == 0),"empty file results in all values being zero"
    def several_ks_per_year(self): #test several inputs in one year
        mockData = [{'launched': '2015-08-11 12:12:28'},{'launched': '2015-09-31 12:12:28'},{'launched': '2015-08-10 12:12:28'}]
        returnDictionary = countProjects(mockData)
        assert(returnDictionary['2015'][7] == 2),"two ks in 08 of 2015"
        assert(returnDictionary['2015'][8] == 1),"one ks in 09 of 2015"
    def several_ks_in_several_years(self):
        mockData = [{'launched': '2014-08-11 12:12:28'},{'launched': '2015-09-31 12:12:28'},{'launched': '2015-09-10 12:12:28'},{'launched': '2014-08-10 12:12:28'},{'launched': '2011-01-11 12:12:28'}]
        returnDictionary = countProjects(mockData)
        assert(returnDictionary['2014'][7] == 2),"two ks in 08 of 2014"
        assert(returnDictionary['2015'][8] == 2),"two ks in 09 of 2015"
        assert(returnDictionary['2011'][0] == 1),"one ks in 01 of 2011"

avg_length_unit_test_object = unit_tests_average_length_ks()
avg_length_unit_test_object.run_all()
unit_tests_count_projects_object = unit_tests_count_projects()
unit_tests_count_projects_object.run_all()