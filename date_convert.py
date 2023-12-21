from datetime import datetime
"""Functions to get user date period input and convert it to beginning of from day and end of to day timestamps"""

def from_time(search_from):
        """0hrs, 0mins for a day"""
        from_time = datetime.strptime(search_from, '%Y-%m-%d')
        fromdatetime = from_time.replace(hour=0, minute=0, second=0, microsecond=0)
        return fromdatetime

def to_time(search_to):
        """23hrs, 59mins of a day"""
        to_time = datetime.strptime(search_to, '%Y-%m-%d')
        todatetime = to_time.replace(hour=23, minute=59, second=59, microsecond=59)
        return todatetime