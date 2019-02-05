from sqlalchemy.orm.attributes import InstrumentedAttribute

from app import db
from app.models import Course, Tag, Category

class SearchManager:
   def __init__(self):
      self.courses = Course.query

   def add_tags_filter(self, tags):
      tags = db.session.query(Tag.id).filter(Tag.name.in_(tags)).all()
      tags = map(lambda id: id[0], tags)
      self.courses = self.courses.filter(Course.tag_id.in_(tags))
   
   def add_categories_filter(self, categories):
      categories = db.session.query(Category.id) \
         .filter(Category.name.in_(categories)).all()
      categories = map(lambda id: id[0], categories)
      tags = db.session.query(Tag.id) \
         .filter(Tag.category_id.in_(categories)).all()
      tags = map(lambda id: id[0], tags)
      self.courses = self.courses.filter(Course.tag_id.in_(tags))

   def add_duration_filter(self, duration):
      self.courses = self.courses.filter(Course.duration == duration)
   
   def add_fees_filter(self, fees_max=None, fees_min=None):
      if fees_min:
         self.courses = self.courses.filter(Course.fees >= fees_min)
      if fees_max:
         self.courses = self.courses.filter(Course.fees <= fees_max)

   def add_start_date_filter(self, start_date):
      if len(start_date) == 1:
         self.courses = self.courses.filter(Course.start_date == start_date[0])
      if len(start_date) == 2:
         self.courses = self.courses \
            .filter(Course.start_date >= start_date[0]) \
            .filter(Course.start_date <= start_date[1])

   def sort_by(self, sort_order):
      by, order = sort_order[0], sort_order[1]
      if type(getattr(Course, by, None)) is not InstrumentedAttribute:
         return
      
      if order == 'asc':
         self.courses.order_by(getattr(Course, by))
      elif order == 'desc':
         self.courses.order_by(getattr(Course, by).desc())

   def get_result(self):
      return self.courses.all()