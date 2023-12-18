from datetime import datetime

def from_time(search_from):
        
        from_time = datetime.strptime(search_from, '%Y-%m-%d')
        fromdatetime = from_time.replace(hour=0, minute=0, second=0, microsecond=0)
        return fromdatetime

def to_time(search_to):
        to_time = datetime.strptime(search_to, '%Y-%m-%d')
        todatetime = to_time.replace(hour=23, minute=59, second=59, microsecond=59)
        return todatetime