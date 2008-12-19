import re
import urllib2
from BeautifulSoup import BeautifulSoup  

# OWNERS_NAME = re.compile (r"([A-Z][A-Z]+)\s+([A-Z][A-Z]+)")

abandonedFile = open('real.listing', 'r')
outputFile = open('new.abandoned.listing', 'w')

for line in abandonedFile: #I had this as abandoned-file for a while. no dashes in var names.
    print line
    parcelID = re.search("^(\d+)", line)
    print parcelID.group(1)
       
    try:
        ownerURLOPEN = urllib2.urlopen("http://www.cityofboston.gov/assessing/search/default.asp?mode=owner&pid=" + parcelID.group(1)) 
        ownerHTML = ownerURLOPEN.read() #turns the object returned by urlopen and gives a html file.
        
    except:
        continue

    #owner = re.search(r"<td align=\"right\">\s+([A-Z]+)\s+([A-Z]+)", ownerHTML)
    #print owner.group(1)
    #print owner.group(2)
      #owner = re.search(r"<td align=\"right\">\s+([A-Z])\s+([A-Z])", ownerHTML   
    #if owner:
    #   ownersFirstName = owner.group(2)
    #   ownersLastName = owner.group(1)
  

    #print "The owner's name is " + ownersFirstName + " " + ownersLastName

    soup = BeautifulSoup(ownerHTML)
    #print soup.prettify()
    #td = soup('td')
    #print soup.contents
    #print td.contents[0]


    allTR = soup.findAll("tr", "mainCategoryModuleText")

    x = 0

    for TR in allTR:
        print TR.findAll("td", {"align" : "right"})[0].contents[0].strip()
        #infoArray[x] = TR.findAll("td", {"align" : "right"}[0].contents[0].strip()
        #x = x + 1

    infoArray = map(lambda x : x.findAll("td", {"align" : "right"})[0].contents[0].strip(), allTR)

    print infoArray
    #print parcelID

    parcelID = infoArray[0]
    ownersAddress = infoArray[1]
    zoneAType = infoArray[2]
    lotSize = infoArray[3]
    name = infoArray[4] #last name, first name
    address = infoArray[6]

    print "Owner's address is " + address
    
    try:
        streetAddress = re.search("^([\w\d]+\s+[\w\d]+)", address).group(1)
    except:
        streetAddress =""

    #city = re.search(", (.+?),", address).group(1)
    zipCode = re.search("(\d+)$", address).group(1)

    
    print "Name debug: variable name is " + name
    lastName = re.search("^(\w+)", name).group(1)
    if re.search("^[\w']+\s+([\w']+)", name):
        firstName = re.search("^[\w']+\s+([\w']+)", name).group(1)
    else:
        firstName = ""
    state = re.search("(\w+)\s+\d+$", address).group(1)
    
    print "The owner's name is " + firstName + " " + lastName
    print "Lot Size is " + lotSize
    print "The address is " + address
    print "The street address is " + streetAddress
    #print "The city is " + city
    print "The zip code is " + zipCode
    print "The state is " + state
    
    #print soup.contents.contents

    print "hitting try clause"

    ownerURL = "http://api.whitepages.com/find_person/1.0/?firstname=" + firstName + ";lastname=" + lastName + ";street=" + streetAddress + ";city=;state=" + state + ";zip=" + zipCode + ";api_key=162d71ceef8f4aa20bad304f7b2e092a"

    ownerURL = ownerURL.replace(' ','%20')


    #print "trying to open: " + ownerURL

    #ownerHTML = urllib2.urlopen(ownerURL).read()
    
    ownerURLmetro = "http://api.whitepages.com/find_person/1.0/?firstname=" + firstName + ";lastname=" + lastName + ";street=;city=;state=" + state + ";zip=" + zipCode + ";metro=1;api_key=162d71ceef8f4aa20bad304f7b2e092a"

    ownerURLmetro = ownerURLmetro.replace(' ','%20')

   # print "trying ownerHTMLmetro"
   # ownerHTMLmetro = urllib2.urlopen(ownerURLmetro).read()
   # print "ownerHTMLmetro opened"

 #   if re.search("(\(\d+\)\d+-\d+)", ownerHTML).group(1):
    #        phoneNumber = re.search("(\(\d+\)\s+\d+-\d+)", ownerHTML).group(1)
   #         print "1st phone number reg exp match worked."
  #  else:
  #         print "trying to open HTML metro in else/if"
  #         ownerHTMLmetro = urllib2.urlopen(ownerURLmetro).read()
  #         print "just read 2nd owner HTML, metro = 1"
  #         if re.search("(\(\d+\)\s+\d+-\d+)", ownerHTMLmetro).group(1):
  #              phoneNumber = re.search("(\(\d+\)\s+\d+-\d+)", ownerHTML).group(1)
  #              print "2nd reg exp phone number match worked"


#    if re.search("(\(\d+\)\s+\d+-\d+)", ownerHTML):
#        phoneNumber = re.search("(\(\d+\)\s+\d+-\d+)", ownerHTML).group(1)
#        print "1st phone number reg exp match worked."
#    else:
#        print "trying to open HTML metro"
#        ownerHTMLmetro = urllib2.urlopen(ownerURLmetro).read()
#        print "just read 2nd owner HTML, metro = 1"
#        print ownerURLmetro
#        if re.search("(\(\d+\)\s+\d+-\d+)", ownerHTMLmetro):
#            phoneNumber = re.search("(\(\d+\)\s+\d+-\d+)", ownerHTMLmetro).group(1)

    phoneNumber = 0
    
    try:
    
        
        
        ownerHTML = urllib2.urlopen(ownerURL).read()
        print "grabbed owner info HTML"
        if re.search("(\(\d+\)\s+\d+-\d+)", ownerHTML):
            phoneNumber = re.findall("(\(\d+\)\s+\d+-\d+)", ownerHTML)
            #phoneNumber = re.search("(\(\d+\)\s+\d+-\d+)", ownerHTML).group(1)
            print "1st phone number reg exp match worked."
        else:
           print "trying to open HTML metro"
           ownerHTMLmetro = urllib2.urlopen(ownerURLmetro).read()
           print "just read 2nd owner HTML, metro = 1"
           print ownerURLmetro
           if re.search("(\(\d+\)\s+\d+-\d+)", ownerHTMLmetro):
               phoneNumber = re.findall("(\(\d+\)\s+\d+-\d+)", ownerHTMLmetro) 
               #phoneNumber = re.search("(\(\d+\)\s+\d+-\d+)", ownerHTMLmetro).group(1)
    except:
        print "Hitting except clause in phone number logic"
        
    output = line.strip() + "\t" + firstName + "\t" + lastName + "\t" + name + "\t" + lotSize + "\t" + address

    if phoneNumber:

        for listing in phoneNumber:
        
            output = output + "\t" + listing
            print "The owner's # may be " + listing            
    else:
     
        print "No number matched"
        output = output + "\t" + "no number"

    output = output + "\n"
    outputFile.write(output)
