import time
import random
from environmentConstants import *
from HelperFunctions import *

LEFT_WHEEL_JOINT = "/leftWheelJoint_"
RIGHT_WHEEL_JOINT = "/rightWheelJoint_"
ULTRASONIC_SENSOR = "/ultrasonicSensor_"
VISION_SENSOR = "/sensor[1]"
GOAL_BUFFER = 1


class dr20:
    """
        A controller for the DR20 Robot
    """

    def __init__(self, sim, nameString, threadID):
        self.sim = sim
        self.floor = sim.getObject(FLOOR)
        self.robot = sim.getObject(nameString)
        self.ID = threadID
        self.leftWheel = sim.getObject(nameString + LEFT_WHEEL_JOINT)
        self.rightWheel = sim.getObject(nameString + RIGHT_WHEEL_JOINT)
        self.ultrasonicSensor = sim.getObject(nameString + ULTRASONIC_SENSOR)
        self.visionSensor = sim.getObject(VISION_SENSOR)
        self.visionSensorResolution = sim.getVisionSensorResolution(self.visionSensor)

    def getCurrentAngle(self):
        lx, ly, lz = self.sim.getObjectPosition(self.leftWheel, self.floor)
        rx, ry, rz = self.sim.getObjectPosition(self.rightWheel, self.floor)
        return round(math.atan2(ly - ry, lx - rx) * 180 / math.pi) - 90

    def getCurrentPosition(self):
        cx, cy, cz = self.sim.getObjectPosition(self.robot, self.floor)
        return cx, cy, cz

    def stop(self):
        self.sim.setJointTargetVelocity(self.leftWheel, 0)
        self.sim.setJointTargetVelocity(self.rightWheel, 0)
        sleep(.1)

    def setBothMotorsToSameVelocity(self, velocity=0.75):
        self.sim.setJointTargetVelocity(self.leftWheel, velocity)
        self.sim.setJointTargetVelocity(self.rightWheel, velocity)
        sleep(.1)

    def rotateToFaceAngle(self, newAngle, velocity=0.3):
        # Adjust for an odd occurrence
        newAngle += 0

        # turn counterclockwise
        currentAngle = self.getCurrentAngle()
        if (currentAngle < newAngle and (newAngle - currentAngle) <= 180) or (
                currentAngle > newAngle and currentAngle - newAngle > 180):
            while self.getCurrentAngle() != newAngle:
                #print(f"Robot {str(self.ID)} adjusting")
                #print(f"{newAngle} -> {self.getCurrentAngle()}")
                self.sim.setJointTargetVelocity(self.leftWheel, -velocity)
                self.sim.setJointTargetVelocity(self.rightWheel, velocity)
                sleep(.1)
            self.stop()

        else:
            while self.getCurrentAngle() != newAngle:
                #print(f"Robot {str(self.ID)} adjusting")
                #print(f"{newAngle} -> {self.getCurrentAngle()}")
                self.sim.setJointTargetVelocity(self.leftWheel, velocity)
                self.sim.setJointTargetVelocity(self.rightWheel, -velocity)
                sleep(.1)
            self.stop()
        sleep(1)

    def readUltrasonicSensor(self):
        excludedObjects = ["Floor", "visibleElement", "element"]
        reading = self.sim.readProximitySensor(self.ultrasonicSensor)
        #print(f"Robot {str(self.ID)} reading.")
        #print(reading)
        sleep(1)
        if reading != 0 and reading[1] < 0.75:
            obstacleHandle = reading[3]

            alias = self.sim.getObjectAlias(obstacleHandle, -1)
            for i in excludedObjects:
                if i in alias:
                    return False

            return True
        else:
            return False

    def checkCollision(self):
        pass

    def generateRandomAngle(self):
        value = random.randint(1, 269)

        if value <= 90:
            return value
        else:
            return -value

    def readVisionSensor(self):
        print(f"Robot {str(self.ID)} reading vision sensor")
        print("reading vision sensor")
        print(f"Sensor Handle: {self.visionSensor}")
        print(f"Sensor Resolution: {self.visionSensorResolution}")

        # image = self.sim.getVisionSensorImage(self.visionSensor)
        # print(image)
        # self.sim.saveImage(image, self.visionSensorResolution, 0, 'test.jpg', 100)


class wanderer(dr20):
    """Functionality of the dr20 to seek for target objects"""
    def randomlyExploreForSetTime(self, timeLimit=1200):
        # Basically takes the while loop out of our main function
        self.setBothMotorsToSameVelocity(0.5)
        sleep(5)
        self.stop()

        start = time()

        while time() - start < timeLimit - 5:

            if self.readUltrasonicSensor():
                self.rotateToFaceAngle(self.generateRandomAngle(), 0.18)
            else:
                self.setBothMotorsToSameVelocity(1.5)

        # TODO: Add a return home function here!

class seeker(dr20):
    """Functionality of the dr20 to collect target objects"""
