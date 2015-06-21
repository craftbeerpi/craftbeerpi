class PIDController:

    def __init__(self,P=25.0, I=1000.0, D=9.0):

        self.tempRef = 67
        self.pMax = 1000
        self.Kp=P
        self.Ki=I
        self.Kd=D

        tempRef = 67
        self.pMax = 1000

        self._P = 0
        self._I = 0
        self._D = 0

        self._MaxP = 1000
        self._MaxI = 1000
        self._MaxD = 1000
        self._MaxU = 1000

        self._e = 0
        self._U = 0
        self.ePrev = 0

    def setPoint(self, temp):
        self.tempRef = temp

    def calcualte(self, temp):

        self.ePrv = self._e
        self._e = self.tempRef - temp

        # Calculate the P
        self._P = self.Kp * self._e;

        if (self._P > self._MaxP):
            self._P = self._MaxP
        elif (self._P < (-1 * self._MaxP)):
            self._P = -1 * self._MaxP
    
        # Calculate the D
        self._D = self.Kd * (self._e - self.ePrev)

        if (self._D > self._MaxD):
            self._D = self._MaxD
        elif (self._D < (-1 * self._MaxD)):
            self._D = -1 * self._MaxD

        # Calculate the I
        self._I += (self.Ki * self._e);

        if (self._I > self._MaxI):
            self._I = self._MaxI
        elif (self._I < (-1 * self._MaxI)):
            self._I = -1 * self._MaxI

        # PID algorithm
        self._U = self._P + self._I + self._D;

        # Some value limitation
        if (self._U > self._MaxU):
            self._U = self._MaxU;
        elif (self._U < 0): # Power cannot be a negative number
            self._U = 0 # self means that the system can only heating


        # Calculate the output
        # and transform U to the [0..1] interval
        return (self._U / 1000) * self.pMax;


# Test Code
if __name__ == "__main__":

    p = PIDController()
    p.setPoint(67)    
    temp = 45

    for x in range(0, 200):
        print p.calcualte(temp)
        temp += 0.5
