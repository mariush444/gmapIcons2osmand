#!/usr/bin/python
#
# command is kmz2osmand.py file.kmz > new_file.gpx
#
#==================info==converter made on ================================
# https://timwise.co.uk/2014/02/03/converting-kml-to-gpx-with-python/
# https://gist.github.com/timabell/8791116
# https://01027865525950270145.googlegroups.com/attach/6d0b727d3116c/KMLtoOSMAndGPX.py?part=0.1&view=1&vt=ANaJVrF87hVJpbOELCCSiOKXR2bKZ3OiLSQJOVUJ5vodeupKHMSVD5bdBwMe1lyf-RAx8zIt9JGcMZxumJrTzj0_LjaVLu-73-YeYbGtF_fkTiJmWS8_Ug4
# https://github.com/timabell/timwise.co.uk/blob/main/_posts/2014-02-03-converting-kml-to-gpx-with-python.md
# https://www.mail-archive.com/osmand@googlegroups.com/msg07817.html
#==========================run==============================================
# ./kmlToGpx.py "25-01 12-48.kml" > "25-01 12-48.kml.gpx"
# mulit conversion for f in *.kml; do ./kml_to_gpx.py ${f} > ${f}.gpx; done
#=====================main idea=============================================
# 8/11/2020 Tom Musolf - based on some code I found on the internet from Tim Abell
#
# Quick hack (no error checking & I'm not a python guy) to convert Google My Maps KML export files to
# GPX files for OSMAnd mapping program on Android phones.
#
# There are lots of KML to GPX converters out there, like GPSVisualizer.com, but they all lose the KML icon and color info
# during the translation.  In addition, OSMAnd has it's own GPX extensions for it's custom icons.
# What this program does is convert KML waypoints and tracks/lines into their OSMAnd GPX equivalents.
#
# KML Layers
#		Layers are ignored, but all tracks and points found in the KML file are translated into their OSMAnd GPX file equivalent.
#
# Tracks
#		Track name and description are translated.
#		Tracks will carry the color specified in the KML file into OSMAnd.
#		Line width is not translated because it is not supported in OSMAnd.
#		A default transparency value for the track is specified using the TrackTransparency variable.
#
# Points
#		Name and description are translated.
#		The KML icon is translated to an OSMAnd equivalent using the iconDictionary translation table.
#		This table contains
#			OSMAnd equivalent icon
#			A color for the icon or you can specify using the icon color from the KML file
#			Which of the 3 icon shapes that OSMAnd supports.
#		If the KML icon is not found in the table then a default/unknown icon is used.
# Other
#		All other KML structures/tags are ignored
#
# Once you have your GPX file copy it to this location on your android phone: .../Android/data/net.osmand.plus/files/tracks
# Note: The tracks folder supports nested folders so you can create folders such as: .../tracks/hikes and .../tracks/BikeRoutes
# These folders and their GPX files will then show up in OSMAnd MyPlaces>Tracks
#
# I use OSMAnd configure map>GPX files>Appearance>Bold for the tracks I display with my GPX files.  With track transparency set to
# 55 (via this program) it lets me read street names and still see the track.
#
# Make sure you have python installed on your PC
#
#		Cmd format: py KMLToOSMAndGPX.py "input file" > "output file"
#
# If no output file is specified output goes to standard out.
#
# Again, NO ERROR CHECKING is done for presence of input file, valid KML file structure, etc.
#=======================modifications======================================
# 01/07/2021 Mariusz444
# works with python3
# converting icons directly from KMZ instead of KML !!!!!! - new styles icon only
# command is kmz2osmand.py file.kmz > new_file.gpx
# some modification for new ver. of OSMAND v. 3.9.10
#
#		<wpt lat="39.2906659" lon="-121.4965106">
#			<name>hiker, pale yellow</name>
#			<extensions>
#			<osmand:color>#eeee10</osmand:color>
#			<osmand:icon>special_trekking</osmand:icon>
#			<osmand:background>circle</osmand:background>
#			</extensions>
#		</wpt>
#   some icons were added
#   additionally some variants of color for google icon 1899 and 503 -> osmand special_star
#===========================================================================

import argparse
import xml.sax
from zipfile import ZipFile
import os

parser = argparse.ArgumentParser(description='Convert annoying google android my tracks kmz data to sensible gpx files')
parser.add_argument('input_file')

args = parser.parse_args()
input = args.input_file

with ZipFile(input, 'r') as zipObj: zipObj.extract('doc.kml')
input = 'doc.kml'

#iconDictionary describes the mapping between a KML icon number and an OSMAnd icon name.
#It also contains a default OSMAnd color and shape to use for each OSMAnd icon type.
#
#iconDictionary format:
#		"KML icon number":["OSMAnd Icon name","HTML hex color code or flag to use KMLCOLOR","OSMAnd shape"]
#
#Color code is a standard HTML hex color code.  This is what OSMAnd uses
#As of 8/2020 OSMAnd icons do not support transparent colors.
#As of 8/2020 OSMAnd supports 3 icon shapes: circle, octagon, square
#
#Adding additional KML icons to the dictionary.
#
# For each icon you want to translate you need to add a new entry/line into the iconDictionary table.
# To determine what the KML and OSMAnd icons are you want go through the following steps:
#
# KML icon number
# 	1) Create a google my maps test file with the icons you want to use.
# 	2) Export this map as a KML file.
# 	3) Open up the file in a text editor and look for your points. You can ignore all the <style> & <StyleMap> tags at the
#	   beginning of the KML file.  The points/waypoints/Placemarks will look like this:
#
#		<Placemark>
#			<name>Mileage Marker dot</name>
#			<styleUrl>#icon-1739-0288D1-nodesc</styleUrl>
#			<Point>
#				<coordinates>-120.8427259,38.8170119,0</coordinates>
#			</Point>
#		</Placemark>
#
#The <styleUrl> tag has the icon number.  In the preceeding example it's "1739".
#
# OSMAnd Icon name
#	1) Create some favorites using the icons you want.
#	2) Goto .../Android/data/net.osmand.plus/files/favourites.gpx    !!! yes, it's spelled the british way.
#	3) Open the favorites file in a text editor and look for the waypoints.  I
#	   in the following example the icon name is: "special_trekking"
#
#		<wpt lat="39.2906659" lon="-121.4965106">
#			<name>hiker, pale yellow</name>
#			<extensions>
#			<color>#eeee10</color>
#			<icon>special_trekking</icon>
#			<background>circle</background>
#			</extensions>
#		</wpt>
#
# Put the string "KMLCOLOR", without the double quotes, in for a color value if you want to use the color specified in the KML file
# for a particular icon.
KMLCOLOR = "KMLCOLOR"

iconDictionary ={
	"unknown":["special_symbol_question_mark","000001","octagon"],			#unknown KML icon code - this entry will be used if the KML icon is not found in the iconDictionary.
	"503":["special_star","d00d0d","circle"],								# red point -> red star
	"1501":["special_bookmark","eecc22","circle"],							#POI #5, ribbon/diamond
	"1502":["special_star",KMLCOLOR,"circle"],								#POI #4, star
	"1504":["air_transport","10c0f0","circle"],								#airport, airstrip
	"1507":["shop_pet","d00d0d","circle"],									# animals, birds, ...
	"1510":["amenity_atm","10c0f0","square"],								#ATM
	"1525":["water_transport","a71de1","octagon"],							#river access
	"1528":["bridge_structure_arch","d00d0d","circle"],						#bridge
	"1535":["special_photo_camera","eecc22","circle"],						#POI #1, camera
	"1538":["special_wagon","a71de1","square"],								# rental car, pick car up
	"1539":["shop_car_repair","a71de1","circle"],							# workshop, rapir car
	"1541":["special_symbol_exclamation_mark","ff0000","octagon"],			#danger #1 exclamation
	"1546":["place_city","d00d0d","circle"],								# nice building, ethno house, old town ...
	"1564":["special_symbol_exclamation_mark","ff0000","octagon"],			#danger #2 explosion
	"1574":["special_flag_stroke","eecc22","circle"],						#POI #2, flag
	"1577":["restaurants","10c0f0","square"],								#retaurant, diner, dining
	"1578":["shop_supermarket","10c0f0","circle"],							#grocery store, supermarket
	"1581":["fuel","a71de1","circle"],										#gas station
	"1596":["special_trekking","d00d0d","cirlce"],							#hiking trailhead, walk
	"1598":["historic_castle","d00d0d","cirlce"],							#archeo, palace, castle, historic monument ...
	"1602":["tourism_hotel","1010a0","circle"],								#hotel, lodge
	"1603":["special_house","d00d0d","circle"],								#house
	"1608":["tourism_information","10c0f0","square"],						#tourism information
	"1624":["amenity_hospital","d00d0d","circle"],							#hospital, doctor, emergency room
	"1636":["tourism_museum","d00d0d","circle"],							# museum
	"1644":["parking","a71de1","circle"],									#parking area
	"1650":["tourism_picnic_site","eecc22","circle"],						#picnic site
	"1655":["amenity_police","1010a0","circle"],							#ranger/police station #1
	"1657":["amenity_police","1010a0","circle"],							#ranger/police station #2
	"1670":["religion_christian","d00d0d","circle"],						# christian, church, monastery, chapel
	"1673":["religion_muslim","d00d0d","circle"],							# muslim, islam, madrasah, mosque
	"1685":["shop_supermarket","10c0f0","square"],							# supermarket, glocery, frashmarket
	"1703":["amenity_drinking_water","10c0f0","square"],					# water, potable woter
	"1710":["special_arrow_up_and_down","10c0f0","circle"],					#river gauge, up/down arrow or thermometer
	"1723":["tourism_viewpoint","d90000","octagon"],						#rapid
	"1729":["tourism_viewpoint","d00d0d","cirlce"],							# viewpoint, panorama
	"1733":["amenity_toilets","10c0f0","circle"],							#toilet, restroom
	"1739":["special_symbol_plus","1010a0","circle"],						#Mileage marker plus-KML dot
	"1765":["tourism_camp_site","1010a0","circle"],							# campsite -> camping
	"1767":["natural_cave_entrance","d00d0d","cirlce"],						# cave
	"1803":["special_arrow_right_arrow_left","d00d0d","circle"],			# turn, nice road, should be special_arrow_down_left but I prefered special_arrow_right_arrow_left
	"1879":["amenity_biergarten","10c0f0","circle"],						#brewery, brew pub
	"1892":["waterfall","d00d0d","circle"],									# waterfall
	"1899":["special_star","d00d0d","circle"],								#POI #3, pin -> red star
	}

# TrackTransparency: This value specifies the amount of transparency that a track will have when displayed in OSMAnd.
# this is a 2 digit hex value from 00 (fully transparent) to FF (fully opaque)
# This value is concatinated to the front of the track color value.
# For example: Bright pink is: F700FF if you want it very transparent, say only 25%, you would set TrackTransparency to "40".
# A 2 digit hex value goes from 0x00=0 to 0xFF=255 so 25% of 255 is 64 decimal which is 40 hex.
# So the <color> value for a 25% bright pink line would end up being "40F700FF" in the GPX file.
#
# As of 8/2020 transparency in the color value is only supported for OSMAnd tracks, not icons TrackTransparency = "55"
#
# TrackTransparency = '7D'
#
#There are certain characters that can't be in HTML/XML name or description strings.
#This function converts them to the HTML escaped version
html_escape_table = {
	"&": "&amp;",
	'"': "&quot;",
	"'": "&apos;",
	">": "&gt;",
	"<": "&lt;",
	}

def html_escape(text):
	"""Produce entities within text."""
	return "".join(html_escape_table.get(c,c) for c in text)

class KmlParser(xml.sax.ContentHandler):
	def __init__(self):
		self.in_tag=0
		self.chars=""
		self.inPlacemark=0
		self.inDocument=0
		self.inLine=0
		self.name =""
		self.description=""
		self.style=""
		self.styleIcon=""
		self.styleColor=""

	def startElement(self, name, attrs):
		if self.inDocument==0: #we're entering document section looking for <name> element only
			if name == "Document":
				#print("Start Document")
				self.inDocument = 1
			elif self.inPlacemark==0: # we're not in a placemark, ignore other elements till we get a placemark
				if name =="Placemark":
					self.inPlacemark = 1
			else: # we're in a placemark
				if name == "LineString":
					self.chars=""
					self.inLine=1
				if name == "name":
					self.in_tag =1
					self.chars=""
				elif name == "styleUrl":
					self.in_tag=1
					self.chars=""
				elif name =="coordinates":
					self.in_tag =1
					self.chars=""
				elif name =="description":
					self.in_tag = 1
					self.chars=""
		else: # we're in a docment looking only for <name> element
			if name == "name":
				self.in_tag =1
				self.chars=""
	def characters(self, char):
		if self.in_tag:
			self.chars += char
	def endElement(self, name):
		if self.inDocument==1: #we're in a document and looking only for the </name> element
			if name == "name":
				self.inDocument = 0
				print("<metadata>")
				print("\t<name>"+self.chars+"</name>")
				print("</metadata>")
				self.chars=""
				self.in_tag = 0
		elif self.inPlacemark == 1:
			if name == "Placemark":
				if self.inLine==1: #we're doing a line/track placemark
					print("<trk>")
					print("\t<name>"+self.name+"</name>")
					if self.description != "":
						print("\t<desc>"+self.description+"</desc>")
					print("\t<trkseg>")
					i=0
					while i < len(self.coordinates):
						print("\t\t<trkpt lat=\""+self.coordinates[i+1]+"\" lon=\""+self.coordinates[i]+"\"/>")
						i=i+3
					print("\t</trkseg>")
					print("\t<extensions>")
					style = self.style.split("-")
					self.styleWidth=float(style[2])/1000
					self.styleColor=style[1]
					print("\t\t<osmand:color>#"+TrackTransparency+self.styleColor+"</osmand:color>")
					# 8/2020 it appears that OSMAnd ignores width and opacity tags
					print("\t\t<width>"+str(self.styleWidth)+"</width>")
					print("\t\t<opacity>1</opacity>")
					print("\t</extensions>")
					print("</trk>")
				else:	#it's waypoint
					print("<wpt lat=\""+self.coordinates[1]+"\" lon=\""+self.coordinates[0]+"\">")
					print("\t<name>"+self.name+"</name>")
					if self.description != "":
						print("\t<desc>"+self.description+"</desc>")
					print("\t<extensions>")
					style = self.style.split("-")
					self.styleIcon=style[1]
					self.styleColor=style[2]
					#it's a KML icon that we haven't put in the dictionary so use a default one.
					if not self.styleIcon in iconDictionary:
						self.styleIcon="unknown"
					if iconDictionary[self.styleIcon][1] == KMLCOLOR: choosen_color=self.styleColor #use the icon color from the KML file # print("\t\t<osmand:color>#"+choosen_color+"</osmand:color>")
					else: choosen_color=iconDictionary[self.styleIcon][1] #use the icon color from the dictionary table
					if self.styleIcon in ['1507','1528','1546','1596','1598','1603','1636','1670','1673','1729','1767','1803','1892','1899']: # change from red (default) to ...
						if self.styleColor in ['FFEA00','ffea00','FFD600','ffd600']: choosen_color='eecc22'  # yallow
						elif self.styleIcon == '1899' and self.styleColor in ['000000','424242']: choosen_color='000001'  # black
						elif self.styleIcon == '1899' and self.styleColor in ['0F9D58','0f9d58','097138','7CB342','7cb342','55892F','55892f']: choosen_color='00842b'  # green
					if self.styleIcon == '503': # change from red (old default point) to ... ...
						if self.styleColor in ['F4EB37','f4eb37','FAF7A7','faf7a7','FFDD5E','ffdd5e']: choosen_color='eecc22'  # yallow point
					# print("\t\t"+self.styleIcon+" "+self.styleColor)
					print("\t\t<osmand:color>#"+choosen_color+"</osmand:color>")
					print("\t\t<osmand:icon>"+iconDictionary[self.styleIcon][0]+"</osmand:icon>")
					print("\t\t<osmand:background>"+iconDictionary[self.styleIcon][2]+"</osmand:background>")
					print("\t</extensions>")
					print("</wpt>")
				self.name =""
				self.description=""
				self.styleIcon=""
				self.styleColor=""
				self.style=""
				self.inLine=0
				self.inPlacemark = 0 #closing out a placemark
			elif name == "name":
				#ampersands and other special characters cause a problem in the XML/GPX file so replace them
				#with an XML escaped version.
				self.name = html_escape(self.chars.strip())
				self.chars=""
				self.in_tag = 0
			elif name == "styleUrl":
				#style string is a different format for a track/line vs waypoint in KML
				self.style=self.chars
				self.chars=""
				self.in_tag = 0
			elif name == "coordinates":
				#end up with a list of coordinates lon, lat, alt
				self.coordinates=self.chars.strip().replace(" ","").replace("\n",",").split(",")
				self.chars=""
				self.in_tag = 0
			elif name == "description":
				# Make sure to escape special characters and convert <br> in KML descriptions into carriage return/line feed
				# characters that OSMAnd likes.
				self.description = html_escape(self.chars.replace("<br>","\r\n"))
				self.chars=""
				self.in_tag = 0

#GPX header
print ("""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<gpx version="1.1" creator="OsmAnd+ 3.9.10" xmlns="http://www.topografix.com/GPX/1/1" xmlns:osmand="https://osmand.net" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">""")

parser = xml.sax.make_parser()
parser.setContentHandler(KmlParser())
parser.parse(open(input,"r"))

#GPX footer
print ("</gpx>")
#***end***
if os.path.exists(input):  os.remove(input)
