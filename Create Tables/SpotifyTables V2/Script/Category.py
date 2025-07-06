from Script.SQLConn import SQLConn
from Script.RAMData import RAMData
from Script.SQLData import SQLData

def getCategoryId(category):
    category_id = RAMData.instance().category.get(category['category'])
    if category_id is not None:
        return category_id

    category['category_id'] = SQLConn.instance().getId('category')
    SQLData.instance().insert_category(category)
    RAMData.instance().category[category['category']] = category['category_id']
    return category['category_id']

def updateCategory(category):
    SQLData.instance().update_category(category)
