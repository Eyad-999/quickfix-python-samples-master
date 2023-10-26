"""FIX Application"""
import quickfix as fix
import logging
import time
from model.logger import setup_logger
__SOH__ = chr(1)

setup_logger('logfix', 'Logs/message.log')
logfix = logging.getLogger('logfix')

class Application(fix.Application):
    """FIX Application"""
    orderID = 0
    execID = 0


    def onCreate(self, sessionID):
        """onCreate"""
        print("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        """onLogon"""
        self.sessionID = sessionID
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        """onLogout"""
        print("Session (%s) logout !" % sessionID.toString())
        return


    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("(Admin) R << %s" % msg)
        return
 
    def toAdmin(self, message, sessionID):
        # Check the message type
        msgType = message.getHeader().getField(fix.MsgType())

        # Handle specific message types
        if msgType == "A":  # "A" represents Logon
            # Process Logon message
            pass
        elif msgType == "5":  # "5" represents Logout
            # Process Logout message
            pass
        else:
            # Handle other administrative messages
            pass
        return


    # You can modify or add custom fields to the outgoing message here
    
    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("(App) S >> %s" % msg)
        return

    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.debug("(App) R << %s" % msg)
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Mockup execution report for newordersingle"""
        beginString = fix.BeginString()
        msgType = fix.MsgType()
        message.getHeader().getField( beginString )
        message.getHeader().getField( msgType )

        symbol = fix.Symbol()
        side = fix.Side()
        ordType = fix.OrdType()
        orderQty = fix.OrderQty()
        price = fix.Price()
        clOrdID = fix.ClOrdID()

        message.getField( ordType )
        if ordType.getValue() != fix.OrdType_LIMIT:
            raise fix.IncorrectTagValue( ordType.getField() )

        message.getField( symbol )
        message.getField( side )
        message.getField( orderQty )
        message.getField( price )
        message.getField( clOrdID )

        executionReport = fix.Message()
        executionReport.getHeader().setField( beginString )
        executionReport.getHeader().setField( fix.MsgType(fix.MsgType_ExecutionReport) )

        executionReport.setField( fix.OrderID(self.genOrderID()) )
        executionReport.setField( fix.ExecID(self.genExecID()) )
        executionReport.setField( fix.OrdStatus(fix.OrdStatus_FILLED) )
        executionReport.setField( symbol )
        executionReport.setField( side )
        executionReport.setField( fix.CumQty(orderQty.getValue()) )
        executionReport.setField( fix.AvgPx(price.getValue()) )
        executionReport.setField( fix.LastShares(orderQty.getValue()) )
        executionReport.setField( fix.LastPx(price.getValue()) )
        executionReport.setField( clOrdID )
        executionReport.setField( orderQty )

        if beginString.getValue() == fix.BeginString_FIX40 or beginString.getValue() == fix.BeginString_FIX41 or beginString.getValue() == fix.BeginString_FIX42:
            executionReport.setField( fix.ExecTransType(fix.ExecTransType_NEW) )

        if beginString.getValue() >= fix.BeginString_FIX41:
            executionReport.setField( fix.ExecType(fix.ExecType_FILL) )
            executionReport.setField( fix.LeavesQty(0) )

        try:
            fix.Session.sendToTarget( executionReport, sessionID )
        except fix.SessionNotFound as e:
            return
        
    def genOrderID(self):
        self.orderID += 1
        return str(self.orderID).zfill(5)

    def genExecID(self):
        self.execID += 1
        return str(self.execID).zfill(5)

def run(self):
    """Run"""
    while True:  # Use 'True' instead of '1' for an infinite loop
        time.sleep(2)

