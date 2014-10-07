from scipy.io import loadmat
import pygmaps
import webbrowser

import os
import gzip
import zlib
import struct
import sys
from optparse import OptionParser

class Point:
  longitude = 0.0
  latitude = 0.0
  
class Trip:
  name = ''
  start_point = Point()
  end_point = Point()
  path_list = None # list cannot be initialized here!
  path_color = ''
  Trip_index = 0
  
def traverseFolder(directory, suffix, number):
    fileList = []
    for file in os.listdir(directory):
        if os.path.isdir(directory + file): # if current path is still the folder, then get into it
            thisPath = directory + file + '/'
            fileList = fileList+traverseFolder(thisPath, suffix)
        elif file.endswith(suffix):
            fileName = directory + file
            fileList.append(fileName)
            if len(fileList) >= number:
              break
    return fileList

def draw_coroutes(directory, number):
  filelist = traverseFolder(directory, '.mat', number)
  print(filelist)
  
  color_list = ['Aqua',
    'Alizarin crimson',
    'Amber',
    'Amethyst',
    'Android Green',
    'Azure',
    'Deep pink']
  
  color_dictionary = {'Aqua':       "#00ffff",
          'Alizarin crimson': "#e32636",
          'Amber':      "#ffbf00",
          'Amethyst':   "#9966cc",
          'Android Green':    "#a4c639",
          'Azure':      "#007fff",
          'Deep pink':    "#ff1493"
      }
  
  start_color = "#0000FF"
  end_color = "#FF0000"
  
  index = 0
  coRoute_list = []
  
  for file in filelist:
    Trip_data = load_mat_file(file) # load origin .mat data
    point_list = extract_points_location(Trip_data)
    
    trip = Trip()
    trip.name = file
    trip.start_point = point_list[0]
    trip.end_point = point_list[-1]
    trip.Trip_index = index
    trip.path_list = []
    trip.path_color = color_list[index]
    
    for i in point_list:
      route.path_list.append(tuple([i.longitude, i.latitude]))

    # draw start point, end point, route_path
    mymap = pygmaps.maps(route.start_point.longitude, route.start_point.latitude, 12) # start a map
    mymap.addpoint(route.start_point.longitude, route.start_point.latitude, start_color)
    mymap.addpoint(route.end_point.longitude, route.end_point.latitude, end_color)
    mymap.addpath(route.path_list, color_dictionary[route.path_color])
    index = index + 1
    
    map_path = file.split("/")[-1][:-4] + '.map.draw.html'  # delete the '.mat' and add '.map.draw.html'
    mymap.draw(map_path)
    url = map_path
    webbrowser.open_new_tab(url)
    coRoute_list.append(route)

def load_mat_file (filepath):
  structure_data = c(filepath)
  Trip_data = structure_data['trip']
  return Trip_data

# extract data of each point
def extract_points_location (Trip_data):

  a = Trip_data['Location']
  b = a['Longitude']
  print(len(b))
  c = a['Latitude']
  
  for i in Trip_data:
    new_point = Point()

    point_list.append(new_point)
  return point_list

def main(): 
    parser = OptionParser(usage = "usage: %prog [-b] arg1 [-n] arg2", version = "%prog 1.0")
    parser.add_option("-d", "--directory", action="store", dest="directory",
          default='../test_data/SOSD1/',
          help="set directory path of coroute .mat files.")
    parser.add_option("-n", "--number", action="store", dest="number",
          default=10,
                      help="Choose how many routes you want to draw")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
    (options, args) = parser.parse_args()
    # print options
    # print args
    # if len(options) < 3:
        # parser.error("incorrect number of arguments")
    if options.verbose:
        print "unzip all .gz files in %s..., and extract them in the same folder hierachy in %s" % (options.directory, options.number)
    
    draw_coroutes(options.directory, 7)
    
if __name__ == '__main__':
  main()