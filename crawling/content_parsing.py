import logging


logger = logging.getLogger("ebay_consumer")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)




from newspaper import Article
from newspaper import fulltext
import sys
sys.path.append('..')
from db import DataBase
db = DataBase('../newsdata.sqlite')
conn = db.create_connection()


urls = db.select_column(conn, 'url, id', 'news' )
insert_record_sql = """ UPDATE news SET title= ?, alltext =?, publish_date =?, author=?  WHERE id = ?"""

for url in urls[36900:]:
    try:
        article = Article(url[0], language='vi')
        index = url[1]
        article.download()
        article.parse()
        article.nlp()
        source = article.source_url
        title = article.title
        body = article.text
        publish_date = ''.join(article.meta_img.split('/')[-4:-1])
        db.insert_table(conn, (title, body,publish_date, source, index), insert_record_sql)
        logger.info(f"Insert sucessfull title: {title}, publish_date: {publish_date}")
    except:
        pass
