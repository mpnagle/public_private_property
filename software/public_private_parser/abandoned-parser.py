#!/usr/bin/env python

""" abandoned-parser.py
original author: http://michaelnagle.org
maintainer: http://michaelnagle.org

abandoned-parser.py

"""

import re # Regular expressions module for flexible text processing
import urllib2 # Used to open and download HTML files from URLs

from BeautifulSoup import BeautifulSoup # Used for screen scraping HTML

# Opens tab-separated-value (TSV) file where the first value of every
# line is a parcel ID number
abandonedFile = open('real.listing', 'r') # read mode

# The file we are writing owners' information to
outputFile = open('new.abandoned.listing', 'w') # write more


for line in abandonedFile:
    # TODO: Document abandoned-parser writing experience
    # TODO: Note no dashes in variable names
    print line

    # This regular expression looks for one or more digits at the
    # beginning of a line In our case, it matches the parcel ID number
    # at the beginning of each line in real.listing
    parcelIDmatches = re.search("^(\d+)", line)

    parcelID = parcelIDmatched.group(1) # The actual parcel ID number.
    print parcelID

    # Trying to download the page 
    try:
        bostonParcelSearchURL = "http://www.cityofboston.gov/assessing/search/default.asp?mode=owner&pid=" + parcelID
        ownerURLobject = urllib2.urlopen(bostonParcelSearchURL) 
        ownerHTML = ownerURLobject.read() # Converts urlopen object to HTML file.

    except: # If opening the HTML file fails, skip to next parcel
        continue

    soup = BeautifulSoup(ownerHTML) # BeautifulSoup takes HTML and
                                    # creates an easy to navigate tree
                                    # structure to browse the HTML
                                    # tree (also known as the DOM
                                    # tree)

    allTableRows = soup.findAll("tr", "mainCategoryModuleText")


    # TODO: Document list comprehensions

    # Finds all td elements with the "align" attribute set to "right",
    # grabs the first (which was the owner's information, and grabs
    # the child root using contents, takes the first element, and
    # strips all the whitespace, creating a list out of the results.
    infoArray = (TR.findAll("td", {"align" : "right"})[0].contents[0].strip() for TR in allTableRows)
    print "\n".join(infoArray) # Prints property info broken up by newlines

    (parcelID,
     ownersAddress,
     zoneType,
     lotSize,
     ownerName, # ownerName is a string of the form "lastName firstName"
     lotAddress) = infoArray


    print "Owner's address is " + address
    
    # Searches address for two alphanumeric character blocks
    # ([\w\d]+) broken up by whitespace (\s+)
    streetAddressMatch = re.search("^([\w\d]+\s+[\w\d]+)", address)
    if streetAddressMatch: # Won't execute if no street address found
        streetAddress = streetAddressMatch.group(1)
    else: # If there are no matches
        streetAddress = ""

    # Searches address for group of digits (\d+) which ends the line ($)
    zipCodeMatches = re.search("(\d+)$", address)
    zipCode = zipCodeMatches.group(1)

    
    print "DEBUG: ownersName = " + ownersName

    lastNameMatches = re.search("^(\w+)", name)
    lastName = lastNameMatches.group(1)

    # TODO: Find out why ' make sense; we assume that this is just
    # handling a one-off case

    firstNameMatch = re.search("^[\w']+\s+([\w']+)", ownersName)
    if firstNameMatch: # Won't execute if no first name found
        firstName = firstNameMatch.group(1)
    else:
        firstName = ""

    # Captures the group of letters that precedes the zipcode
    stateMatch = re.search("(\w+)\s+" + zipCode + "$", address)
    state = stateMatch.group(1)
    
    print "The owner's name is " + firstName + " " + lastName
    print "Lot Size is " + lotSize
    print "The address is " + address
    print "The street address is " + streetAddress
    print "The zip code is " + zipCode
    print "The state is " + state

    # Starting WhitePages.com parsing and searching

    # Constructs URL for searching whitepages, using an API key which
    # you can sign up for at http://developer.whitepages.com/page As
    # of Dec 2008, the API key lets you make 1500 searches a day at a
    # rate of 2 per second.

    # This is the tightest match; it searches for the street name.
    rawWhitePagesURL = "http://api.whitepages.com/find_person/1.0/?firstname=" + firstName + ";lastname=" + lastName + ";street=" + streetAddress + ";city=;state=" + state + ";zip=" + zipCode + ";api_key=162d71ceef8f4aa20bad304f7b2e092a"

    # TODO: Document debugging frustration
    # ownerURL = ownerURL.replace(' ','%20')

    # Encodes the string appropriately for passing to urlopen, turning
    # spaces --> %20 and other special characters.  See
    # http://docs.python.org/library/urllib.html#urllib.quote for
    # details
    whitePagesURL = urllib.quote(rawWhitePagesURL)

    #phoneNumber = 0 

    try:        
        ownerHTML = urllib2.urlopen(ownerURL).read()
        print "grabbed owner info HTML"
        if re.search("(\(\d+\)\s+\d+-\d+)", ownerHTML):
            phoneNumber = re.findall("(\(\d+\)\s+\d+-\d+)", ownerHTML)
            print "1st phone number reg exp match worked."
        else:
            rawWhitePagesURLmetro = "http://api.whitepages.com/find_person/1.0/?firstname=" + firstName + ";lastname=" + lastName + ";street=;city=;state=" + state + ";zip=" + zipCode + ";metro=1;api_key=162d71ceef8f4aa20bad304f7b2e092a"

            ownerURLmetro = ownerURLmetro.replace(' ','%20')

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
