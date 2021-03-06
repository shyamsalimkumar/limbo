# copied this stupid-ass interface from SlackClient. Just use a damned dictionary!
class SearchList(list):
    def find(self, name):
        items = []
        for child in self:
            if child.__class__ == self.__class__:
                items += child.find(name)
            else:
                if child == name:
                    items.append(child)

        if len(items) == 1:
            return items[0]
        elif items != []:
            return items

class User(object):
    def __init__(self, server, name, id, real_name, tz):
        self.tz = tz
        self.name = name
        self.real_name = real_name
        self.server = server
        self.id = id

    def __eq__(self, compare_str):
        if self.id == compare_str or self.name == compare_str:
            return True
        else:
            return False

    def __str__(self):
        data = ""
        for key in list(self.__dict__.keys()):
            if key != "server":
                data += "{} : {}\n".format(key, str(self.__dict__[key])[:40])
        return data

    def __repr__(self):
        return self.__str__()
