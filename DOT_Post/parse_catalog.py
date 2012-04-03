from BeautifulSoup import BeautifulSoup
import re




# class name is the next sibling after the bb class
# <tr valign="top" style="background-color:#F0F0F0">
#       <td class="bb">
#         <nobr>SOC&nbsp;
# 010</nobr>
#       </td>
#       <td>
#         <b>
#           <i>Racism</i>
#         </b>
#         <br>(same as: 
#             <span class="s">AFR S&nbsp;
# <nobr>010</nobr></span>)
#       </td>
#       <td class="s" align="right">
#         <nobr>Social and Behavioral Sciences</nobr>
#         <wbr>
#         <br>
#       </td>
#     </tr>

def ExtractCourseTitle(node):
  """Return the title of the course as a string"""
  # Title appears in between italics
  return node.find('i').text.strip()

def ExtractAliases(node):
  """Return a list of (Department, Number) tuples, or empty list if no aliases found"""
  #(same as: 
  #              <span class="s">SOC&nbsp;
  #  <nobr>010</nobr></span>)
  alias_nodes = node.findAll('span', {'class':'s'})
  # Department&nbsp;<nobr>course_number</nobr>
  aliases = []
  for alias_node in alias_nodes:
    department = alias_node.text.split('&nbsp;')[0].strip()
    course_number = alias_node.find('nobr').text.strip()
    aliases.append((department, course_number))
  return aliases

def ExtractDepartmentAndNumber(node):
  department, number = node.text.replace('&nbsp;', ' ').split('\n')
  department = department.strip()
  number = number.strip()
  return department, number

def ExtractDivision(node):
  """Returns top level division, e.g. Social and Behavioral Sciences."""
  return ""
  
def ExtractDistributionRequirements(node):
  """Returns the list of distribution requirements this course meets, e.g. Exploring Social Differences""" 
  return []

def ExtractCourseInfo(tr):
  """Given tr containing course info, returns a Course object"""
  tds = tr.findAll('td')
  assert len(tds) == 3
  
  # td 0 has the department and number
  department, number = ExtractDepartmentAndNumber(tds[0])
  
  # td 1 has the title and optionally the aliases
  title = ExtractCourseTitle(tds[1])
  aliases = ExtractAliases(tds[1])
  
  # td 2 has the type of the course - e.g. Social and Behavioral Sciences
  division = ExtractDivision(tds[2])
  distribution_requirements_fulfilled = ExtractDistributionRequirements(tds[2])
  
  return Course(department, number, title, division, distribution_requirements_fulfilled, aliases)
  
class Course(object):
  def __init__(self, 
              department, 
              course_number,
              title,
              division,
              distribution_requirements_fulfilled=None,
              alias_list=None,
              prerequesites=None,
              comments=None):
    self.department = department
    self.course_number = course_number
    self.title = title
    self.distribution_requirements_fulfilled = distribution_requirements_fulfilled or []
    self.alias_list = alias_list or []
    self.prerequesites = prerequesites or []
    self.comments = comments or []
    
  def __str__(self):
    return "%s %s %s" %(self.department, self.course_number, self.title)
    
def main():
  doc = open('CourseCatalog.html').readlines()
  soup = BeautifulSoup(''.join(doc))

  # The class names are held in td elems with class "bb".  The underlying table row has
  # even more metadata
  
  bbs = soup.findAll('td', {'class':'bb'})
  # trs containining class info:
  trs = map(lambda bb:bb.parent, bbs)
  
  courses = map(ExtractCourseInfo, trs)
  print courses
      
    
if __name__ == '__main__':
  main()
#all_classes = map(ExtractDepartmentAndNumber, bbs)
#>>> print len(all_classes)
#567
  