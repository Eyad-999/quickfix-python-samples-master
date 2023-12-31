#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import sys
import quickfix as fix
import time
import logging
from datetime import datetime
from model.logger import setup_logger
__SOH__ = chr(1)

# Logger
setup_logger('logfix', 'Logs/message.log')
logfix = logging.getLogger('logfix')

class ResendRequestHandler(fix.Application):
    def onCreate(self, sessionID):
        pass

    def onLogon(self, sessionID):
        pass

    def onLogout(self, sessionID):
        pass

    def toAdmin(self, message, sessionID):
        msgType = fix.MsgType()
        message.getHeader().getField(msgType)

        if msgType.getValue() == fix.MsgType_ResendRequest:
            self.onResendRequest(message, sessionID)

    def fromAdmin(self, message, sessionID):
        pass

    def toApp(self, message, sessionID):
        pass

    def fromApp(self, message, sessionID):
        pass

    def onResendRequest(self, message, sessionID):
        # Handle Resend Request messages here
        # You can access fields of the Resend Request message and take appropriate action
        pass


class Application(fix.Application):
    """FIX Application"""
    execID = 0

    def onCreate(self, sessionID):
        print("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        print("Session (%s) logout !" % sessionID.toString())
        return

    def toAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Admin) S >> %s" % msg)
        return
    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Admin) R << %s" % msg)
        return
    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(App) S >> %s" % msg)
        return
    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(App) R << %s" % msg)
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        pass

    def genExecID(self):
    	self.execID += 1
    	return str(self.execID).zfill(5)

    def resetSequenceNumber(self):
        try:
            fix.Session.reset(self.sessionID)
            print("Sequence number reset for session '%s'." % self.sessionID.toString())
        except fix.SessionNotFound as e:
            print("Session not found: %s" % e)
        except fix.InvalidState as e:
            print("Invalid state for sequence number reset: %s" % e)
        
        

    def put_new_order(self):
        """Request sample new order single"""
        message = fix.message()
        header = message.getHeader()

        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle)) #39 = D 

        message.setField(fix.ClOrdID(self.genExecID())) #11 = Unique Sequence Number
        message.setField(fix.Side(fix.Side_BUY)) #43 = 1 BUY 
        message.setField(fix.Symbol("MSFT")) #55 = MSFT
        message.setField(fix.OrderQty(1)) #38 = 1000
        message.setField(fix.Price(100))
        message.setField(fix.OrdType(fix.OrdType_LIMIT)) #40=2 Limit Order 
        message.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION)) #21 = 3
        message.setField(fix.TimeInForce('0'))
        message.setField(fix.Text("NewOrderSingle"))
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
        message.setField(trstime)

        fix.Session.sendToTarget(message, self.sessionID)

    def run(self):
        """Run"""
        while 1:
            options = str(input("Please choose 1 for Put New Order or 2 for Exit!\n"))
            if options == '1':
                self.put_new_order()
                print("Done: Put New Order\n")
                continue
            if  options == '2':
                 self.resetSequenceNumber()
            else:
                print("Valid input is 1 for order, 2 for exit\n")
            time.sleep(2)