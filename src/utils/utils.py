from datetime import datetime

class Utils:
    
    @staticmethod
    def getEpoch(datetimeObj: datetime = None) -> int:
        # This method converts given datetimeObj to epoch seconds
        if datetimeObj == None:
            datetimeObj = datetime.now()
        epochSeconds = datetime.timestamp(datetimeObj)
        return int(epochSeconds)  # converting double to long