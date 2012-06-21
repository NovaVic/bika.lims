from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from Products.Archetypes.ArchetypeTool import registerType
from Products.CMFCore.utils import getToolByName
from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.config import PROJECTNAME
from bika.lims import bikaMessageFactory as _
from bika.lims.content.bikaschema import BikaFolderSchema
from bika.lims.interfaces import IDepartments
from plone.app.layout.globals.interfaces import IViewView
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.folder.folder import ATFolder, ATFolderSchema
from zope.interface.declarations import implements
from operator import itemgetter

class DepartmentsView(BikaListingView):
    implements(IFolderContentsView, IViewView)

    def __init__(self, context, request):
        super(DepartmentsView, self).__init__(context, request)
        self.catalog = 'bika_setup_catalog'
        self.contentFilter = {'portal_type': 'Department',
                              'sort_on': 'sortable_title'}
        self.context_actions = {_('Add'):
                                {'url': 'createObject?type_name=Department',
                                 'icon': '++resource++bika.lims.images/add.png'}}
        self.title = _("Lab Departments")
        self.icon = "++resource++bika.lims.images/department_big.png"
        self.description = ""
        self.show_sort_column = False
        self.show_select_row = False
        self.show_select_column = True
        self.pagesize = 25

        self.columns = {
            'Title': {'title': _('Department'),
                      'index':'sortable_title'},
            'Description': {'title': _('Description'),
                            'index': 'description',
                            'toggle': True},
            'Manager': {'title': _('Manager'),
                        'index': 'getManagerName',
                        'toggle': True},
            'ManagerPhone': {'title': _('Manager Phone'),
                             'index': 'getManagerPhone',
                             'toggle': True},
            'ManagerEmail': {'title': _('Manager Email'),
                             'index': 'getManagerEmail',
                             'toggle': True},
        }

        self.review_states = [
            {'id':'default',
             'title': _('Active'),
             'contentFilter': {'inactive_state': 'active'},
             'transitions': [{'id':'deactivate'}, ],
             'columns': ['Title',
                         'Description',
                         'Manager',
                         'ManagerPhone',
                         'ManagerEmail']},
            {'id':'inactive',
             'title': _('Dormant'),
             'contentFilter': {'inactive_state': 'inactive'},
             'transitions': [{'id':'activate'}, ],
             'columns': ['Title',
                         'Description',
                         'Manager',
                         'ManagerPhone',
                         'ManagerEmail']},
            {'id':'all',
             'title': _('All'),
             'contentFilter':{},
             'columns': ['Title',
                         'Description',
                         'Manager',
                         'ManagerPhone',
                         'ManagerEmail']},
        ]

    def folderitems(self):
        items = BikaListingView.folderitems(self)
        for x in range(len(items)):
            if not items[x].has_key('obj'): continue
            obj = items[x]['obj']
            items[x]['Description'] = obj.Description()
            items[x]['Manager'] = obj.getManagerName()
            items[x]['ManagerPhone'] = obj.getManagerPhone()
            items[x]['ManagerEmail'] = obj.getManagerEmail()

            items[x]['replace']['Title'] = "<a href='%s'>%s</a>" % \
                 (items[x]['url'], items[x]['Title'])

            if items[x]['ManagerEmail']:
                items[x]['replace']['ManagerEmail'] = "<a href='%s'>%s</a>"%\
                     ('mailto:%s' % items[x]['ManagerEmail'],
                      items[x]['ManagerEmail'])


        return items

schema = ATFolderSchema.copy()
class Departments(ATFolder):
    implements(IDepartments)
    displayContentsTab = False
    schema = schema

schemata.finalizeATCTSchema(schema, folderish = True, moveDiscussion = False)
atapi.registerType(Departments, PROJECTNAME)
