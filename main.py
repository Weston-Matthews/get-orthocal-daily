## Project: get-orthocal-daily
## A simple program which querys the info for the current day from Orthocal.info's API

## Process:
# 1. Check the current date
# 2. Send a GET request to Orthocal.info and get a response
# 3. Unpack the response, organize the info into internal memory
# 4. Set up an email to send to a list of emails in a local JSON file

# First, let's check the current date
# import the date class from the datetime package
from datetime import date

# get the current date
today = date.today();
print("Today's date: ", today);

# Next, use the info from the date to GET a response from Orthocal.info
# import the requests package
import requests

# Set up our date and request info
cal = "gregorian";
year = today.year;
month = today.month;
day = today.day;

# API endpoint
print("Setting up API request URL");
URL = "https://orthocal.info/api/"+cal+"/"+str(year)+"/"+str(month)+"/"+str(day)+"/"

# Send the request
print("Making GET request");
r = requests.get(url = URL);

# Receive the request response JSON
print("Got response!");
data = r.json();

# Formalizing the response data into memory
tone = data["tone"];
print("Tone: ",str(tone));

titles = data["titles"];
print("Titles: "+str(titles));

summary_title = data["summary_title"];
print("Summary title: ",summary_title);

feast_level = data["feast_level"];
print("Feast Level: "+str(feast_level));

feast_level_desc = data["feast_level_description"];
print("Feast Level Description: ",feast_level_desc);

feasts = data["feasts"];
print("Feasts: "+str(feasts));

fast_level = data["fast_level"];
print("Fast Level: "+str(fast_level));

fast_level_desc = data["fast_level_desc"];
print("Fast Level Description: "+str(fast_level_desc));

fast_exception = data["fast_exception"];
print("Fast Exception: "+str(fast_exception));

fast_exception_desc = data["fast_exception_desc"];
print("Fast Exception Description: "+str(fast_exception_desc));

saints = data["saints"];
print("Saints:");
for saint in saints:
    print("   * "+str(saint));

service_notes = data["service_notes"];
print("Service Notes: "+str(service_notes));

abb_reading_ind = data["abbreviated_reading_indices"];
print("Abbreviated Reading Indices: "+str(abb_reading_ind));

readings = data["readings"];
print("Readings:");
for reading in readings:
    print("   * "+reading["display"]);
    for passage in reading["passage"]:
        if str(passage["paragraph_start"]) == "true":
            print("\n")
        print("     "+str(passage["verse"])+" "+str(passage["content"]));
    print("\n")

stories = data["stories"];
print("Stories:");
for story in stories:
    print("   * "+str(story["title"]));
    print("     "+str(story["story"]));
    print("\n")

# Cleaning up the data
clean_tone = "";
if tone == 1:
    clean_tone = "1st Tone";
elif tone == 2:
    clean_tone = "2nd Tone";
elif tone == 3:
    clean_tone = "3rd Tone";
elif tone == 4:
    clean_tone = "4th Tone";
elif tone == 5:
    clean_tone = "5th Tone";
elif tone == 6:
    clean_tone = "6th Tone";
elif tone == 7:
    clean_tone = "7th Tone";
elif tone == 8:
    clean_tone = "8th Tone";
else:
    clean_tone = "No Tone";
    
print(clean_tone);

clean_fast_info = ""
if fast_level > 0:
    clean_fast_info = str(fast_level_desc)
    if fast_exception_desc != "":
        clean_fast_info += " - "+str(fast_exception_desc);
else:
    clean_fast_info = "No Fast";

print(clean_fast_info);

for title in titles:
    print(title);
    
for saint in saints:
    print("* "+saint);

clean_reading = "";
print("Scripture Readings (KJV)");
for reading in readings:
    print(reading["display"]);
    clean_reading += "<b>"+reading["display"]+" ("+reading["source"]+")</b><br>";
    clean_reading += "<p>"
    for passage in reading["passage"]:
        if passage["paragraph_start"] == True:
            clean_reading += "</p><p>";
        clean_reading += "<sup>"+str(passage["verse"])+"</sup>"+str(passage["content"])+" ";
    clean_reading += "</p>"
    clean_reading += "\n"
    print(clean_reading);
    print("\n");
    
clean_date = today.strftime('%A, %B %d, %Y');

clean_feasts = ""
if feasts != None:
    for feast in feasts:
        clean_feasts += str(feast)+"\n";

clean_title = titles[0];

if saints != None:
    clean_saints = "";
    for saint in saints:
        clean_saints += "+ "+str(saint)+"<br>"

clean_stories = "";
if stories != None:
    for story in stories:
        clean_stories += "<b>+ "+story["title"]+"</b><br>";
        clean_stories += story["story"]+"<br>";
    clean_stories += "\n";

# Preparing the data to send in an email
import smtplib
my_gmail = "orthodox.daily.mail@gmail.com";
app_password = "estp ydpg fqwh brwd";

smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465);
smtp_server.ehlo();
smtp_server.login(my_gmail, app_password);

# Building the email to send
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sent_from = my_gmail;

message = MIMEMultipart("alternative");
message["Subject"] = "Orthodox Daily Reflections - "+str(month)+"/"+str(day)+"/"+str(year);
message["From"] = sent_from;

total_email_body = "";

email_body_intro = """\
<html>
 <body>
  <p>Good morning,<br>
    <br>
    Glory to Jesus Christ!<br>
    <br>
    Today is %s<br>
    <br>
    <b>%s</b><br>
    <br>
    %s<br>
    <br>
  </p>
""" % (clean_date, clean_title, clean_tone);

total_email_body += email_body_intro;

email_body_fasting = """\
  <p><b>%s</b><br>
   <br>
  </p>
""" % (clean_fast_info);

total_email_body += email_body_fasting;

if feasts != None:
    email_body_feasts = """\
      <p><b>Feasts</b><br>
       %s<br>
      </p>
    """ % (clean_feasts);

    total_email_body += email_body_feasts;

if saints != None:
    email_body_saints = """\
      <p><b>Commemorations</b><br>
      %s<br>
      </p>
    """ % (clean_saints);
    
    total_email_body += email_body_saints;

email_body_reading = """\
  <p><b>Today's Scripture Readings (KJV)</b><br>
  <br>
  %s<br>
  </p>
""" % (clean_reading);

total_email_body += email_body_reading;

email_body_stories = """\
  <p><b>Commemorations</b><br>
  <br>
  %s
  </p>
""" % (clean_stories);

total_email_body += email_body_stories;

email_body_farewell = """\
  <p><i>May God bless you this day in all that you do!</i><br>
  <br>
  Orthodox Daily Reflections<br>
  Weston Matthews<br>
  </p>
 </body>
</html>
"""

total_email_body += email_body_farewell;

email_content = MIMEText(total_email_body, "html");
message.attach(email_content);

# Getting the list of all the email addresses to send to
from pathlib import Path

filename = "target_addresses.txt";
file_path = Path(__file__).with_name(filename);
send_to_list = [];
with open(file_path) as file:
    for line in file:
        send_to_list.append(line.rstrip("\n"));
print(send_to_list);

smtp_server.sendmail(sent_from, send_to_list, message.as_string());
print("Email sent successfully!");
smtp_server.close();

print("\n");
print("All done!");