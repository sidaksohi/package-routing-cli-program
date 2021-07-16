# NAME: Sidak Sohi ID: 001126252
import csv
import random

# Parse distances table
with open('distances.csv') as enter_distance:
    reader = csv.reader(enter_distance, delimiter='/')
    distance_dict = {}
    temp_list = []
    counter = 1
    #Puts the distances into a dictionary, the keys being hubs, and the values being other hubs + distance to those hubs
    #Ex: MAIN_HUB : [HUB1, 4.2, HUB2, 5.6, MAIN_HUB, 0.0]

    #Worst case O(n)
    #Space complexity: O(n)
    for row in reader:
        if row != [''] and row != ['', '']:
            row = (str(row).replace("['", "").replace("']", "").replace("South", "S").replace("East", "E"))
            row = str(row).replace("West", "W").replace("Wern", "Western")
            if '.' in row and len(row) <= 5:
                miles = float(row)
                temp_list.append(miles)
                counter += 1
            if counter == 1:
                temp_list.clear()
                temp_key = row
                counter += 1
            elif counter > 1 and len(row) > 5:
                location = row
                temp_list.append(location)
                counter += 1
        else:
            distance_dict[temp_key] = temp_list.copy()
            counter = 1

# Parse packages table
with open('packages.csv') as enter_packages:
    reader = csv.reader(enter_packages, delimiter=',')
    packages = []
    #Put the packages into a hash table, which in this case is a list with another list as each element
    #Ex: [['1', '195 W Oakland Ave', 'Salt Lake City', 'UT', '84115', '10:30 AM', '21', 'None'],['2',...]

    #Worst case: O(n)
    #Space complexity: O(n)
    for row in reader:
        packages.append(row)
    for i in packages:
        i[1] = i[1].replace("South", "S").replace("East", "E").replace("West", "W")
        i.append('AT_HUB')

# All methods
    #Given a start location and end location, find the distance between the two locations
    #Returns the distance, package id, start location, and end location

    #Finds the key in which the start location exists, if one of the values is the end location, then it will append
    #the element right after the end location, as that would be the distance, in how our data structure is set up

    #If the key is found but it doesn't have the end location as a value, then it will look for the distance from the
    #end location to the start location, since the value is the same

    #Worst case: O(n^2)
    #Space complexity: O(n)

    def distance(__start__, __end__, __id__):
        packageDistanceItem = []
        search_check = False
        for x in distance_dict.keys():
            if __start__ in x:
                for index, item in enumerate(distance_dict[x]):
                    if __end__ in str(item):
                        search_check = True
                        packageDistanceItem.append(distance_dict[x].__getitem__(index + 1))
                        packageDistanceItem.append(__id__)
                        packageDistanceItem.append(__start__)
                        packageDistanceItem.append(__end__)
                        return packageDistanceItem
        if not search_check:
            for x in distance_dict.keys():
                if __end__ in x:
                    for index, item in enumerate(distance_dict[x]):
                        if __start__ in str(item):
                            packageDistanceItem.append(distance_dict[x].__getitem__(index + 1))
                            packageDistanceItem.append(__id__)
                            packageDistanceItem.append(__start__)
                            packageDistanceItem.append(__end__)
                            return packageDistanceItem

    #Given a list of packages, this method will find the distances to each package from the hub
    #It will then sort the packages by descending order, and then return the list
    #The last index in the returned list will have the lowest miles, so using pop() on the returned list
    #will get you the package closest to the hub

    #Worst case: O(n^3)
    #Space complexity: O(n)
    def shortestRoute1(routeSort, start):
        routeHiToLow = []
        for index, item in enumerate(routeSort):
            routeHiToLow.append(distance(start, item[1], item[0]))
        routeHiToLow.sort(reverse=True)
        return routeHiToLow

    #This method is very similar to the one above it, however instead of finding the distance to each package from the
    #hub, it finds the shortest distance to the next package, from the given package's delivery address
    #The last index in the returned list will have the lowest miles, so using pop() on the returned list
    #will get you the package closest to the given package's delivery address

    #Worst case: O(n^3)
    #Space complexity: O(n)
    def shortestRoute2(routeSort, start):
        routeHiToLow = []
        for index, item in enumerate(routeSort):
            routeHiToLow.append(distance(start, item[3], item[1]))
        routeHiToLow.sort(reverse=True)
        return routeHiToLow

    #Using the three methods above, this method takes a list of unsorted packages as input, and returns a 'route'
    #First, it finds the package closest to the hub
    #Then, it uses that package's delivery address to find the package closest to that
    #It repeats the above step with the remaining packages
    #Once it runs out of packages, it will then find the distance from the last package to the hub, creating a 'route'

    #Each element in the route is a list, each element being: distance, package id, start location, and end location
    #The last element in the route will have package id stored as 'None', since you are simply returning to the hub

    #Worst case: O(n^4)
    #Space complexity: O(n)
    def routeList(routeSort):
        sortedRoute = []
        sortedRouteTemp = []
        for index, item in enumerate(routeSort):
            if index == 0:
                sortedRouteTemp = shortestRoute1(routeSort, 'Western Governors University')
                sortedRoute.append(sortedRouteTemp.pop())
            if 0 < index < (len(routeSort)-1):
                sortedRouteTemp = shortestRoute2(sortedRouteTemp, sortedRoute[index-1][3])
                sortedRoute.append(sortedRouteTemp.pop())
            if index == (len(routeSort)-1):
                sortedRoute.append(sortedRouteTemp.pop())
                sortedRoute.append(distance((sortedRoute[index][3]), 'Western Governors University', None))
                return sortedRoute
    #Once you have a 'route' already, you can pass it through this method to get the total distance of that route

    #Worst case: O(n)
    #Space complexity: O(n)
    def routeDistance(routeList):
        miles = 0.0
        for i in routeList:
            miles += i[0]
        return miles

    #Given a 'route', this method will append the cumulative distance travelled along the route to each package in route
    #Used to track where the truck is at a given moment, Ex: Truck 1 has travelled 3.3 miles, and the first package is
    #3.0 miles into the route, then the truck has delivered the first package

    #Worst case: O(n)
    #Space complexity: O(1)
    def routeTruckLocation(routeList):
        x = 0.0
        for i in routeList:
            x += i[0]
            i.append(x)

    #Given a 'route', this method will mark that route as IN_TRANSIT, meaning it will update each package's information
    #from 'AT_HUB', to 'IN_TRANSIT', if it is in this route

    #Worst case: O(n^2)
    #Space complexity: O(1)
    def in_transit(routeList):
        for x in routeList:
            for y in packages:
                if x[1] == y[0]:
                    y[8] = 'IN_TRANSIT'


    # Given a package and a time, this method will mark that package as DELIVERED AT [given time], from IN_TRANSIT

    #Worst case: O(n)
    #Space complexity: O(1)
    def delivered(id, time):
        for i in packages:
            if id == i[0]:
                i[8] = 'DELIVERED AT '+time

    #This method takes a package id as input, and returns all information about that package

    #Worst case: O(n)
    #Space complexity: O(1)
    def searchPackage(id):
            for i in packages:
                if str(id) == i[0]:
                    return i
    #This method takes various elements as input, and then uses them to insert a new package into the hash table

    #Worst case: O(1)
    def insertPackage(tempID, address, city, state, zip, deadline, weight, status):
        if status == '1':
            temp_package = [tempID, address, city, state, zip, deadline, weight, None, 'AT_HUB']
        if status == '2':
            temp_package = [tempID, address, city, state, zip, deadline, weight, None, 'IN_TRANSIT']
        if status == '3':
            temp_package = [tempID, address, city, state, zip, deadline, weight, None, 'DELIVERED']
        packages.append(temp_package)

# Sort packages
    initial_packageAssign = packages.copy()
    truck2_1 = []
    delayed = []
    wrongAddress = []
    packagesLeft = []

    #Using the hash table of packages, sort the packages into loads for each route

    #Worst case: O(n)
    #Space complexity: O(n)
    for index, item in enumerate(initial_packageAssign):
        if 12 < int(item[0]) < 21:
            if not 16 < int(item[0]) < 19:
                truck2_1.append(item)
            else:
                packagesLeft.append(item)
        elif 'truck 2' in item[7]:
            truck2_1.append(item)
        elif 'Delayed' in item[7]:
            delayed.append(item)
        elif 'Wrong address' in item[7]:
            wrongAddress.append(item)
        else:
            packagesLeft.append(item)

# Create routes using sorted packages
    #Truck 2 Route 1

    #Worst case: O(n)
    #Space complexity: O(n)
    packagesLeft2 = []
    for i in packagesLeft:
        if i[5] == '10:30:00':
            truck2_1.append(i)
        else:
            packagesLeft2.append(i)

    truck2_1 = routeList(truck2_1)
    truck2_1miles = routeDistance(truck2_1)

    #Truck 2 Route 2

    #Worst case: O(n)
    #Space complexity: O(n)
    truck2_2 = []
    for i in delayed:
        if i[5] == '10:30:00':
            truck2_2.append(i)
        else:
            packagesLeft2.append(i)
    truck2_2 = routeList(truck2_2)
    truck2_2miles = routeDistance(truck2_2)

    #Update the wrong delivery address, add to master list of packages left to ship

    #Worst case: O(1)
    #Space complexity: O(1)
    wrongAddress.append(['9', '410 S State St', 'Salt Lake City', 'UT', '84111', 'EOD', '2', 'None', 'AT_HUB'])
    packagesLeft2.append(wrongAddress.pop())

    #Truck 1 Route 1, Truck 2 Route 3
    #Make a lot of (250) random routes from remaining packages, then pick the routes with the least total distance

    #Worst case: O(n)
    #Space complexity: O(n)

    truck1_1 = []
    randomRoutes = []
    randomShortestRoute = 70.0
    shortestRouteIndex = 0

    for i in range(0, 250, 1):
        __packagesLeft2__ = packagesLeft2.copy()
        random.shuffle(__packagesLeft2__)
        __truck1_1__ = __packagesLeft2__[:14]
        __truck2_3__ = [item for item in __packagesLeft2__ if item not in __truck1_1__]
        randomRoutes.append([__truck1_1__, __truck2_3__])

    for index, item in enumerate(randomRoutes):
        item[0] = routeList(item[0])
        item[1] = routeList(item[1])
        if routeDistance(item[0]) + routeDistance(item[1]) < randomShortestRoute:
            randomShortestRoute = routeDistance(item[0]) + routeDistance(item[1])
            shortestRouteIndex = index

    truck1_1 = randomRoutes[shortestRouteIndex][0]
    truck1_1miles = routeDistance(truck1_1)

    truck2_3 = randomRoutes[shortestRouteIndex][1]
    truck2_3miles = routeDistance(truck2_3)

    print('Total distance for all routes: ', truck1_1miles + truck2_1miles + truck2_2miles + truck2_3miles,
          '\nAll packages were delivered on time!')

#Simulate the day, from 8:00 to 13:00
locationTruck2 = 0.0
locationTruck1 = 0.0
truck2 = True
truck1 = True
truck2_1done = False
truck2_2done = False
truck2_3done = False
truck1_1start = False
truck1_1done = False
    #Using two for loops to get a 'time' for each minute between 8:00 and 13:00

    #Since the for loops both run a constant number of times
    #Worst case: O(1), not including inside of the loops
    #Space complexity: O(n)
for counter in range(8, 14, 1):
     for y in range(0, 60, 1):
            #Sets the time

            #Worst case: O(1)
            #Space complexity: O(1)
            if y < 10:
                time = str(counter) + ':0' + str(y) + ':00'
            else:
                time = str(counter) + ':' + str(y) + ':00'

            #While truck1 or truck2 are delivering packages, add 0.3 miles per minute (or 18 miles per hour)

            #Worst case: O(1)
            #Space complexity: O(1)
            if truck2:
                locationTruck2 += 0.3
            if truck1:
                locationTruck1 += 0.3

            #Fix wrong address at 10:20:00

            #Worst case: O(1)
            #Space complexity: O(1)
            if time == '10:20:00':
                packages[8][1] = '410 S State St'
                packages[8][4] = '84111'
                packages[8][7] = 'None'

            #Start Truck 2 Route 1

            #Worst case: O(n)
            #Space complexity: O(n)
            if time == '8:00:00':
                locationTruck2 = 0.0
                routeTruckLocation(truck2_1)
                in_transit(truck2_1)
            if not truck2_1done:
                if truck2_1[len(truck2_1)-2][0] == 'delivered':
                    truck2_1done = True
                    locationTruck2 = 0.0
                    routeTruckLocation(truck2_2)
                    in_transit(truck2_2)
                for i in truck2_1:
                    if i[4] < locationTruck2:
                        if i[0] != 'delivered' and i[1] is not None:
                            i[0] = 'delivered'
                            delivered(i[1], time)

            #Start Truck 2 Route 2

            #Worst case: O(n)
            #Space complexity: O(n)
            if not truck2_2done and truck2_1done:
                if truck2_2[len(truck2_2) - 2][0] == 'delivered':
                    truck2_2done = True
                    locationTruck2 = 0.0
                    routeTruckLocation(truck2_3)
                    in_transit(truck2_3)
                for i in truck2_2:
                    if i[4] < locationTruck2:
                        if i[0] != 'delivered' and i[1] is not None:
                            i[0] = 'delivered'
                            delivered(i[1], time)

            #Start Truck 2 Route 3

            #Worst case: O(n)
            #Space complexity: O(n)
            if not truck2_3done and truck2_2done:
                if truck2_3[len(truck2_3) - 2][0] == 'delivered':
                    truck2_3done = True
                    truck2 = False
                for i in truck2_3:
                    if i[4] < locationTruck2:
                        if i[0] != 'delivered' and i[1] is not None:
                            i[0] = 'delivered'
                            delivered(i[1], time)

            #Start Truck 1 Route 1

            #Worst case: O(n)
            #Space complexity: O(n)
            if time == '10:20:00':
                locationTruck1 = 0.0
                truck1_1start = True
                routeTruckLocation(truck1_1)
                in_transit(truck1_1)

            if not truck1_1done and truck1_1start:
                if truck1_1[len(truck1_1)-2][0] == 'delivered':
                    truck1_1done = True
                    truck1 = False
                    locationTruck1 = 0.0
                for i in truck1_1:
                    if i[4] < locationTruck1:
                        if i[0] != 'delivered' and i[1] is not None:
                            i[0] = 'delivered'
                            delivered(i[1], time)

            #Create timestamp

            #Worst case: O(n)
            #Space complexity: O(n)
            if time == '8:00:00':
                timeStamp8 = []
                for i in packages:
                    timeStamp8.append(i.copy())
            if time == '9:00:00':
                timeStamp9 = []
                for i in packages:
                    timeStamp9.append(i.copy())
            if time == '10:00:00':
                timeStamp10 = []
                for i in packages:
                    timeStamp10.append(i.copy())
            if time == '11:00:00':
                timeStamp11 = []
                for i in packages:
                    timeStamp11.append(i.copy())
            if time == '12:00:00':
                timeStamp12 = []
                for i in packages:
                    timeStamp12.append(i.copy())
            if time == '13:00:00':
                timeStamp13 = []
                for i in packages:
                    timeStamp13.append(i.copy())

#Main / Command Line Interface
    #A for loop that runs 100 times, used to display the commands again once an endpoint is reached in the CLI

    #Since the for loop runs a constant number of times
    #Worst case: O(1), not including inside of the loop
for counter in range(0, 100):
    userInput = input('\nWelcome! Commands: \'search\', \'insert\', \'status\'\n')

    #Takes a package ID number from the user, and then prints all details of that package

    #Worst case: O(n)
    #Space complexity: O(1)
    if userInput == 'search':
        ID = input('Type a package ID number (1-40):\n')
        print('\nPACKAGE FOUND:\n', searchPackage(ID))

    #Takes elements of a package as input and then adds them into the hashtable of packages

    #Worst case: O(n)
    #Space complexity: O(n)
    if userInput == 'insert':
        tempID = input('Enter a package ID:\n')
        address = input('Enter an address:\n')
        city = input('Enter a city:\n')
        state = input('Enter a state:\n')
        zipCode = input('Enter a zipcode:\n')
        deadline = input('Ex: 9:00:00 for 9:00 AM, 15:00:00 for 3:00 PM, EOD for \'End of Day\''
                         '\nEnter a package deadline:\n')
        weight = input('Enter package weight:\n')
        status = input('1=AT_HUB 2=IN_TRANSIT 3=DELIVERED\nEnter package status:\n')
        insertPackage(tempID, address, city, state, zipCode, deadline, weight, status)
        print('\nPACKAGE INSERTED!:\n', packages.copy().pop())

    #Shows status of packages at a given time or at end of day

    #Worst case: O(n)
    #Space complexity: O(1)
    if userInput == 'status':
        timeStamp = input('Press [Enter] to view all packages at end of day, or type \'more\' to'
                          ' view the status of packages at a certain time!\n')
        if timeStamp == '':
            for i in packages:
                print(i)
        elif timeStamp == 'more':
            timeStamp = input('Type an hour to view all package status at that hour! (Military Time)'
                              '\nValid Inputs: 8, 9, 10, 11, 12, or 13\n'
                              '8 = 8:00 AM, 9 = 9:00 AM, 10 = 10:00 AM, 11 = 11:00 AM, 12 = 12:00 PM, 13 = 1:00 PM\n')
            if timeStamp == '8':
                for i in timeStamp8:
                    print(i)
            elif timeStamp == '9':
                for i in timeStamp9:
                    print(i)
            elif timeStamp == '10':
                for i in timeStamp10:
                    print(i)
            elif timeStamp == '11':
                for i in timeStamp11:
                    print(i)
            elif timeStamp == '12':
                for i in timeStamp12:
                    print(i)
            elif timeStamp == '13':
                for i in timeStamp13:
                    print(i)




