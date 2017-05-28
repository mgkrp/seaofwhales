# seaofwhales
Python program used for a scientific research about suicide propaganda in social networks.  

# Description  
Link to research: https://drive.google.com/file/d/0B-R8HH0HcSEZTDNXbEVPem1QbjA/view?usp=sharing  
Program is used for gathering information about groups of social network "Vkontakte". It collects links from one group to another in ones posts, and classifies group as "good" (no suicide propaganda) or "bad" (consists suicide propaganda). Classificator is Naive Bayess.


# Files and configuration
main.py - main program, requires vk_api library. To successfully use it you need to change "login, password = 'your_login', 'your_password'" to login and passwords from legit Vkontakte account. 
test_Bgroups and test_Ggroups consist of groups for training set. WARNING!!!! There is a good chance that most of groups in test_Bgroups are now closed, so you'll probably need new one if you want to launch it.  
groupdate.py - additional program which takes list of groups and returns number of groups created monthly (i.e groups created at May 2016).

Output files:  
groups.txt - returns number of bad and good posts for each group. Number of bad posts has a multiplier for classifing purposes.
output.txt - returns classes for each group, 0 for "good" and 1 for "bad".
connections.txt - returns every link form one group to another.

# Naive Bayes classifier
For testing set there are 2 sets of group: good and bad. Every group is parsed and every post is used as a post for training based on a class.
For training set groups are formed starting from one account and his groups. Program parses groups from one user as a first iteration and searches for links to another groups. Second iterations consists of groups, found from first, third one consists of groups from second etc. Every post from group is classified with Naive Bayes. After every post is classified groups gets classified depending on which amount of posts is higher. 
