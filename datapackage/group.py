from itertools import chain
from datapackage import exceptions


# Module API

class Group(object):

    # Public

    def __init__(self, resources):

        # Contract checks
        assert resources
        assert all([resource.tabular for resource in resources])
        assert all([resource.group for resource in resources])

        # Get props from the resources
        self.__name = resources[0].group
        self.__headers = resources[0].headers
        self.__schema = resources[0].schema
        self.__resources = resources

    @property
    def name(self):
        """https://github.com/frictionlessdata/datapackage-py#group
        """
        return self.__name

    @property
    def headers(self):
        """https://github.com/frictionlessdata/datapackage-py#group
        """
        return self.__headers

    @property
    def schema(self):
        """https://github.com/frictionlessdata/datapackage-py#group
        """
        return self.__schema

    def iter(self, **options):
        """https://github.com/frictionlessdata/datapackage-py#group
        """
        return chain(*[resource.iter(**options) for resource in self.__resources])

    def read(self, limit=None, **options):
        """https://github.com/frictionlessdata/datapackage-py#group
        """
        rows = []
        for count, row in enumerate(self.iter(**options), start=1):
            rows.append(row)
            if count == limit:
                break
        return rows

    def check_relations(self):
        # this function mimics the resource.check_relations but optimize it for groups
        # it's also a prototype to proprose a faster check_relations process for all resources

        # opti relations should ne loaded only once for the group
        foreign_keys = self.__resources[0].get_foreign_keys()
        print("got foreignkeys")
        
        # alternative to check_relations from tableschema-py
        for resource in self.__resources:
            try :
                resource.read(foreign_keys_values=foreign_keys)
            except exceptions.DataPackageException as exception:
                print('in %s: '%resource.name)
                if exception.multiple:
                    for error in exception.errors:
                        print(error)
                else : 
                    print(exception)

        return True

    
